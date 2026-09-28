# Example H: Maze Explorer

Generate a maze, find the exit yourself, or watch **breadth-first search** and
**A\*** explore the same graph. Blue cells show the recorded exploration order;
gold cells show the shortest route.

## Exploring

Press **Run**. Choose Backtracker or Binary tree, then **New maze**. The maze has
15 × 15 cells, an S entrance and an E exit. Click inside the maze and use the
arrow keys to move the white marker through open passages. Walls block movement.

- **BFS** animates a breadth-first search.
- **A\*** animates a search guided by Manhattan distance to the exit.
- **Clear trail** removes the search colouring and returns you to S without changing the maze. New maze makes a different one.

Compare the reported exploration counts and route lengths. Both searches find a
shortest path; A* is not guaranteed to explore fewer cells on every maze. Search
is computed first, then replayed in small batches using `after()` so the display
stays responsive. A new search, Clear trail or New maze cancels the old animation.

## Read the code

| File | What it does |
| --- | --- |
| `maze_model.py` | A dictionary of cells, each with N/E/S/W walls and a cell type |
| `maze_generators.py` | Shared wall operations, stack backtracking and binary-tree generation |
| `maze_search.py` | BFS queue, A* priority queue, predecessor maps and path reconstruction |
| `main.py` | Canvas walls, search animation, keyboard navigation and statistics |

Removing an east wall must also remove the next cell's west wall. Follow these
paired updates in `Generator`. The backtracker carves into unvisited neighbours
and retreats on a stack at dead ends. Binary tree instead chooses north or west
passages, creating a noticeably different texture. Despite its name, it is not
the binary-search algorithm.

## Adaptation notes

The original maze project combined tkinter menus with a large pygame display.
This port retains its cell model, wall operations and binary-tree generator,
adapts its backtracker to an explicit stack, and presents everything in tkinter.
The BFS and A* implementations are repaired iterative adaptations of its search
designs: the original BFS called a missing method, and recursive searches or an
empty blocking queue could fail or hang. The demo preserves predecessor maps,
path reconstruction and Manhattan scoring while handling exhausted frontiers.
Only these two generators and two solvers are exposed. Login screens and all
original database data are omitted.

**Try extending it:** add some loops by removing extra reciprocal walls, then
compare shortest paths with a depth-first search, which need not be shortest.
