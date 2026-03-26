from sleeping_queen.rl_solver import solve_with_reinforcement_learning


if __name__ == "__main__":
    _, win_rate = solve_with_reinforcement_learning(episodes=25_000, seed=42)
    print(f"Solved policy win rate (vs random policy): {win_rate:.1%}")
