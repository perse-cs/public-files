# Example I: Dots and Boxes

A small board with a surprisingly strategic endgame. Blue and Coral take turns
drawing edges. Complete the fourth side of a box to claim it and take another
turn. One poorly chosen edge can give away a whole chain of boxes.

## Playing

Press **Run**. Click between two neighbouring dots to draw an unclaimed edge.
Claimed boxes fill with the owner's colour and show B or C. Most boxes wins.

- Choose **Two players**, **Tactical AI** or **Chain AI**, then **New game**. You play Blue; the computer plays Coral.
- **Hint** highlights a suggested edge in white without playing it.
- **Undo turn** restores the board before your last click, including any chain the computer claimed afterwards. In Two players mode it undoes one move.

The computer pauses briefly between moves so that a chain of captures can be
watched. Restarting or undoing cancels its pending move.

## Read the code

| File | What it does |
| --- | --- |
| `boxes_engine.py` | Board/player objects, shared edges, capture rules and scoring |
| `boxes_ai.py` | Edge classification, recursive chain detection and move choice |
| `main.py` | Edge hit-testing, coloured ownership, undo snapshots and turn scheduling |

A shared edge appears in two neighbouring boxes. `MatchedPlace` maps one side
to its equivalent in the neighbour; `place` can therefore complete **two boxes
in one move**. `ReturnAvailable` avoids counting the shared edge twice.

Tactical AI takes captures and otherwise favours safe edges. Chain AI groups
two-free-sided boxes into connected components using recursion. When forced to
open a chain, it prefers a smaller one. This is a heuristic, not a proof of
optimal play or a complete double-cross strategy.

## Adaptation notes

The board, player and game objects and the random/easy/tactical move classifiers
come from the original Dots and Boxes coursework. The Canvas interface and undo
snapshots are adapted for the browser. Partial-board scoring now skips unclaimed
boxes, and repeated edges cannot award points twice. The original difficult AI
had incomplete branches, a malformed direction tuple and unsafe chain traversal;
its chain strategy has been repaired with a bounded visited-set traversal and a
move ranking that always returns a legal choice. Accounts and original account
files are omitted; no personal data or assets are copied.

**Try extending it:** display chain lengths, or improve the AI's strategy for
sacrificing two boxes to keep control of the endgame.
