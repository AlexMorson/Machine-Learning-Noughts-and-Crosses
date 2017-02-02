import random
from enum import Enum
import pickle

class Tile(Enum):
    Empty = 0
    Noughts = 1
    Crosses = 2

try:
    with open("boards.pickle", "rb") as file:
        ALL_BOARDS = pickle.load(file)
except FileNotFoundError:
    print("Place the boards.pickle file in the same directory as the python file")
    raise

class Matchbox:
    def __init__(self, state):
        self.board = Board(state)
        self.box = Box()

        self.fill()

    def fill(self):
        self.box.fill(self.board)

class Box:
    def __init__(self):
        self.beads = [0 for y in range(3) for x in range(3)]

    def fill(self, board):
        def eliminate(*positions):
            for x,y in positions:
                eligible[y][x] = False
        
        eligible = [[True if board[y][x] is Tile.Empty else False for x in range(3)] for y in range(3)]

        if board == board.rotate90():
            eliminate((1,0),(2,0),(2,1),(0,2),(1,2),(2,2))
        if board == board.rotate180():
            eliminate((1,0),(2,0),(2,1),(2,2))
        if board == board.flipH():
            eliminate((0,2),(1,2),(2,2))
        if board == board.flipV():
            eliminate((2,0),(2,1),(2,2))
        if board == board.flipH().rotate90():
            eliminate((1,0),(2,0),(2,1))
        if board == board.rotate90().flipH():
            eliminate((2,1),(1,2),(2,2))

        beadCount = 2**(3-board.moveCount()//2)

        # A 1D array makes it easier to pick a random bead
        self.beads = [beadCount if eligible[y][x] else 0 for y in range(3) for x in range(3)]

    def pickBead(self): #Returns a pos: (x, y)
        beadNum = random.randint(1, sum(self.beads))
        for pos, beads in enumerate(self.beads):
            beadNum -= beads
            if beadNum <= 0:
                return divmod(pos, 3)

class Board:
    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        return self.state == other.state

    def __getitem__(self, key):
        return self.state[key]

    def moveCount(self):
        return sum(True if self.state[y][x] is not Tile.Empty else False for y in range(3) for x in range(3))

    def flipH(self):
        return Board(self.state[::-1])

    def flipV(self):
        return Board(list(map(lambda x:x[::-1], self.state)))

    def rotate90(self):
        return Board([[self.state[2][0],self.state[1][0],self.state[0][0]],
                      [self.state[2][1],self.state[1][1],self.state[0][1]],
                      [self.state[2][2],self.state[1][2],self.state[0][2]]])

    def rotate180(self):
        return self.rotate90().rotate90()

    def rotate270(self):
        return self.rotate90().rotate90().rotate90()

    def standardise(self):
        currentBoard = self
        for rot in range(4):
            if currentBoard.state in ALL_BOARDS:
                return currentBoard
            currentBoard = currentBoard.rotate90()

        currentBoard = self.flipH()
        for rot in range(4):
            if currentBoard.state in ALL_BOARDS:
                return currentBoard
            currentBoard = currentBoard.rotate90()

        raise ValueError("Cannot find standardised board")

class Machine:
    def __init__(self):
        self.matchboxes = [Matchbox(board) for board in ALL_BOARDS]

    def getMatchbox(self, board):
        standardisedBoard = board.standardise()
        for matchbox in self.matchboxes:
            if matchbox.board == standardisedBoard:
                return matchbox

if __name__ == "__main__":
    machine = Machine()
