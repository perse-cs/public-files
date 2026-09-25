# Example F: Connect Four

A colourful two-player game with three computer opponents, an undo stack and
**real SQLite saves**. Get four counters in a horizontal, vertical or diagonal
line. Red starts; the computer plays Gold.

## Playing

Press **Run**. Choose Two players, Practice AI, Easy AI or Medium AI, then choose
**New game** to apply it. Click a column number or anywhere in that column to
drop a counter. A full column is rejected. Winning counters get white outlines.

- **Undo turn** takes back your move and the computer's reply (one move in Two players mode). It also works while the computer is waiting to move.
- **Save** replaces the single saved-game slot; **Load** restores it.
- Completed games add an anonymous Red, Gold or Draw result. Undoing a finished game leaves that result in history and does not record a second result for it.

## A database that really persists

The first run creates `connect_four_demo.db` from an empty schema. There is no
downloaded student database and no login. `saved_game` stores a sequence of
column numbers and an opponent choice; `results` stores a colour, move count
and numeric ID. The totals use `GROUP BY` and `COUNT(*)`.

Try playing three turns, choosing Save, closing the tkinter window or pressing
**Stop**, then pressing Run and Load. Your counters return. Closing or stopping
lets PythonCoder copy the binary database from Pyodide to its virtual filesystem.
The database appears in Files and can be downloaded. Avoid reloading the web
page while a program is running: its latest changes may not yet be synced.

SQLite connections commit and close after each operation. `?` placeholders keep
values separate from SQL. This is a local demonstration, not a shared online
leaderboard. PythonCoder's Pyodide package loader supplies `sqlite3`.

## Read the code

| File | What to investigate |
| --- | --- |
| `connect_engine.py` | The board, four-in-a-row detection, `MoveStack`, play and undo |
| `connect_ai.py` | Random play, heuristic evaluation and recursive minimax |
| `connect_store.py` | Fresh schema creation, parameterised SQL, aggregation and connection lifetime |
| `main.py` | Canvas drawing, callbacks, turn scheduling and winning highlights |

Medium AI explores replies recursively and prefers a central column when moves
tie. Its minimax is **not alpha–beta pruning**: compare the work it performs with
the pruned searches elsewhere in this book. Each branch uses a copied board so
that investigating one move cannot change another branch.

## Adaptation notes

The board, stack and AI come from the earlier Connect Four coursework project.
The desktop/network interface was replaced with this smaller tkinter adapter;
network play, account screens and original data are omitted. SQLite persistence
is new demo code. The stack's empty operation now resets its pointer, invalid
column numbers are checked, and an AI tie-handling index is corrected. The very
expensive Hard AI is retained for reading but is not offered in the browser menu.
No student names, account records or original settings are included.

**Try extending it:** add a second named save slot using generic slot numbers,
or count visited minimax nodes and display the search cost.
