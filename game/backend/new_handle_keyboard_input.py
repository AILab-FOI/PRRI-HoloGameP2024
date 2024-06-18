import bge
import random

class Node:
    def __init__(self, position, isStart, isHouse, empty, figureColor, color, cube):
        self.position = position
        self.isStart = isStart
        self.isHouse = isHouse
        self.empty = empty
        self.figureColor = figureColor
        self.color = color
        self.cube = cube
        self.next = None

class Player:
    def __init__(self, color):
        self.color = color
        self.has_rolled_six = False

class Figure:
    def __init__(self, color, index, start_position, start_object):
        self.color = color
        self.index = index
        self.position = start_position
        self.object = start_object
        self.in_base = True

class GameBoard:
    def __init__(self):
        self.head = None
        self.size = 0
        self.players = [Player("zelena"), Player("zuta"), Player("crvena"), Player("plava")]
        self.current_player_index = 0
        self.initialize_game_board()
        self.movement = Movement(self)

    def initialize_game_board(self):
        scene = bge.logic.getCurrentScene()
        for i in range(1, 73):
            color = None
            isStart = False
            isHouse = False
            empty = True
            figureColor = None
            cube_name = f"Polje_{i:02d}"
            cube_object = scene.objects.get(cube_name)
            if cube_object:
                if i <= 4:
                    color = "zelena"
                    figureColor = "zelena"
                    empty = False
                    isStart = True
                elif 15 <= i <= 18:
                    color = "zuta"
                    isHouse = True
                elif 19 <= i <= 22:
                    color = "zuta"
                    figureColor = "zuta"
                    empty = False
                    isStart = True
                elif 33 <= i <= 36:
                    color = "crvena"
                    isHouse = True
                elif 37 <= i <= 40:
                    color = "crvena"
                    figureColor = "crvena"
                    empty = False
                    isStart = True
                elif 51 <= i <= 54:
                    color = "plava"
                    isHouse = True
                elif 55 <= i <= 58:
                    color = "plava"
                    figureColor = "plava"
                    empty = False
                    isStart = True
                elif 69 <= i <= 72:
                    color = "zelena"
                    isHouse = True
                else:
                    color = ""
                    isStart = False
                    isHouse = False
                    empty = True
                    figureColor = None
            self.append_node(i, isStart, isHouse, empty, figureColor, color, cube_object)

        game_instance = scene.objects.get("Unutarnje")
        if game_instance:
            game_instance['game_instance'] = True
            game_instance['game_board_instance'] = self

    def append_node(self, position, isStart, isHouse, empty, figureColor, color, cube):
        new_node = Node(position, isStart, isHouse, empty, figureColor, color, cube)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

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
        current_player_color = self.players[self.current_player_index].color
        figures_outside_base = [figure for figure in self.movement.figures if figure.color == current_player_color and not figure.in_base]

        if len(figures_outside_base) > 1:
            self.select_figure_to_move(current_player_color, roll)
        else:
            self.movement.move_figure(current_player_color, roll)
        
        if roll != 6 or not self.players[self.current_player_index].has_rolled_six:
            self.next_turn()

    def select_figure_to_move(self, figure_color, steps):
        print(f"Player {figure_color} has multiple figures outside the base. Select a figure to move.")
        scene = bge.logic.getCurrentScene()
        game_instance = scene.objects['Unutarnje']
        game_instance['selecting_figure'] = True
        game_instance['figure_color'] = figure_color
        game_instance['steps'] = steps

class Movement:
    def __init__(self, game_board):
        self.game_board = game_board
        self.figures = self.initialize_figures()

    def initialize_figures(self):
        figures = []
        scene = bge.logic.getCurrentScene()

        for color in ["zelena", "zuta", "crvena", "plava"]:
            for i in range(1, 5):
                figure_name = f"{color.capitalize()}{i}pijun"
                figure_object = scene.objects.get(figure_name)
                start_position = self.get_starting_position(color)
                if figure_object:
                    figures.append(Figure(color, i, start_position, figure_object))

        return figures

    def get_figure(self, color, index):
        for figure in self.figures:
            if figure.color == color and figure.index == index:
                return figure
        return None

    def move_figure(self, figure_color, steps, figure_index=None):
        if figure_index:
            figure_to_move = self.get_figure(figure_color, figure_index)
            if not figure_to_move:
                print(f"Figure {figure_color}{figure_index}pijun not found.")
                return
            figures_in_base = [figure_to_move] if figure_to_move.in_base else []
            figures_outside_base = [figure_to_move] if not figure_to_move.in_base else []
        else:
            figures_in_base = [figure for figure in self.figures if figure.color == figure_color and figure.in_base]
            figures_outside_base = [figure for figure in self.figures if figure.color == figure_color and not figure.in_base]

        print(f"Figures in base: {[(f.position, f.object) for f in figures_in_base]}")
        print(f"Figures outside base: {[(f.position, f.object) for f in figures_outside_base]}")

        if steps == 6 and figures_in_base:
            figure_to_move = figures_in_base[0]
            new_position = self.get_first_non_start_house_position(figure_color)
            if self.is_valid_move(figure_to_move.position, new_position, figure_color):
                figure_to_move.position = new_position
                figure_to_move.in_base = False
                self.update_object_position(figure_to_move.object, new_position)
                print(f"Figure moved from base to start position: {figure_to_move.position}")
            else:
                print("Invalid move!")
        elif figures_outside_base:
            figure_to_move = figures_outside_base[0]
            new_position = (figure_to_move.position + steps) % 72
            if self.is_valid_move(figure_to_move.position, new_position, figure_color):
                if self.is_figure_at_position(new_position):
                    self.return_opponent_figure_to_start(new_position)
                figure_to_move.position = new_position
                self.update_object_position(figure_to_move.object, new_position)
                print(f"Figure moved to position: {figure_to_move.position}")
            else:
                print("Invalid move!")
        else:
            print("No figures to move.")

    def get_first_non_start_house_position(self, figure_color):
        start_position = self.get_starting_position(figure_color)
        current = self.game_board.head

        while current:
            if current.position == start_position:
                break
            current = current.next

        while current:
            if not current.isStart and not current.isHouse:
                return current.position
            current = current.next

        return -1

    def get_starting_position(self, figure_color):
        if figure_color == "zelena":
            return 1
        elif figure_color == "zuta":
            return 15
        elif figure_color == "crvena":
            return 33
        elif figure_color == "plava":
            return 51
        else:
            return -1

    def is_valid_move(self, current_position, new_position, figure_color):
        if new_position != current_position:
            if self.is_empty(new_position):
                if self.is_house(new_position):
                    if self.is_correct_house(new_position, figure_color):
                        return True
                    else:
                        return False
                return True
            else:
                figure_at_new_position = self.get_figure_at_position(new_position)
                if figure_at_new_position and figure_at_new_position.color != figure_color:
                    self.return_opponent_figure_to_start(new_position)
                    return True
                elif figure_at_new_position and figure_at_new_position.color == figure_color:
                    return False
        return False

    def is_empty(self, position):
        current = self.game_board.head
        while current:
            if current.position == position:
                return current.empty
            current = current.next
        return False

    def is_house(self, position):
        current = self.game_board.head
        while current:
            if current.position == position:
                return current.isHouse
            current = current.next
        return False

    def is_correct_house(self, position, figure_color):
        if figure_color == "zelena":
            return position in range(68, 72)
        elif figure_color == "zuta":
            return position in range(14, 18)
        elif figure_color == "crvena":
            return position in range(32, 36)
        elif figure_color == "plava":
            return position in range(50, 54)
        return False

    def is_figure_at_position(self, position):
        for figure in self.figures:
            if figure.position == position and not figure.in_base:
                return True
        return False

    def get_figure_at_position(self, position):
        for figure in self.figures:
            if figure.position == position and not figure.in_base:
                return figure
        return None

    def return_opponent_figure_to_start(self, position):
        figure = self.get_figure_at_position(position)
        if figure:
            figure.position = self.get_starting_position(figure.color)
            figure.in_base = True
            self.update_object_position(figure.object, figure.position)
            print(f"Opponent's figure {figure.color}{figure.index}pijun returned to start: {figure.position}")

    def update_object_position(self, figure_object, new_position):
        scene = bge.logic.getCurrentScene()
        cube_name = f"Polje_{new_position:02d}"
        new_position_object = scene.objects.get(cube_name)
        
        if not new_position_object:
            print(f"Error: New position object {cube_name} not found.")
            return

        figure_object.worldPosition = new_position_object.worldPosition
        print(f"Moved {figure_object.name} to {cube_name}")

def handle_keyboard_input():
    keyboard = bge.logic.keyboard
    active_keys = bge.logic.KX_INPUT_ACTIVE
    scene = bge.logic.getCurrentScene()
    game_instance = scene.objects['Unutarnje']

    if game_instance.get('selecting_figure', False):
        for key, status in keyboard.inputs.items():
            if status.activated:
                if key in [bge.events.ONEKEY, bge.events.TWOKEY, bge.events.THREEKEY, bge.events.FOURKEY]:
                    figure_index = key - bge.events.ONEKEY + 1
                    figure_color = game_instance['figure_color']
                    steps = game_instance['steps']
                    game_instance['selecting_figure'] = False
                    movement = game_instance['game_board_instance'].movement
                    movement.move_figure(figure_color, steps, figure_index)
    else:
        # Assuming spacebar is used to roll the dice
        if keyboard.inputs[bge.events.SPACEKEY].activated:
            game_instance['game_board_instance'].play_turn()

# Ensure the game board is initialized
game_board_instance = GameBoard()
