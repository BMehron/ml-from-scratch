1. Deriving Policy Gradient:

Consider the case of a stochastic, parameterized policy, \pi_{\theta}. We aim to maximize the expected return J(\pi_{\theta}) = \underE{\tau \sim \pi_{\theta}}{R(\tau)}. For the purposes of this derivation, we’ll take R(\tau) to give the finite-horizon undiscounted return, but the derivation for the infinite-horizon discounted return setting is almost identical.

We would like to optimize the policy by gradient ascent, eg

\theta_{k+1} = \theta_k + \alpha \left. \nabla_{\theta} J(\pi_{\theta}) \right|_{\theta_k}.

The gradient of policy performance, \nabla_{\theta} J(\pi_{\theta}), is called the policy gradient, and algorithms that optimize the policy this way are called policy gradient algorithms.

Probability of a Trajectory. The probability of a trajectory \tau = (s_0, a_0, ..., s_{T+1}) given that actions come from \pi_{\theta} is

P(\tau|\theta) = \rho_0 (s_0) \prod_{t=0}^{T} P(s_{t+1}|s_t, a_t) \pi_{\theta}(a_t |s_t).


grad G = grad integral [P(trajectory) R_trajectory] = integral grad [P(trajectory) * R_trajectory] = integral grad [P(trajectory)] * R_trajectory

grad F = F * grad log F

grad G = integral [grad P(trajectory)] * R_trajectory = integral P(trajectory) [grad log P(trajectory)] * R_trajectory = 
= E[[grad log P(trajectory)] * R_trajectory]

grad log P(trajectory) = grad [log P(s_0) + sum log P(s_i+1 | s_i, a_i) + log pi(a_i | s_i)] = sum grad log pi(a_i | s_i)

grad G = E[[sum grad log pi(a_i | s_i)] R_trajectory]. We can estimate this expectation with sample mean. If we collect a set of trajectories D where each trajectory is obtained by letting the agent act in the environment using the policy \pi_{\theta}, the policy gradient can be estimated with:

\hat{g} = \frac{1}{|\mathcal{D}|} \sum_{\tau \in \mathcal{D}} \sum_{t=0}^{T} \nabla_{\theta} \log \pi_{\theta}(a_t |s_t) R(\tau),