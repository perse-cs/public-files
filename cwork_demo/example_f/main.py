import tkinter as tk
from tkinter import ttk
from connect_engine import game, gameError, StackEmptyError
from connect_ai import Ai
import connect_store as store

# Browser presentation adapter. The original game and minimax live separately.
BG, INK, RED, GOLD = "#101d36", "#edf5ff", "#ff6578", "#ffd166"


class ConnectFour:
    def __init__(self, root):
        self.root = root
        root.title("Connect Four | the thinking game")
        root.configure(bg=BG)
        tk.Label(root, text="CONNECT FOUR", bg=BG, fg=GOLD,
                 font=("Arial", 20, "bold")).pack(pady=8)
        bar = tk.Frame(root, bg=BG)
        bar.pack()
        self.mode = tk.StringVar(value="Medium AI")
        ttk.Combobox(bar, textvariable=self.mode, state="readonly", width=15,
                     values=["Two players", "Practice AI", "Easy AI", "Medium AI"]).pack(side="left")
        for text, action in [("New game", self.new), ("Undo turn", self.undo),
                             ("Save", self.save), ("Load", self.load)]:
            tk.Button(bar, text=text, command=action).pack(side="left", padx=3)
        self.canvas = tk.Canvas(root, width=490, height=420, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=8, pady=6)
        self.canvas.bind("<Button-1>", self.click)
        self.status = tk.Label(root, bg=BG, fg=INK, font=("Arial", 11))
        self.status.pack(pady=4)
        self.history = tk.Label(root, bg=BG, fg="#a7bfdc", font=("Arial", 10))
        self.history.pack(pady=4)
        self.timer = None
        self.new()

    def cancel(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None

    def new(self):
        self.cancel()
        self.board = game()
        self.opponent = self.mode.get()
        self.recorded = False
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(10, 42, 480, 412, fill="#224da1", outline="#5381dd", width=3)
        for col in range(7):
            c.create_text(43+67*col, 22, text=str(col+1), fill=INK, font=("Arial", 13, "bold"))
        winner, run = self.board.getRun
        for row in range(6):
            for col in range(7):
                piece = self.board.getSpace(row, col)
                colour = RED if piece == game.PONE else GOLD if piece == game.PTWO else BG
                x, y = 43+67*col, 75+60*row
                c.create_oval(x-24, y-24, x+24, y+24, fill=colour,
                              outline=INK if (row, col) in run else "#315eb3", width=3)
                if piece != game.EMPTY:
                    c.create_oval(x-15, y-17, x-5, y-7, fill="#ffffff", outline="")
        if winner:
            result = "Draw" if winner == "Draw" else "Red" if winner == game.PONE else "Gold"
            self.status.config(text="Draw!" if result == "Draw" else result+" wins! Four in a row.")
            if not self.recorded:
                store.record(result, len(self.board.getMoves))
                self.recorded = True
        else:
            turn = "Red" if self.board.getPlayer == game.PONE else "Gold"
            self.status.config(text=f"{turn} to play · click a column · {self.opponent}")
        totals = store.totals()
        self.history.config(text="Saved results  |  "+"  ·  ".join(f"{p}: {totals.get(p, 0)}" for p in ("Red", "Gold", "Draw")))

    def click(self, event):
        col = (event.x-10)//67
        if self.timer is not None or self.board.getWinner or not 0 <= col < 7:
            return
        self.play(col)
        self.queue_ai()

    def play(self, col):
        try:
            self.board.play(col+1)
            self.draw()
        except gameError as error:
            self.status.config(text=str(error))

    def queue_ai(self):
        if self.opponent != "Two players" and self.board.getPlayer == game.PTWO and not self.board.getWinner:
            self.status.config(text="Gold is searching the game tree…")
            self.timer = self.root.after(120, self.computer)

    def computer(self):
        self.timer = None
        col = Ai(self.opponent).getColumn(self.board.Board, game.PTWO)
        self.play(col)

    def undo(self):
        self.cancel()
        try:
            self.board.undo()
            if self.opponent != "Two players" and self.board.getPlayer == game.PTWO:
                self.board.undo()
        except StackEmptyError:
            pass
        # A completed game's result stays in history; undo cannot record it twice.
        self.draw()

    def save(self):
        store.save(self.board.getMoves, self.opponent)
        self.status.config(text="Saved to connect_four_demo.db. Close or Stop before reloading the page.")

    def load(self):
        saved = store.load()
        if saved is None:
            self.status.config(text="No saved game yet. Play a few moves and choose Save.")
            return
        self.cancel()
        self.board = game()
        self.board.load(saved[0])
        self.opponent = saved[1]
        self.mode.set(self.opponent)
        self.recorded = bool(self.board.getWinner)
        self.draw()
        self.queue_ai()


root = tk.Tk()
app = ConnectFour(root)
root.mainloop()
