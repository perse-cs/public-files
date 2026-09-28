# Example G: Battleships

Deploy five ships, then hunt a hidden enemy fleet. The computer does more than
guess: it enumerates possible ship placements to build a **probability map**,
then follows up promising hits.

## Playing

Press **Run**. The left grid is your fleet; the right grid is the enemy sea.

1. Click the left grid to place the next ship, starting at that square. **Rotate** switches horizontal/vertical placement. Overlaps and off-board positions are rejected. **Random fleet** starts a fresh game with your ships already placed.
2. Choose **Battle!** once all five ships are placed.
3. Click a square in the enemy sea to fire. The computer replies automatically. Orange crosses show hits and pale dots show misses; repeat shots are rejected.
4. Sink all five enemy ships to win. The counters below the grids track shots, hits and sunken ships. **New game** starts over.

Each side has ships of lengths 5, 4, 3, 3 and 2. Ships can touch, so a hit does
not necessarily tell you which nearby squares belong to the same ship.

## Read the code

| File | What it does |
| --- | --- |
| `fleet_engine.py` | `Game`, `Player`, `AI`, `Ship`, `ShipPart`, `Array2d`, statistics and placement rules |
| `fleet_errors.py` | Distinct exceptions for invalid placement and repeated shots |
| `main.py` | Two Canvas grids, deployment, firing callbacks and delayed computer turns |

Look at `generateProbabilityMap`, `__huntHit` and `coveredSquares`: the AI tries
each surviving ship in each orientation and scores squares covered by plausible
placements. It records its own shots and known hits rather than reading your
hidden ship positions to choose a target. Composition is central: ships contain
parts, players contain fleets and statistics, and the game owns four boards.

## Adaptation notes

This keeps the original Battleships game and probability AI with a new compact
tkinter interface. Full-screen menus, audio playback, accounts, fleet editors,
pickled saves and database access are omitted. The original GUI required a
desktop audio library and disk paths. No original database, audio or saved fleet
file is copied. Fresh ship objects are created on every restart, and verbose
terminal diagnostics that revealed hidden ship locations are suppressed.

**Try extending it:** show a heat map of the AI's current estimates, or compare
its hit rate with a random opponent over many games.
