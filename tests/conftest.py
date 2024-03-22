import pytest 
from sleeping_queen.data_type import Card, Deck, Player
from sleeping_queen.cards import *
from sleeping_queen.game import Game

@pytest.fixture
def player1():
    return Player(name='Player 1', 
                  hand=[one,one,three, dragon, king], 
                  queens=[queen_5,cat_queen])
@pytest.fixture
def player2():
    return Player(name='Player 2', 
                  hand=[king, potion, two, three, five], 
                  queens=[])

@pytest.fixture
def draw_pile():
    return Deck(cards = [potion, two, three, four])

@pytest.fixture
def discard_pile():
    return [king, one, king, two, three]

@pytest.fixture
def game(player1, player2, discard_pile, draw_pile):
    game = Game([player1, player2])
    game.discard_pile = discard_pile
    game.draw_pile = draw_pile
    game.queen_pile = Deck(cards = [dog_queen, rose_queen, queen_20, queen_15])
    game.round = 1
    return game