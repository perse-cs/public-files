# Anonymised coursework engine; browser changes are documented in guide.md.
from fleet_errors import ShotError, ShipPlacementError
from itertools import product
from random import randrange, choice

# A class for keys and references to ensure they are always unique
class Unique:
    def __init__(self):
        pass

vertical = Unique()
horizontal = Unique()

# Group B skill: Multi-dimensional arrays
class Array2d:
    def __init__(self, startValue = None, **kwargs):
        """Requires either "shape" or "width" and "height"""
        if "shape" in kwargs:
            self.__grid = kwargs["shape"]
        else:
            width = kwargs["width"]
            height = kwargs["height"]
            self.__grid = [[startValue for _ in range(width)] for _ in range(height)]
        self.__defaultValue = startValue

    def __len__(self):
        return self.width*self.height

    def __getitem__(self, row):
        return self.__grid[row]
        # Returns the row. When grid[x][y] is called, getitem
        # is called with [x] and returns a list that is then indexed from [y]
    
    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n >= self.width * self.height:
            raise StopIteration
        col, row = divmod(self.__n, self.width)
        self.__n += 1
        return self.__grid[row][col], (row, col)

    def __str__(self):
        s = str()
        for row in self.__grid:
            s += "|".join([str(x) for x in row])+"\n"+"-"*3*self.width+"\n"
        return s

    def expand(self, additionalColumns:int):
        for _ in range(additionalColumns):
            self.__grid.append([self.__defaultValue for _ in range(self.height)])

    def extend(self, additionalRows:int):
        for column in self.__grid:
            for _ in range(additionalRows):
                column.append(self.__defaultValue)

    def trim(self):
        """Removes rows and columns from all 4 sides from the grid if they contain only default values"""
        # Trim rows from end
        while True:
            delete = True
            for y in range(self.height):
                if self.__grid[-1][y] != self.__defaultValue:
                    delete = False
                    break
            if delete:
                self.__grid.pop(-1)
            else:
                break
        
        # Trim rows from start
        while True:
            delete = True
            for y in range(self.height):
                if self.__grid[0][y] != self.__defaultValue:
                    delete = False
                    break
            if delete:
                self.__grid.pop(0)
            else:
                break

        #Trim columns from end
        while True:
            delete = True
            for x in range(self.width):
                if self.__grid[x][-1] != self.__defaultValue:
                    delete = False
                    break
            if delete:
                for column in range(self.width):
                    self.__grid[column].pop(-1)
            else:
                break

        #Trim columns from start
        while True:
            delete = True
            for x in range(self.width):
                if self.__grid[x][0] != self.__defaultValue:
                    delete = False
                    break
            if delete:
                for column in range(self.width):
                    self.__grid[column].pop(0)
            else:
                break

        return self

    @property
    def width(self):
        return len(self.__grid)

    @property
    def height(self):
        return len(self.__grid[0])
    
    @property
    def shape(self):
        return self.__grid

class Player:
    def __init__(self, name:str, ships:list):
        self._name = name
        self._ships = ships
        self._shipsLeftToPlace = ships[::]
        self._stats = StatsTracker()

    @property
    def name(self):
        return self._name
    
    @property
    def ships(self):
        return self._ships

    @property
    def shipsLeftToPlace(self):
        return self._shipsLeftToPlace

    @property
    def stats(self):
        return self._stats
    
    def resetStats(self):
        self._stats = StatsTracker()
class AI(Player):
    def __init__(self, name, ships, board, game, difficulty):
        super().__init__(name, ships)
        self.__difficulty = difficulty
        self.__board = board
        self.__game = game
        self.__huntingHits = list()
        self.__shotsTaken = Array2d(width = Game.dim, height = Game.dim, startValue= False)

    def initialiseAI(self):
        self.__opponentShips = self.__game.playerOpponent(self).ships[::]
        self.generateProbabilityMap()

    def generateProbabilityMap(self):
        probabilityMap = Array2d(width = Game.dim, height = Game.dim, startValue = 0)
        for ship in self.__opponentShips:
            for orientation in (horizontal, vertical):
                maxRow = Game.dim - ship.length + 1 if orientation == vertical else Game.dim - ship.width + 1
                maxCol = Game.dim - ship.width + 1 if orientation == vertical else Game.dim - ship.length + 1
                for row in range(maxRow):
                    for col in range(maxCol):
                        if self.__isValidPlacement(ship, row, col, orientation):
                            for y, x in self.__game.coveredSquares(ship, row, col, orientation):
                                probabilityMap[x][y] += 1
        self.__probabilityMap = probabilityMap
    
    def __isValidPlacement(self, ship, row, col, orientation):
        for square in self.__game.coveredSquares(ship, row, col, orientation):
            x, y = square
            if square in self.__huntingHits:
                continue
            if self.__shotsTaken[x][y]:
                break
        else:
            return True
        return False


    def __huntHit(self):
        probabilityMap = Array2d(width = Game.dim, height = Game.dim, startValue = 0)
        for ship in self.__opponentShips:
            for orientation in (horizontal, vertical):
                maxRow = Game.dim - ship.length + 1 if orientation == vertical else Game.dim - ship.width + 1
                maxCol = Game.dim - ship.width + 1 if orientation == vertical else Game.dim - ship.length + 1
                for row in range(maxRow):
                    for col in range(maxCol):
                        if self.__isValidPlacement(ship, row, col, orientation):
                            squares = self.__game.coveredSquares(ship, row, col, orientation)
                            valid = False
                            for square in squares:
                                y, x = square
                                if square in self.__huntingHits:
                                    valid = True
                            if valid:
                                for square in squares:
                                    squareContense = self.__board[self][self.__game.ShotBoard][x][y]
                                    if squareContense == self.__game.miss:
                                        valid = False
                                        break
                            if valid:
                                for s in squares:
                                    if s not in self.__huntingHits:
                                        x, y = s
                                        probabilityMap[x][y] += 1
        self.__probabilityMap = probabilityMap

    def takeShot(self):
        trackedProbs = set([0])
        potentialShots = list()
        pass # Demo: omit verbose terminal diagnostics.

        # Build a set of the top n probabilities in the probability map
        for prob, coords in self.__probabilityMap:
            x, y = coords
            if prob == 0 or self.__shotsTaken[x][y]:
                continue
            if len(trackedProbs) < self.__difficulty:
                trackedProbs.add(prob)
                continue
            if prob > min(trackedProbs) and prob not in trackedProbs:
                trackedProbs.add(prob)
                trackedProbs.remove(min(trackedProbs))

        # Pick out all of the items with probability in the top n
        for prob, coords in self.__probabilityMap:
            if prob in trackedProbs:
                x, y = coords
                if not self.__shotsTaken[x][y]:
                    potentialShots.append(coords)

        shotToFire = choice(potentialShots)
        x, y = shotToFire
        p = self.__probabilityMap[x][y]
        self.__shotsTaken[x][y] = True
        pass # Demo: omit verbose terminal diagnostics.
        row, col = shotToFire
        hit = self.__game.fire(row, col)
        pass # Demo: omit verbose terminal diagnostics.
        pass # Demo: omit verbose terminal diagnostics.


        if type(hit) == Ship:
            self.__huntingHits.append(shotToFire)
            self.__removeShip(shotToFire, hit)
        elif hit == True:
            self.__huntingHits.append(shotToFire)
        
        if self.__huntingHits:
            self.__huntHit()
        else:
            self.generateProbabilityMap()

    def __removeShip(self, shot, ship):
        self.__opponentShips.remove(ship)
        self.__huntingHits = list()

    def __removeShip(self, ShotThatSunk, ship):
        self.__opponentShips.remove(ship)
        candidatePlacements = []

        for orientation in (horizontal, vertical):
            # To get a candidate cover, the ship must be translated left. max[XY] is the furthest it makes sense to check
            # How far in X and Y the ship is translated from the coords
            for x, y in product(range(Game.dim), range(Game.dim)):
                placeCoords = (x, y)
                if ship.wouldOverlap(placeCoords, ShotThatSunk, orientation):
                    for coordsInPlacement in self.__game.coveredSquares(ship, x, y, orientation):
                        if coordsInPlacement not in self.__huntingHits:
                            break
                    else:
                        candidatePlacements.append((x, y ,orientation))  

        if candidatePlacements:
            x, y, o = candidatePlacements[0]
            for sqaure in self.__game.coveredSquares(ship, x, y, o):
                self.__huntingHits.remove(sqaure)
        else:
            self.__huntingHits = list()


    def placeShips(self):
        # This should be optimised
        OrientationOptions = (horizontal, vertical)
        for ship in self._ships:
            Orientation = OrientationOptions[randrange(0, len(OrientationOptions))]
            Placed = False
            while Placed == False:
                maxX = Game.dim - ship.length + 1 if Orientation == horizontal else Game.dim - ship.width + 1
                maxY = Game.dim - ship.length + 1 if Orientation == vertical else Game.dim - ship.width + 1
                x = randrange(0, maxX)
                y = randrange(0, maxY)
                try:
                    self.__game.placeShip(self, ship, x, y, Orientation)
                    Placed = True
                except ShipPlacementError:
                    pass # Demo: omit verbose terminal diagnostics.
                    continue
            pass # Demo: omit verbose terminal diagnostics.
        pass # Demo: omit verbose terminal diagnostics.
    
    @property
    def difficulty(self):
        return self.__difficulty

class Ship:
    def __init__(self, name, **kwargs):
        self.__name = name
        if "shape" in kwargs:
            shape = kwargs["shape"]
            pass # Demo: omit verbose terminal diagnostics.
            self.__shape = Array2d(width = shape.width, height = shape.height)
            self.__length = shape.width
            self.__width = shape.height
            for shipPart, coords in kwargs["shape"]:
                pass # Demo: omit verbose terminal diagnostics.
                try:
                    if shipPart:
                        pass # Demo: omit verbose terminal diagnostics.
                        y, x = coords
                        self.__shape[x][y] = ShipPart(self)
                except IndexError:
                    pass # Demo: omit verbose terminal diagnostics.
        else:
            self.__length = kwargs["length"]
            self.__width = kwargs["width"]
            # Group B skill: Multi-dimensional arrays
            self.__shape = Array2d(width = self.__length, height = self.__width)
            for row, col in product(range(self.__width), range(self.__length)):
                # Group A skill: Dynamic generation of objects
                self.__shape[row][col] = ShipPart(self)
        
        self.__remainingHits = list()
        for part, coords in self.__shape:
            if part != None:
                self.__remainingHits.append(part)

    def __str__(self):
        return f"""Name: {self.__name}
Length: {self.__length}
Width: {self.__width}"""

    def __iter__(self):
        return self.__shape.__iter__()

    def wouldOverlap(self, placementCoords, overlapCoords, orientation) -> bool:
        placeRow, placeCol = placementCoords
        overlapRow, overlapCol = overlapCoords
        row = overlapRow - placeRow
        col = overlapCol - placeCol
        if orientation == vertical:
            row, col = col, row
        if 0 <= row < self.__width and 0 <= col < self.__length:
            return False if self.__shape[row][col] == None else True
        else:
            return False

    def hit(self, part):
        self.__remainingHits.remove(part)
        if len(self.__remainingHits) == 0:
            return self
        else:
            return True

    @property
    def name(self):
        return self.__name
    
    @property
    def width(self):
        return self.__width
    
    @property
    def length(self):
        return self.__length
    
    @property
    def shape(self):
        return self.__shape
        
class ShipPart:
    def __init__(self, parentShip):
        self.__parentShip = parentShip

    def __eq__(self, other):
        if type(other) == ShipPart:
            return self.__parentShip == other.parentShip

    def onHit(self):
        """Calls a function in the parent ship that tells it that it has been 
        hit, so that it can decrement it's remaining health and return if the ship has been sunk.
        returns True if the ship hit has not been sunk and a Ship object if it has been sunk"""
        return self.__parentShip.hit(self)

    @property
    def parentShip(self):
        return self.__parentShip

class Game:
    dim = 8
    empty = None

    def __init__(self, player1Name, player2Name, player1ships, player2ships, player1AI = False, player2AI = False):
        # Must use properties rather than class variables to keep instances consistent when the game is loaded from the hard drive
        self.__ship = Unique()
        self.__hit = Unique()
        self.__miss = Unique()
        self.__ShotBoard = Unique()
        self.__ShipBoard = Unique()
        
        # The board must be initialised and provided to the AI to create it and then the board must be populated
        # as it requires an instance of the AI to use as a key
        self.__board = dict()
        self.__player1 = AI(player1Name, player1ships, self.__board, self, player1AI) if player1AI else Player(player1Name, player1ships)
        self.__player2 = AI(player2Name, player2ships, self.__board, self, player2AI) if player2AI else Player(player2Name, player2ships)
        # The board requires 4 seperate grids. A grid of ships and grid of shots for each player
        # Group B skill: Multi-dimensional arrays
        # Group B skill: Dictionaries
        self.__board[self.__player1] = {self.__ShotBoard:Array2d(width = Game.dim, height = Game.dim), self.__ShipBoard:Array2d(width = Game.dim, height = Game.dim)}
        self.__board[self.__player2] = {self.__ShotBoard:Array2d(width = Game.dim, height = Game.dim), self.__ShipBoard:Array2d(width = Game.dim, height = Game.dim)}
        
        # Prepare the AI porbability boards
        if player1AI:
            self.__player1.initialiseAI()
        if player2AI:
            self.__player2.initialiseAI()

        self.__currentPlayerTurn = self.__player1
        self.__turnNumber = 0
        self.__gameMode = self.__ShipBoard

    def placeShip(self, player:Player, ship:Ship, column:int, row:int, orientation):
        #Checking that the ship will remain within the bounds of the board
        # This will raise an AssertionError if the ship does not remain within the board
        if not self.IsValidPlacement(player, ship, row, column, orientation):
            raise ShipPlacementError
        # This board is the grid belonging to the relevant player tracking that player's ships
        board = self.__board[player][self.__ShipBoard]

        # Placing the ship
        if orientation == vertical:
            for y in range(ship.width):
                for x in range(ship.length):
                    board[row+x][column+y] = ship.shape[y][x]
        else:
            for x in range(ship.width):
                for y in range(ship.length):
                    board[row+x][column+y] = ship.shape[x][y]
        
        player.shipsLeftToPlace.remove(ship)

    def IsValidPlacement(self, player, ship, row, col, orientation) -> bool:
        """Checks constraints of the board and existing ships to see if the parameters 
        would produce a valid ship position"""
        board = self.__board[player][self.__ShipBoard]
        if orientation not in (horizontal, vertical):
            return False
        # Check the initial point is within the constrains of the board
        if not (0 <= row < Game.dim and 0 <= col < Game.dim):
            return False

        if orientation == vertical:
            if row + ship.length-1 < Game.dim and col + ship.width-1 < Game.dim:
                pass
            else:
                return False
        else:
            if col + ship.length-1 < Game.dim and row + ship.width-1 < Game.dim:
                pass
            else:
                return False

        # Checking that the area that the ship will go in is empty
        # This check myst be done before the ship starts to be placed
        for shipPart, coords in ship:
            if shipPart:
                if orientation == horizontal:
                    x, y = coords
                else:
                    y, x = coords
                if board[row+x][col+y] != Game.empty:
                    return False

        return True 

    def coveredSquares(self, ship, row, column, orientation):
        coveredSquares = []
        for shipRow, shipCol in product(range(ship.width), range(ship.length)):
            deltaR = shipRow if orientation == horizontal else shipCol
            deltaC = shipCol if orientation == horizontal else shipRow
            if ship.shape[shipRow][shipCol] != None:
                # Group C skill: Single-dimensional arrays
                coveredSquares.append((row + deltaR, column + deltaC))
        return coveredSquares

    def fire(self, column:int, row:int):
        assert 0 <= row < Game.dim and 0 <= column <Game.dim
        # The ship board is the map of enemy ships and the shot board is the current player's board
        # of shots It is needed to track the shots taken
        ShipBoard = self.__board[self.playerOpponent(self.__currentPlayerTurn)][self.__ShipBoard]
        ShotBoard = self.__board[self.__currentPlayerTurn][self.__ShotBoard]
        if ShotBoard[row][column] != Game.empty:
            raise ShotError
        statTrack = self.player1Stats if self.__currentPlayerTurn == self.__player1 else self.player2Stats
        statTrack.incShots()
        if type(ShipBoard[row][column]) == ShipPart:
            ShotBoard[row][column] = self.__hit
            shotReturn = ShipBoard[row][column].onHit()
            statTrack.incHits()
            if type(shotReturn) == Ship:
                statTrack.incSinks()
            return shotReturn
        else:
            ShotBoard[row][column] = self.__miss
            return False

    def playerOpponent(self, player:Player):
        if player == self.__player1:
            return self.__player2
        else:
            return self.__player1

    def changeTurn(self):
        self.__currentPlayerTurn = self.playerOpponent(self.__currentPlayerTurn)
        self.__turnNumber += 1

    @property
    def board(self):
        return self.__board

    @property
    def currentPlayerTurn(self):
        return self.__currentPlayerTurn

    @property
    def winner(self):
        # Iterating through each board of ships and checking to see if any ships remain
        for player, playerBoard in self.__board.items():
            shipBoard = playerBoard[self.__ShipBoard]
            win = True
            for row in range(Game.dim):
                for col in range(Game.dim):
                    square = shipBoard[row][col]
                    if type(square) == ShipPart:
                        if self.board[self.playerOpponent(player)][self.__ShotBoard][row][col] != self.__hit:
                            win = False
                            pass # Demo: omit verbose terminal diagnostics.
                            break
                if win == False:
                    break
                    # For each square on the board, if there is a ship, check if it is hit. If not, the player has not won
            if win == True:
                return self.playerOpponent(player)
        return None
    
    @property
    def turnNumber(self):
        return self.__turnNumber

    @property
    def player1(self):
        return self.__player1

    @property
    def player2(self):
        return self.__player2

    @property
    def player1Stats(self):
        return self.__player1.stats

    @property
    def player2Stats(self):
        return self.__player2.stats

    def resetStats(self, player:int):
        if player == 1:
            self.__player1.resetStats()
        else:
            self.__player2.resetStats()

    @property
    def ship(self):
        return self.__ship

    @property
    def hit(self):
        return self.__hit

    @property
    def miss(self):
        return self.__miss

    @property
    def ShotBoard(self):
        return self.__ShotBoard

    @property
    def ShipBoard(self):
        return self.__ShipBoard

    @property
    def gameMode(self):
        return self.__gameMode

    @gameMode.setter
    def gameMode(self, value):
        self.__gameMode = value

class StatsTracker:
    def __init__(self):
        self.__shotsTaken = 0
        self.__shipsSunk = 0
        self.__hitsMade = 0
    
    def incShots(self):
        self.__shotsTaken += 1

    def incHits(self):
        self.__hitsMade += 1

    def incSinks(self):
        self.__shipsSunk += 1
    
    @property
    def shots(self):
        return self.__shotsTaken

    @property
    def hits(self):
        return self.__hitsMade
    
    @property
    def sunk(self):
        return self.__shipsSunk

SHIPS = [Ship("Carrier", length = 5, width = 1),
Ship("Battleship", length = 4, width = 1),
Ship("Crusier", length = 3, width = 1),
Ship("Submarine", length = 3, width = 1),
Ship("Destroyer", length = 2, width = 1)]