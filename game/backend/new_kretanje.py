from board import GameBoard

class Movement:
    def __init__(self, game_board):
        self.game_board = game_board

    def move_figure(self, figure_color, steps):
        figures_outside_base = []
        figures_in_base = []
        current = self.game_board.head

        while current:
            if current.figureColor == figure_color:
                if current.isStart:
                    figures_in_base.append(current)
                else:
                    figures_outside_base.append(current)
            current = current.next

        if steps == 6 and figures_in_base:
            # Omogući pomicanje figure iz baze na početnu poziciju
            figure_to_move = figures_in_base[0]  # Nađi prvu figuru u bazi
            new_position = self.get_starting_position(figure_color)
            if self.is_valid_move(figure_to_move.position, new_position):
                figure_to_move.position = new_position
                figure_to_move.isStart = False
                print(f"Figure moved from base to start position: {figure_to_move.position}")
            else:
                print("Invalid move!")
        elif figures_outside_base:
            # Pomakni prvu figuru izvan baze
            figure_to_move = figures_outside_base[0]
            new_position = (figure_to_move.position + steps) % 72
            if self.is_valid_move(figure_to_move.position, new_position):
                if self.is_figure_at_position(new_position):
                    self.return_opponent_figure_to_start(new_position)
                figure_to_move.position = new_position
                print(f"Figura se pomakla na poziciju: {figure_to_move.position}")
            else:
                print("Invalid move!")
        else:
            print("No figures to move.")

    def is_valid_move(self, current_position, new_position):
        # Provjera položaja
        if new_position != current_position:
            # Provjera zauzetosti polja
            if self.is_empty(new_position):
                # Provjera dolaska u kuću
                if self.is_house(new_position) and not self.is_house(current_position):
                    # Potez je valjan samo ako je figurica došla do krajnjeg polja kuće
                    if self.is_end_of_house(current_position):
                        return True
                    else:
                        return False
                else:
                    return True
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

    def is_end_of_house(self, position):

        yellow_end = 17
        red_end = 35
        blue_end = 53
        green_end = 71

        return position in [yellow_end, red_end, blue_end, green_end]

    def is_figure_at_position(self, position):
        current = self.game_board.head
        while current:
            if current.position == position and not current.empty:
                return True
            current = current.next
        return False

    def return_opponent_figure_to_start(self, position):
        current = self.game_board.head
        while current:
            if current.position == position:
                current.position = self.get_starting_position(current.figureColor)
                print(f"Protivnicka figura vracena na start: {current.position}")
                return
            current = current.next

    def get_starting_position(self, figure_color):
        if figure_color == "zelena":
            return 0
        elif figure_color == "zuta":
            return 14
        elif figure_color == "crvena":
            return 32
        elif figure_color == "plava":
            return 50
        else:
            return -1

game_board = GameBoard()
movement = Movement(game_board)
