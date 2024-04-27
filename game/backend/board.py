class Node:
    def __init__(self, position, isStart, isHouse, empty, figureColor, color):
        self.position = position
        self.isStart = isStart
        self.isHouse = isHouse
        self.empty = empty
        self.figureColor = figureColor
        self.color = color
        self.next = None

class GameBoard:
    def __init__(self):
        self.head = None
        self.size = 0
        self.initialize_board()

    def initialize_board(self):
        for i in range(72):
            color = None
            isStart = False
            isHouse = False
            empty = True
            figureColor = None
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
            self.append(Node(i, isStart, isHouse, empty, figureColor, color))

    def append(self, node):
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
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
        print("----------------------------------")
        current = current.next

game_board_instance = GameBoard()
log_game_data(game_board_instance)
