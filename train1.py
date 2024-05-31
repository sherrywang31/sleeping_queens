import numpy as np
import random
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from gymnasium.spaces import Discrete, Box
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

# Define the customized Sleeping Queens environment
class SleepingQueensEnv(AECEnv):
    metadata = {'render.modes': ['human'], "name": "sleeping_queens_v0"}

    def __init__(self):
        super().__init__()

        self.num_players = 2
        self.num_queens = 12
        self.max_points = 50
        self.hand_size = 5

        # 7 main actions + additional discard combinations
        self.action_space = Discrete(7 + 32)
        self.observation_space = Box(low=0, high=1, shape=(self.num_queens*2 + self.hand_size*2,), dtype=np.int32)

        self.agents = ["player_1", "player_2"]
        self.agent_name_mapping = dict(zip(self.agents, list(range(len(self.agents)))))
        self._agent_selector = agent_selector(self.agents)

        self.reset() # Ensure reset is called to initialize attributes

    def reset(self):
        # Initialize game state
        self.queens = [0] * self.num_queens  # 0 = sleeping, 1 = player 1, 2 = player 2
        self.points = [0, 0]  # Points for player 1 and player 2
        self.hands = [self.draw_hand() for _ in range(self.num_players)]
        self.draw_pile = self.generate_draw_pile()
        self.discard_pile = []
        self.dones = {agent: False for agent in self.agents}

        self.current_agent = self._agent_selector.reset()
        self.num_moves = 0

    def generate_draw_pile(self):
        draw_pile = (
            ['K']*8 + ['Kn']*4 + ['D']*3 + ['J']*5 +
            ['P']*4 + ['W']*3 + list(range(1, 11))*4
        )
        random.shuffle(draw_pile)
        return draw_pile

    def draw_hand(self):
        return [self.draw_card() for _ in range(self.hand_size)]

    def draw_card(self):
        if not self.draw_pile:
            self.draw_pile, self.discard_pile = self.discard_pile, []
            random.shuffle(self.draw_pile)
        return self.draw_pile.pop()

    def play_counter(self, action, opponent_hand):
        if action == 1 and 'D' in opponent_hand:  # Counter a Knight with a Dragon
            opponent_hand.remove('D')
            self.discard_pile.extend(['Kn', 'D'])
            return True
        elif action == 3 and 'W' in opponent_hand:  # Counter a Sleeping Potion with a Wand
            opponent_hand.remove('W')
            self.discard_pile.extend(['P', 'W'])
            return True
        return False

    def awaken_queen(self, agent_id, queen_index):
        self.queens[queen_index] = agent_id + 1
        if queen_index == 0:  # Rose Queen special power
            for i in range(len(self.queens)):
                if self.queens[i] == 0:
                    self.queens[i] = agent_id + 1
                    break
        self.check_cat_dog_rule(agent_id)

    def check_cat_dog_rule(self, agent_id):
        cat_queen_index = 1  # Assuming Cat Queen is at index 1
        dog_queen_index = 2  # Assuming Dog Queen is at index 2
        if self.queens[cat_queen_index] == agent_id + 1 and self.queens[dog_queen_index] == agent_id + 1:
            self.queens[dog_queen_index] = 0  # Put Dog Queen back to sleep

    def is_action_valid(self, action, hand):
        if action == 0 and 'K' not in hand:  # Play a King
            return False
        if action == 1 and 'Kn' not in hand:  # Play a Knight
            return False
        if action == 2:  # Play a Dragon (reactive action)
            return False
        if action == 3 and 'P' not in hand:  # Play a Sleeping Potion
            return False
        if action == 4:  # Play a Wand (reactive action)
            return False
        if action == 5 and 'J' not in hand:  # Play a Jester
            return False
        if action >= 7 and not self.is_discard_valid(action - 7, hand):  # Discard actions
            return False
        return True

    def is_discard_valid(self, discard_action, hand):
        indices = self.get_discard_indices(discard_action, len(hand))
        discard_cards = [hand[i] for i in indices]
        if len(discard_cards) == 1:
            return True
        if len(discard_cards) == 2 and isinstance(discard_cards[0], int) and discard_cards[0] == discard_cards[1]:
            return True
        if len(discard_cards) >= 3 and all(isinstance(card, int) for card in discard_cards) and sum(discard_cards[:-1]) == discard_cards[-1]:
            return True
        return False

    def get_discard_indices(self, discard_action, hand_size):
        indices = []
        for i in range(hand_size):
            if discard_action & (1 << i):
                indices.append(i)
        return indices

    def step(self, action):
        agent = self.current_agent
        agent_id = self.agent_name_mapping[agent]
        opponent_id = (agent_id + 1) % self.num_players
        hand = self.hands[agent_id]
        opponent_hand = self.hands[opponent_id]

        if not self.is_action_valid(action, hand):
            print(f"Invalid action: {action} by {agent}")
            self.num_moves -= 1
            self.current_agent = self._agent_selector.next()
            return

        if action == 0:  # Play a King
            hand.remove('K')
            for i in range(len(self.queens)):
                if self.queens[i] == 0:
                    self.awaken_queen(agent_id, i)
                    break
        elif action == 1:  # Play a Knight
            hand.remove('Kn')
            if not self.play_counter(action, opponent_hand):
                for i in range(len(self.queens)):
                    if self.queens[i] == opponent_id + 1:
                        self.queens[i] = agent_id + 1
                        break
        elif action == 3:  # Play a Sleeping Potion
            hand.remove('P')
            if not self.play_counter(action, opponent_hand):
                for i in range(len(self.queens)):
                    if self.queens[i] == opponent_id + 1:
                        self.queens[i] = 0
                        break
        elif action == 5:  # Play a Jester
            hand.remove('J')
            drawn_card = self.draw_card()
            if drawn_card in ['K', 'Kn', 'D', 'P', 'W', 'J']:
                hand.append(drawn_card)
                self.num_moves -= 1
            else:
                count = drawn_card
                target_player = (agent_id + count) % self.num_players
                for i in range(len(self.queens)):
                    if self.queens[i] == 0:
                        self.awaken_queen(target_player, i)
                        break
        elif action >= 7:  # Discard cards to draw new ones
            discard_action = action - 7
            discard_indices = self.get_discard_indices(discard_action, len(hand))
            hand = self.discard_and_draw(hand, discard_indices)

        while len(hand) < self.hand_size:
            hand.append(self.draw_card())

        self.hands[agent_id] = hand
        self.points[agent_id] = sum([queen for queen in self.queens if queen == agent_id + 1])
        if self.points[agent_id] >= self.max_points or self.queens.count(agent_id + 1) >= 5:
            self.dones = {agent: True for agent in self.agents}
        else:
            self.dones = {agent: False for agent in self.agents}

        self.num_moves += 1
        self.current_agent = self._agent_selector.next()

    def discard_and_draw(self, hand, discard_indices):
        discard_cards = [hand[i] for i in discard_indices]
        if len(discard_cards) == 1 or \
           (len(discard_cards) == 2 and isinstance(discard_cards[0], int) and discard_cards[0] == discard_cards[1]) or \
           (len(discard_cards) >= 3 and all(isinstance(card, int) for card in discard_cards) and sum(discard_cards[:-1]) == discard_cards[-1]):
            for i in sorted(discard_indices, reverse=True):
                del hand[i]
            self.discard_pile.extend(discard_cards)
            hand.extend(self.draw_card() for _ in discard_cards)
        return hand

    def render(self, mode='human'):
        print(f"Queens: {self.queens}")
        print(f"Points: {self.points}")
        print(f"Player Hands: {self.hands}")
        print(f"Draw Pile: {len(self.draw_pile)} cards")
        print(f"Discard Pile: {self.discard_pile}")

    def observe(self, agent):
        agent_id = self.agent_name_mapping[agent]
        opponent_id = (agent_id + 1) % 2
        return np.array(self.queens + self.hands[agent_id] + self.hands[opponent_id])

# Initialize the environment
env = SleepingQueensEnv()

# Check the environment to ensure it's valid
check_env(env, warn=True)

# Wrap the environment in a DummyVecEnv for Stable-Baselines3
vec_env = DummyVecEnv([lambda: env])

# Define the model
model = PPO('MlpPolicy', vec_env, verbose=1)

# Train the model
model.learn(total_timesteps=100000)

# Save the model
model.save("ppo_sleeping_queens")

# Optionally, load the model
# model = PPO.load("ppo_sleeping_queens")

# Evaluate the model (optional)
obs = vec_env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render()
