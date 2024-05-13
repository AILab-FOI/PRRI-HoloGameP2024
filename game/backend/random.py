import bge
import random

def generate_random_number():
    return random.randint(1, 6)

def move_figure(game_board):
    random_number = generate_random_number()
    print("Random number:", random_number)

    if random_number == 6:
        current = game_board.head
        while current:
            if not current.isStart:
                move_figure_to_field()
                break
            current = current.next

def move_figure_to_field():
    zeleni_pijun = bge.logic.getCurrentScene().objects.get("Zeleni1pijun")
    if zeleni_pijun:
        polje_06 = bge.logic.getCurrentScene().objects.get("Polje_06")
        if polje_06:
            zeleni_pijun.worldPosition = polje_06.worldPosition
            print("Moving Zeleni1pijun to Polje_06")
        else:
            print("Polje_06 object not found.")
    else:
        print("Zeleni1pijun object not found.")


  
game_instance = bge.logic.getCurrentScene().objects.get("Unutarnje")

if game_instance and game_instance.get("game_instance", False):
    game_board_instance = game_instance.get("game_board_instance")
    if game_board_instance:
        move_figure(game_board_instance)
    else:
        print("Game board instance not found.")
else:
    print("Game instance not found or 'game_instance' property is not set to True.")
