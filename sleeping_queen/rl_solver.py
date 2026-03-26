from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random
from typing import DefaultDict, Dict, List, Tuple

State = Tuple[int, int, int, int, int, int, int]
QTable = DefaultDict[State, List[float]]


@dataclass
class MiniSleepingQueensEnv:
    """A compact Sleeping Queens inspired environment for tabular RL.

    The learning agent (player 0) always acts first and plays against a random
    policy opponent (player 1).
    """

    max_score: int = 50
    max_queens: int = 5
    max_turns: int = 60

    def __post_init__(self) -> None:
        self.rng = random.Random()
        self.queen_values = [5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 20]
        self.deck_template = ["K"] * 8 + ["Kn"] * 4 + ["P"] * 4 + ["J"] * 5 + ["N"] * 20
        self.reset()

    def seed(self, seed: int) -> None:
        self.rng.seed(seed)

    def reset(self, seed: int | None = None) -> State:
        if seed is not None:
            self.seed(seed)
        self.turn_count = 0
        self.sleeping_queens = self.queen_values[:]
        self.awake_queens: List[List[int]] = [[], []]
        self.hands = [self._draw_hand(), self._draw_hand()]
        return self._state()

    def _draw_hand(self) -> Dict[str, int]:
        cards = {"K": 0, "Kn": 0, "P": 0, "J": 0, "N": 0}
        for _ in range(5):
            cards[self.rng.choice(self.deck_template)] += 1
        return cards

    def _draw_one(self, player: int) -> None:
        self.hands[player][self.rng.choice(self.deck_template)] += 1

    def _state(self) -> State:
        my_score = min(sum(self.awake_queens[0]) // 5, 10)
        opp_score = min(sum(self.awake_queens[1]) // 5, 10)
        sleeping = min(len(self.sleeping_queens), 12)
        hand = self.hands[0]
        return (
            my_score,
            opp_score,
            sleeping,
            min(hand["K"], 4),
            min(hand["Kn"], 4),
            min(hand["P"], 4),
            min(hand["J"], 4),
        )

    def legal_actions(self, player: int) -> List[int]:
        hand = self.hands[player]
        actions = [4]  # always can discard/pass
        if hand["K"] > 0 and self.sleeping_queens:
            actions.append(0)
        if hand["Kn"] > 0 and self.awake_queens[1 - player]:
            actions.append(1)
        if hand["P"] > 0 and self.awake_queens[1 - player]:
            actions.append(2)
        if hand["J"] > 0 and self.sleeping_queens:
            actions.append(3)
        return actions

    def _apply_action(self, player: int, action: int) -> None:
        opp = 1 - player
        hand = self.hands[player]

        if action == 0:
            hand["K"] -= 1
            queen = self.sleeping_queens.pop(self.rng.randrange(len(self.sleeping_queens)))
            self.awake_queens[player].append(queen)
        elif action == 1:
            hand["Kn"] -= 1
            queen = max(self.awake_queens[opp])
            self.awake_queens[opp].remove(queen)
            self.awake_queens[player].append(queen)
        elif action == 2:
            hand["P"] -= 1
            queen = max(self.awake_queens[opp])
            self.awake_queens[opp].remove(queen)
            self.sleeping_queens.append(queen)
        elif action == 3:
            hand["J"] -= 1
            target = player if self.rng.random() < 0.5 else opp
            queen = self.sleeping_queens.pop(self.rng.randrange(len(self.sleeping_queens)))
            self.awake_queens[target].append(queen)
        else:
            if hand["N"] > 0:
                hand["N"] -= 1

        self._draw_one(player)

    def _winner(self) -> int | None:
        for player in (0, 1):
            score = sum(self.awake_queens[player])
            if score >= self.max_score or len(self.awake_queens[player]) >= self.max_queens:
                return player
        return None

    def step(self, action: int) -> Tuple[State, float, bool]:
        self.turn_count += 1
        pre_score = sum(self.awake_queens[0]) - sum(self.awake_queens[1])
        legal = self.legal_actions(player=0)
        if action not in legal:
            action = 4

        self._apply_action(player=0, action=action)
        winner = self._winner()
        if winner is not None:
            return self._state(), 1.0 if winner == 0 else -1.0, True

        if self.sleeping_queens:
            opp_action = self.rng.choice(self.legal_actions(player=1))
            self._apply_action(player=1, action=opp_action)

        winner = self._winner()
        done = winner is not None or self.turn_count >= self.max_turns or not self.sleeping_queens
        score_delta = (sum(self.awake_queens[0]) - sum(self.awake_queens[1])) - pre_score
        shaped_reward = score_delta / 20.0
        if not done:
            return self._state(), shaped_reward, False
        if winner is None:
            my_score = sum(self.awake_queens[0])
            opp_score = sum(self.awake_queens[1])
            if my_score == opp_score:
                return self._state(), shaped_reward, True
            terminal = 0.5 if my_score > opp_score else -0.5
            return self._state(), terminal + shaped_reward, True
        terminal = 1.0 if winner == 0 else -1.0
        return self._state(), terminal + shaped_reward, True


def epsilon_greedy_action(q_table: QTable, state: State, legal_actions: List[int], epsilon: float, rng: random.Random) -> int:
    if rng.random() < epsilon:
        return rng.choice(legal_actions)
    values = q_table[state]
    return max(legal_actions, key=lambda a: values[a])


def train_q_learning(
    episodes: int = 20_000,
    alpha: float = 0.1,
    gamma: float = 0.97,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    seed: int = 0,
) -> QTable:
    env = MiniSleepingQueensEnv()
    env.seed(seed)
    rng = random.Random(seed)
    q_table: QTable = defaultdict(lambda: [0.0] * 5)

    for episode in range(episodes):
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * max(0.0, (episodes - episode) / episodes)
        state = env.reset()
        done = False

        while not done:
            legal = env.legal_actions(player=0)
            action = epsilon_greedy_action(q_table, state, legal, epsilon, rng)
            next_state, reward, done = env.step(action)
            next_legal = env.legal_actions(player=0)
            next_best = max(q_table[next_state][a] for a in next_legal)
            td_target = reward + gamma * (0.0 if done else next_best)
            q_table[state][action] += alpha * (td_target - q_table[state][action])
            state = next_state

    return q_table


def evaluate_policy(q_table: QTable, games: int = 2_000, seed: int = 1) -> float:
    env = MiniSleepingQueensEnv()
    env.seed(seed)
    wins = 0
    for _ in range(games):
        state = env.reset()
        done = False
        while not done:
            legal = env.legal_actions(player=0)
            action = max(legal, key=lambda a: q_table[state][a])
            state, reward, done = env.step(action)
        if reward > 0:
            wins += 1
    return wins / games


def solve_with_reinforcement_learning(episodes: int = 20_000, seed: int = 0) -> Tuple[QTable, float]:
    q_table = train_q_learning(episodes=episodes, seed=seed)
    win_rate = evaluate_policy(q_table, seed=seed + 1)
    return q_table, win_rate


if __name__ == "__main__":
    learned_q, rate = solve_with_reinforcement_learning()
    print(f"Trained {len(learned_q)} states.")
    print(f"Greedy policy win rate vs random opponent: {rate:.1%}")
