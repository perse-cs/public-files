# Anonymised coursework engine; browser changes are documented in guide.md.
from boxes_engine import Game
import random
# add return moves to board class
class Chain:
    """A connected component of boxes with exactly two free sides."""
    def __init__(self, references):
        self.references = references

    def getLength(self):
        return len(self.references)


def createChains(game):
    # Repair of the original recursive chain traversal: follow only open
    # shared edges, stop at junctions, and visit each box at most once.
    visited, chains = set(), []

    def free_sides(cell):
        return [d for d in ("N", "S", "E", "W") if game.checkClear(cell, d)]

    def visit(cell, refs):
        if cell in visited or len(free_sides(cell)) != 2:
            return
        visited.add(cell)
        refs.append(cell)
        for direction in free_sides(cell):
            neighbour = game.MatchedPlace(cell, direction)
            if neighbour is not None:
                visit(neighbour[:2], refs)

    for row in range(game.getHeight()):
        for col in range(game.getWidth()):
            refs = []
            visit((row, col), refs)
            if refs:
                chains.append(Chain(refs))
    return chains


def MoveDif(game):
    # Keep the student's capture/safe/chain strategy, with a total ordering
    # instead of branches that could leave the chosen move undefined.
    chains = createChains(game)
    lengths = {cell: chain.getLength() for chain in chains for cell in chain.references}

    def rank(move):
        row, col, direction = move
        sides = [(row, col, direction)]
        neighbour = game.MatchedPlace((row, col), direction)
        if neighbour is not None:
            sides.append(neighbour)
        levels = [optLevel(side, game) for side in sides]
        captures = levels.count(3)
        if captures:
            return (0, -captures)
        if max(levels) < 2:
            return (1, max(levels))
        return (2, sum(lengths.get(side[:2], 1) for side in sides))

    moves = game.ReturnAvailable()
    best = min(map(rank, moves))
    return random.choice([move for move in moves if rank(move) == best])


def MoveMed(Game: Game):
    opts = Game.ReturnAvailable()
    length = len(opts)
    o = [[] for _ in range(4)]
    for i in range(length):
        test = opts[i]
        matchedTest = Game.MatchedPlace((test[0], test[1]), test[2])
        level_t1 = optLevel(test, Game)
        if matchedTest != None:
            level_t2 = optLevel(matchedTest, Game)
        else:
            level_t2 = 0
        if level_t1 >= level_t2:
            o[level_t1].append(test)
        else:
            o[level_t2].append(test)
    
    if len(o[3]) > 0:
        choice = random.randint(0, len(o[3]) - 1)
        move = o[3][choice]
        return move
    elif len(o[1]) > 0 and len(o[0]) > 0:
        superchoice = random.randint(0, 1)
        choice = random.randint(0, len(o[superchoice]) - 1)
        move = o[superchoice][choice]
        return move
    elif len(o[1]) > 0:
        choice = random.randint(0, len(o[1]) - 1)
        move = o[1][choice]
        return move
    elif len(o[0]) > 0:
        choice = random.randint(0, len(o[0]) - 1)
        move = o[0][choice]
        return move
    else:
        choice = random.randint(0, len(o[2]) - 1)
        move = o[2][choice]
        return move

def MoveEasy(Game: Game):
    opts = Game.ReturnAvailable()
    length = len(opts)
    o = [[] for _ in range(4)]
    for i in range(length):
        test = opts[i]
        matchedTest = Game.MatchedPlace((test[0], test[1]), test[2])
        level_t1 = optLevel(test, Game)
        if matchedTest != None:
            level_t2 = optLevel(matchedTest, Game)
        else:
            level_t2 = 0
        if level_t1 >= level_t2:
            o[level_t1].append(test)
        else:
            o[level_t2].append(test)
    
    if len(o[3]) > 0:
        choice = random.randint(0, len(o[3]) - 1)
        move = o[3][choice]
        return move
    elif len(o[2]) > 0:
        choice = random.randint(0, len(o[2]) - 1)
        move = o[2][choice]
        return move
    elif len(o[1]) > 0:
        choice = random.randint(0, len(o[1]) - 1)
        move = o[1][choice]
        return move
    else:
        choice = random.randint(0, len(o[0]) - 1)
        move = o[0][choice]
        return move


def MoveRan(Game: Game):
    opts = Game.ReturnAvailable()
    length = len(opts)
    choice = random.randint(0, length-1)
    move = opts[choice]
    return move

def optLevel(opt: tuple, Game: Game):
    dirs = ["N", "S", "E", "W"]
    dirs.remove(opt[2])
    count = 0
    for i in range(3):
        if not Game.checkClear((opt[0], opt[1]), dirs[i]):
            count += 1
    return count


def Move(Difficulty: int, Game: Game):
    if Difficulty == 0:
        return MoveRan(Game)
    elif Difficulty == 1:
        return MoveEasy(Game)
    elif Difficulty == 2:
        return MoveMed(Game)
    elif Difficulty == 3:
        return MoveDif(Game)