import pytest
from sleeping_queen.data_type import Card, Deck, Player
from sleeping_queen.game import Game
from sleeping_queen.cards import *

class TestPlayer:
    def test_score(self, player1):
        assert player1.score() == 20

    def test_draw(self, game, player1):
        draw_count = 2
        draws = player1.draw(game, draw_count)
        assert player1.hand == [one,one,three,dragon, king, potion, two]
        assert draws == [potion, two]
        assert game.draw_pile == Deck(cards = [three, four])

    def test_play(self, player1, game):
        player1.play(cards = [one, one], game=game)
        assert player1.hand == [three,dragon,king]
        assert game.discard_pile == [king, one, king, two, three, one, one]
    
    def test_success_false(self, player1):
        assert player1.success() == False
    
    def test_success_true(self):
        player_score = Player(name='Player 1', 
                            hand=[], 
                            queens=[Card('Queen 5', 5), Card('Cat Queen', 15), Card('Queen 20', 20), Card('Queen 10', 10)])
        player_nqueue = Player(name='Player 1', 
                            hand=[], 
                            queens=[Card('Queen 5', 0), Card('Cat Queen', 0), Card('Queen 5', 0), Card('Queen 5', 0), Card('Queen 5', 0)])
        assert player_score.success() == True
        assert player_nqueue.success() == True