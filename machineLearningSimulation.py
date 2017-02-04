import time
import random
from enum import Enum
import pickle
import logging

logging.basicConfig(level=logging.DEBUG)

class Tile(Enum):
    Empty = 0
    Noughts = 1
    Crosses = 2

try:
    with open("boards.pickle", "rb") as file:
        ALL_BOARDS = pickle.load(file)
        logging.info("Loaded boards from boards.pickle.")
except FileNotFoundError:
    logging.error("Could not find boards.pickle file.")
    raise

class Matchbox:
    def __init__(self, state):
        self.board = Board(state)
        self.box = Box()

        self.fill()

    def fill(self):
        self.box.fill(self.board)

    def pickBead(self):
        return self.box.pickBead()

    def addBeads(self, bead, number):
        self.box.addBeads(bead, number)

    def isEmpty(self):
        return self.box.getBeadCount() == 0

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

        beadCount = int(2**(3-board.getMoveCount()//2))

        self.beads = [[beadCount if eligible[y][x] else 0 for x in range(3)] for y in range(3)]

    def getBeadCount(self):
        return sum(map(sum,self.beads))

    def pickBead(self): #Returns a pos: (x, y)
        beadNum = random.randint(1, self.getBeadCount())
        for y in range(3):
            for x in range(3):
                beadNum -= self.beads[y][x]
                if beadNum <= 0:
                    return (x, y)

    def addBeads(self, bead, number):
        if self.beads[bead[1]][bead[0]] + number < 0:
            self.beads[bead[1]][bead[0]] = 0
        else:
            self.beads[bead[1]][bead[0]] += number

class Board:
    def __init__(self, state):
        self.state = state

        noughtsCount = 0
        crossesCount = 0
        for y in range(3):
            for x in range(3):
                if self.state[y][x] is Tile.Noughts:
                    noughtsCount += 1
                elif self.state[y][x] is Tile.Crosses:
                    crossesCount += 1

        self.nextTurn = Tile.Noughts if noughtsCount == crossesCount else Tile.Crosses

    def __eq__(self, other):
        return self.state == other.state

    def __getitem__(self, key):
        return self.state[key]

    def __str__(self):
        def formatTile(t):
            return " " if t is Tile.Empty else "X" if t is Tile.Crosses else "O"
        return "{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}".format(*([formatTile(t) for t in self.state[0]]+[formatTile(t) for t in self.state[1]]+[formatTile(t) for t in self.state[2]]))

    def makeMove(self, bead):
        newState = [[self.state[y][x] for x in range(3)] for y in range(3)]
        newState[bead[1]][bead[0]] = self.nextTurn
        return Board(newState)

    def getMoveCount(self):
        return sum(True if self.state[y][x] is not Tile.Empty else False for y in range(3) for x in range(3))

    def isValidMove(self, x, y):
        return 0 <= x <= 2 and 0 <= y <= 2 and self.state[y][x] is Tile.Empty

    def isGameOver(self): # False or the winner (where Tile.Empty = draw)
        for row in range(3):
            if self.state[row][0] == self.state[row][1] == self.state[row][2] is not Tile.Empty:
                return self.state[row][0]

        for col in range(3):
            if self.state[0][col] == self.state[1][col] == self.state[2][col] is not Tile.Empty:
                return self.state[0][col]

        if self.state[0][0] == self.state[1][1] == self.state[2][2] is not Tile.Empty:
            return self.state[0][0]

        if self.state[0][2] == self.state[1][1] == self.state[2][0] is not Tile.Empty:
            return self.state[0][2]

        if self.getMoveCount() == 9:
            return Tile.Empty

        return False

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

        logging.error("Could not find standardised board")
        raise ValueError

class Machine:
    def __init__(self):
        self.matchboxes = [Matchbox(board) for board in ALL_BOARDS]
        self.moves = []

    def getMatchbox(self, board):
        standardisedBoard = board.standardise()
        for matchbox in self.matchboxes:
            if matchbox.board == standardisedBoard:
                return matchbox

    def startTrainingGame(self):
        self.moves = []

    def makeMove(self, board, training=True):
        #Assuming a full board or finished game will never be given
        def findEmptyTile(board):
            for y in range(3):
                for x in range(3):
                    if board[y][x] is Tile.Empty:
                        return (x, y)
        
        board = board.standardise()
        
        matchbox = self.getMatchbox(board)
        
        if board.getMoveCount() == 8:
            bead = findEmptyTile(board)
        else:
            bead = matchbox.pickBead()
            if training:
                self.moves.append((matchbox, bead))

        return board.makeMove(bead)

    def endTrainingGame(self, result, started, winDelta=3, drawDelta=1, loseDelta=-1): #Tile.Empty = draw
        beadChange = drawDelta if result == Tile.Empty else winDelta if ((result == Tile.Noughts and started) or (result == Tile.Crosses and not started)) else loseDelta
        for matchbox, bead in self.moves:
            matchbox.addBeads(bead, beadChange)
            if matchbox.isEmpty():
                matchbox.fill()

class GameManager:
    @staticmethod
    def playAgainstHuman(machine, machineStart=True, training=True, winDelta=3, drawDelta=1, loseDelta=-1):
        board = Board([[Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty]])

        if training:
            machine.startTrainingGame()

        machineTurn = machineStart
        while not board.isGameOver():
            if machineTurn:
                print("\n{}".format(board.standardise()))
                print(machine.getMatchbox(board).box.beads)
                board = machine.makeMove(board, training)
            else:
                print("\n{}".format(board))
                x, y = -1, -1
                while not board.isValidMove(x, y):
                    try:
                        x, y = list(map(int, input("Enter your move (x y): ").split()))
                        if not board.isValidMove(x, y):
                            print("2 integers between 0 and 2, at a position that is empty!")
                    except (TypeError, ValueError):
                        print("Oi! Enter 2 integers between 0 and 2 with a space between 'em.")
                board = board.makeMove((x, y))
            machineTurn = not machineTurn

        result = board.isGameOver()
        print("\n{}\n{}!".format(board, "Crosses won" if result is Tile.Crosses else "Noughts won" if result is Tile.Noughts else "It was a tie"))

        if training:
            machine.endTrainingGame(result, machineStart, winDelta, drawDelta, loseDelta)

        return result

    @staticmethod
    def playAgainstRandom(machine, machineStart=True, training=True, winDelta=0, drawDelta=0, loseDelta=-1):
        board = Board([[Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty]])
        
        if training:
            machine.startTrainingGame()
        
        machineTurn = machineStart
        while not board.isGameOver():
            if machineTurn:
                board = machine.makeMove(board, training)
            else:
                x, y = -1, -1
                while not board.isValidMove(x, y):
                    x, y = random.randint(0, 2), random.randint(0, 2)
                board = board.makeMove((x, y))
            machineTurn = not machineTurn
        
        result = board.isGameOver()
        
        if training:
            machine.endTrainingGame(result, machineStart, winDelta, drawDelta, loseDelta)
        
        return result

    @staticmethod
    def playAgainstMachine(machine1, machine2, machine1Start=True, training1=True, training2=True, winDelta1=3, drawDelta1=1, loseDelta1=-1, winDelta2=3, drawDelta2=1, loseDelta2=-1):
        board = Board([[Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty],
                       [Tile.Empty, Tile.Empty, Tile.Empty]])

        if training1:
            machine1.startTrainingGame()
        if training2:
            machine2.startTrainingGame()

        machine1Turn = machine1Start
        while not board.isGameOver():
            if machine1Turn:
                board = machine1.makeMove(board, training1)
            else:
                board = machine2.makeMove(board, training2)
            machine1Turn = not machine1Turn

        result = board.isGameOver()

        if training1:
            machine1.endTrainingGame(result, machine1Start, winDelta1, drawDelta1, loseDelta1)
        if training2:
            machine2.endTrainingGame(result, not machine1Start, winDelta2, drawDelta2, loseDelta2)

        return result

if __name__ == "__main__":
    with open("trainedMachine2.pickle", "rb") as file:
        machine = pickle.load(file)
        logging.info("Loaded machine from pickle file.")

    try:
        logging.info("Start training.")
        iteration = 0
        startTime = time.time()
        while True:
            iteration += 1
            GameManager.playAgainstRandom(machine, iteration%2)
    except KeyboardInterrupt:
        endTime = time.time()
        logging.info("Stopped training.")
        logging.info("Played {} games in {} minutes.".format(iteration, int((endTime-startTime)/60)))

    with open("trainedMachine2.pickle", "wb") as file:
        pickle.dump(machine, file)
        logging.info("Saved trainedMachine to pickle file.")
