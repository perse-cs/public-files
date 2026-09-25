import tkinter as tk
from tkinter import ttk
from copy import deepcopy
from boxes_engine import Game
from boxes_ai import Move

BG, INK = "#201b35", "#f4edff"
COLOURS = ["#71d9ea", "#ffa980"]


class DotsAndBoxes:
    def __init__(self, root):
        self.root, self.timer = root, None
        root.title("Dots and Boxes | the chain reaction")
        root.configure(bg=BG)
        tk.Label(root, text="DOTS + BOXES", bg=BG, fg="#c6a7ff", font=("Arial", 20, "bold")).pack(pady=8)
        bar = tk.Frame(root, bg=BG)
        bar.pack()
        self.mode = tk.StringVar(value="Chain AI")
        ttk.Combobox(bar, textvariable=self.mode, values=["Two players", "Tactical AI", "Chain AI"], state="readonly", width=14).pack(side="left")
        for text, callback in [("New game", self.new), ("Undo turn", self.undo), ("Hint", self.hint)]:
            tk.Button(bar, text=text, command=callback).pack(side="left", padx=4)
        self.score = tk.Label(root, bg=BG, fg=INK, font=("Arial", 13, "bold"))
        self.score.pack(pady=6)
        self.canvas = tk.Canvas(root, width=430, height=430, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=10)
        self.canvas.bind("<Button-1>", self.click)
        self.status = tk.Label(root, bg=BG, fg=INK, font=("Arial", 11), wraplength=430)
        self.status.pack(pady=6)
        tk.Label(root, text="Click between two dots. Close a box to score and play again.\nThink ahead: one edge can give away a whole chain!", bg=BG, fg="#c6b8dc", font=("Arial", 10)).pack(pady=6)
        self.new()

    def new(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
        self.timer = None
        self.game = Game((4, 4), 2, ["Blue", "Coral"], ["P", "P"])
        self.opponent = self.mode.get()
        self.edges, self.stack = {}, []
        self.suggestion = None
        self.draw()

    def coords(self, move):
        row, col, direction = move
        x, y = 35+col*90, 35+row*90
        return {"N": (x, y, x+90, y), "S": (x, y+90, x+90, y+90),
                "W": (x, y, x, y+90), "E": (x+90, y, x+90, y+90)}[direction]

    def draw(self):
        c, g = self.canvas, self.game
        c.delete("all")
        for r in range(4):
            for col in range(4):
                owner = g.getBoxExists((r, col))
                if owner >= 0:
                    x, y = 35+col*90, 35+r*90
                    c.create_rectangle(x+8, y+8, x+82, y+82, fill=COLOURS[owner], outline="")
                    c.create_text(x+45, y+45, text="B" if owner == 0 else "C", fill=BG, font=("Arial", 20, "bold"))
        for move in g.ReturnAvailable():
            c.create_line(*self.coords(move), fill="#49405f", width=5)
        for coords, owner in self.edges.items():
            c.create_line(*coords, fill=COLOURS[owner], width=6)
        if self.suggestion:
            c.create_line(*self.coords(self.suggestion), fill="#ffffff", width=8)
        for r in range(5):
            for col in range(5):
                x, y = 35+col*90, 35+r*90
                c.create_oval(x-6, y-6, x+6, y+6, fill=INK, outline="")
        a, b = g.CalculateScores()
        self.score.config(text=f"BLUE  {a}     :     {b}  CORAL")
        if g.End():
            self.status.config(text="Draw!" if a == b else ("Blue" if a > b else "Coral")+" wins!")
        else:
            self.status.config(text=("Blue" if g.getTurn() == 0 else "Coral")+f" to play · {self.opponent}")

    def click(self, event):
        if self.timer is not None or self.game.End():
            return
        # Hit-test the centre of the nearest unclaimed horizontal/vertical edge.
        for move in self.game.ReturnAvailable():
            x1, y1, x2, y2 = self.coords(move)
            if x1 == x2:
                near = abs(event.x-x1) < 14 and y1+9 < event.y < y2-9
            else:
                near = abs(event.y-y1) < 14 and x1+9 < event.x < x2-9
            if near:
                self.stack.append((deepcopy(self.game), dict(self.edges)))
                self.play(move)
                self.queue_ai()
                return

    def play(self, move):
        self.suggestion = None
        self.edges[self.coords(move)] = self.game.getTurn()
        captured = self.game.place(move[:2], move[2])
        if not captured:
            self.game.nextTurn()
        self.draw()

    def queue_ai(self):
        if self.opponent != "Two players" and self.game.getTurn() == 1 and not self.game.End():
            self.status.config(text="Coral is considering captures and chains…")
            self.timer = self.root.after(240, self.computer)

    def computer(self):
        self.timer = None
        self.play(Move(3 if self.opponent == "Chain AI" else 2, self.game))
        self.queue_ai()

    def hint(self):
        if self.timer is None and not self.game.End():
            self.suggestion = Move(3, self.game)
            self.draw()
            self.status.config(text="The white edge is a suggestion. Can you explain the choice?")

    def undo(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None
        if self.stack:
            self.game, self.edges = self.stack.pop()
        self.suggestion = None
        self.draw()


root = tk.Tk()
app = DotsAndBoxes(root)
root.mainloop()
