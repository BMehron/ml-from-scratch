
# DeepMind Research Engineer Interview Prep Plan (NLP / RL / GenAI)

This is a **6-week, step-by-step preparation plan** for a DeepMind Research Engineer interview, tailored to your background:
- ~3 years of experience
- Python: 7–8 / 10
- ML: 8 / 10
- Focus: NLP, RL, GenAI (not Safety / Optimization / Robotics)

You can treat “days” as study sessions. If you don’t study every day, just move through the plan session-by-session.

---

## Week 0 – Setup & Baseline (Optional but Recommended, 1–3 days)

**Goal:** Set up environment, gather resources, and quickly check your baseline.

### Day 0.1 – Environment & Tools
- Make sure you have:
  - Python 3.10+ environment (conda or venv)
  - PyTorch or JAX installed
  - A code editor (VSCode, PyCharm, etc.)
- Create a “DeepMind-Prep” repo/folder with:
  - `coding/` – Algorithms & DS
  - `math/` – notes + derivations
  - `ml/` – theory + small experiments
  - `papers/` – paper summaries
  - `projects/` – 1–2 small end-to-end ML projects

### Day 0.2 – Baseline Coding Check (90–120 min)
- Solve 2–3 LeetCode-style problems (or equivalent) in Python:
  - 1 easy graph or BFS/DFS
  - 1 medium DP
  - 1 medium array/string or hashing
- Focus on:
  - Clean code: functions, docstrings, type hints
  - Time/space complexity explanations after each problem
- Write a short self-review:
  - Where did you hesitate?
  - Any Python syntax you had to look up?

### Day 0.3 – Baseline Math & ML Check (60–90 min)
- Try to:
  - Derive gradient of logistic regression loss
  - Explain SVD and how it’s used in PCA
  - Write down the Bellman equation for value iteration
- Mark anything that feels fuzzy—these will be key focus points.

---

## Week 1 – Algorithms & Python Fluency

**Theme:** Become very comfortable writing clean, efficient Python and core algorithms under interview conditions.

---

### Day 1.1 – Python Fundamentals & Idioms
- Review:
  - References vs values, mutability (lists vs tuples vs dicts)
  - List/dict/set comprehensions
  - `*args`, `**kwargs`, default arguments
  - Context managers (`with` and `__enter__/__exit__`)
- Implement:
  - A context manager that times a block of code.
  - A small utility: `cached_property`-like decorator.
- Practice 1–2 easy coding problems focusing on **clarity** of Python style.

---

### Day 1.2 – Data Structures & Complexity
- Revisit complexity:
  - O(1), O(log n), O(n), O(n log n), O(n^2), and how to derive them.
- Implement from scratch:
  - Singly linked list with insert/delete.
  - Stack and queue (using both list and `collections.deque`).
  - A min-heap using `heapq` and discuss complexity of push/pop.
- Do 1–2 problems where you must **choose the right DS** and justify it.

---

### Day 1.3 – Graphs I (BFS & DFS)
- Review:
  - Representations: adjacency list vs matrix.
  - BFS and DFS (recursive and iterative).
- Implement:
  - `bfs(graph, start)` that returns distances or levels.
  - `dfs(graph, start)` that returns discovery/finish order.
- Do 1 graph problem:
  - Shortest path in unweighted graph (BFS).
  - Connected components (DFS).

---

### Day 1.4 – Graphs II (Dijkstra, Topological Sort)
- Study:
  - Dijkstra’s algorithm and its complexity.
  - Topological sort (Kahn’s algorithm + DFS-based).
- Implement:
  - `dijkstra(graph, start)` with a priority queue.
  - `topological_sort(graph)` (assume DAG).
- Practice:
  - One problem that combines Dijkstra with some constraint or twist.

---

### Day 1.5 – Dynamic Programming Patterns
- Review common DP patterns:
  - 1D DP (e.g., climbing stairs).
  - 2D DP (e.g., edit distance).
  - Knapsack-style.
- Implement:
  - Edit distance (Levenshtein).
  - 0–1 knapsack (bottom-up).
- After each, write out:
  - State definition.
  - Recurrence.
  - Complexity.

---

### Day 1.6 – NumPy / PyTorch Fluency
- Practice vectorized operations:
  - Broadcasting, matrix multiplication, elementwise ops.
  - Indexing, masking.
- Implement from scratch (NumPy or PyTorch):
  - A simple linear regression with gradient descent (no autograd).
- Focus on:
  - Avoiding Python loops via vectorization.
  - Clear separation of data, model, and training loop.

---

### Day 1.7 – Week 1 Mock Coding Interview
- Simulate a 60–75 minute interview:
  - 1 graph problem.
  - 1 DP or array problem.
  - 1 small design question (e.g., implementing a beam search interface).
- Afterward, do a retro:
  - Time spent understanding vs coding.
  - Any major bugs.
  - Any Python gaps.

---

## Week 2 – Math Foundations for DL & RL

**Theme:** Lock in a strong base in calculus, linear algebra, probability, and optimization.

---

### Day 2.1 – Single-variable Calculus & Taylor
- Review:
  - Derivatives, chain rule, product/quotient rules.
  - Taylor series expansion and remainder term (intuitively).
- Exercises:
  - Derive derivative of: sigmoid, tanh, softplus.
  - Write 2nd-order Taylor expansion of a simple function at a point.
- Reflect:
  - How does Taylor relate to gradient descent and local minima?

---

### Day 2.2 – Multivariate Calculus & Matrix Calculus I
- Review:
  - Gradient, Jacobian, Hessian.
  - Chain rule in vector form.
- Exercises:
  - Compute gradient of `f(w) = 1/2 ||Xw - y||^2`.
  - Compute gradient of `softmax` w.r.t. logits.
- Write these derivations clearly in your `math/` folder.

---

### Day 2.3 – Matrix Calculus II & Optimization Basics
- Study:
  - Quadratic forms: `x^T A x`.
  - Positive definite / semidefinite matrices.
- Exercises:
  - Derive gradient and Hessian of `f(w) = 1/2 w^T A w - b^T w`.
  - Show why convex quadratic has a unique minimizer.
- Conceptual:
  - Condition number & implications for optimization.

---

### Day 2.4 – Probability & Distributions I
- Review:
  - Axioms of probability, random variables, expectation, variance.
  - Common distributions: Bernoulli, Binomial, Gaussian.
- Exercises:
  - Derive mean and variance of Binomial.
  - Conditionals and joint distributions for simple discrete cases.
- ML link:
  - Explain MLE for Bernoulli and Binomial.

---

### Day 2.5 – Probability & Distributions II (Continuous & KL)
- Study:
  - Gaussian, Exponential, Beta (at least qualitatively).
  - KL divergence: definition and interpretation.
- Exercises:
  - Derive KL between two Gaussians in 1D.
  - Derive posterior for Gaussian likelihood with Gaussian prior (conjugacy).
- Connect to:
  - Bayesian linear regression.

---

### Day 2.6 – Optimization for ML (GD & Newton)
- Study:
  - Gradient descent: step size, convergence conditions.
  - Newton’s method: idea & limitations.
- Exercises:
  - Show why too large a learning rate can diverge.
  - Compare vanilla GD vs Newton on a simple 1D quadratic.

---

### Day 2.7 – Week 2 Math Mock Interview
- Simulate a 60-minute math interview:
  - Derive logistic regression gradient.
  - Explain SVD and its ML relevance.
  - Prove a property about expectation & variance.
- Afterward, summarize:
  - Any derivation you couldn’t finish.
  - Any definition you struggled to recall.

---

## Week 3 – Deep Learning & Transformers (NLP / GenAI Focus)

**Theme:** Master core DL concepts and be able to implement Transformers from scratch.

---

### Day 3.1 – Backpropagation & MLPs
- Review:
  - Computational graph view of backprop.
  - Chain rule through layers.
- Implement:
  - A 2-layer MLP with manual backprop in NumPy.
- Verify:
  - Compare your gradients to autograd from PyTorch on small examples.

---

### Day 3.2 – Regularization, Normalization, Initialization
- Study:
  - L2 regularization, dropout.
  - BatchNorm vs LayerNorm (where they are used and why).
  - Weight initialization (Xavier, Kaiming).
- Exercises:
  - Implement LayerNorm from scratch.
  - Explain why normalization helps optimization.

---

### Day 3.3 – Attention Mechanism Basics
- Study:
  - Scaled dot-product attention formula.
  - Q, K, V projections and scaling by sqrt(d_k).
- Implement:
  - Single-head attention in PyTorch/NumPy.
- Verify:
  - Test on small toy tensors and check shapes carefully.

---

### Day 3.4 – Multi-Head Attention & Transformer Block
- Implement:
  - Multi-head self-attention module from scratch.
  - A minimal Transformer encoder block:
    - MHA
    - Residual connection
    - LayerNorm
    - Position-wise feedforward.
- Ensure:
  - Code is clean, modular, and easy to extend.

---

### Day 3.5 – Positional Encoding & Sequence Modeling
- Study:
  - Sinusoidal positional encodings.
  - Learned vs fixed positional encodings.
- Implement:
  - Sinusoidal positional encoding module.
  - A tiny Transformer encoder and run it on dummy data.

---

### Day 3.6 – Practical Issues in Training Transformers
- Study:
  - Masking (causal and padding masks).
  - Gradient clipping.
  - Learning rate schedules (warmup).
- Implement:
  - Causal masking in attention.
  - A training loop for a toy language modeling problem.

---

### Day 3.7 – Week 3 DL/Transformer Mock Interview
- Simulate:
  - Explain self-attention from scratch, derive shapes and complexity.
  - Design a small Transformer for character-level modeling.
  - Discuss how you would modify it for long sequences.
- Review your own explanations for clarity and depth.

---

## Week 4 – RL Foundations

**Theme:** Build a solid understanding of RL math and algorithms, especially policy gradient methods.

---

### Day 4.1 – MDPs & Bellman Equations
- Review:
  - States, actions, transition probabilities, rewards, discount factor.
  - Value function, Q-function.
- Exercises:
  - Write down Bellman expectation and optimality equations.
  - Solve a tiny MDP manually.

---

### Day 4.2 – Value Iteration & Policy Iteration
- Study:
  - Value iteration algorithm.
  - Policy iteration and policy evaluation.
- Implement:
  - Value iteration for a small gridworld.
  - Policy iteration and compare convergence.

---

### Day 4.3 – Q-Learning & SARSA
- Study:
  - Off-policy vs on-policy methods.
  - Tabular Q-learning and SARSA update rules.
- Implement:
  - Tabular Q-learning on a simple environment (e.g., gridworld).
- Analyze:
  - Effects of learning rate and epsilon.

---

### Day 4.4 – Policy Gradients & REINFORCE
- Study:
  - Policy gradient theorem.
  - REINFORCE algorithm.
- Derive:
  - Gradient of expected return w.r.t. policy parameters.
- Implement:
  - REINFORCE on a toy environment (e.g., CartPole-like or custom).

---

### Day 4.5 – Actor–Critic & Advantage Methods
- Study:
  - Actor–critic concept.
  - Advantage function and variance reduction.
- Implement:
  - Simple A2C-style algorithm on a small environment.
- Reflect:
  - Why actor–critic can be more stable than REINFORCE.

---

### Day 4.6 – Deep RL Practical Issues
- Study:
  - Function approximation & instability.
  - Replay buffers, target networks (DQN ideas).
  - Exploration strategies (epsilon-greedy, entropy regularization).
- Thought exercises:
  - Why is RL often harder to train than supervised learning?
  - How would you debug learning that diverges?

---

### Day 4.7 – Week 4 RL Mock Interview
- Simulate:
  - Explain and derive the policy gradient theorem.
  - Walk through Q-learning and when it fails.
  - Design an RL algorithm for a tiny game.
- Capture:
  - Any shaky definitions (advantage, value functions, etc.).

---

## Week 5 – Research Engineering Skills

**Theme:** Practice what makes a Research Engineer different from a regular SWE: experiments, debugging, paper implementations.

---

### Day 5.1 – Research Code Structure & Experimentation
- Study:
  - Good practices for research code:
    - Config files
    - Logging
    - Seeds & reproducibility
- Implement:
  - A small training script (e.g., for MNIST or a synthetic task) with:
    - Config-driven hyperparams
    - Logging of loss/metrics
    - Seed-setting.

---

### Day 5.2 – Debugging Training Loops
- Practice:
  - Take a working training loop and:
    - Introduce bugs (wrong LR, no shuffling, missing `.train()`/`.eval()`, etc.).
    - Diagnose them by monitoring loss curves.
- Write down:
  - A checklist for “training is not converging, what do I check?”.

---

### Day 5.3 – Performance & Profiling
- Study:
  - Common performance bottlenecks in PyTorch:
    - Data loading
    - Unnecessary CPU–GPU transfers
    - Non-vectorized operations
- Practice:
  - Profile a small model training loop.
  - Try to reduce runtime (batch size, fewer sync points, etc.).

---

### Day 5.4 – Paper Implementation Exercise I
- Choose a relatively simple paper (e.g., a small NLP or RL paper).
- Task:
  - Read only the core method section and pseudo-code.
  - Implement the key algorithm in a clean, modular way.
- Focus:
  - Match notation to code.
  - Identify and implement any missing details logically.

---

### Day 5.5 – Paper Implementation Exercise II
- Pick a different method (e.g., a variant of attention, or PPO/A2C).
- Implement:
  - The algorithm in code.
  - A tiny experiment to verify it behaves as expected (even on toy data).
- Afterward:
  - Write a 1–2 page summary in your `papers/` folder:
    - Problem
    - Method
    - Key equations
    - Implementation notes

---

### Day 5.6 – End-to-End Mini Project
- Combine your skills in a small end-to-end project:
  - Example 1: Tiny language model with your own Transformer.
  - Example 2: RL agent solving a small environment with A2C or PPO.
- Include:
  - Clean repo structure
  - README with how to run
  - Plots of training curves
- This becomes a strong talking point in interviews.

---

### Day 5.7 – RE Mock Interview
- Simulate:
  - “Here is a broken training script, fix it.” (You can create your own broken version.)
  - “Explain how you’d implement and debug PPO from a paper.”
  - “How do you organize experiments for a new idea?”
- Reflect:
  - How clearly you communicated trade-offs and experiment design.

---

## Week 6 – Full Mock Interviews & Consolidation

**Theme:** Tie everything together and simulate the real DeepMind process.

---

### Day 6.1 – Coding Mock #1
- 60–75 minutes:
  - 1 graph/DP problem.
  - 1 implementation-heavy problem (e.g., beam search, priority-based scheduler).
- Afterward:
  - Write a mini post-mortem:
    - What went well
    - What failed
    - Concrete improvements

---

### Day 6.2 – Coding Mock #2 (ML-Flavored)
- 60–75 minutes:
  - Implement a simple ML algorithm end-to-end, e.g.:
    - Logistic regression with GD
    - K-means clustering
- Be ready to:
  - Derive the update rules as you code.
  - Explain complexity & numerical stability.

---

### Day 6.3 – Math + ML Theory Mock
- 60–75 minutes:
  - Derivations:
    - Logistic regression gradient
    - KL between Gaussians
  - Conceptual:
    - SVD & PCA
    - Curse of dimensionality
    - Why overparameterized neural networks can still generalize
- Check:
  - Are your explanations crisp and structured?

---

### Day 6.4 – RL & Transformers Theory Mock
- 60–75 minutes:
  - Explain policy gradient theorem and REINFORCE.
  - Explain self-attention & multi-head attention.
  - Discuss trade-offs of Transformers vs RNNs/CNNs.

---

### Day 6.5 – Paper Discussion Mock
- Choose 1–2 of the following (or similar):
  - “Attention Is All You Need”
  - PPO paper
  - A diffusion model paper
- For one paper:
  - 10–15 min: explain the problem, method, and key contributions.
  - 10–15 min: discuss strengths, weaknesses, and extensions.
  - 10–15 min: describe *how you would implement it*.

---

### Day 6.6 – General Behavioral & RE Focused Chat
- Prepare answers for:
  - “Tell me about a time you debugged a very hard bug.”
  - “Describe a research project where you contributed most to the engineering.”
  - “How do you handle disagreements with researchers about design choices?”
- Emphasize:
  - Clarity, ownership, collaboration, and curiosity.

---

### Day 6.7 – Final Review & Light Day
- Skim:
  - Your derivations in `math/`
  - Your mini-project(s) in `projects/`
  - Notes & summaries in `papers/`
- Identify:
  - 3–5 key stories/experiences you want to highlight.
  - 3–5 technical areas you can confidently “go deep” on (Transformers, RL, etc.).

---

## How to Use This Plan

- Treat each “day” as one focused session (2–4 hours).  
- If you have more time, combine two days.  
- If you have less, split a day across multiple evenings.  
- Revisit any topic that feels weak, especially:
  - Transformer implementation
  - RL policy gradients
  - Matrix calculus & SVD
  - Debugging ML training loops

Good luck with your DeepMind preparation — this plan is designed so that at the end, you can confidently handle **coding, math, ML theory, and research engineering** interviews.
