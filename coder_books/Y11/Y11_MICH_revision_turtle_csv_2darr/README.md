# GCSE Revision: Turtle, CSV files and 2D arrays

A learning book of 12 auto-marked exercises (four per topic, trivial → hard) followed by
12 runnable model solutions. Every program follows the Edexcel GCSE template
(`# LIBRARIES`, `# CONSTANTS`, `# GLOBAL VARIABLES`, `# SUBPROGRAMS`, `# MAIN`) with
UPPERCASE constants, camelCase names and all variables initialised (globals at global
level, locals at the start of their subprogram; loop counters are initialised by their
`for`).

Open it with `?book=<url of this folder's book.json>` — once pushed, that is
`https://raw.githubusercontent.com/bakerpdgit/pythoncoder/HEAD/example%20books/gcse_revision_turtle_csv_2d/book.json`.

## Layout

```
book.json            root: Start here · Exercises · Model solutions
start_here.md/.py    the template and conventions (example)
*.csv                data files, shared by exercises and solutions (found by walking up the tree)
exercises/           12 activities with tests; t1_check.py / t2_check.py are hidden
                     reference drawings for the exact-match turtle tests
solutions/           the same 12 tasks as isExample activities with the model code
```

## The exercises

| Topic | Level | Task | Style | How it is marked |
|---|---|---|---|---|
| Turtle | Trivial | Fix the hexagon | 5 errors (4 syntax/runtime, 1 logic) | exact drawing match (`t` + solution file) |
| Turtle | Simple | A row of squares | complete numbered lines | exact drawing match for 5, 2, 1 squares |
| Turtle | Medium | Archery target | task only; validation loop | messages + SVG patterns (fill colours, sizes, largest first) |
| Turtle | Hard | Bar chart of scores | 4 required subprograms | messages, SVG patterns, `s+` unit tests on `chooseColour`/`calculateHeight` |
| CSV | Trivial | Big cities | 6 blanks | output for 3 thresholds |
| CSV | Simple | Club members by year | complete numbered lines | output for 3 years (incl. none) |
| CSV | Medium | Exam results report | task only; skip header, write CSV | message + `f+` exact `report.csv` for 2 pass marks (boundary case) |
| CSV | Hard | Validating orders | 3 required subprograms | messages, `f+` exact `valid_orders.csv`, `s+` unit tests incl. edge cases |
| 2D arrays | Trivial | Unscramble the totals | reorder lines, indentation already correct | exact table |
| 2D arrays | Simple | Cinema seat booking | complete numbered lines | exact plan for 3 bookings (incl. taken seat) |
| 2D arrays | Medium | Sales table | task only; row/column totals, `format` widths | exact table + top seller for 3 inputs |
| 2D arrays | Hard | Minesweeper | 4 required subprograms | messages, grid, `s+` unit tests on other grids |

Turtle medium/hard use SVG pattern tests rather than an exact match, so equivalent
drawing code (e.g. `goto` instead of `forward`/`left`) still passes; trivial/simple
constrain the drawing commands, so they use the exact match and get a turtle preview.

## Checking changes

Every model solution passes all its tests, every starter file fails them, and a set of
alternative-correct and deliberately wrong variants were checked in both directions.
If you edit a test or solution, keep `exercises/t1_check.py` and `exercises/t2_check.py`
identical to `solutions/t1_hexagon.py` and `solutions/t2_squares.py`.
