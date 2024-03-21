from sleeping_queen.data_type import Card, Deck, Player
from typing import List

# effects
def _can_add_queen(queen_to_add:Card, queens_in_hands:List[Card]) -> bool:
    if queen_to_add == cat_queen:
        return not dog_queen in queens_in_hands
    if queen_to_add == dog_queen:
        return not cat_queen in queens_in_hands
    return True

def _draw_queen(player:Player, game) -> Card:
    queen_to_add = game.queen_pile.draw()
    if _can_add_queen(queen_to_add, player.queens):
        player.queens.append(queen_to_add)
    else:
        game.queen_pile.cards = [queen_to_add] + game.queen_pile.cards
    return(queen_to_add)

def wake_queen(player:Player, game) -> None:
    queen_to_add = _draw_queen(player, game)
    if queen_to_add.name == 'Rose Queen':
        _draw_queen(player, game)


rose_queen = Card('Rose Queen', 5)
cat_queen = Card('Cat Queen', 15)
dog_queen = Card('Dog Queen', 15)
queen_5 = Card('Queen 5', 5)
queen_10 = Card('Queen 10', 10)
queen_15 = Card('Queen 15', 15)
queen_20 = Card('Queen 20', 20)
king = Card('King',point=None, effect=wake_queen)
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

