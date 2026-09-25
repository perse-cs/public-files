"""Browser adaptation of the coursework's BFS and A* searches.

Retains the wall-map, predecessor dictionaries, g/f scores and Manhattan
heuristic. Iteration replaces recursion and a blocking empty priority queue.
Each search returns its exploration order for an after() animation.
"""
from collections import deque
from heapq import heappush, heappop


class Solver:
    def __init__(self, maze):
        self.maze = maze
        self.start = tuple(maze.getStartPos)
        self.end = tuple(maze.getEndPos)

    def neighbours(self, cell):
        x, y = cell
        for direction, dx, dy in [("N", 0, -1), ("E", 1, 0), ("S", 0, 1), ("W", -1, 0)]:
            child = x+dx, y+dy
            if child in self.maze.getMazeMap and self.maze.getMazeMap[cell][direction] == 0:
                yield child

    def path(self, parents):
        if self.end not in parents:
            return []
        result = [self.end]
        while result[-1] != self.start:
            result.append(parents[result[-1]])
        return result[::-1]


class BFS(Solver):
    def run(self):
        frontier = deque([self.start])
        parents = {self.start: None}
        explored = []
        while frontier:
            current = frontier.popleft()
            explored.append(current)
            if current == self.end:
                break
            for child in self.neighbours(current):
                if child not in parents:
                    parents[child] = current
                    frontier.append(child)
        return explored, self.path(parents)


class AStar(Solver):
    def heuristic(self, cell):
        return abs(cell[0]-self.end[0])+abs(cell[1]-self.end[1])

    def run(self):
        frontier = [(self.heuristic(self.start), self.heuristic(self.start), self.start)]
        parents = {self.start: None}
        g_score = {self.start: 0}
        closed, explored = set(), []
        while frontier:
            _, _, current = heappop(frontier)
            if current in closed:
                continue
            closed.add(current)
            explored.append(current)
            if current == self.end:
                break
            for child in self.neighbours(current):
                cost = g_score[current]+1
                if cost < g_score.get(child, float("inf")):
                    parents[child] = current
                    g_score[child] = cost
                    h = self.heuristic(child)
                    heappush(frontier, (cost+h, h, child))
        return explored, self.path(parents)
