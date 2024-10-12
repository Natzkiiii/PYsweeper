import tkinter as tk
from main import Minesweeper

class MinesweeperSolver:
    def __init__(self, game, debug_text_widget=None):
        self.game = game
        self.rows = game.rows
        self.cols = game.cols
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)] 
        self.current_row = 0
        self.current_col = 0
        self.debug_text_widget = debug_text_widget

    def log_debug(self, message):
        if self.debug_text_widget:
            self.debug_text_widget.insert(tk.END, message + "\n")
            self.debug_text_widget.see(tk.END)

    def flag_mine(self, row, col):
        self.game.flag(row, col)
        self.log_debug(f"Flagged mine at ({row}, {col})")

    def solve_step(self):
        if self.current_row < self.rows:
            if self.current_col < self.cols:
                if not self.game.is_mine(self.current_row, self.current_col):
                    adjacent_mines = self.game.count_adjacent_mines(self.current_row, self.current_col)
                    self.board[self.current_row][self.current_col] = adjacent_mines
                    self.game.reveal(self.current_row, self.current_col)
                    self.log_debug(f"Revealed cell at ({self.current_row}, {self.current_col}) with {adjacent_mines} adjacent mines")
                else:
                    self.board[self.current_row][self.current_col] = 'M'
                    self.flag_mine(self.current_row, self.current_col)
                self.current_col += 1
            else:
                self.current_col = 0
                self.current_row += 1
            self.game.master.after(50, self.solve_step)  # Delay of 50 milliseconds after each step
        else:
            self.log_debug("Solver finished")

    def solve(self):
        self.log_debug("Starting solver")
        self.solve_step()

def start_solver(debug_text_widget=None):
    global root, solver_window, solver
    if solver_window is not None:
        solver_window.destroy()
    solver_window = tk.Toplevel(root)
    game = Minesweeper(master=solver_window, rows=10, cols=10, mines=10)
    solver = MinesweeperSolver(game, debug_text_widget=debug_text_widget)
    solver.solve()

def restart_solver():
    start_solver(debug_text_widget=debug_text)

if __name__ == "__main__":
    root = tk.Tk()
    solver_window = None

    start_solver_button = tk.Button(root, text="Start Solver", command=lambda: start_solver(debug_text_widget=debug_text))
    start_solver_button.pack()

    restart_solver_button = tk.Button(root, text="Restart Solver", command=restart_solver)
    restart_solver_button.pack()

    debug_text = tk.Text(root, height=10, width=75)
    debug_text.pack()

    root.mainloop()
