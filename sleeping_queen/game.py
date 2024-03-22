from sleeping_queen.data_type import Card, Deck, Player
from typing import List
from itertools import combinations
import sys
from sleeping_queen.cards import _can_add_queen, king, jester, knight, potion, wand, dragon, one, two, three, four, five, six, seven, eight, nine, ten, cat_queen, dog_queen, rose_queen, queen_5, queen_10, queen_15, queen_20

ALL_CARDS = Deck([king] * 8 + 
            [jester] * 5 + 
            [knight] * 4 + 
            [potion] * 4 + 
            [wand] * 3 + 
            [dragon] * 3 + 
            ([one] + [two] + [three] + [four] + [five] + [six] + [seven] + [eight] + [nine] + [ten]) * 4)
QUEENS = Deck([cat_queen] + [dog_queen] + [rose_queen] + [queen_5] * 3 + [queen_10] * 4 + [queen_15] + [queen_20])

class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.draw_pile = ALL_CARDS
        self.queen_pile = QUEENS
        self.discard_pile = []
        self.round = 0
        self.end_game = False
    
    @staticmethod
    def _check_sum(numbers:List[int]):
        # Iterate over each number in the list
        for index, total in enumerate(numbers):
            # Exclude the current number and get the rest of the list
            others = numbers[:index] + numbers[index+1:]
            # Check every combination of the remaining numbers
            for r in range(1, len(others) + 1):
                for combo in combinations(others, r):
                    if sum(combo) == total:
                        return True
        return False
    def _can_take_queen(self, current_player:int):
        player = self.players[current_player]
        opponent = 0 if current_player == 1 else 1
        opponent = self.players[opponent]
        if (opponent.queens == [cat_queen]) & (dog_queen in player.queens):
            return False
        elif (opponent.queens == [dog_queen]) & (cat_queen in player.queens):
            return False
        return True
    def _play_cards_legal(self, current_player:int, cards_to_play: List[Card]) -> bool:
        player = self.players[current_player]
        opponent = 0 if current_player == 1 else 1
        opponent = self.players[opponent]
        if not all([card in player.hand for card in cards_to_play]):
            print(f'Invalid input. You do not have {cards_to_play} in hands. Try again.')
            return False
        if len(cards_to_play) == 1:
            if cards_to_play[0] in [dragon, wand]:
                print(f'Invalid input. {cards_to_play} is a defend card; it can not be played. Try again.')
                return False
            if (cards_to_play[0] in [king, knight, potion]) & (len(opponent.queens) == 0):
                    print(f'Invalid input. {cards_to_play} can not be played because opponent has no queen. Try again.')
                    return False
            if (cards_to_play[0] in [king, knight]) & (not self._can_take_queen(current_player)):
                    print(f'Invalid input. can not take queen but {cards_to_play} is played. Try again.')
                    return False

        else:
            if not all([card in [one, two, three, four, five, six, seven, eight, nine, ten] for card in cards_to_play]):
                print(f'Invalid input. {cards_to_play} 1+ card played all must be number cards. Try again.')
                return False
            if len(cards_to_play) ==2: 
                print(f'Invalid input. {cards_to_play} are not a pair. Try again.')
                return len(set([c.name for c in cards_to_play])) == 1 # pair
            else:
                print(f'Invalid input.{cards_to_play} failed check sum. Try again.')
                return self._check_sum([c.point for c in cards_to_play])
        return True
    
    def executeCardEffect(self, card:Card, player:Player):
        card.effect(game=self, player=player)
        
    def step(self):
        if self.round == 0:
            # initial setup
            self.draw_pile.shuffle()
            self.queen_pile.shuffle()
            for player in self.players:
                player.draw(self, 5)
        self.round += 1
        current_player = 0
        print(f'Round {self.round}')
        for player in self.players:
            # play cards
            cards_valid = False
            while not cards_valid:
                card_indices = input('Indices of cards to play? Comma seperated!')
                card_indices = card_indices.split(',')
                # check if indices are valid
                try:
                    cards_to_play = [player.hand[int(i)] for i in card_indices]
                except:
                    print('Invalid input. Try again.')
                    continue
                # check if cards are valid
                cards_valid = self._play_cards_legal(current_player, cards_to_play)
            if cards_to_play > 1:
                # discard cards and draw
                player.play(cards_to_play, self)
                player.draw(self, len(cards_to_play))
            else: # always take the first card because cards_to_play only has 1 card
                if cards_to_play[0] == knight:
                    self.knight_effect(current_player)
                elif cards_to_play[0] == jester:
                    self.jester_effect(current_player)
                elif cards_to_play[0] == potion:
                    self.potion_effect(current_player)
                elif cards_to_play[0] == king:
                    self.king_effect(current_player)
                else: # discard cards and draw
                    player.play(cards_to_play, self)
                    player.draw(self, len(cards_to_play))
            # draw
            player.draw(self, 1)
            # check if game is over
            if player.success():
                print(f'{player.name} won!')
                self.end_game = True
                sys.exit()
            current_player = 0 if current_player == 1 else 1 # switch players
        print('Round over')
        print('')

if __name__ == '__main__':
    player1 = Player('Player 1', [], [])
    player2 = Player('Player 2', [], [])
    game = Game([player1, player2])
    while not game.end_game:
        game.step()