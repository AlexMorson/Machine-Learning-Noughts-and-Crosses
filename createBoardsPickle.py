import pickle
import json
from enum import Enum

class Tile(Enum):
    Empty = 0
    Noughts = 1
    Crosses = 2

def flipH(b): #X axis flip (top/bottom)
    return b[::-1]

def flipV(b): #Y axis flip (left/right)
    return [b[0][::-1],b[1][::-1],b[2][::-1]]

def rotate90(b):
    return [[b[2][0],b[1][0],b[0][0]],
            [b[2][1],b[1][1],b[0][1]],
            [b[2][2],b[1][2],b[0][2]]]

def rotate180(b):
    return rotate90(rotate90(b))

def rotate270(b):
    return rotate90(rotate90(rotate90(b)))

def getTransformations(b):
    return [b, rotate90(b), rotate180(b), rotate270(b),
            flipH(b), rotate90(flipH(b)), rotate180(flipH(b)), rotate270(flipH(b))]

def isWinningState(b):
    return b[0][0]==b[0][1]==b[0][2]!=Tile.Empty or\
           b[1][0]==b[1][1]==b[1][2]!=Tile.Empty or\
           b[2][0]==b[2][1]==b[2][2]!=Tile.Empty or\
           b[0][0]==b[1][0]==b[2][0]!=Tile.Empty or\
           b[0][1]==b[1][1]==b[2][1]!=Tile.Empty or\
           b[0][2]==b[1][2]==b[2][2]!=Tile.Empty or\
           b[0][0]==b[1][1]==b[2][2]!=Tile.Empty or\
           b[2][0]==b[1][1]==b[0][2]!=Tile.Empty

def printBoard(b):
    def formatTile(t):
        return " " if t is Tile.Empty else "X" if t is Tile.Crosses else "O"
    print("{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}\n".format(*([formatTile(t) for t in b[0]]+[formatTile(t) for t in b[1]]+[formatTile(t) for t in b[2]])))

def getAllBoardsFrom(startBoard):
    def getNextBoards(b, turn):
        for y in range(3):
            for x in range(3):
                if b[y][x] is Tile.Empty:
                    newBoard = [[tile for tile in row] for row in b]
                    newBoard[y][x] = turn
                    for boardTransformation in getTransformations(newBoard):
                        if boardTransformation in boards:
                            break
                    else:
                        if not isWinningState(newBoard):
                            boards.append(newBoard)
                            getNextBoards(newBoard, Tile.Noughts if turn is Tile.Crosses else Tile.Crosses)

    boards = [startBoard]
    getNextBoards(startBoard, Tile.Noughts)
    return boards

def removeOddTurns(boards):
    evenBoards = []
    for b in boards:
        c = 0
        for y in range(3):
            for x in range(3):
                if b[y][x] is not Tile.Empty:
                    c += 1
        if c in (0, 2, 4, 6):
            evenBoards.append(b)
    return evenBoards

if __name__ == "__main__":
    boards = getAllBoardsFrom([[Tile.Empty,Tile.Empty,Tile.Empty],[Tile.Empty,Tile.Empty,Tile.Empty],[Tile.Empty,Tile.Empty,Tile.Empty]])
    boards = removeOddTurns(boards)

    with open("boards.pickle", "wb") as f:
        pickle.dump(boards, f)
