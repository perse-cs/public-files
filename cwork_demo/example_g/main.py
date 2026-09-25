import tkinter as tk
import random
from fleet_engine import Game, Ship, ShipPart, horizontal, vertical
from fleet_errors import ShotError, ShipPlacementError

BG, SEA, INK = "#0c2336", "#123d55", "#e2f4fa"
CELL, TOP = 29, 40


def fleet():
    # Fresh objects each game: Ship holds its remaining hits.
    return [Ship(name, length=size, width=1) for name, size in
            [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]]


class Battleships:
    def __init__(self, root):
        self.root = root
        root.title("Battleships | fleet command")
        root.configure(bg=BG)
        tk.Label(root, text="FLEET COMMAND", bg=BG, fg="#58d3cf", font=("Arial", 20, "bold")).pack(pady=8)
        bar = tk.Frame(root, bg=BG)
        bar.pack()
        for text, action in [("New game", self.new), ("Random fleet", self.random_fleet),
                             ("Rotate", self.rotate), ("Battle!", self.start)]:
            tk.Button(bar, text=text, command=action).pack(side="left", padx=4)
        self.canvas = tk.Canvas(root, width=550, height=300, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=6, pady=8)
        self.canvas.bind("<Button-1>", self.click)
        self.status = tk.Label(root, bg=BG, fg=INK, font=("Arial", 11), wraplength=540)
        self.status.pack(pady=5)
        self.stats = tk.Label(root, bg=BG, fg="#8fd9df", font=("Arial", 11))
        self.stats.pack(pady=5)
        tk.Label(root, text="YOUR FLEET: click to place  |  ENEMY SEA: click to fire\nOrange X = hit · pale dot = miss · sink all five ships to win",
                 bg=BG, fg=INK, font=("Arial", 10)).pack(pady=8)
        self.timer = None
        self.new()

    def new(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.game = Game("Player", "Computer", fleet(), fleet(), player2AI=1)
        self.orientation = horizontal
        self.active = False
        self.finished = False
        self.game.player2.placeShips()
        self.draw()
        self.placement_status()

    def placement_status(self):
        ships = self.game.player1.shipsLeftToPlace
        if ships:
            direction = "horizontal" if self.orientation == horizontal else "vertical"
            self.status.config(text=f"Place {ships[0].name} ({ships[0].length} squares), {direction}. Or choose Random fleet.")
        else:
            self.status.config(text="Fleet ready. Choose Battle! to launch.")

    def rotate(self):
        if not self.active and not self.finished:
            self.orientation = vertical if self.orientation == horizontal else horizontal
            self.placement_status()

    def random_fleet(self):
        self.new()
        for ship in list(self.game.player1.shipsLeftToPlace):
            options = [(r, c, o) for r in range(8) for c in range(8) for o in (horizontal, vertical)
                       if self.game.IsValidPlacement(self.game.player1, ship, r, c, o)]
            r, c, o = random.choice(options)
            self.game.placeShip(self.game.player1, ship, c, r, o)
        self.draw()
        self.placement_status()

    def start(self):
        if self.finished or self.active:
            return
        if self.game.player1.shipsLeftToPlace:
            self.status.config(text="Place all five ships first, or choose Random fleet.")
            return
        self.active = True
        self.status.config(text="Your turn. Choose a square in the enemy sea.")

    def click(self, event):
        row = (event.y-TOP)//CELL
        if not 0 <= row < 8 or self.finished or self.timer is not None:
            return
        if not self.active:
            col = (event.x-30)//CELL
            remaining = self.game.player1.shipsLeftToPlace
            if 0 <= col < 8 and remaining:
                try:
                    self.game.placeShip(self.game.player1, remaining[0], col, row, self.orientation)
                    self.draw()
                    self.placement_status()
                except ShipPlacementError:
                    self.status.config(text="That ship overlaps or runs off the grid. Rotate or try another square.")
            return
        col = (event.x-310)//CELL
        if not 0 <= col < 8:
            return
        try:
            hit = self.game.fire(col, row)
        except ShotError:
            self.status.config(text="You already fired there. Choose another square.")
            return
        self.draw()
        if self.finish():
            return
        message = "Sunk "+hit.name+"!" if isinstance(hit, Ship) else "Hit!" if hit else "Miss."
        self.status.config(text=message+" Computer is choosing a target…")
        self.game.changeTurn()
        self.timer = self.root.after(300, self.computer)

    def computer(self):
        self.timer = None
        self.game.player2.takeShot()
        self.game.changeTurn()
        self.draw()
        if not self.finish():
            self.status.config(text="Your turn. Choose another square in the enemy sea.")

    def finish(self):
        winner = self.game.winner
        if winner:
            self.finished = True
            self.active = False
            self.status.config(text=winner.name+" wins! All five enemy ships are sunk.")
            return True
        return False

    def draw(self):
        c, g = self.canvas, self.game
        c.delete("all")
        for origin, title, owner, shooter, reveal in [
                (30, "YOUR FLEET", g.player1, g.player2, True),
                (310, "ENEMY SEA", g.player2, g.player1, False)]:
            c.create_text(origin+116, 12, text=title, fill=INK, font=("Arial", 12, "bold"))
            for n in range(8):
                c.create_text(origin+n*CELL+14, 30, text=str(n+1), fill="#8fd9df")
                c.create_text(origin-13, TOP+n*CELL+14, text=chr(65+n), fill="#8fd9df")
            for r in range(8):
                for col in range(8):
                    x, y = origin+col*CELL, TOP+r*CELL
                    part = g.board[owner][g.ShipBoard][r][col]
                    shot = g.board[shooter][g.ShotBoard][r][col]
                    colour = "#468e9d" if reveal and isinstance(part, ShipPart) else SEA
                    c.create_rectangle(x+1, y+1, x+CELL-1, y+CELL-1, fill=colour, outline="#28566c")
                    if shot == g.hit:
                        c.create_line(x+7, y+7, x+22, y+22, fill="#ff9966", width=3)
                        c.create_line(x+22, y+7, x+7, y+22, fill="#ff9966", width=3)
                    elif shot == g.miss:
                        c.create_oval(x+11, y+11, x+17, y+17, fill=INK, outline="")
        a, b = g.player1Stats, g.player2Stats
        self.stats.config(text=f"You: {a.shots} shots / {a.hits} hits / {a.sunk} sunk     Computer: {b.shots} shots / {b.hits} hits / {b.sunk} sunk")


root = tk.Tk()
app = Battleships(root)
root.mainloop()
