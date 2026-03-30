# ML Knowledge Refresher

Personal study repository covering algorithms, ML foundations, and deep reinforcement learning. All code is written by me for learning, so it’s not always optimal or perfectly clean.

## Contents

### [coding/](coding/) — Data Structures & Algorithms
Problems from Cracking the Coding Interview with my solutions, complexity analysis, and some custom data structure implementations. Also there are 20 other leetcode style problems in [coding/MORE_DSA.md](coding/MORE_DSA.md).

- `ctci_1_*.py` — Strings & arrays
- `ctci_2_*.py` — Linked lists
- `ctci_3_*.py` — Stacks & queues
- `ctci_4_*.py` — Trees & graphs
- `ctci_5_*.py` — Bit manipulation
- `python_essentials.ipynb` — Python language fundamentals

### [ml/](ml/) — Machine Learning from Scratch
Core ML components implemented in PyTorch without relying on high-level abstractions.

| File | Description |
|---|---|
| [transformer_from_scratch.py](ml/transformer_from_scratch.py) | Full transformer decoder/encoder in PyTorch with inline explanations |
| [bpe_tokenizer.py](ml/bpe_tokenizer.py) | Byte-Pair Encoding tokenizer built from bytes up |
| [inference_strategies.py](ml/inference_strategies.py) | Greedy, top-k/top-p sampling, beam search, and speculative decoding |
| [manual_forward_backward.ipynb](ml/manual_forward_backward.ipynb) | Forward and backward pass by hand, numerical gradient checks |
| [training_inference_hf.ipynb](ml/training_inference_hf.ipynb) | Training and inference with Hugging Face Transformers |

### [deep_rl/](deep_rl/) — Deep Reinforcement Learning
Study notes and experiments based on OpenAI's Spinning Up curriculum, covering policy optimization, PPO, SAC, TD3, and DDPG.

## Setup

Requires Python 3.13+.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
