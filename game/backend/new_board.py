import bge
import random

SAFE_ZONES = {
    "zelena": [5],
    "zuta": [23],
    "crvena": [41],
    "plava": [59]
}

START_POSITIONS = {
    "zelena": [1, 2, 3, 4],
    "zuta": [19, 20, 21, 22],
    "crvena": [37, 38, 39, 40],
    "plava": [55, 56, 57, 58]
}

HOUSE_POSITIONS = {
    "zelena": range(69, 73),
    "zuta": range(15, 19),
    "crvena": range(33, 37),
    "plava": range(51, 55)
}

FINAL_HOUSE_POSITIONS = {
    "zelena": 72,
    "zuta": 18,
    "crvena": 36,
    "plava": 54
}

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
        self.start_position = start_position  # Remember the starting position
        self.object = start_object
        self.in_base = True
        self.in_house = False
        self.finished = False

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
            color, isStart, isHouse, empty, figureColor = self.get_node_properties(i)
            cube_name = f"Polje_{i:02d}"
            cube_object = scene.objects.get(cube_name)
            self.append_node(i, isStart, isHouse, empty, figureColor, color, cube_object)
        
        game_instance = scene.objects.get("Unutarnje")
        if game_instance:
            game_instance['game_instance'] = True
            game_instance['game_board_instance'] = self

    def get_node_properties(self, index):
        color = None
        isStart = False
        isHouse = False
        empty = True
        figureColor = None

        if index in range(1, 5):
            color, figureColor, empty, isStart = "zelena", "zelena", False, True
        elif index in range(15, 19):
            color, isHouse, empty = "zuta", True, True
        elif index in range(19, 23):
            color, figureColor, empty, isStart = "zuta", "zuta", False, True
        elif index in range(33, 37):
            color, isHouse, empty = "crvena", True, True
        elif index in range(37, 41):
            color, figureColor, empty, isStart = "crvena", "crvena", False, True
        elif index in range(51, 55):
            color, isHouse, empty = "plava", True, True
        elif index in range(55, 59):
            color, figureColor, empty, isStart = "plava", "plava", False, True
        elif index in range(69, 73):
            color, isHouse, empty = "zelena", True, True

        return color, isStart, isHouse, empty, figureColor


    def append_node(self, position, isStart, isHouse, empty, figureColor, color, cube):
        new_node = Node(position, isStart, isHouse, empty, figureColor, color, cube)
        if not self.head:
            self.head = new_node
            self.head.next = self.head  # Initialize circular reference
            print(f"Added head node: {self.head.position}")
        else:
            current = self.head
            # Traverse to the last node (i.e., where current.next is self.head)
            while current.next != self.head:
                current = current.next
            # Link the last node to the new node
            current.next = new_node
            # Link the new node back to the head to maintain circular reference
            new_node.next = self.head
            print(f"Added node: {new_node.position} after node: {current.position}")
        self.size += 1

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.players[self.current_player_index].has_rolled_six = False
        print(f"Next player is {self.players[self.current_player_index].color}")

    def roll_dice(self):
        roll = random.randint(1, 6)
        print(f"Player {self.players[self.current_player_index].color} rolled a {roll}")
        if roll == 6:
            self.players[self.current_player_index].has_rolled_six = True
        return roll

    def play_turn(self):
        roll = self.roll_dice()
        current_player_color = self.players[self.current_player_index].color
        figures_outside_base = [figure for figure in self.movement.figures if figure.color == current_player_color and not figure.in_base and not figure.finished]
        figures_in_base = [figure for figure in self.movement.figures if figure.color == current_player_color and figure.in_base]

        if roll == 6:
            if figures_in_base or figures_outside_base:
                self.prompt_player_choice(current_player_color, roll)
            else:
                self.next_turn()
        else:
            if figures_outside_base:
                if len(figures_outside_base) > 1:
                    self.prompt_player_choice(current_player_color, roll)
                else:
                    self.movement.move_figure(current_player_color, roll, figures_outside_base[0].index)
                    self.next_turn()
            else:
                print("No valid moves available.")
                self.next_turn()

    def prompt_player_choice(self, figure_color, steps):
        print(f"Player {figure_color} rolled a 6. Choose a figure to move:")
        scene = bge.logic.getCurrentScene()
        game_instance = scene.objects['Unutarnje']
        game_instance['selecting_figure'] = True
        game_instance['figure_color'] = figure_color
        game_instance['steps'] = steps
        if steps == 6:
            available_figures = [
                figure.index for figure in self.movement.figures if figure.color == figure_color and not figure.finished
            ]
        else:
            available_figures = [
                figure.index for figure in self.movement.figures if figure.color == figure_color and not figure.in_base and not figure.finished
            ]
        game_instance['available_figures'] = available_figures
        print(f"Available figures to move: {game_instance['available_figures']}")

def log_game_data(game_board):
    current = game_board.head
    start_position = current.position
    while True:
        print(f"Position: {current.position}")
        print(f"Is Start: {current.isStart}")
        print(f"Is House: {current.isHouse}")
        print(f"Empty: {current.empty}")
        print(f"Figure Color: {current.figureColor}")
        print(f"Color: {current.color}")
        print(f"Cube: {current.cube}") 
        print("----------------------------------")
        current = current.next
        if current.position == start_position:  # Stop if we've come full circle
            break


class Movement:
    def __init__(self, game_board):
        self.game_board = game_board
        self.figures = self.initialize_figures()
        self.available_house_positions = {
            "zelena": [69, 70, 71, 72],
            "zuta": [15, 16, 17, 18],
            "crvena": [33, 34, 35, 36],
            "plava": [51, 52, 53, 54]
        }

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
        if self.check_for_win(figure_color):
            print(f"Player {figure_color} has already won the game. No further moves allowed.")
            return

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
            figure_to_move = figures_in_base[0]  # Move the first figure in the base
            new_position = self.get_first_non_start_house_position(figure_color)
            print(f"Trying to move from base to start: current {figure_to_move.position}, new {new_position}")
            if self.is_valid_move(figure_to_move.position, new_position, figure_color):
                self.update_node_status(figure_to_move.position, True)
                figure_to_move.position = new_position
                figure_to_move.in_base = False
                self.update_object_position(figure_to_move.object, new_position)
                self.update_node_status(new_position, False)
                print(f"Figure moved from base to start position: {figure_to_move.position}")
            else:
                print("Invalid move!")
        elif figures_outside_base:
            if len(figures_outside_base) > 1 and figure_index is None:
                print(f"Multiple figures available to move, but no selection made.")
                return

            figure_to_move = self.get_figure(figure_color, figure_index) if figure_index else figures_outside_base[0]

            # Check if the figure is in the house area
            house_positions = self.get_house_positions(figure_color)
            if figure_to_move.position in house_positions:
                if not self.move_within_house(figure_to_move, steps):
                    print("Invalid move within the house")
                    return
            else:
                new_position = figure_to_move.position
                for _ in range(steps):
                    new_position = self.get_next_position(new_position, figure_color)
                    if new_position == -1:
                        print("Invalid move: No valid next position.")
                        return

                print(f"Trying to move: current {figure_to_move.position}, new {new_position}")
                if self.is_valid_move(figure_to_move.position, new_position, figure_color):
                    if self.is_figure_at_position(new_position):
                        self.return_opponent_figure_to_start(new_position)
                    self.update_node_status(figure_to_move.position, True)
                    figure_to_move.position = new_position
                    self.update_object_position(figure_to_move.object, new_position)
                    self.update_node_status(new_position, False)
                    print(f"Figure moved to position: {figure_to_move.position}")
                else:
                    print("Invalid move!")
        else:
            print("No figures to move.")

    def move_within_house(self, figure, steps):
        house_positions = self.available_house_positions[figure.color]
        current_position_index = house_positions.index(figure.position)
        target_index = current_position_index + steps

        # If the target position is outside the house, the move is invalid
        if target_index >= len(house_positions):
            print(f"Invalid move for {figure.color}{figure.index}: Cannot move beyond the last house field")
            return False

        # Ensure the figure moves exactly to the last position or the furthest available position
        for index in range(target_index, -1, -1):
            if self.is_empty(house_positions[index]):
                target_position = house_positions[index]
                break
        else:
            print(f"No available position found within the house for {figure.color}{figure.index}")
            return False

        # Move the figure to the target position
        self.update_node_status(figure.position, True)
        figure.position = target_position
        self.update_node_status(target_position, False)
        self.update_object_position(figure.object, target_position)

        # Mark figure as finished if it reaches the final house position and adjust house
        if target_position == house_positions[-1]:
            figure.finished = True
            house_positions.pop()  # Remove the last house position
            new_final_house_position = house_positions[-1] if house_positions else None
            print(f"Figure {figure.color}{figure.index} has reached the final house position and is now finished.")
            if new_final_house_position:
                print(f"The new final house position for {figure.color} is now {new_final_house_position}.")
            else:
                print(f"No more positions left in the house for {figure.color}.")
        else:
            print(f"Figure {figure.color}{figure.index} moved within the house to position {target_position}")

        # Check for win condition
        if self.check_for_win(figure.color):
            print(f"Player {figure.color} has won the game!")

        return True

    def check_for_win(self, color):
        house_positions = self.available_house_positions[color]
        if all(not self.is_empty(pos) for pos in house_positions):
            return True  # All house positions are occupied
        return False


    def check_for_win(self, color):
        house_positions = self.available_house_positions[color]
        if len(house_positions) == 0:
            return True  # All house positions are occupied
        return False

    def get_valid_house_position(self, current_position, steps, figure_color):
        house_positions = self.get_house_positions(figure_color)
        if current_position in house_positions:
            index = house_positions.index(current_position)
            new_index = index + steps
            if new_index < len(house_positions) and self.is_empty(house_positions[new_index]):
                return house_positions[new_index]
            else:
                # Find the first empty house position if the exact move is not possible
                for pos in house_positions[index:]:
                    if self.is_empty(pos):
                        return pos
        return -1
    
    def get_last_house_position(self, figure_color):
        house_positions = self.get_house_positions(figure_color)
        return house_positions[-1] if house_positions else -1

    def get_next_position(self, current_position, figure_color):
        current = self.game_board.head
        start_position = current.position

        # Find the current node
        while True:
            if current.position == current_position:
                break
            current = current.next
            if current.position == start_position:  # Stop if we've come full circle
                return -1

        # Move steps forward, skipping fields as necessary
        for _ in range(1):
            current = current.next

            # Skip other color house positions
            skip_positions = {
                "zuta": range(15, 19),
                "crvena": range(33, 37),
                "plava": range(51, 55),
                "zelena": range(69, 73)
            }
            while current.position in skip_positions.get(current.color, []) and current.color != figure_color:
                for _ in range(9):
                    current = current.next

        return current.position if current else -1

    def get_first_non_start_house_position(self, figure_color):
        start_position = self.get_starting_position(figure_color)
        current = self.game_board.head
        start_position_flag = current.position

        while True:
            if current.position == start_position:
                break
            current = current.next
            if current.position == start_position_flag:  # Stop if we've come full circle
                return -1

        while True:
            if not current.isStart and not current.isHouse:
                return current.position
            current = current.next
            if current.position == start_position_flag:  # Stop if we've come full circle
                return -1

    def get_starting_position(self, figure_color):
        if figure_color == "zelena":
            return 1
        elif figure_color == "zuta":
            return 19
        elif figure_color == "crvena":
            return 37
        elif figure_color == "plava":
            return 55
        else:
            return -1
        
    def get_house_positions(self, figure_color):
        if figure_color == "zelena":
            return [69, 70, 71, 72]
        elif figure_color == "zuta":
            return [15, 16, 17, 18]
        elif figure_color == "crvena":
            return [33, 34, 35, 36]
        elif figure_color == "plava":
            return [51, 52, 53, 54]
        return []

    def get_next_start_position(self, position, figure_color):
        start_positions = START_POSITIONS[figure_color]
        index = start_positions.index(position)
        next_index = (index + 1) % len(start_positions)
        return start_positions[next_index]

    def get_first_empty_start_position(self, figure_color):
        start_positions = START_POSITIONS[figure_color]
        for position in start_positions:
            node = self.get_node(position)
            if node and node.empty:
                return position
        return -1

    def get_node(self, position):
        current = self.game_board.head
        start_position = current.position
        while True:
            if current.position == position:
                return current
            current = current.next
            if current.position == start_position:  # Stop if we've come full circle
                break
        return None

    def update_node_status(self, position, empty):
        node = self.get_node(position)
        if node:
            node.empty = empty
            print(f"Updated node {position} empty status to {empty}")

    def is_valid_move(self, current_position, new_position, figure_color):
        if new_position == current_position:
            print(f"Move from {current_position} to {new_position} is invalid: same position")
            return False

        if self.is_empty(new_position):
            if self.is_house(new_position):
                if self.is_correct_house(new_position, figure_color):
                    return True
                else:
                    print(f"Move to house {new_position} is invalid: not correct house for {figure_color}")
                    return False
            return True
        else:
            figure_at_new_position = self.get_figure_at_position(new_position)
            if figure_at_new_position:
                if figure_at_new_position.color != figure_color:
                    if new_position not in SAFE_ZONES[figure_at_new_position.color]:
                        return True  # Opponent figure can be captured
                    else:
                        print(f"Move to {new_position} is invalid: safe zone for opponent {figure_at_new_position.color}")
                        return False
                else:
                    print(f"Move to {new_position} is invalid: same color figure at position")
                    return False
        return False

    def is_empty(self, position):
        node = self.get_node(position)
        return node.empty if node else True  # Default to True if position is not found

    def is_house(self, position):
        node = self.get_node(position)
        return node.isHouse if node else False

    def is_correct_house(self, position, figure_color):
        if figure_color == "zelena":
            return position in range(69, 73)
        elif figure_color == "zuta":
            return position in range(15, 19)
        elif figure_color == "crvena":
            return position in range(33, 37)
        elif figure_color == "plava":
            return position in range(51, 55)
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
            if figure.in_house:
                print(f"Cannot capture figure {figure.color}{figure.index}pijun in house.")
                return

            self.move_to_start_position(figure)

    def move_to_start_position(self, figure):
        start_position = figure.start_position
        current_start_position = start_position

        # Check if the start position is occupied
        while not self.is_empty(current_start_position):
            current_start_position = self.get_next_start_position(current_start_position, figure.color)
            if current_start_position == start_position:
                print(f"No empty start position found for {figure.color}")
                return

        self.update_node_status(figure.position, True)  # Update the current position to empty
        figure.position = current_start_position
        figure.in_base = True
        self.update_object_position(figure.object, current_start_position)
        self.update_node_status(current_start_position, False)  # Update the start position to not empty
        print(f"Opponent's figure {figure.color}{figure.index}pijun returned to start: {current_start_position}")

    def update_object_position(self, figure_object, new_position):
        scene = bge.logic.getCurrentScene()
        cube_name = f"Polje_{new_position:02d}"
        new_position_object = scene.objects.get(cube_name)

        if not new_position_object:
            print(f"Error: New position object {cube_name} not found.")
            return

        figure_object.worldPosition = new_position_object.worldPosition
        print(f"Moved {figure_object.name} to {cube_name}")

game_board_instance = GameBoard()
log_game_data(game_board_instance)
