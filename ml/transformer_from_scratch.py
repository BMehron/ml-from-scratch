# Full implementation of transformer architecture from scratch.
import torch
import torch.nn as nn

class LayerNorm(nn.Module):
    """"
    Input: (B, L, D)
    Definition: mean = input.mean(dim=-1), var = input.var(dim=-1). output = (input - mean) / sqrt(var + 1e-8). output = alhpa * input + beta.
    Why do wee need this?: 
    LayerNorm normalizes each token independently across its hidden dimension.
    So for an input of shape (B, L, D), for each (b, l) pair, I compute the mean and variance over the last dimension D, 
    then normalize and apply learned scale and shift parameters.

    We need it because in deep transformers the scale of activations can drift across layers due to repeated linear projections, 
    nonlinearities, and residual additions. That makes optimization harder and gradients less stable. 
    LayerNorm keeps the hidden states in a more controlled range, which improves training stability.
    For example in FeedForward: output = input @ W. Let's consider first cell: if we assume W is from Normal(0, 1), then Var(ouput) = Var(input) * d
    """

    def __init__(self, input_dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones(input_dim))
        self.beta = nn.Parameter(torch.zeros(input_dim))
    
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        mean = input.mean(dim = -1, keepdim=True)
        var = input.var(dim = -1, keepdim=True, unbiased=False)
        input_hat = (input - mean) / torch.sqrt(var + self.eps)
        return self.alpha * input_hat + self.beta
    

class RMSNorm(nn.Module):
    """""
    Input: (B, L, D)
    Definition: output = input / sqrt(input ** 2 + eps).
    Why do wee need this?: In transformers often the main issue is controlling scale of activations not mean.
    RMS simpler and cheaper. In practice often matches LayerNorm in practice
    
    RMSNorm normalizes a token’s hidden state by its root mean square, without subtracting the mean. 
    So compared to LayerNorm, it only rescales the vector instead of centering and rescaling it. 
    The main goal is still to keep activation magnitudes stable across layers, which helps optimization. 
    It is simpler and slightly cheaper than LayerNorm, and empirically works very well in modern LLMs such as LLaMA-family models.
    """
    def __init__(self, input_dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(input_dim))
    
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        rms = torch.sqrt(torch.mean(input ** 2, dim=-1, keepdim=True) + self.eps)
        # rms = torch.sqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        input_hat = input / rms
        return self.gamma * input_hat
    
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_hidden: int | None = None, dropout: float = 0.1):
        super().__init__()
        assert d_hidden is not None or d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_hidden = d_hidden if d_hidden is not None else d_model // n_heads
        self.flat_dim = self.n_heads * self.d_hidden

        self.W_Q = nn.Linear(d_model, self.flat_dim)
        self.W_K = nn.Linear(d_model, self.flat_dim)
        self.W_V = nn.Linear(d_model, self.flat_dim)
        self.W_output = nn.Linear(self.flat_dim, d_model)
        self.dropout = nn.Dropout(dropout)

    def split_across_heads(self, x: torch.Tensor) -> torch.Tensor:
        B, L, _ = x.shape
        return x.reshape(B, L, self.n_heads, self.d_hidden).transpose(1, 2)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        scores = Q @ K.transpose(-2, -1) / (self.d_hidden ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(~mask, float("-inf"))   # if mask=True means keep, and should be broadcastable
        probs = torch.softmax(scores, dim=-1)
        probs = self.dropout(probs)
        return probs @ V

    def forward(self, q, k, v, mask=None):
        B, L_q, _ = q.shape
        assert k.shape[0] == B and v.shape[0] == B
        assert k.shape[1] == v.shape[1]

        Q = self.split_across_heads(self.W_Q(q))
        K = self.split_across_heads(self.W_K(k))
        V = self.split_across_heads(self.W_V(v))

        out = self.scaled_dot_product_attention(Q, K, V, mask)
        out = out.transpose(1, 2).contiguous().view(B, L_q, self.flat_dim)
        return self.W_output(out)

def make_src_mask(self, src):
    src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
    return src_mask

def make_trg_mask(self, trg):
    trg_pad_mask = (trg != self.trg_pad_idx).unsqueeze(1).unsqueeze(3)
    trg_len = trg.shape[1]
    trg_sub_mask = torch.tril(torch.ones(trg_len, trg_len)).type(torch.ByteTensor).to(self.device)
    trg_mask = trg_pad_mask & trg_sub_mask
    return trg_mask

def build_causal_mask(padding_mask: torch.Tensor) -> torch.Tensor:
    """
    padding_mask: (B, L_k)
    returns mask broadcastable to (B, H, L_q, L_k)
    """
    seq_len = padding_mask.shape[1]
    device = padding_mask.device
    causal_mask = torch.tril(torch.ones(seq_len, seq_len, dtype=torch.bool, device=device)).unsqueeze(0).unsqueeze(0) # 1 x 1 x L x L
    attention_mask = padding_mask.unsqueeze(1).unsqueeze(2) & causal_mask
    return attention_mask
    
def build_cross_attention_mask(attention_mask: torch.Tensor):
    """
    attention_mask: (B, L_enc)
    return mask broadcastable to (B, H, L_dec, L_enc)
    """
    return attention_mask.unsqueeze(1).unsqueeze(2)

class FeedForwardNetwork(nn.Module):
    """
    The feed-forward network is applied independently to each token. It expands the hidden dimension, 
    applies a nonlinearity such as GELU, and projects back to the model dimension. 
    In transformers, this gives each token a more expressive nonlinear transformation after attention mixes information across tokens.
    """
    def __init__(self, d_model: int, activation = nn.GELU, dropout: float = 0.1):
        super().__init__()
        self.linear_1 = nn.Linear(d_model, 4*d_model)
        self.act = activation()
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(4*d_model, d_model)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.linear_1(x)
        x = self.act(x)
        x = self.dropout(x)
        x = self.linear_2(x)
        return x
    
class GatedFeedForward(nn.Module):
    """
    A gated FFN introduces a multiplicative interaction between two projected feature streams. 
    One branch produces candidate features while the other acts as a gate controlling how much of each feature passes through. 
    This makes the transformation more expressive than a standard FFN and empirically improves performance in many modern LLM architectures. 
    """
    def __init__(
        self,
        d_model: int,
        hidden_dim: int | None = None,
        activation = nn.SiLU
    ):
        super().__init__()

        hidden_dim = hidden_dim or int(8/3 * d_model)

        self.gate_proj = nn.Linear(d_model, hidden_dim)
        self.value_proj = nn.Linear(d_model, hidden_dim)
        self.out_proj = nn.Linear(hidden_dim, d_model)

        self.act = activation()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gate = self.act(self.gate_proj(x))
        value = self.value_proj(x)
        return self.out_proj(gate * value)
    
class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_hidden: int = None, dropout: float = 0.1):
        super().__init__()
        self.norm_1 = RMSNorm(d_model)
        self.self_attn = MultiHeadAttention(d_model, n_heads, dropout=dropout)
        self.norm_2 = RMSNorm(d_model)
        self.ffn = GatedFeedForward(d_model, d_hidden)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        # Attention Block
        x_norm = self.norm_1(x)
        x_attn = x + self.self_attn(x_norm, x_norm, x_norm, mask)
        # Feed-Forward-Block
        x_norm = self.norm_2(x_attn)
        return x_attn + self.ffn(x_norm)
    
class EncoderDecoderBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_hidden: int | None = None, dropout: float = 0.1):
        super().__init__()
        # Causal-Attn
        self.norm1 = RMSNorm(d_model)
        self.causal_attn = MultiHeadAttention(d_model, n_heads, dropout=dropout)
        # Cross-Attn
        self.norm2 = RMSNorm(d_model)
        self.cross_attn = MultiHeadAttention(d_model, n_heads, dropout=dropout)
        # FFN
        self.norm3 = RMSNorm(d_model)
        self.ffn = GatedFeedForward(d_model, d_hidden)

    def forward(self, x: torch.Tensor, padding_mask: torch.Tensor, encoder_key, encoder_value, encoder_mask):
        # causal Attn
        causal_mask = build_causal_mask(padding_mask)
        h = self.norm1(x)
        x = x + self.causal_attn(h, h, h, mask=causal_mask)
        # Cross-Attn
        cross_attn_mask = build_cross_attention_mask(encoder_mask)
        h = self.norm2(x)
        x = x + self.cross_attn(q=h, k=encoder_key, v=encoder_value, mask=cross_attn_mask)
        # FFN
        h = self.norm3(x)
        x = x + self.ffn(h)
        return x
    

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 2048, base: int = 10000):
        super().__init__()
        pe = torch.zeros(max_len, d_model, requires_grad=False)

        freqs = 1 / (base ** (torch.arange(0, d_model, 2) / d_model))
        positions = torch.arange(max_len)

        angles = positions.unsqueeze(1) * freqs.unsqueeze(0)

        pe[:, 0::2] = torch.sin(angles)
        pe[:, 1::2] = torch.cos(angles)

        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, L, D)
        return x + self.pe[:, :x.shape[1]]
    

class RoPEEncoding(nn.Module):
    def __init__(self, head_dim: int, max_len: int = 2048, base: int = 10000):
        super().__init__()
        assert head_dim % 2 == 0, "head_dim must be even for RoPE"

        freqs = 1 / (base ** (torch.arange(0, head_dim, 2).float() / head_dim))  # (D/2,)
        positions = torch.arange(max_len).float()  # (L,)

        angles = positions.unsqueeze(1) * freqs.unsqueeze(0)  # (L, D/2)

        self.register_buffer("pe_sin", torch.sin(angles).unsqueeze(0).unsqueeze(0))  # (1,1,L,D/2)
        self.register_buffer("pe_cos", torch.cos(angles).unsqueeze(0).unsqueeze(0))  # (1,1,L,D/2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, H, L, D)
        sin = self.pe_sin[..., :x.shape[2], :]   # (1,1,L,D/2)
        cos = self.pe_cos[..., :x.shape[2], :]   # (1,1,L,D/2)

        x_even = x[..., 0::2]
        x_odd = x[..., 1::2]

        out = torch.empty_like(x)
        out[..., 0::2] = x_even * cos - x_odd * sin
        out[..., 1::2] = x_even * sin + x_odd * cos
        return out
    
class MHAWithRoPE(MultiHeadAttention):
    def __init__(self, d_model: int, n_heads: int, d_hidden: int | None = None, dropout: float = 0.1, max_len: int = 2048):
        super().__init__(d_model, n_heads, d_hidden, dropout)
        self.rope = RoPEEncoding(self.d_hidden, max_len=max_len)

    def forward(self, q, k, v, mask=None):
        B, L_q, _ = q.shape
        assert k.shape[0] == B and v.shape[0] == B
        assert k.shape[1] == v.shape[1]

        Q = self.split_across_heads(self.W_Q(q))
        K = self.split_across_heads(self.W_K(k))
        V = self.split_across_heads(self.W_V(v))

        Q = self.rope(Q)
        K = self.rope(K)

        out = self.scaled_dot_product_attention(Q, K, V, mask)
        out = out.transpose(1, 2).contiguous().view(B, L_q, self.flat_dim)
        return self.W_output(out)

class LearnedEncodings(nn.Module):
    def __init__(self, d_model, max_len):
        super().__init__()
        self.pe = nn.Embedding(max_len, d_model)

    def forward(self, x):
        # x: B x L x D
        L = x.shape[1]
        pos_emb = self.pe(torch.arange(L, device=x.device))
        x = x + pos_emb.unsqueeze(0)
        return x
    
class DecoderModel(nn.Module):
    def __init__(self, vocab_size, d_model, n_layers, n_heads, pad_idx):
        super().__init__()
        self.pad_idx = pad_idx
        self.embeddings = nn.Embedding(vocab_size, d_model)
        self.layers = nn.ModuleList(
            [TransformerBlock(d_model, n_heads) for _ in range(n_layers)]
        )

    def forward(self, input_ids):
        # input_ids: (B, L)
        x = self.embeddings(input_ids)
        mask = self.get_input_mask(input_ids)

        for layer in self.layers:
            x = layer(x, mask)

        return x @ self.embeddings.weight.T

    def get_input_mask(self, input_ids):
        pad_mask = (input_ids != self.pad_idx)  # (B, L)
        L = input_ids.shape[1]

        causal_mask = torch.tril(
            torch.ones(L, L, device=input_ids.device, dtype=torch.bool)
        )  # (L, L)

        final_mask = causal_mask.unsqueeze(0) & pad_mask.unsqueeze(1)  # (B, L, L)
        return final_mask.unsqueeze(1)  # (B, 1, L, L)
    
class GQAAttention(nn.Module):
    def __init__(self, d_model, q_heads, k_heads, dropout=0.1, max_len=2048):
        super().__init__()
        self.d_model = d_model
        self.q_heads = q_heads
        self.k_heads = k_heads

        assert d_model % q_heads == 0
        assert q_heads % k_heads == 0

        self.d_hidden = d_model // q_heads
        self.group_size = q_heads // k_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, self.d_hidden * self.k_heads)
        self.W_v = nn.Linear(d_model, self.d_hidden * self.k_heads)

        self.rope = RoPEEncoding(self.d_hidden, max_len=max_len)
        self.dropout = nn.Dropout(dropout)
        self.W_out = nn.Linear(d_model, d_model)

    def split_across_heads(self, x, n_heads):
        # x: (B, L, n_heads * d_hidden) -> (B, n_heads, L, d_hidden)
        B, L, _ = x.shape
        return x.reshape(B, L, n_heads, self.d_hidden).transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        # q: (B, L_q, d_model)
        # k,v: (B, L_k, d_model)
        B, L_q, D_q = q.shape
        Bk, L_k, D_k = k.shape
        Bv, L_v, D_v = v.shape

        assert B == Bk == Bv
        assert L_k == L_v
        assert D_q == D_k == D_v == self.d_model

        Q = self.split_across_heads(self.W_q(q), self.q_heads)   # (B, Hq, Lq, Dh)
        K = self.split_across_heads(self.W_k(k), self.k_heads)   # (B, Hk, Lk, Dh)
        V = self.split_across_heads(self.W_v(v), self.k_heads)   # (B, Hk, Lk, Dh)

        Q = self.rope(Q)
        K = self.rope(K)

        # regroup query heads: (B, Hq, Lq, Dh) -> (B, Hk, G, Lq, Dh)
        Q = Q.view(B, self.k_heads, self.group_size, L_q, self.d_hidden)

        # K_exp = K.unsqueeze(2)   # (B, Hk, 1, Lk, Dh)
        # V_exp = V.unsqueeze(2)   # (B, Hk, 1, Lk, Dh)

        # attn_score = Q @ K_exp.transpose(-2, -1) / (self.d_hidden ** 0.5)   # (B,Hk,G,Lq,Lk)
        # attn_probs = torch.softmax(attn_score, dim=-1)
        # output = attn_probs @ V_exp   # (B,Hk,G,Lq,Dh)

        # attention scores: (B, Hk, G, Lq, Lk)
        attn_score = torch.einsum("bhgld,bhmd->bhglm", Q, K) / (self.d_hidden ** 0.5)

        if mask is not None:
            # mask expected shape broadcastable to (B, 1, 1, Lq, Lk) or (B, 1, Lq, Lk)
            attn_score = attn_score.masked_fill(~mask.unsqueeze(2), float("-inf"))

        attn_probs = self.dropout(torch.softmax(attn_score, dim=-1))

        # output: (B, Hk, G, Lq, Dh)
        output = torch.einsum("bhglm,bhmd->bhgld", attn_probs, V)

        # merge back to (B, Hq, Lq, Dh)
        output = output.reshape(B, self.q_heads, L_q, self.d_hidden)

        # merge heads to (B, Lq, d_model)
        output = output.transpose(1, 2).contiguous().view(B, L_q, self.d_model)
        return self.W_out(output)

class DynamicKVCache:
    def __init__(self):
        # layer_idx -> (k_cache, v_cache)
        # each tensor shape: (B, H_kv, T, D_h)
        self.kv = {}

    def update(self, k: torch.Tensor, v: torch.Tensor, layer_idx: int):
        # k, v: (B, H_kv, 1, D_h) for one decoding step

        if layer_idx not in self.kv:
            self.kv[layer_idx] = (k, v)
        else:
            k_cache = torch.cat([self.kv[layer_idx][0], k], dim=2)   # append along sequence dimension
            v_cache = torch.cat([self.kv[layer_idx][1], v], dim=2)
            self.kv[layer_idx] = (k_cache, v_cache)

        return self.kv[layer_idx]
    

class StaticKVCache:
    def __init__(self, n_layers: int, batch_size: int, n_heads: int, max_seq_len: int, head_dim: int, device=None, dtype=None):
        self.max_seq_len = max_seq_len
        self.kv = {}

        for layer_idx in range(n_layers):
            k_cache = torch.empty(
                batch_size, n_heads, max_seq_len, head_dim,
                device=device, dtype=dtype
            )
            v_cache = torch.empty(
                batch_size, n_heads, max_seq_len, head_dim,
                device=device, dtype=dtype
            )
            self.kv[layer_idx] = {
                "k": k_cache,
                "v": v_cache,
                "length": 0,
            }

    def update(self, k: torch.Tensor, v: torch.Tensor, layer_idx: int):
        # k, v: (B, H, 1, D)
        layer_cache = self.kv[layer_idx]
        t = layer_cache["length"]

        layer_cache["k"][:, :, t:t+1, :] = k
        layer_cache["v"][:, :, t:t+1, :] = v
        layer_cache["length"] += 1

        current_len = layer_cache["length"]
        return (
            layer_cache["k"][:, :, :current_len, :],
            layer_cache["v"][:, :, :current_len, :],
        )

    def get(self, layer_idx: int):
        layer_cache = self.kv[layer_idx]
        current_len = layer_cache["length"]
        return (
            layer_cache["k"][:, :, :current_len, :],
            layer_cache["v"][:, :, :current_len, :],
        )

class MoE(nn.Module):
    def __init__(self, d_model: int, num_experts: int, topk: int = 2):
        super().__init__()
        assert topk <= num_experts

        self.router = nn.Linear(d_model, num_experts)
        self.experts = nn.ModuleList(
            [GatedFeedForward(d_model) for _ in range(num_experts)]
        )
        self.topk = topk

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, L, D)
        router_probs = torch.softmax(self.router(x), dim=-1)             # (B, L, E)
        top_prob, top_idx = torch.topk(router_probs, k=self.topk, dim=-1)  # (B, L, K)
        # optional but common
        top_prob = top_prob / top_prob.sum(dim=-1, keepdim=True)
        output = torch.zeros_like(x)
        for i, expert in enumerate(self.experts):
            # which top-k slots chose this expert
            expert_mask = (top_idx == i)                                 # (B, L, K)
            # token selected by this expert in any slot
            token_mask = expert_mask.any(dim=-1)                         # (B, L)
            if not token_mask.any():
                continue
            # gather inputs for this expert
            x_i = x[token_mask]                                          # (N_i, D)
            # gather routing weights for this expert
            expert_weight = top_prob[expert_mask]                        # (N_i,)
            # expert output
            y_i = expert(x_i)                                            # (N_i, D)
            output[token_mask] += expert_weight.unsqueeze(-1) * y_i
        return output


if __name__ == "__main__":
    input = torch.tensor([[[1., 2], [4,5]]])
    layer_norm = LayerNorm(2)
    output = layer_norm(input)
    print(f"Input: {input}")
    print(f"Output: {output}")

