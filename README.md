# sleeping_queens

A lightweight Sleeping Queens simulator with a tabular reinforcement-learning solver.

## Train a policy

```bash
python train1.py
```

This trains a Q-learning agent against a random opponent in a compact
Sleeping-Queens-inspired environment and prints the final win rate.

## Programmatic usage

```python
from sleeping_queen.rl_solver import solve_with_reinforcement_learning

q_table, win_rate = solve_with_reinforcement_learning(episodes=20_000, seed=0)
print(win_rate)
```
