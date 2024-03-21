from dataclasses import dataclass
from typing import List, Optional, Callable
import random

@dataclass
class Card:
    name: str
    point: Optional[int] = None
    effect: Optional[Callable] = None # todo: take game, player as input
            
@dataclass
class Deck:
    cards: List[str]

    def shuffle(self):
        random.shuffle(self.cards)

    def count(self):
        return(len(self.cards))
    
    def draw(self):
        return self.cards.pop(0)

@dataclass
class Player:
    name: str
    hand: List[Card]
    queens: List[Card] # TODO: queens should be a separate class?

    def score(self):
        return sum([card.point for card in self.queens])
    

    def draw(self, game, count: int) -> List[Card]:
        '''
        Current player draws count cards from the draw pile.
        '''
        draws = []
        for _ in range(count):
            draws.append(game.draw_pile.draw())
        self.hand = self.hand + draws
        return(draws)

    def play(self, cards: List[Card], game) -> None:
        '''
        Current player plays a card from their hand. 
        It is removed from their hand and added to the discard pile.
        '''
        for card in cards:
            self.hand.remove(card)
            game.discard_pile.append(card)
            if card.effect is not None:
                game.executeCardEffect(card=card, player=self)

    def success(self) -> bool:
        score = self.score() >= 50
        queens = len(self.queens) >= 5
        return score or queens