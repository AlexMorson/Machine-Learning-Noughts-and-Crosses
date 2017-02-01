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
    mode = 0
    check2 = False
    check1and3 = False
    
    if mode == 0:
        groups = {str(key):{key1:{str(key2):0 for key2 in range(5)} for key1 in ('X','O',' ')} for key in range(0,7,2)}
        if check2:
            groups['X']['2'] = {"Opp" : 0, "Adj" : 0}
            groups['O']['2'] = {"Opp" : 0, "Adj" : 0}
            groups[' ']['2'] = {"Opp" : 0, "Adj" : 0}
        if check1and3:
            groups['X']['1'] = {"X" : 0, "O" : 0}
            groups['O']['1'] = {"X" : 0, "O" : 0}
            groups[' ']['1'] = {"X" : 0, "O" : 0}
            groups['X']['3'] = {"X" : 0, "O" : 0}
            groups['O']['3'] = {"X" : 0, "O" : 0}
            groups[' ']['3'] = {"X" : 0, "O" : 0}
        
        for b in boards:
            c = 0
            if b[0][0] is not Tile.Empty: c += 1
            if b[2][0] is not Tile.Empty: c += 1
            if b[0][2] is not Tile.Empty: c += 1
            if b[2][2] is not Tile.Empty: c += 1

            e = 0
            if b[1][0] is not Tile.Empty: e += 1
            if b[1][2] is not Tile.Empty: e += 1
            if b[0][1] is not Tile.Empty: e += 1
            if b[2][1] is not Tile.Empty: e += 1

            m = 0
            if b[1][1] is not Tile.Empty: m += 1

            if c == 2 and check2:
                if b[0][0] is not Tile.Empty and b[2][2] is not Tile.Empty or b[2][0] is not Tile.Empty and b[0][2] is not Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['2']["Opp"] += 1
                else:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['2']["Adj"] += 1
            elif c == 1 and check1and3:
                if b[0][0] is not Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[0][0] is Tile.Noughts else 'X'] += 1
                if b[2][0] is not Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[2][0] is Tile.Noughts else 'X'] += 1
                if b[0][2] is not Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[0][2] is Tile.Noughts else 'X'] += 1
                if b[2][2] is not Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[2][2] is Tile.Noughts else 'X'] += 1
            elif c == 3 and check1and3:
                if b[0][0] is Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[2][2] is Tile.Noughts else 'X'] += 1
                if b[2][0] is Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[0][2] is Tile.Noughts else 'X'] += 1
                if b[0][2] is Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[2][0] is Tile.Noughts else 'X'] += 1
                if b[2][2] is Tile.Empty:
                    groups[' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X']['1']['O' if b[0][0] is Tile.Noughts else 'X'] += 1
            else:
                groups[str(c+e+m)][' ' if b[1][1] is Tile.Empty else 'O' if b[1][1] is Tile.Noughts else 'X'][str(c)] += 1
            
    elif mode == 1:
        groups = {}
        for b in boards:
            s = 0
            if b[1][0] is not Tile.Empty: s += 1
            if b[1][2] is not Tile.Empty: s += 1
            if b[0][1] is not Tile.Empty: s += 1
            if b[2][1] is not Tile.Empty: s += 1
            if b[1][1] is not Tile.Empty: s += 5
            if str(s) in groups:
                groups[str(s)]+=1
            else:
                groups[str(s)]=1

    toDelete = []
    for key in groups:
        for key2 in groups[key]:
            for key3 in groups[key][key2]:
                if groups[key][key2][key3] == 0:
                    toDelete.append((key, key2, key3))
    for key, key2, key3 in toDelete:
        del groups[key][key2][key3]
    del groups["0"]["O"]
    del groups["0"]["X"]
    print(json.dumps(groups, indent=4, sort_keys=True))
            
