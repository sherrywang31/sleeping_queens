from sleeping_queen.cards import *
from sleeping_queen.cards import _can_add_queen, _draw_queen
from sleeping_queen.game import Game


class TestCard:
    def test_dog_cat_together(self):
        assert _can_add_queen(queen_to_add = dog_queen, queens_in_hands=[cat_queen]) == False
        assert _can_add_queen(queen_to_add = dog_queen, queens_in_hands=[queen_10]) == True

    def test_draw_queen(self, game, player1, player2):
        queen = _draw_queen(player1, game)
        assert queen == dog_queen
        assert player1.queens == [queen_5,cat_queen]
        assert game.queen_pile == Deck(cards = [dog_queen, rose_queen, queen_20, queen_15])
        queen = _draw_queen(player2, game)
        assert queen == dog_queen
        assert player2.queens == [dog_queen]
        assert game.queen_pile == Deck(cards = [rose_queen, queen_20, queen_15])
    
    def test_wake_queen(self, player2, game):
        game.queen_pile = Deck(cards = [rose_queen, queen_20, queen_15])
        player2.queens = []
        wake_queen(player2, game)
        assert player2.queens == [rose_queen, queen_20]
        assert game.queen_pile == Deck(cards = [queen_15])
    
    def test_defend(self, player1, game):
        defend(player1, game)
        assert game.players[0].hand == [one, one, three, dragon, king, potion]
        assert game.players[1].hand == [king, potion, two, three, five, two]
        assert game.draw_pile.cards == [three, four]

    def test_take_queen(self, player2, game):
        take_queen(player2, game)
        assert player2.queens == [queen_5]
        assert game.players[0].queens == [cat_queen]
        player3 = Player(name='Player 3', hand=[], queens=[cat_queen])
        player4= Player(name='Player 4', hand=[], queens=[dog_queen, queen_5])
        game = Game([player3, player4])
        take_queen(player3, game)
        assert player3.queens == [cat_queen, queen_5]
        assert player4.queens == [dog_queen]




