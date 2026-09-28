"""Demo-only SQLite persistence. No names, logins or imported database data."""
import sqlite3
from contextlib import closing

DATABASE = "connect_four_demo.db"


def connect():
    db = sqlite3.connect(DATABASE)
    db.execute("CREATE TABLE IF NOT EXISTS saved_game (slot INTEGER PRIMARY KEY, moves TEXT NOT NULL, opponent TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, winner TEXT NOT NULL, moves INTEGER NOT NULL)")
    db.commit()
    return db


def save(moves, opponent):
    with closing(connect()) as db, db:
        db.execute("INSERT OR REPLACE INTO saved_game VALUES (1, ?, ?)", (moves, opponent))


def load():
    with closing(connect()) as db:
        return db.execute("SELECT moves, opponent FROM saved_game WHERE slot = 1").fetchone()


def record(winner, moves):
    with closing(connect()) as db, db:
        db.execute("INSERT INTO results (winner, moves) VALUES (?, ?)", (winner, moves))


def totals():
    with closing(connect()) as db:
        return dict(db.execute("SELECT winner, COUNT(*) FROM results GROUP BY winner"))
