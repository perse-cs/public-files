# Anonymised coursework engine; browser changes are documented in guide.md.



class Board():

    EMPTY = "  "
    H_LINE = "--"
    V_LINE = "|"

    def __init__(self, rows: int, cols: int):
        self.__grid = [[[Board.EMPTY, Board.EMPTY, Board.EMPTY, Board.EMPTY] for _ in range(cols)] for _ in range(rows)]
        self.__claimed = [[Board.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.__rows = rows
        self.__cols = cols

    def __repr__(self):
        display = []
        for row in range(self.__rows):
            dRow1 = []
            dRow2 = []
            for col in range(self.__cols):
                dRow1.append(".")
                dRow1.append(self.__grid[row][col][0])
                if self.__grid[row][col][3] == Board.EMPTY:
                    dRow2.append(" ")
                else:
                    dRow2.append(self.__grid[row][col][3])
                if self.__claimed[row][col] == Board.EMPTY:
                    dRow2.append(Board.EMPTY)
                else:
                    dRow2.append(str(self.__claimed[row][col]+1) + " ")
            col = self.__cols - 1
            dRow1.append(".")
            dRow1.append("\n")
            if self.__grid[row][col][2] == Board.EMPTY:
                dRow2.append(" ")
            else:
                dRow2.append(self.__grid[row][col][2])

            dRow2.append("\n")
            display += dRow1
            display += dRow2
        row = self.__rows - 1
        dRow = []
        for col in range(self.__cols):
            dRow.append(".")
            dRow.append(self.__grid[row][col][1])
            
        dRow.append(".")
        display += dRow
        ReturnStr = ""
        for i in range(len(display)):
            ReturnStr += display[i]
        return ReturnStr
                    
            #go box by box, check each side
    
    
    def getBoxExists(self, pos: tuple):
        if self.__claimed[pos[0]][pos[1]] == Board.EMPTY:
            return -1
        return self.__claimed[pos[0]][pos[1]]
    
    def directionConvert(self, dir:str):
        if dir.upper() == "N":
            return 0
        elif dir.upper() == "S":
            return 1
        elif dir.upper() == "E":
            return 2
        elif dir.upper() == "W":
            return 3
    
    def getDataPoint(self, row, col, dir):
        dir = self.directionConvert(dir)
        if self.__grid[row][col][dir] == Board.EMPTY:
            return 0
        return 1
    
    def checkLine(self, pos: tuple, dir: int):
        if (self.__grid[pos[0]][pos[1]])[dir] == Board.EMPTY:
            return False
        return True

    def checkBox(self, pos: tuple):
        for i in range(4):
            if not self.checkLine(pos, i):
                return False
        return True
     
    def CheckFull(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if not self.checkBox((i, j)):
                    return False
        return True
    
    def checkClear(self, pos: tuple, dir: str):
        dir = self.directionConvert(dir)
        if self.__grid[pos[0]][pos[1]][dir] == Board.EMPTY:
            return True
        return False
    
    def place(self, pos: tuple, dir: str):
        dir = self.directionConvert(dir)
        if dir <= 1:
            self.__grid[pos[0]][pos[1]][dir] = Board.H_LINE
        elif dir >= 2:
            self.__grid[pos[0]][pos[1]][dir] = Board.V_LINE
    
    def MatchedPlace(self, pos: tuple, dir: str):
        dir = self.directionConvert(dir)
        if dir == 0:
            if pos[0] - 1 >= 0:
                return pos[0] - 1, pos[1], "S"
        elif dir == 1:
            if pos[0] + 1 < self.__rows:
                return pos[0] + 1, pos[1], "N"
        elif dir == 2:
            if pos[1] + 1 < self.__cols:
                return pos[0], pos[1] + 1, "W"
        elif dir == 3:
            if pos[1] - 1 >= 0:
                return pos[0], pos[1] - 1, "E"
    # match up placement to equivalent place in neighbouring box

    def ClaimBox(self, pos: tuple, pnum: int):
        self.__claimed[pos[0]][pos[1]] = pnum
    
    def getScores(self, numPlayers: int):
        scores = [0 for _ in range(numPlayers)]
        for i in range(self.__rows):
            for j in range(self.__cols):
                owner = self.__claimed[i][j]
                if owner != Board.EMPTY:
                    scores[owner] += 1
        return scores
    
    def getRows(self):
        return self.__rows

    def getCols(self):
        return self.__cols
    
    def ReturnAvailable(self):
        Available = []
        reject = []
        for i in range(self.__rows):
            for j in range(self.__cols):
                for k in range(4):
                    if self.__grid[i][j][k] == Board.EMPTY:
                        dirs = ["N", "S", "E", "W"]
                        direc = dirs[k]
                        test = (i, j, direc)
                        if test not in reject:
                            Available.append((i, j, direc))
                            rejected = self.MatchedPlace((i, j), direc)
                            reject.append(rejected)
        return Available



            
            

class Player():
    def __init__(self, name: str, type: str):
        self.__name = name
        self.__claimedBoxes = 0
        self.__type = type[0]
        self.__difficulty = None
        if self.__type == "C": #C = Computer, P = Person / Player
            self.__difficulty =int(type[1]) #0=random, 1=easy, 2=medium, 3=hard
    
    def addBox(self):
        self.__claimedBoxes += 1
    
    @property
    def getName(self):
        return self.__name
    
    def getType(self):
        return self.__type
    
    def getDifficulty(self):
        return self.__difficulty

#####################################################
# Skill set B - Simple OOP model                    #
# Once the Game class is instantiated, it will      #
# create instances of the player class and board    #
# class for it to use                               #
#####################################################

class Game():

    def __init__(self, dims: tuple, pnum: int, names: list, types: list):
        self.__board = Board(dims[0], dims[1])
        self.players = []
        for i in range(pnum):
            x = Player(names[i], types[i])
            self.players.append(x)
        self.__turn = 0
    
    def getDataPoint(self, row, col, dir):
        return self.__board.getDataPoint(row, col, dir)

    def checkClear(self, pos: tuple, dir: str):
        return self.__board.checkClear(pos, dir)

    def getTurn(self):
        return self.__turn
    
    def getBoxExists(self, pos: tuple):
        return self.__board.getBoxExists(pos)

    ################################################################
    # Skill set A - Complex User-Defined Algorithms                #
    # Place and Matched place methods are used to compensate for   #
    # the potential occurrence of a line appearing twice in the    #
    # board as it is between two sqaures. This will update both    #
    # where necessary, claim boxes appropriately and update both   #
    # the grid array and claimed array                             #
    ################################################################
    
    def place(self, pos: tuple, dir: str):
        boxCreated = False
        if not self.__board.checkClear(pos, dir):
            return False
        if self.__board.checkClear(pos, dir):
            self.__board.place(pos, dir)
            res = self.__board.MatchedPlace(pos, dir)
            if res != None:
                if res[0] != -1 and res[0] < self.__board.getRows() and res[1] != -1 and res[1] < self.__board.getCols():
                    newPos = (res[0], res[1])
                    newDir = res[2]
                    self.__board.place(newPos, newDir)
                    if self.__board.checkBox(newPos):
                        self.__board.ClaimBox(newPos, self.__turn)
                        boxCreated = True
                        self.players[self.__turn].addBox()
        if self.__board.checkBox(pos):
            self.__board.ClaimBox(pos, self.__turn)
            boxCreated = True
            self.players[self.__turn].addBox()
        
        return boxCreated
        

    def __repr__(self):
        return str(self.__board)
    
    def MatchedPlace(self, pos: tuple, dir: str):
        return self.__board.MatchedPlace(pos, dir)

    def End(self):
        if self.__board.CheckFull():
            return True
        return False
    
    def CalculateScores(self):
        scores = self.__board.getScores(len(self.players))
        return scores

    def nextTurn(self):
        if self.__turn + 1 < len(self.players):
            self.__turn += 1
        elif self.__turn +1 == len(self.players):
            self.__turn = 0
    
    def ReturnAvailable(self):
        return self.__board.ReturnAvailable()
    
    def getHeight(self):
        return self.__board.getRows()
    
    def getWidth(self):
        return self.__board.getCols()


