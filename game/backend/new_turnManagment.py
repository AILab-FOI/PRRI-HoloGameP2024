import random
from board import GameBoard
from movement import Movement

class Player:
    def __init__(self, color):
        self.color = color
        self.has_rolled_six = False

class Game:
    def __init__(self):
        self.game_board = GameBoard()
        self.movement = Movement(self.game_board)
        self.players = [Player("zelena"), Player("zuta"), Player("crvena"), Player("plava")]
        self.current_player_index = 0

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.players[self.current_player_index].has_rolled_six = False

    def roll_dice(self):
        roll = random.randint(1, 6)
        print(f"Player {self.players[self.current_player_index].color} rolled a {roll}")
        if roll == 6:
            self.players[self.current_player_index].has_rolled_six = True
        return roll

    def play_turn(self):
        roll = self.roll_dice()
        self.movement.move_figure(self.players[self.current_player_index].color, roll)
        if roll != 6 or not self.players[self.current_player_index].has_rolled_six:
            self.next_turn()

