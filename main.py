from dataclasses import dataclass
import random
from typing import List, Optional

@dataclass
class Card:
    name: str
    point: Optional[int] = None
    effect: Optional[function] = None # TODO: implement effect``
    
@dataclass
class Deck:
    cards: List[str]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)

    def count(self):
        return(len(self.cards))

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

draw_pile = Deck([king] * 8 + 
            [jester] * 5 + 
            [knight] * 4 + 
            [potion] * 4 + 
            [wand] * 3 + 
            [dragon] * 3 + 
            ([one] + [two] + [three] + [four] + [five] + [six] + [seven] + [eight] + [nine] + [ten]) * 4)
queens = Deck([cat_queen] + [dog_queen] + [rose_queen] + [queen_5] * 3 + [queen_10] * 4 + [queen_15] + [queen_20])
discards = Deck([])

@dataclass
class Player:
    name: str
    hand: List[Card]
    queens: List[Card] # TODO: queens should be a separate class?
    score: int = 0

    def draw(self, count: int):
        for _ in range(count):
            self.hand.append(draw_pile.draw())

    def play(self, card: Card):
        self.hand.remove(card)
        discards.cards.append(card)

    def score(self):
        return sum([card.point for card in self.queens])

    def __str__(self):
        return f'{self.name} has {self.hand}'