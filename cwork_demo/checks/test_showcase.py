"""Run with: python -B past_projects/cwork_demo/checks/test_showcase.py

Requires NumPy. Imports only the anonymised book, never the original archive.
Runtime files are written in temporary directories, never into shipped examples.
"""
import ast
from contextlib import closing
import json
import os
from pathlib import Path
import random
import sqlite3
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
BOOK = Path(__file__).resolve().parents[1]
for letter in "fghij":
    sys.path.insert(0, str(BOOK / f"example_{letter}"))

from connect_engine import game, gameError, MoveStack, StackEmptyError
from connect_ai import Ai
import connect_store
from fleet_engine import Game as Fleet, Ship, horizontal, vertical
from fleet_errors import ShotError, ShipPlacementError
from maze_model import MazeGen
from maze_generators import RBT, BinaryTree
from maze_search import BFS, AStar
from boxes_engine import Game as Boxes
from boxes_ai import Move
from sudoku_engine import Game as Sudoku


class ShowcaseChecks(unittest.TestCase):
    def test_manifests_are_self_contained(self):
        ids = set()

        def visit(path):
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data["children"]:
                self.assertNotIn(item["id"], ids)
                ids.add(item["id"])
                if "bookLink" in item:
                    visit((path.parent / item["bookLink"]).resolve())
                else:
                    for key in ("py", "guide"):
                        self.assertTrue((path.parent / item[key]).is_file())
                    for extra in item.get("additionalFiles", []):
                        self.assertTrue((path.parent / extra["filename"]).is_file())

        visit(BOOK / "book.json")
        for letter in "fghij":
            folder = BOOK / f"example_{letter}"
            item = json.loads((folder / "book.json").read_text())["children"][0]
            shipped = {"book.json", "guide.md", "main.py"} | {f["filename"] for f in item["additionalFiles"]}
            self.assertEqual(shipped, {p.name for p in folder.iterdir() if p.is_file()})
            self.assertFalse(any(p.suffix in (".db", ".sqlite", ".pyc", ".pickle", ".save") for p in folder.rglob("*")))
            for source in folder.glob("*.py"):
                ast.parse(source.read_text(encoding="utf-8"), filename=source.name)

    def test_connect_four_wins_undo_and_validation(self):
        for moves in ([1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 3, 3, 4],
                      [1, 2, 2, 3, 4, 3, 3, 4, 5, 4, 4]):
            board = game()
            for col in moves:
                board.play(col)
            self.assertEqual(board.getWinner, game.PONE)
            self.assertEqual(len(board.getRun[1]), 4)
            saved = board.getMoves
            restored = game()
            restored.load(saved)
            self.assertEqual(restored.Board, board.Board)
            restored.undo()
            self.assertIsNone(restored.getWinner)
        board = game()
        for _ in range(6):
            board.play(1)
        with self.assertRaises(gameError):
            board.play(1)
        for col in (0, 8, -1):
            with self.assertRaises(gameError):
                board.play(col)
        stack = MoveStack()
        stack.push((1, 2))
        stack.empty()
        with self.assertRaises(StackEmptyError):
            stack.pop()
        stack.push((3, 4))
        self.assertEqual(stack.peek(), (3, 4))

    def test_minimax_wins_blocks_and_does_not_mutate_board(self):
        for moves, expected in [([1, 2, 1, 2, 3, 2, 3], 1), ([1, 2, 1, 2, 1], 0)]:
            board = game()
            for col in moves:
                board.play(col)
            before = [row[:] for row in board.Board]
            self.assertEqual(Ai("Medium AI").getColumn(board.Board, game.PTWO), expected)
            self.assertEqual(board.Board, before)

    def test_sqlite_has_only_fresh_anonymous_data_and_reopens(self):
        with tempfile.TemporaryDirectory() as temp:
            old_path = connect_store.DATABASE
            connect_store.DATABASE = str(Path(temp) / "demo.db")
            try:
                self.assertEqual(connect_store.totals(), {})
                self.assertIsNone(connect_store.load())
                connect_store.save("0123", "Two players")
                self.assertEqual(connect_store.load(), ("0123", "Two players"))
                connect_store.record("Red", 7)
                self.assertEqual(connect_store.totals(), {"Red": 1})
                with closing(sqlite3.connect(connect_store.DATABASE)) as db:
                    self.assertEqual(db.execute("PRAGMA integrity_check").fetchone(), ("ok",))
                    self.assertEqual({row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}, {"saved_game", "results"})
                self.assertEqual(Path(connect_store.DATABASE).read_bytes()[:16], b"SQLite format 3\x00")
            finally:
                connect_store.DATABASE = old_path

    @staticmethod
    def fleet():
        return [Ship(str(i), length=n, width=1) for i, n in enumerate((5, 4, 3, 3, 2))]

    def test_fleet_placement_and_repeat_shots(self):
        g = Fleet("Blue", "Gold", self.fleet(), self.fleet())
        ship = g.player1.ships[0]
        with self.assertRaises(ShipPlacementError):
            g.placeShip(g.player1, ship, 7, 7, horizontal)
        g.placeShip(g.player1, ship, 0, 0, horizontal)
        self.assertFalse(g.IsValidPlacement(g.player1, g.player1.ships[1], 0, 0, vertical))
        g.fire(0, 0)
        with self.assertRaises(ShotError):
            g.fire(0, 0)

    def test_probability_ai_finishes_games_without_repeat_shots(self):
        for seed in range(20):
            random.seed(seed)
            g = Fleet("Blue", "Gold", self.fleet(), self.fleet(), 1, 1)
            g.player1.placeShips()
            g.player2.placeShips()
            for _ in range(128):
                g.currentPlayerTurn.takeShot()
                if g.winner:
                    break
                g.changeTurn()
            self.assertIsNotNone(g.winner)
            self.assertEqual(g.winner.stats.sunk, 5)

    def test_maze_connectivity_reciprocal_walls_and_shortest_paths(self):
        opposite = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
        for seed in range(20):
            random.seed(seed)
            for generator in (RBT, BinaryTree):
                maze = MazeGen()
                gen = generator(maze)
                gen.run("NW") if generator is BinaryTree else gen.run()
                solver = BFS(maze)
                seen = {tuple(maze.getStartPos)}
                pending = list(seen)
                for cell in pending:
                    for child in solver.neighbours(cell):
                        if child not in seen:
                            seen.add(child)
                            pending.append(child)
                self.assertEqual(len(seen), 225)
                for (x, y), walls in maze.getMazeMap.items():
                    for direction, (dx, dy, reverse) in opposite.items():
                        if (x+dx, y+dy) in maze.getMazeMap:
                            self.assertEqual(walls[direction], maze.getMazeMap[x+dx, y+dy][reverse])
                _, bfs = solver.run()
                _, astar = AStar(maze).run()
                self.assertEqual(len(bfs), len(astar))
                self.assertEqual(bfs[0], tuple(maze.getStartPos))
                self.assertEqual(bfs[-1], tuple(maze.getEndPos))
                for a, b in zip(astar, astar[1:]):
                    self.assertIn(b, list(solver.neighbours(a)))

    def test_search_handles_no_route(self):
        maze = MazeGen(3, 3)
        for solver in (BFS, AStar):
            self.assertEqual(solver(maze).run()[1], [])

    def test_boxes_double_capture_and_no_duplicate_points(self):
        g = Boxes((1, 2), 2, ["Blue", "Coral"], ["P", "P"])
        for move in [(0, 0, "N"), (0, 0, "S"), (0, 0, "W"),
                     (0, 1, "N"), (0, 1, "S"), (0, 1, "E")]:
            self.assertFalse(g.place(move[:2], move[2]))
        self.assertEqual(g.CalculateScores(), [0, 0])
        self.assertTrue(g.place((0, 0), "E"))
        self.assertEqual(g.CalculateScores(), [2, 0])
        self.assertFalse(g.place((0, 0), "E"))
        self.assertEqual(g.CalculateScores(), [2, 0])

    def test_boxes_ai_finishes_and_conserves_boxes(self):
        for seed in range(40):
            random.seed(seed)
            g = Boxes((4, 4), 2, ["Blue", "Coral"], ["P", "P"])
            for turn in range(40):
                move = Move(2 if turn % 2 else 3, g)
                self.assertIn(move, g.ReturnAvailable())
                if not g.place(move[:2], move[2]):
                    g.nextTurn()
                self.assertEqual(len(g.ReturnAvailable()), 39-turn)
            self.assertTrue(g.End())
            self.assertEqual(sum(g.CalculateScores()), 16)

    def test_sudoku_generation_constraints_solve_and_save(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as temp:
            try:
                os.chdir(temp)
                Path("cage_shapes.json").write_bytes((BOOK / "example_j/cage_shapes.json").read_bytes())
                for seed in range(5):
                    random.seed(seed)
                    g = Sudoku()
                    g.newGame(2, 1)
                    self.assertEqual(len(g.getCagesDict()), 81)
                    cells = [tuple(cell) for cage in g.getCages() for cell in cage.cells]
                    self.assertEqual(len(cells), len(set(cells)))
                    self.assertGreaterEqual(len(g.fixedCells()), 36)
                    self.assertLess(len(g.fixedCells()), 81)
                    self.assertEqual(g.getErrorCells(), set())
                    g.saveGame("test.json")
                    loaded = Sudoku()
                    loaded.loadGame("test.json")
                    self.assertEqual(loaded.getGrid(), g.getGrid())
                    g.solve()
                    self.assertTrue(g.checkComplete())
                    for cage in g.getCages():
                        values = [g.getCell(x, y) for x, y in cage.cells]
                        self.assertEqual(sum(values), cage.sum)
                        self.assertEqual(len(set(values)), len(values))
                    loaded.solve()
                    self.assertEqual(loaded.getGrid(), g.getGrid())
                    g.updateCell(0, 0, g.getCell(1, 0))
                    self.assertFalse(g.checkComplete())
                    self.assertTrue(g.getErrorCells())
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main(verbosity=2)
