import random
from enum import Enum

class Tile(Enum):
    Empty = 0
    Noughts = 1
    Crosses = 2

class Matchbox:
    def __init__(self, board):
        self.board = board
        self.box = Box(self.state)

class Box:
    def __init__(self, board):
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

        self.beads = [beadCount if eligible[y][x] else 0 for x in range(3) for y in range(3)]

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
        pass #return the "standard" board state (rotation/reflection)
