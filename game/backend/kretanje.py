from board import GameBoard

class Movement:
    def __init__(self, game_board):
        self.game_board = game_board

    def move_figure(self, figure_color, steps):
        current = self.game_board.head
        while current:
            if current.figureColor == figure_color:
                new_position = (current.position + steps) % 72 
                if self.is_valid_move(current.position, new_position):
                    if self.is_figure_at_position(new_position):
                        self.return_opponent_figure_to_start(new_position)
                    current.position = new_position
                    print(f"Figura se pomakla na poziciju: {current.position}")
                    return
                else:
                    print("Nepravilni potez!")
                    return
            current = current.next

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
game_board = GameBoard()
movement = Movement(game_board)
