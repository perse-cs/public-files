import tkinter as tk
from tkinter import ttk
from maze_model import MazeGen
from maze_generators import RBT, BinaryTree
from maze_search import BFS, AStar

BG, INK = "#101e2b", "#e3f4ed"


class MazeExplorer:
    def __init__(self, root):
        self.root, self.timer = root, None
        root.title("Maze Explorer | watch an algorithm think")
        root.configure(bg=BG)
        tk.Label(root, text="MAZE EXPLORER", bg=BG, fg="#68e0b3", font=("Arial", 20, "bold")).pack(pady=8)
        bar = tk.Frame(root, bg=BG)
        bar.pack()
        self.generator = tk.StringVar(value="Backtracker")
        ttk.Combobox(bar, textvariable=self.generator, values=["Backtracker", "Binary tree"], state="readonly", width=14).pack(side="left")
        for text, callback in [("New maze", self.new), ("BFS", lambda: self.solve(BFS)),
                               ("A*", lambda: self.solve(AStar)), ("Clear trail", self.clear)]:
            tk.Button(bar, text=text, command=callback).pack(side="left", padx=4)
        self.canvas = tk.Canvas(root, width=460, height=460, bg=BG, highlightthickness=0)
        self.canvas.pack(padx=8, pady=6)
        self.canvas.bind("<Button-1>", lambda event: self.canvas.focus_set())
        for key, dx, dy, direction in [("Up", 0, -1, "N"), ("Right", 1, 0, "E"), ("Down", 0, 1, "S"), ("Left", -1, 0, "W")]:
            root.bind("<"+key+">", lambda event, a=dx, b=dy, d=direction: self.move(a, b, d))
        self.status = tk.Label(root, bg=BG, fg=INK, font=("Arial", 10), wraplength=460)
        self.status.pack(pady=5)
        tk.Label(root, text="S = start · E = exit · blue = explored · gold = shortest path\nClick the maze, then use arrow keys to play it yourself.",
                 bg=BG, fg="#b7cbd6", font=("Arial", 10)).pack(pady=5)
        self.new()

    def cancel(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None

    def new(self):
        self.cancel()
        self.maze = MazeGen(15, 15)
        if self.generator.get() == "Binary tree":
            BinaryTree(self.maze).run("NW")
        else:
            RBT(self.maze).run()
        self.clear()

    def clear(self):
        self.cancel()
        self.explored, self.route = set(), set()
        self.player = tuple(self.maze.getStartPos)
        self.steps = 0
        self.draw()
        self.status.config(text="Find your way to E, or compare BFS and A* on the same maze.")

    def draw(self):
        c = self.canvas
        c.delete("all")
        for cell, walls in self.maze.getMazeMap.items():
            x, y = 5+(cell[0]-1)*30, 5+(cell[1]-1)*30
            fill = "#edbf5c" if cell in self.route else "#28658b" if cell in self.explored else "#1b3343"
            c.create_rectangle(x, y, x+30, y+30, fill=fill, outline="")
            for d, coords in [("N", (x, y, x+30, y)), ("S", (x, y+30, x+30, y+30)),
                              ("E", (x+30, y, x+30, y+30)), ("W", (x, y, x, y+30))]:
                if walls[d]:
                    c.create_line(*coords, fill="#91b7b9", width=2)
        for pos, letter, colour in [(self.maze.getStartPos, "S", "#68e0b3"), (self.maze.getEndPos, "E", "#ff9096")]:
            x, y = 20+(pos[0]-1)*30, 20+(pos[1]-1)*30
            c.create_text(x, y, text=letter, fill=colour, font=("Arial", 14, "bold"))
        x, y = 20+(self.player[0]-1)*30, 20+(self.player[1]-1)*30
        c.create_oval(x-5, y-5, x+5, y+5, fill="#ffffff", outline=BG)

    def solve(self, solver):
        self.clear()
        visited, path = solver(self.maze).run()
        self.frames = iter(visited)
        self.solution = path
        self.algorithm = "BFS" if solver == BFS else "A*"
        self.animate()

    def animate(self):
        self.timer = None
        # Draw a few expansions per frame to keep the browser responsive.
        for _ in range(4):
            cell = next(self.frames, None)
            if cell is None:
                self.route = set(self.solution)
                self.draw()
                self.status.config(text=f"{self.algorithm}: explored {len(self.explored)} cells · shortest route {len(self.solution)-1} steps")
                return
            self.explored.add(cell)
        self.draw()
        self.status.config(text=f"{self.algorithm}: exploring… {len(self.explored)} cells")
        self.timer = self.root.after(30, self.animate)

    def move(self, dx, dy, direction):
        if self.timer is not None:
            return
        new = self.player[0]+dx, self.player[1]+dy
        if new in self.maze.getMazeMap and self.maze.getMazeMap[self.player][direction] == 0:
            self.player = new
            self.steps += 1
            self.draw()
            message = "Exit reached!" if new == tuple(self.maze.getEndPos) else "Exploring"
            self.status.config(text=f"{message} {self.steps} steps taken.")


root = tk.Tk()
app = MazeExplorer(root)
root.mainloop()
