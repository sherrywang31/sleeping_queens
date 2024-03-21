from dataclasses import dataclass
import random
from typing import List, Optional
from itertools import combinations
import sys

@dataclass
class Card:
    name: str
    point: Optional[int] = None
    
@dataclass
class Deck:
    cards: List[str]

    def shuffle(self):
        random.shuffle(self.cards)

    def count(self):
        return(len(self.cards))
    
    def draw(self):
        return self.cards.pop(0)
    
rose_queen = Card('Rose Queen', 5)
cat_queen = Card('Cat Queen', 15)
dog_queen = Card('Dog Queen', 15)
queen_5 = Card('Queen 5', 5)
queen_10 = Card('Queen 10', 10)
queen_15 = Card('Queen 15', 15)
queen_20 = Card('Queen 20', 20)
king = Card('King')
jester = Card('Jester')
knight = Card('Knight')
potion = Card('Potion')
wand = Card('Wand')
dragon = Card('Dragon')
one= Card('1', 1)
two = Card('2', 2)
three = Card('3', 3)
four = Card('4', 4)
five = Card('5', 5)
six = Card('6', 6)
seven = Card('7', 7)
eight = Card('8', 8)
nine = Card('9', 9)
ten = Card('10', 10)

ALL_CARDS = Deck([king] * 8 + 
            [jester] * 5 + 
            [knight] * 4 + 
            [potion] * 4 + 
            [wand] * 3 + 
            [dragon] * 3 + 
            ([one] + [two] + [three] + [four] + [five] + [six] + [seven] + [eight] + [nine] + [ten]) * 4)
QUEENS = Deck([cat_queen] + [dog_queen] + [rose_queen] + [queen_5] * 3 + [queen_10] * 4 + [queen_15] + [queen_20])


@dataclass
class Player:
    name: str
    hand: List[Card]
    queens: List[Card] # TODO: queens should be a separate class?

    def score(self):
        return sum([card.point for card in self.queens])
    

    def draw(self, draw_pile:Deck, count: int) -> List[Card]:
        '''
        Current player draws count cards from the draw pile.
        '''
        draws = []
        for _ in range(count):
            draws.append(draw_pile.draw())
        self.hand = self.hand + draws
        return(draws)

    def play(self, cards: List[Card]) -> None:
        '''
        Current player plays a card from their hand. 
        It is removed from their hand and added to the discard pile.
        '''
        for card in cards:
            self.hand.remove(card)

    def success(self) -> bool:
        score = self.score() >= 50
        queens = len(self.queens) >= 5
        return score or queens
    
    def _dog_cat_together(self, queen:Card) -> bool:
        if queen == cat_queen:
            return dog_queen in self.queens
        if queen == dog_queen:
            return cat_queen in self.queens
        return False
    
    def _draw_queen(self, queen_pile:Deck) -> Card:
        queen = self.draw(queen_pile, 1)[0] # only 1 item in the list
        if not self._dog_cat_together(queen):
            self.queens.append(queen)
        else: # can't draw this queen. put it back to the queen pile
            queen_pile.cards = [queen] + queen_pile.cards
        return(queen)
    
    def wake_queen(self, queen_pile:Deck) -> None:
        queen = self._draw_queen(queen_pile)
        if queen.name == 'Rose Queen':
            self._draw_queen(queen_pile)

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

    def _play_cards_legal(self, current_player:int, cards_to_play: List[Card]) -> bool:
        player = self.players[current_player]
        opponent = 0 if current_player == 1 else 1
        opponent = self.players[opponent]
        if not all([card in player.hand for card in cards_to_play]):
            return False
        if any(card in [dragon, wand] for card in cards_to_play):
            print(f'Invalid input. {cards_to_play} can not be played. Try again.')
            return False
        if len(cards_to_play) == 1:
            if cards_to_play[0] in [king, knight, potion]:
                if len(opponent.queens) == 0:
                    print(f'Invalid input. {cards_to_play} can not be played because opponent has no queen. Try again.')
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
    
    def knight_effect(self, current_player:int):
        self.discard_pile = self.players[current_player].play(self.discard_pile, [knight])
        passive_player = 0 if current_player == 1 else 1
        if dragon in self.players[passive_player].hand:
            action = input('Do you want to play the dragon? (y/n)')
            if action == 'y':
                self.discard_pile = self.players[passive_player].play(self.discard_pile, [dragon])
                self.draw_pile, _ = self.players[passive_player].draw(self.draw_pile, 1)
                self.draw_pile, _ = self.players[current_player].draw(self.draw_pile, 1)
        action = input('Pick a queue from {opponent.queens}')
        while action not in [queen.name for queen in self.players[passive_player].queens]:
            action = input('Invalid input: {action}. Pick a queue from {opponent.queens}')
        self.players[passive_player].queens.remove(globals()[action]) # TODO: fix this
        self.players[current_player].queens.append(globals()[action])
        
    def potion_effect(self, current_player:int):
        self.discard_pile = self.players[current_player].play(self.discard_pile, [potion])
        passive_player = 0 if current_player == 1 else 1
        if wand in self.players[passive_player].hand:
            action = input('Do you want to play the wand? (y/n)')
            if action == 'y':
                self.discard_pile = self.players[passive_player].play(self.discard_pile, [wand])
                self.draw_pile, _ = self.players[passive_player].draw(self.draw_pile, 1)
                self.draw_pile, _ = self.players[current_player].draw(self.draw_pile, 1)
        action = input('Pick a queue from {opponent.queens}')
        while action not in [queen.name for queen in self.players[passive_player].queens]:
            action = input('Invalid input: {action}. Pick a queen from {opponent.queens}')
        self.players[passive_player].queens.remove(globals()[action]) # TODO: fix this
        self.queens.append(globals()[action])
    
    def jester_effect(self, current_player:int):
        self.discard_pile = self.players[current_player].play(self.discard_pile, [jester])
        while self.draw_pile[0] in [king, knight, potion, wand, dragon]:
            self.draw_pile, _ = self.players[current_player].draw(self.draw_pile, 1)
        else:
            if self.draw_pile[0] in [one, three, five, seven, nine]:
                self.players[current_player].wake_queen(self.queen_pile)
            else:
                self.players[0 if current_player == 1 else 1].wake_queen(self.queen_pile)

    def king_effect(self, current_player:int):
        self.players[current_player].play([king])
        self.discard_pile.append(king)
        self.players[current_player].wake_queen(self.queen_pile)
        
    def step(self):
        if self.round == 0:
            # initial setup
            self.draw_pile.shuffle()
            self.queen_pile.shuffle()
            for player in self.players:
                player.draw(self.draw_pile, 5)
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
                player.play(cards_to_play)
                self.discard_pile.append(cards_to_play)
                player.draw(self.draw_pile, len(cards_to_play))
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
                    player.play(cards_to_play)
                    self.discard_pile.append(cards_to_play)
                    player.draw(self.draw_pile, len(cards_to_play))
            # draw
            player.draw(self.draw_pile, 1)
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