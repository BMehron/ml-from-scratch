from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
import torch 
from functools import partial 
from typing import Optional

class CustomWrapper:
    def __init__(self, model_id: str, max_completions_len: int = 512, temperature: float=0.8, 
                 top_p: float = 0.95, top_k: int = 1, beam_size: int=1, 
                 speculative_model_id: Optional[str] = None, num_tokens_speculate: int = 5):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(model_id).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.generation_kwargs = {"max_completions_len": max_completions_len, "temperature": temperature,
                                  "top_p": top_p, "top_k": top_k, "beam_size": beam_size,
                                  "num_tokens_speculate": num_tokens_speculate
                                  }
        self.eos_token_id = self.model.generation_config.eos_token_id
        if not isinstance(self.eos_token_id, list):
            self.eos_token_id = [self.eos_token_id]
        
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.generation_algorithms = {
            "hf_greedy": self.hf_greedy,
            "greedy_vanilla": self.greedy_vanilla,
            "greedy_sampling": partial(self.custom_generation, sampling_method=self.greedy_sampling),
            "topp_sampling": partial(self.custom_generation, sampling_method=self.topp_sampling),
            "topk_sampling": partial(self.custom_generation, sampling_method=self.topk_sampling),
            "beam_search": self.beam_search,
            "speculative_decoding": self.speculative_decoding
        }
        
        if speculative_model_id is not None:
            self.draft_model = AutoModelForCausalLM.from_pretrained(speculative_model_id)
            draft_tokenizer = AutoTokenizer.from_pretrained(speculative_model_id)
            assert draft_tokenizer.get_vocab() == self.tokenizer.get_vocab()

    @torch.no_grad()
    def generate(self, prompt, algorithm="greedy_sampling"):
        self.model.eval()
        tokenized_prompt = self.tokenizer(prompt, return_tensors="pt")
        model_inputs = {"input_ids": tokenized_prompt.input_ids,
                        "attention_mask": tokenized_prompt.attention_mask
                    }
        generated_ids = self.generation_algorithms[algorithm](model_inputs)
        generated_ids = generated_ids if algorithm == "beam_search" else generated_ids[:, model_inputs["input_ids"].shape[1]:] 
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    @torch.no_grad() 
    def hf_greedy(self, model_inputs):
        generated_ids = self.model.generate(
            input_ids=model_inputs["input_ids"].to(self.device),
            attention_mask=model_inputs["attention_mask"].to(self.device),
            max_new_tokens=self.generation_kwargs["max_completions_len"],
            do_sample=False,
            use_cache=True,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        return generated_ids
        
    @torch.no_grad()
    def greedy_vanilla(self, model_inputs):
        generated_ids = model_inputs["input_ids"]
        input_ids = model_inputs["input_ids"]
        attention_mask = model_inputs["attention_mask"]
        B = model_inputs["input_ids"].shape[0]
        for _ in range(self.generation_kwargs["max_completions_len"]):
            next_token_id = self.model(
                        input_ids=input_ids.to(self.device),
                        attention_mask=attention_mask.to(self.device),
                    ).logits[:, -1, :].argmax(dim=-1, keepdim=True)
            generated_ids = torch.cat((generated_ids, next_token_id), dim=1)
            if torch.all(next_token_id.squeeze(-1) == self.eos_token_id[0]):
                break
            input_ids = torch.cat((input_ids, next_token_id), dim=1)
            attention_mask = torch.cat(
                (
                    attention_mask, 
                    torch.ones((B, 1), dtype=attention_mask.dtype, device=self.device)
                ), 
                dim=1
            )
        return generated_ids

    @torch.no_grad()
    def custom_generation(self, model_inputs, sampling_method):
        # model_inputs should contain input_ids and attention_masks: size 1 x L 
        generated_ids = model_inputs["input_ids"]
        attention_mask = model_inputs["attention_mask"]
        
        past_key_values = None
        B = generated_ids.shape[0]
        
        for _ in range(self.generation_kwargs["max_completions_len"]):
            input_ids = generated_ids if past_key_values is None else generated_ids[:, -1:]
            position_ids = None if past_key_values is None else attention_mask.sum(dim=-1, keepdim=True) - 1
            
            output = self.model(
                input_ids=input_ids.to(self.device), 
                attention_mask=attention_mask.to(self.device), 
                use_cache=True, 
                past_key_values=past_key_values, 
                position_ids=position_ids
            )
            
            next_token_logits, past_key_values = output.logits[:, -1, :], output.past_key_values
            next_token_id = sampling_method(next_token_logits / self.generation_kwargs["temperature"]) # B x 1
            
            generated_ids = torch.cat((generated_ids, next_token_id), dim=1)
            
            if torch.all(next_token_id.squeeze(-1) == self.eos_token_id[0]):
                break
            
            attention_mask = torch.cat((attention_mask, torch.ones(B, 1, dtype=attention_mask.dtype, device=self.device)), dim=-1)
            
        return generated_ids
    
    @torch.no_grad()
    def greedy_sampling(self, logits):
        return logits.argmax(dim=-1, keepdim=True)
    
    @torch.no_grad()
    def topk_sampling(self, logits):
        topk_logits, topk_token_ids = logits.topk(k=self.generation_kwargs["top_k"], dim=-1)
        topk_probs = topk_logits.softmax(dim=-1)
        sampled_idx = torch.multinomial(topk_probs, num_samples=1)
        next_token_ids = topk_token_ids.gather(index=sampled_idx, dim=-1)
        return next_token_ids    
    
    @torch.no_grad()
    def topp_sampling(self, logits):
        probs = logits.softmax(dim=-1)
        sorted_probs, sorted_indices = probs.sort(dim=-1, descending=True)
        cum_probs = sorted_probs.cumsum(dim=-1)
        topp_mask = cum_probs > self.generation_kwargs["top_p"]
        # include one extra token to make cum sum > topp
        topp_mask[:, 1:] = topp_mask[:, :-1].clone()
        topp_mask[:, 0] = False
        sorted_probs = sorted_probs.masked_fill(topp_mask, 0.0)
        sorted_probs /= sorted_probs.sum(dim=-1, keepdim=True)
        sampled_sorted_idx = torch.multinomial(sorted_probs, num_samples=1)
        next_token_ids = sorted_indices.gather(index=sampled_sorted_idx, dim=-1)
        return next_token_ids
    
    def _reorder_beam_rows(self, x, parent_beam_idx, B, K):
        """
        Reorder a flattened [B*K, ...] tensor according to selected parent beams.
        parent_beam_idx has shape [B, K].
        """
        batch_idx = torch.arange(B, device=x.device)
        return x.reshape(B, K, *x.shape[1:])[batch_idx, parent_beam_idx].reshape(B * K, *x.shape[1:])


    def _reorder_cache(self, past_key_values, parent_beam_idx, B, K):
        """
        Reorder KV cache to match selected parent beams.
        """
        new_key_values = DynamicCache(config=self.model.config)
        for layer_idx, layer_cache in enumerate(past_key_values):
            k_cache, v_cache = layer_cache[:2]

            # After prefill, cache is [B, ...]; expand so each initial beam gets its own copy.
            if k_cache.shape[0] == B:
                k_cache = k_cache.repeat_interleave(K, dim=0)
                v_cache = v_cache.repeat_interleave(K, dim=0)

            new_k_cache = self._reorder_beam_rows(k_cache, parent_beam_idx, B, K)
            new_v_cache = self._reorder_beam_rows(v_cache, parent_beam_idx, B, K)
            new_key_values.update(new_k_cache, new_v_cache, layer_idx)

        return new_key_values


    @torch.no_grad()
    def beam_search(self, model_inputs):
        B = model_inputs["input_ids"].shape[0]
        K = self.generation_kwargs["beam_size"]
        device = self.device

        attention_mask = model_inputs["attention_mask"].to(device)
        input_ids = model_inputs["input_ids"].to(device)

        beam_scores = torch.zeros(B, 1, device=device)
        finished = torch.zeros(B, dtype=torch.bool, device=device)
        sequences = None
        past_key_values = None

        for _ in range(self.generation_kwargs["max_completions_len"]):
            current_input_ids = input_ids if past_key_values is None else sequences[:, -1:]
            position_ids = None if past_key_values is None else attention_mask.sum(dim=-1, keepdim=True) - 1

            output = self.model(
                input_ids=current_input_ids,
                attention_mask=attention_mask,
                use_cache=True,
                past_key_values=past_key_values,
                position_ids=position_ids,
            )

            next_token_log_probs = output.logits[:, -1, :].log_softmax(dim=-1) # B*K x V after prefill. Before B x V


            next_token_log_probs[finished] = float("-inf")
            next_token_log_probs[finished, self.eos_token_id[0]] = 0.0

            topk_log_probs, topk_tokens = next_token_log_probs.topk(k=K, dim=1) # B*K x K after prefill. Before B x K

            candidate_scores = beam_scores.reshape(-1, 1) + topk_log_probs # B*K x K after prefill. Before B x K
            beam_scores, selected_idx = candidate_scores.reshape(B, -1).topk(k=K, dim=1) # B x K * K after prefill. Before B x K

            next_token_ids = topk_tokens.reshape(B, -1).gather(dim=1, index=selected_idx).reshape(B * K, 1)
            parent_beam_idx = selected_idx // K

            if sequences is None:
                # Prefill
                sequences = next_token_ids
                attention_mask = attention_mask.unsqueeze(1).expand(B, K, attention_mask.shape[-1]).reshape(B * K, -1)
                finished = finished.repeat_interleave(K, dim=0)
            else:
                # Need to Re-Order stats.
                sequences = self._reorder_beam_rows(sequences, parent_beam_idx, B, K)
                finished = self._reorder_beam_rows(finished, parent_beam_idx, B, K)
                attention_mask = self._reorder_beam_rows(attention_mask, parent_beam_idx, B, K)
                sequences = torch.cat([sequences, next_token_ids], dim=1)

            finished = finished | (next_token_ids.squeeze(1) == self.eos_token_id[0])

            attention_mask = torch.cat(
                [attention_mask, torch.ones((B * K, 1), dtype=attention_mask.dtype, device=device)],
                dim=1,
            )

            past_key_values = self._reorder_cache(output.past_key_values, parent_beam_idx, B, K)

            if finished.all():
                break

        sequences = sequences.reshape(B, K, -1)
        best_idx = beam_scores.argmax(dim=1)
        return sequences[torch.arange(B, device=device), best_idx]
    
    @torch.no_grad()
    def _run_draft_model(self, input_ids, attention_mask, past_key_values=None, num_tokens_generate=5):
        B = input_ids.shape[0]
        generated_ids = torch.zeros((B, 0), dtype=input_ids.dtype, device=input_ids.device)
        generated_probs = torch.zeros((B, 0, self.model.vocab_size), dtype=torch.float)
        for i in range(num_tokens_generate):
            #input_ids = input_ids if generated_ids.shape[1] == 0 else generated_ids[:, -1:]
            #position_ids = None if generated_ids.shape[1] == 0 else attention_mask.sum(dim=-1, keepdim=True) - 1
            output = self.draft_model(
                input_ids = input_ids.to(self.device),
                attention_mask = attention_mask.to(self.device),
                # past_key_values = past_key_values,
                # position_ids = position_ids,
                # use_cache = True
            )
            next_token_probs = output.logits[:, -1, :].softmax(dim=-1)
            next_token_ids = next_token_probs.argmax(dim=-1, keepdim=True)
            
            #past_key_values = output.past_key_values
            generated_ids = torch.cat((generated_ids, next_token_ids), dim=-1)
            generated_probs = torch.cat((generated_probs, next_token_probs.unsqueeze(1)), dim=1)
            
            input_ids = torch.cat((input_ids, next_token_ids), dim=1)
            attention_mask = torch.cat((attention_mask, 
                                        torch.ones((B, 1), dtype=attention_mask.dtype, device=attention_mask.device)), 
                                       dim=-1)
        return generated_ids, generated_probs, past_key_values, attention_mask
    
    @torch.no_grad()
    def speculative_decoding(self, model_inputs):
        B = model_inputs["input_ids"].shape[0]
        # Prefill: Draft model
        target_past_key_values = None
        draft_past_key_values = None
        attention_mask = model_inputs["attention_mask"]
        generated_ids = model_inputs["input_ids"]
        num_tokens_speculate = self.generation_kwargs["num_tokens_speculate"]
        for _ in range(self.generation_kwargs["max_completions_len"]):
            # Run the draft model to generate 5 tokens
            draft_candidate_tokens, draft_probs, draft_past_key_values, attention_mask = self._run_draft_model(
                input_ids = generated_ids,
                attention_mask = attention_mask,
                # past_key_values = draft_past_key_values,
                num_tokens_generate = num_tokens_speculate
            )
            # Run the big model to verify
            input_ids = torch.concat((generated_ids, draft_candidate_tokens), dim=1)
            # if target_past_key_values is None:
            #     # Prefill phase
            #     input_ids = torch.concat((generated_ids, draft_candidate_tokens), dim=1)
            #     position_ids = None
            # else:
            #     input_ids = torch.concat((generated_ids[:, -1:], draft_candidate_tokens), dim=1)
            #     position_ids = torch.arange(-num_tokens_speculate-1,0,1).unsqueeze(0).to(self.device) + attention_mask.sum(dim=-1, keepdim=True) 
            output = self.model(
                input_ids = input_ids.to(self.device),
                attention_mask = attention_mask.to(self.device), # Remove mask for the last token.
                #use_cache=True,
                # position_ids = position_ids,
                # past_key_values = target_past_key_values
            )
            target_probs = output.logits[:, -num_tokens_speculate-1:-1, :].softmax(dim=-1)  # B x num_tokens_speculate x V
            # Calculate probs for candidates
            target_candidate_probs = target_probs.gather(index=draft_candidate_tokens.unsqueeze(-1), dim=-1).squeeze(-1) # B x num_tokens_speculate 
            draft_candidate_probs = draft_probs.gather(index=draft_candidate_tokens.unsqueeze(-1), dim=-1).squeeze(-1)
            # Rejection sampling
            acceptance_probs = torch.minimum(torch.ones_like(target_candidate_probs), target_candidate_probs / draft_candidate_probs)
            rejected_tokens_mask = torch.rand_like(acceptance_probs) > acceptance_probs #  B x num_tokens_speculate 
            # find the first rejected token idx
            has_rejection = rejected_tokens_mask.any(dim=1) # B
            first_rejected_idx = rejected_tokens_mask.float().argmax(dim=1) # B
            first_rejected_idx = torch.where(
                has_rejection,
                first_rejected_idx,
                torch.full_like(first_rejected_idx, num_tokens_speculate)
            ) # B
            # mark tokens after  first_rejected_idx as rejected
            positions = torch.arange(num_tokens_speculate, device=self.device).unsqueeze(0) # 1 x num_tokens_speculate
            rejected_tokens = positions >= first_rejected_idx.unsqueeze(1) # B x num_tokens_speculate
            # Resample the rejected_idx token from max(p(a) - q(a), 0) / Normalized
            has_rejection_idxes = torch.arange(B, device=self.device)[has_rejection]
            resampling_dist = target_probs[has_rejection_idxes, first_rejected_idx[has_rejection_idxes]] - draft_probs[has_rejection_idxes, first_rejected_idx[has_rejection_idxes]] # X x V
            resampling_dist = torch.maximum(torch.zeros_like(resampling_dist), resampling_dist) 
            resampling_dist /= resampling_dist.sum(dim=-1, keepdim=True)
            resampled_tokens = torch.multinomial(resampling_dist, num_samples=1).squeeze(1) # X x 1
            # Chose final next_tokens
            draft_candidate_tokens[rejected_tokens] = self.tokenizer.pad_token_id
            attention_mask[:, -num_tokens_speculate:][rejected_tokens] = 0
            generated_ids = torch.cat((generated_ids, draft_candidate_tokens), dim=1)
            # append tokens to generated ids:
            if len(has_rejection_idxes):
                append_tokens = torch.full((B, 1), self.tokenizer.pad_token_id)
                append_tokens[has_rejection_idxes] = resampled_tokens
                append_mask = torch.full((B, 1), 0)
                append_mask[has_rejection_idxes] = 1
                generated_ids = torch.cat((generated_ids, append_tokens), dim=1)
                attention_mask = torch.cat((attention_mask, append_mask), dim=1)
            else:
                # generate using target model. We need to use random smapling from probs in order to keep theory consisitent.
                next_token_id = torch.multinomial(target_probs[:, 0, :], num_samples=1) # B x 1
                generated_ids = torch.cat((generated_ids, next_token_id), dim=1)
                attention_mask = torch.cat((attention_mask, torch.ones((B, 1), dtype=attention_mask.dtype, device=attention_mask.device)), dim=-1)
                
            # Manage KV cache
            #target_past_key_values = output.past_key_values
            
            
        return generated_ids
            
            
if __name__ == "__main__":
    import time

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How to create a personal mission statement?"}
    ]

    custom_api = CustomWrapper(model_id = "Qwen/Qwen2.5-0.5B-Instruct", max_completions_len=20, beam_size=2)

    text = custom_api.tokenizer.apply_chat_template(messages, tokenize=False,
            add_generation_prompt=True)
    print(f"Input Prompt Text: \n{text}")

    for algo in ["beam_search", "hf_greedy", "greedy_vanilla", "greedy_sampling", "topk_sampling", "topp_sampling"]:
        start_time = time.time()
        generated_text = custom_api.generate(prompt=text, algorithm=algo)
        print(f"=============Algorithm  {algo}  =========\n")
        print(f"===Time {time.time()-start_time}=======\n")
        print(generated_text, '\n')