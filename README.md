# ML From Scratch

PyTorch implementations of core ML and LLM components built without high-level abstractions — transformers, tokenizers, decoding strategies, manual backprop for the standard layers, and reinforcement-learning algorithms. Each file is meant to be read end-to-end: short, self-contained, and annotated with the reasoning behind every step.

## ml/ — Modern LLM components

[transformer_from_scratch.py](ml/transformer_from_scratch.py) — a single file covering the moving parts of a modern decoder/encoder-decoder transformer:

- `LayerNorm`, `RMSNorm`
- `MultiHeadAttention` with scaled dot-product attention and masking
- `PositionalEncoding` (sinusoidal), `LearnedEncodings`, `RoPEEncoding`, and `MHAWithRoPE`
- `FeedForwardNetwork` and `GatedFeedForward` (SwiGLU-style)
- `TransformerBlock` (pre-norm residual) and `EncoderDecoderBlock` with cross-attention
- `DecoderModel` with weight tying, causal + padding masks
- `GQAAttention` — grouped-query attention with grouped Q heads sharing K/V heads
- `DynamicKVCache` and `StaticKVCache` for incremental decoding
- `MoE` — mixture-of-experts with top-k routing and renormalized gating

[bpe_tokenizer.py](ml/bpe_tokenizer.py) — byte-level BPE built from raw bytes up. Uses a max-heap of pair frequencies with lazy invalidation of stale entries to keep training near-linear. Includes a pytest suite with round-trip tests over ASCII, unicode (`café`, `你好`, `Привет`), and emoji.

[inference_strategies.py](ml/inference_strategies.py) — a thin wrapper around a Hugging Face causal LM implementing decoding from scratch:

- Greedy (vanilla loop and KV-cached)
- Top-k and top-p (nucleus) sampling with KV cache
- Beam search with explicit beam reordering of the KV cache
- Speculative decoding with rejection sampling between draft and target models
- Side-by-side timing of every algorithm on Qwen2.5-0.5B in `__main__`

[manual_forward_backward.ipynb](ml/manual_forward_backward.ipynb) — 22 sections of forward + manual backward passes, gradient checks against autograd, and small training pipelines with loss curves:

| Section | What's there |
|---|---|
| 1–6 | Linear, MSE, Sigmoid (stable), ReLU, Softmax (stable), Cross-Entropy — each with hand-derived backward |
| 7 | SGD optimizer using torch grads |
| 8–11 | Linear regression closed-form, linear regression via GD, logistic regression, L2 / Ridge |
| 12–13 | StandardScaler (fit / transform / inverse), reproducible train/val split |
| 14–16 | k-NN (mostly vectorized), k-Means, PCA via SVD |
| 17–18 | 2-layer MLP with full manual backprop, finite-difference gradient checking |
| 19–20 | BatchNorm (training-mode) forward + backward, Dropout forward + backward |
| 21 | Backprop of scaled dot-product attention (single head) |
| 22 | Adam / AdamW from scratch |

[training_inference_hf.ipynb](ml/training_inference_hf.ipynb) — using Hugging Face for tokenization, model loading, and training, then driving the from-scratch decoding strategies above on real generations.

The folder also includes reference PDFs: [Optimizers.pdf](ml/Optimizers.pdf), [losses.pdf](ml/losses.pdf), [llms.pdf](ml/llms.pdf), and [RL_David_Silver_Compressed.pdf](ml/RL_David_Silver_Compressed.pdf).

## deep_rl/ — Reinforcement learning

[intro_policy_optimization.md](deep_rl/intro_policy_optimization.md) — derivation notes for the policy gradient, including the log-derivative trick and the reward-to-go reduction.

[rl_algorithms.ipynb](deep_rl/rl_algorithms.ipynb) — Gym environment walk-through, a Vanilla Policy Gradient implementation written from scratch, and a second pass following the OpenAI Spinning Up structure for comparison.

## coding/ — Data structures & algorithms

Solutions to Cracking the Coding Interview problems and a handful of custom data-structure implementations:

- `ctci_1_*.py` — arrays and strings
- `ctci_2_*.py` — linked lists
- `ctci_3_*.py` — stacks and queues (including sort-stack and queue-via-two-stacks)
- `ctci_4_*.py` — trees and graphs
- `ctci_5_*.py` — bit manipulation
- [hash_table.py](coding/hash_table.py), [linked_list.py](coding/linked_list.py), [stack.py](coding/stack.py) — minimal implementations
- [MORE_DSA.md](coding/MORE_DSA.md) — 20 additional LeetCode-style problems with solution sketches

## Setup

Python 3.13+.

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the BPE tests:

```bash
pytest ml/bpe_tokenizer.py
```

Run the inference-strategy comparison:

```bash
python ml/inference_strategies.py
```
