# A Level Computer Science coursework

Every A Level Computer Science student writes a substantial program of their own design for the Non-Exam Assessment (NEA). They choose the problem, research it, design a solution, build it, test it and write it up. It is worth 20% of the A Level.

The examples in this book are real projects written by recent students. They have been adapted so that they run here, in the browser, with nothing to install. The five new graphical examples (F–J) retain student game or puzzle engines with adapted tkinter interfaces and documented algorithm repairs. Their guides distinguish original techniques from demo changes. 

## What to look for

The mark scheme rewards **technical skill**. The hardest techniques are listed as "Group A" skills, and students often label them in their code with comments like this:

```python
###########################
# GROUP A: Tree Traversal #
###########################
```

Look out for:

- **Object-oriented programming** — classes, inheritance and composition
- **Complex algorithms** — searching game trees, finding shortest paths, parsing expressions
- **Data structures** — stacks, queues, trees and graphs, often written from scratch
- **Files and databases** — saving games, high scores and user accounts

## How to use this book

Open an example from the contents, read its page, then press **Run**. Pygame examples take over the display pane — click inside it before using the keyboard, and press **Stop** to finish.

Every file needed by each demo is in the file browser, so you can open any of them and read the code while it runs.

Press **Run** now on this page for a quick list of what is inside.

## Five more graphical projects

| Example | Try it for | Techniques to investigate |
| --- | --- | --- |
| F: Connect Four | A computer opponent, undo and saved games | Minimax, heuristic evaluation, stacks, SQLite |
| G: Battleships | Place a fleet and hunt hidden ships | Object composition, probability maps, state transitions |
| H: Maze Explorer | Watch BFS and A* explore; navigate with arrow keys | Graphs, backtracking, queues, priority queues |
| I: Dots and Boxes | Capture colourful boxes and trigger chains | Shared-edge modelling, recursive traversal, strategy |
| J: Killer Sudoku | Colour-coded sum cages and a working solver | Constraint checking, NumPy, backtracking |

These examples open a **tkinter window in Display**. Press **Run**, then use its
buttons and board. Enlarge Display or collapse the Guide if you need more room.
Use **Stop** or the window's close button before switching projects.

Connect Four creates a fresh `connect_four_demo.db` using Python's `sqlite3`.
It stores one saved board and anonymous Red/Gold/Draw results. Killer Sudoku can
save to `killer_demo_save.json`. Close the window or press Stop to copy changed
files back to PythonCoder's Files panel; then they can be reused on the next run.
Download files you want to keep independently of this browser. None of the five
new examples ships an original account database, password, score history or
personal settings file.
