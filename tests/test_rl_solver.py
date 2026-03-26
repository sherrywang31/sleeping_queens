from sleeping_queen.rl_solver import MiniSleepingQueensEnv, evaluate_policy, train_q_learning


def test_legal_actions_are_always_playable():
    env = MiniSleepingQueensEnv()
    state = env.reset(seed=7)
    for _ in range(10):
        legal = env.legal_actions(player=0)
        assert legal
        action = legal[0]
        state, _, done = env.step(action)
        if done:
            break
    assert isinstance(state, tuple)


def test_training_produces_competitive_policy():
    q_table = train_q_learning(episodes=3000, seed=11)
    win_rate = evaluate_policy(q_table, games=300, seed=12)
    assert len(q_table) > 0
    assert win_rate >= 0.20
