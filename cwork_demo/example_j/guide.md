# Example J: Killer Sudoku

Sudoku with an extra layer of arithmetic: cells are grouped into coloured,
outlined **cages**. Each cage must add up to its small printed total and cannot
repeat a digit. Rows, columns and 3 × 3 boxes each contain 1–9 once.

## Playing

Press **Run** and allow a moment for NumPy and the puzzle generator to load.
Click a blank square, then type 1–9 or use the number buttons. Bold dark digits
are fixed clues; your entries are blue. Erase, Backspace or Delete clears your
selected editable cell. Cage boundaries are dashed: colour alone does not
identify a cage, because colours are reused.

- **Check** highlights conflicting cells; no conflicts does not mean an unfinished puzzle is solved.
- **Undo** reverses the last edit, including a Solve operation.
- **Solve** solves from the original clues, discarding incorrect trial entries.
- **Save / Load** use `killer_demo_save.json` in the virtual filesystem.
- **New puzzle** creates a new puzzle; it does not overwrite your saved one.

Close the tkinter window or press Stop before rerunning or reloading the web
page, so PythonCoder can sync saved files. None of the original player's saved
games or settings is included.

## Read the code

| File | What it does |
| --- | --- |
| `sudoku_engine.py` | Board state, fixed clues, errors, pencil-mark support, saving and loading |
| `sudoku_generator.py` | Cage construction, shape matching, uniqueness tests and recursive solvers |
| `cage_shapes.json` | Numeric shape offsets and candidate sums; no player information |
| `main.py` | Coloured Canvas, selection, input, undo and rule checking |

The generator builds a valid grid, groups cells into cages, then removes clues
while checking that exactly one solution remains. The browser version retains
at least 36 clues and tries each removal once to bound the work. Look for the
NumPy row/column operations and the recursive solution counter.

The repaired killer solver chooses the empty cell with the fewest legal values
first: the **minimum remaining values** heuristic. Every trial must satisfy row,
column, box and cage constraints; failed trials are undone during backtracking.

## Adaptation notes

The game model, NumPy-based generator, cage representation, shape matching and
JSON format come from the original Killer Sudoku coursework. A compact tkinter
interface replaces desktop audio, image resources, settings and file dialogs.
Only numeric cage configuration is carried over; accounts, databases and saved
games are omitted. Paths are relative to the virtual working directory.

Several correctness repairs were needed: cage checks now use the current trial
grid and candidate digit; complete cages must have exactly their target sum;
completed rows must contain precisely 1–9; and solving reports an impossible
puzzle instead of looping forever. The killer solver now backtracks with cage
constraints rather than repeatedly trying a plain Sudoku solution. The source
still includes pencil-mark support, but this compact interface uses pen entries.

**Try extending it:** add a pencil-mode button, or explain which constraint
removed each candidate from the most constrained cell.
