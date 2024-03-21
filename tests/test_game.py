from sleeping_queen.game import Game
from sleeping_queen.data_type import Card
from sleeping_queen.cards import *

class TestGame:
    def test_check_sum(self, game):
        assert game._check_sum([1,2,3]) == True
        assert game._check_sum([1,2,4]) == False
        assert game._check_sum([1,5,3,1]) == True
        assert game._check_sum([2,7,1,1,3]) == True
    
    def test_play_cards_legal(self, game):
        assert game._play_cards_legal(current_player = 0, cards_to_play = [one]) == True
        assert game._play_cards_legal(current_player = 0, cards_to_play = [one, one]) == True
        assert game._play_cards_legal(current_player = 0, cards_to_play = [five]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [dragon]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [king]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [king, five]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [one, five]) == False
        assert game._play_cards_legal(current_player = 0, cards_to_play = [one, one, five]) == False
        assert game._play_cards_legal(current_player = 1, cards_to_play = [potion]) == True
        assert game._play_cards_legal(current_player = 1, cards_to_play = [king]) == True
        assert game._play_cards_legal(current_player = 1, cards_to_play = [two, three, five]) == True        
    
    def test_knight_effect(self):
        pass

    def test_potion_effect(self):
        pass

    def test_jester_effect(self):
        pass