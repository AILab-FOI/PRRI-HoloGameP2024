import bge

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

class GameBoard:
    def __init__(self):
        self.head = None
        self.size = 0
        self.initialize_game_board()

    def initialize_game_board(self):
        scene = bge.logic.getCurrentScene()
        for i in range(72):
            color = None
            isStart = False
            isHouse = False
            empty = True
            figureColor = None
            cube_name = f"Polje_{i:02d}"
            cube_object = scene.objects.get(cube_name)
            if cube_object:
                if i <= 3:
                    color = "zelena"
                    empty = False
                    isStart = True
                elif 14 <= i <= 17:
                    color = "zuta"
                    isHouse = True
                elif 18 <= i <= 21:
                    color = "žuta"
                    isStart = True
                    empty = False
                elif 32 <= i <= 35:
                    color = "crvena"
                    isHouse = True
                elif 36 <= i <= 39:
                    color = "crvena"
                    isStart = True
                    empty = False
                elif 50 <= i <= 53:
                    color = "plava"
                    isHouse = True
                elif 54 <= i <= 57:
                    color = "plava"
                    isStart = True
                    empty = False
                elif 68 <= i <= 71:
                    color = "zelena"
                    isHouse = True
                else:
                    color = ""
                    isStart = False
                    isHouse = False
                    empty = True
                    figureColor = False
                    cube_object.color = [1, 0, 1, 1]
            self.append_node(i, isStart, isHouse, empty, figureColor, color, cube_object)

        game_instance = bge.logic.getCurrentScene().objects.get("Unutarnje")
        if game_instance:
            game_instance['game_instance'] = True
            game_instance['game_board_instance'] = self


    def append_node(self, position, isStart, isHouse, empty, figureColor, color, cube):
        if not self.head:
            self.head = Node(position, isStart, isHouse, empty, figureColor, color, cube)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(position, isStart, isHouse, empty, figureColor, color, cube)
        self.size += 1

def log_game_data(game_board):
    current = game_board.head
    while current:
        print(f"Position: {current.position}")
        print(f"Is Start: {current.isStart}")
        print(f"Is House: {current.isHouse}")
        print(f"Empty: {current.empty}")
        print(f"Figure Color: {current.figureColor}")
        print(f"Color: {current.color}")
        print(f"Cube: {current.cube}") 
        print("----------------------------------")
        current = current.next

game_board_instance = GameBoard()

log_game_data(game_board_instance)
