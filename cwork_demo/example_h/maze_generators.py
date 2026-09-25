# Anonymised coursework engine; browser changes are documented in guide.md.
import random
from maze_model import MazeGen
import copy

class Generator:
    def __init__(self, mazeGen:MazeGen):
        self._maze = mazeGen
        self._mazeMap = self._maze.getMazeMap
        self._startPos = self._maze.getStartPos
        self._endPos = self._maze.getEndPos
        self._compass = ["N", "E", "S", "W"]

    #Algorithm to generate a random path
    def randomPathGen(self):
        direction = random.choice(self._compass)
        return direction 

    def outsideWall(self, x, y):
        '''
        This means and outside wall has been selected as a random path and the path needs to be selected again
        '''
        self.findNextMove(x, y)

    def delNorth(self,x:int,y:int):
        '''
        Checks for a wall on the coords inputed and with change that wall type into a 0 denoting that the wall is removed
        '''
        self._mazeMap[x,y]["N"] = 0
        try:
            if self._mazeMap[x,y-1]["S"] > 0:
                self._mazeMap[x,y-1]["S"] = 0
        except KeyError:
            pass
    
    def delEast(self,x:int,y:int):
        self._mazeMap[x,y]["E"] = 0
        try:
            if self._mazeMap[x+1,y]["W"] > 0:
                self._mazeMap[x+1,y]["W"] = 0   
        except KeyError:
            pass

    def delSouth(self,x:int,y:int):
        self._mazeMap[x,y]["S"] = 0
        try:
            if self._mazeMap[x,y+1]["N"] > 0:
                self._mazeMap[x,y+1]["N"] = 0
        except KeyError:
            pass

    def delWest(self,x:int,y:int):
        self._mazeMap[x,y]["W"] = 0
        try:
            if self._mazeMap[x-1,y]["E"] > 0:
                self._mazeMap[x-1,y]["E"] = 0
        except KeyError:
            pass

    def changeCellType(self, x:int, y:int, newCellType:int):
        '''
        Changes the celltype with the x and y coords to the chosen newCellType
        '''
        self._mazeMap[x,y]["Type"] = newCellType

    @property
    def getCellType(self,x:int,y:int) -> int:
        '''
        Returns the cellType with the position of x and y coords
        '''
        return self._mazeMap[x,y]["Type"]

    def checkNeighCells(self, x:int, y:int, type:int) -> list:
        '''
        This will check the neighbouring cells of the current cell and return a list of the cells that are not visited
        '''
        neighCells = []
        if y+1 > self._maze.getHeight: pass
        else:
            if self._mazeMap[x,y+1]["Type"] == type: neighCells.append((x,y+1))
            #This means that the cell is on the edge of the maze or has been visited
        if x-1 <= 0: pass
        else:
            if self._mazeMap[x-1,y]["Type"] == type: neighCells.append((x-1,y))
        if y-1 <= 0: pass
        else:
            if self._mazeMap[x,y-1]["Type"] == type: neighCells.append((x,y-1))
        if x+1 > self._maze.getWidth: pass
        else:
            if self._mazeMap[x+1,y]["Type"] == type: neighCells.append((x+1,y))
        return neighCells
        
    def findNextMove(self, x:int, y:int):
        '''
        This will find the next move for the maze
        '''
        if len(self.checkNeighCells(x, y, 0)) == 0: return "Dead End"
        else:
            nextMove = random.choice(self.checkNeighCells(x,y,0))
            if nextMove[1] < y: 
                return ("S", x, y-1)
            if nextMove[0] > x: 
                return ("W", x+1, y)
            if nextMove[1] > y: 
                return ("N",x, y+1)
            if nextMove[0] < x: 
                return ("E",x-1, y)
            #As there are no possible moves the maze generator will need to backtrack  

##############################################################
#                                                            #
#     CATEGORY A SKILL: COMPLEX USE OF OOP (INHERITENCE)     #
#     CATEGORY A SKILL: ADVANCED STACK OPERATIONS            #
#     CATEGORY A SKILL: RECURSIVE ALGORITHM                  #
#                                                            #
##############################################################

class RBT(Generator):
    def __init__(self, mazeGen):
        super().__init__(mazeGen)
        self._stack = []
        self._stackGen = []

    def run(self):
        # Browser repair: an explicit stack avoids recursive call-stack limits.
        # Keep the original neighbour selection and reciprocal wall operations.
        start = tuple(self._startPos)
        self.changeCellType(*self._endPos, 0)
        self._stack = [start]
        self._stackGen = [start]
        self.changeCellType(*start, 1)
        while self._stack:
            x, y = self._stack[-1]
            move = self.findNextMove(x, y)
            if move == "Dead End":
                self._stack.pop()
                continue
            direction, nx, ny = move
            {"N": self.delNorth, "S": self.delSouth,
             "E": self.delEast, "W": self.delWest}[direction](nx, ny)
            self.changeCellType(nx, ny, 1)
            self._stack.append((nx, ny))
            self._stackGen.append((nx, ny))
        self.changeCellType(*self._startPos, 3)
        self.changeCellType(*self._endPos, 4)
        self._maze.setTempMaze(copy.deepcopy(self._mazeMap))

    @property
    def getGen(self):
        return self._stackGen

##############################################################
#                                                            #
#     CATEGORY A SKILL: COMPLEX USE OF OOP (INHERITENCE)     #
#     CATEGORY A SKILL: ADVANCED STACK OPERATIONS            #
#     CATEGORY A SKILL: RECURSIVE ALGORITHM                  #
#                                                            #
##############################################################


##############################################################
#                                                            #
#     CATEGORY A SKILL: COMPLEX USE OF OOP (INHERITENCE)     #
#     Binary-tree maze generation (not binary search)                        #
#                                                            #
##############################################################

class BinaryTree(Generator):
    def __init__(self, mazeGen: MazeGen):
        super().__init__(mazeGen)

    def run(self, direction:str):
        self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 0)
        self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 0)
        self.__algorithm(direction)

    def __algorithm(self, direction):
        for cell in self._mazeMap:
            if direction == "NW":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == 1 and cell[0] != 1:
                    self.delWest(cell[0], cell[1])              
                if cell[0] == 1 and cell[1] != 1:
                    self.delNorth(cell[0], cell[1])
                if cell[1] != 1:
                    if randNum == 0:
                        self.delNorth(cell[0], cell[1])
                if cell[0] != 1:
                    if randNum == 1:
                        self.delWest(cell[0], cell[1])
            elif direction == "NE":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == 1 and cell[0] != self._maze.getWidth:
                    self.delEast(cell[0], cell[1])              
                if cell[0] == self._maze.getWidth and cell[1] != 1:
                    self.delNorth(cell[0], cell[1])
                if cell[1] != 1:
                    if randNum == 0:
                        self.delNorth(cell[0], cell[1])
                if cell[0] != self._maze.getWidth:
                    if randNum == 1:
                        self.delEast(cell[0], cell[1])
            elif direction == "SW":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == self._maze.getHeight and cell[0] != 1:
                    self.delWest(cell[0], cell[1])              
                if cell[0] == 1 and cell[1] != self._maze.getHeight:
                    self.delSouth(cell[0], cell[1])
                if cell[1] != self._maze.getHeight:
                    if randNum == 0:
                        self.delSouth(cell[0], cell[1])
                if cell[0] != 1:
                    if randNum == 1:
                        self.delWest(cell[0], cell[1])
            elif direction == "SE":
                self._mazeMap[cell]["Type"] = 1
                randNum = random.randint(0,1)
                if cell[1] == self._maze.getHeight and cell[0] != self._maze.getWidth:
                    self.delEast(cell[0], cell[1])              
                if cell[0] == self._maze.getWidth and cell[1] != self._maze.getHeight:
                    self.delSouth(cell[0], cell[1])
                if cell[1] != self._maze.getHeight:
                    if randNum == 0:
                        self.delSouth(cell[0], cell[1])
                if cell[0] != self._maze.getWidth:
                    if randNum == 1:
                        self.delEast(cell[0], cell[1])
            if cell == (self._maze.getWidth, self._maze.getHeight):
                self.changeCellType(self._maze.getStartPos[0], self._maze.getStartPos[1], 3)
                self.changeCellType(self._maze.getEndPos[0], self._maze.getEndPos[1], 4)
                tempMaze = copy.deepcopy(self._mazeMap)
                self._maze.setTempMaze(tempMaze)
                pass # Demo: omit verbose terminal diagnostics.
                return
