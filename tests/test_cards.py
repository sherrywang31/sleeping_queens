from sleeping_queen.cards import *
from sleeping_queen.cards import _can_add_queen, _draw_queen


class TestCard:
    def test_dog_cat_together(self):
        assert _can_add_queen(queen_to_add = dog_queen, queens_in_hands=[cat_queen]) == False
        assert _can_add_queen(queen_to_add = dog_queen, queens_in_hands=[queen_10]) == True

    def test_draw_queen(self, game, player1, player2):
        queen = _draw_queen(player1, game)
        assert queen == dog_queen
        assert player1.queens == [five,cat_queen]
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



