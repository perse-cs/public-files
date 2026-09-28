import tkinter as tk
from copy import deepcopy
from sudoku_engine import Game

BG, INK = "#202334", "#f3f2ff"
PALETTE = ["#e7edf9", "#ffe5d1", "#d8f3e7", "#e8dcf7", "#fff1be", "#d7f1f6"]


class KillerSudoku:
    def __init__(self, root):
        self.root = root
        root.title("Killer Sudoku | colour cages")
        root.configure(bg=BG)
        tk.Label(root, text="KILLER SUDOKU", bg=BG, fg="#c9b4ff", font=("Arial", 20, "bold")).pack(pady=8)
        bar = tk.Frame(root, bg=BG)
        bar.pack()
        for text, callback in [("New puzzle", self.new), ("Undo", self.undo), ("Check", self.check),
                               ("Solve", self.solve), ("Save", self.save), ("Load", self.load)]:
            tk.Button(bar, text=text, command=callback).pack(side="left", padx=3)
        self.canvas = tk.Canvas(root, width=460, height=460, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=8, pady=6)
        self.canvas.bind("<Button-1>", self.select)
        root.bind("<KeyPress>", self.key)
        numbers = tk.Frame(root, bg=BG)
        numbers.pack()
        for n in range(1, 10):
            tk.Button(numbers, text=str(n), width=2, command=lambda value=n: self.enter(value)).pack(side="left", padx=2)
        tk.Button(numbers, text="Erase", command=lambda: self.enter(0)).pack(side="left", padx=3)
        self.status = tk.Label(root, bg=BG, fg=INK, font=("Arial", 10), wraplength=460)
        self.status.pack(pady=5)
        tk.Label(root, text="Each row, column and 3×3 box uses 1–9 once.\nEach outlined cage adds to its small total, without repeating a digit.", bg=BG, fg="#c8c9e1", font=("Arial", 10)).pack(pady=5)
        self.new()

    def new(self):
        self.game = Game()
        self.game.newGame(2, 1)
        self.stack, self.errors = [], set()
        self.selected = next(( (x, y) for y in range(9) for x in range(9) if self.game.checkCell(x, y)), (0, 0))
        self.draw()
        self.status.config(text="Select a blank square, then type 1–9 or use the number buttons.")

    def draw(self):
        c, g = self.canvas, self.game
        c.delete("all")
        cage_ids = g.getCagesDict()
        for y in range(9):
            for x in range(9):
                left, top = 5+x*50, 5+y*50
                cage_id = cage_ids[x+y*9]
                fill = "#ffc1c9" if (x, y) in self.errors else PALETTE[cage_id % len(PALETTE)]
                c.create_rectangle(left, top, left+50, top+50, fill=fill, outline="#a8aec2", width=1)
                cage = g.getCages()[cage_id]
                cells = {tuple(cell) for cell in cage.cells}
                for neighbour, coords in [((x, y-1), (left+3, top+3, left+47, top+3)),
                                          ((x, y+1), (left+3, top+47, left+47, top+47)),
                                          ((x-1, y), (left+3, top+3, left+3, top+47)),
                                          ((x+1, y), (left+47, top+3, left+47, top+47))]:
                    if neighbour not in cells:
                        c.create_line(*coords, fill="#687087", dash=(2, 2))
                if (x, y) == min(cells, key=lambda cell: (cell[1], cell[0])):
                    c.create_text(left+6, top+5, text=str(cage.sum), anchor="nw", fill="#39435d", font=("Arial", 8, "bold"))
                value = g.getCell(x, y)
                if value:
                    c.create_text(left+27, top+30, text=str(value), fill="#234db5" if g.checkCell(x, y) else "#20283d",
                                  font=("Arial", 18, "normal" if g.checkCell(x, y) else "bold"))
        for n in (0, 3, 6, 9):
            c.create_line(5+n*50, 5, 5+n*50, 455, fill="#20283d", width=3)
            c.create_line(5, 5+n*50, 455, 5+n*50, fill="#20283d", width=3)
        x, y = self.selected
        c.create_rectangle(6+x*50, 6+y*50, 54+x*50, 54+y*50, outline="#426aff", width=3)

    def select(self, event):
        x, y = (event.x-5)//50, (event.y-5)//50
        if 0 <= x < 9 and 0 <= y < 9:
            self.selected = x, y
            self.canvas.focus_set()
            self.draw()
            self.status.config(text="Given clue: choose a blank square." if not self.game.checkCell(x, y) else f"Row {y+1}, column {x+1}: enter a digit.")

    def key(self, event):
        if event.char in "123456789" and event.char:
            self.enter(int(event.char))
        elif event.keysym in ("BackSpace", "Delete", "0"):
            self.enter(0)

    def enter(self, value):
        x, y = self.selected
        if not self.game.checkCell(x, y):
            self.status.config(text="Given clues cannot be changed.")
            return
        if self.game.getCell(x, y) == value:
            return
        self.stack.append(deepcopy(self.game))
        self.game.updateCell(x, y, value)
        self.errors = set()
        self.draw()
        if self.game.checkFull():
            self.check()

    def undo(self):
        if self.stack:
            self.game = self.stack.pop()
        self.errors = set()
        self.draw()
        self.status.config(text="Last edit undone.")

    def check(self):
        self.errors = self.game.getErrorCells()
        self.draw()
        if self.game.checkFull() and self.game.checkComplete():
            text = "Puzzle complete! Every row, column, box and cage is correct."
        elif self.errors:
            text = "Highlighted cells break a row, column, box or cage rule."
        else:
            text = "No conflicts so far. Keep going!"
        self.status.config(text=text)

    def solve(self):
        self.stack.append(deepcopy(self.game))
        self.game.solve()
        self.check()

    def save(self):
        self.game.saveGame("killer_demo_save.json")
        self.status.config(text="Saved to killer_demo_save.json. Close or Stop to sync it to Files.")

    def load(self):
        try:
            loaded = Game()
            loaded.loadGame("killer_demo_save.json")
        except FileNotFoundError:
            self.status.config(text="No saved puzzle yet. Use Save first.")
            return
        self.game = loaded
        self.stack, self.errors = [], set()
        self.draw()
        self.status.config(text="Saved puzzle loaded.")


root = tk.Tk()
app = KillerSudoku(root)
root.mainloop()
