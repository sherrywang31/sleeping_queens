import pytest
from main import Card, Deck, Player, Game

@pytest.fixture
def player1():
    return Player(name='Player 1', 
                  hand=[Card('1', 1),Card('1', 1),Card('3', 3), Card('Dragon'), Card('King')], 
                  queens=[Card('Queen 5', 5),Card('Cat Queen', 15)])
@pytest.fixture
def player2():
    return Player(name='Player 2', 
                  hand=[Card('King'), Card('Potion'), Card('2', 2), Card('3', 3), Card('5', 5)], 
                  queens=[])

@pytest.fixture
def draw_pile():
    return Deck(cards = [Card('Potion'), Card('2', 2), Card('3', 3), Card('4', 4)])

@pytest.fixture
def discard_pile():
    return Deck(cards=[Card('King'), Card('1', 1), Card('King'), Card('2', 2), Card('3', 3)])

@pytest.fixture
def game(player1, player2, discard_pile, draw_pile):
    game = Game([player1, player2])
    game.discards = discard_pile
    game.draw_pile = draw_pile
    game.queen_pile = Deck(cards = [Card('Dog Queen', 15), Card('Rose Queen', 5), Card('Queen 20', 20), Card('Queen 15', 15)])
    game.round = 1
    return game

class TestPlayer:
    def test_score(self, player1):
        assert player1.score() == 20

    def test_draw(self, game, player1):
        draw_count = 2
        draws = player1.draw(game.draw_pile, draw_count)
        assert player1.hand == [Card('1', 1),Card('1', 1),Card('3', 3),Card('Dragon'), Card('King'), Card('Potion'), Card('2', 2)]
        assert draws == [Card('Potion'), Card('2', 2)]
        assert game.draw_pile == Deck(cards = [Card('3', 3), Card('4', 4)])

    def test_play(self, player1):
        player1.play(cards = [Card('1', 1), Card('1', 1)])
        assert player1.hand == [Card('3', 3),Card('Dragon'),Card('King')]
    
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
    
    def test_dog_cat_together(self, player1, player2, game):
        assert player1._dog_cat_together(queen = Card('Dog Queen', 15)) == True
        assert player2._dog_cat_together(queen = Card('Cat Queen', 15)) == False

    def test_draw_queen(self, game, player1, player2):
        queen = player1._draw_queen(game.queen_pile)
        assert queen == Card('Dog Queen', 15)
        assert player1.queens == [Card('Queen 5', 5), Card('Cat Queen', 15)]
        queen = player2._draw_queen(game.queen_pile)
        assert queen == Card('Dog Queen', 15)
        assert player2.queens == [Card('Dog Queen',15)]
    
    def test_wake_queen(self, player2, game):
        game.queen_pile = Deck(cards = [Card('Rose Queen', 5), Card('Queen 20', 20), Card('Queen 15', 15)])
        player2.wake_queen(game.queen_pile)
        assert player2.queens == [Card('Rose Queen', 5), Card('Queen 20', 20)]
        assert game.queen_pile == Deck(cards = [Card('Queen 15', 15)])




class TestGame:
    def test_check_sum(self, game):
        assert game._check_sum([1,2,3]) == True
        assert game._check_sum([1,2,4]) == False
        assert game._check_sum([1,5,3,1]) == True
        assert game._check_sum([2,7,1,1,3]) == True
    
    def test_play_cards_legal(self, game):
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('1', 1)]) == True
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('1', 1), Card('1', 1)]) == True
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('5', 5)]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('Dragon')]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('King')]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('King'), Card('5', 5)]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('1', 1), Card('5', 5)]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [Card('1', 1), Card('1', 1), Card('5', 1)]) == False
        assert game._play_cards_legal(current_player = 1, cards_to_play = [Card('Potion')]) == True
        assert game._play_cards_legal(current_player = 1, cards_to_play = [Card('King')]) == True
        assert game._play_cards_legal(current_player = 1, cards_to_play = [Card('2', 2), Card('3', 3), Card('5', 5)]) == True        
    
    def test_knight_effect(self):
        pass

    def test_potion_effect(self):
        pass

    def test_jester_effect(self):
        pass