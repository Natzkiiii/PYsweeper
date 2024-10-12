import tkinter as tk
import random
import time
import subprocess

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mine_positions = set()
        self.flags = set()
        self.start_time = time.time()
        self.timer_label = tk.Label(master, text="Time: 0", font=("Helvetica", 10, "bold"))
        self.timer_label.grid(row=0, column=0, columnspan=cols)
        self.create_widgets()
        self.place_mines()
        self.update_timer()

    def create_widgets(self):
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                button = tk.Button(self.master, width=2, height=1, font=("Helvetica", 10, "bold"), fg='black')
                button.bind("<Button-1>", lambda e, r=r, c=c: self.on_click(r, c))
                button.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                button.grid(row=r+1, column=c)
                row.append(button)
            self.buttons.append(row)
        restart_button = tk.Button(self.master, text="Restart", command=self.restart, font=("Helvetica", 10, "bold"))
        restart_button.grid(row=self.rows+1, column=0, columnspan=self.cols)
        
        solve_button = tk.Button(self.master, text="Solve", command=self.run_solve_script, font=("Helvetica", 10, "bold"))
        solve_button.grid(row=self.rows+2, column=0, columnspan=self.cols)

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_positions.add((r, c))

    def on_click(self, r, c):
        if (r, c) in self.flags:
            return
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red', font=("Helvetica", 10, "bold"), fg='black')
            self.game_over()
        else:
            self.reveal(r, c)
            self.check_win()

    def on_right_click(self, r, c):
        if self.buttons[r][c]['text'] == '':
            self.buttons[r][c].config(text='F', bg='yellow')
            self.flags.add((r, c))
        elif self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flags.remove((r, c))
        self.check_win()

    def reveal(self, r, c, initial=False):
        if self.buttons[r][c]['text'] == '' or initial:
            mines_count = self.count_mines(r, c)
            if not initial:
                self.buttons[r][c].config(text=str(mines_count), state='disabled')
            if mines_count == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                            self.reveal(r + dr, c + dc)

    def count_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mine_positions:
                    count += 1
        return count

    def game_over(self):
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red', font=("Helvetica", 10, "bold"), fg='black')
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')
        self.master.after_cancel(self.timer_id)

    def restart(self):
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons = []
        self.mine_positions = set()
        self.flags = set()
        self.start_time = time.time()
        self.create_widgets()
        self.place_mines()
        self.update_timer()

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}")
        self.timer_id = self.master.after(1000, self.update_timer)

    def is_mine(self, r, c):
        return (r, c) in self.mine_positions

    def run_solve_script(self):
        subprocess.run(["python", "solve.py"])

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_positions and self.buttons[r][c]['state'] != 'disabled':
                    return
        self.win()

    def win(self):
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')
        self.master.after_cancel(self.timer_id)
        self.timer_label.config(text="You Win!", font=("Helvetica", 10, "bold"), fg='green')


    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if (r != row or c != col) and self.is_mine(r, c):
                    count += 1
        return count

    def flag(self, r, c):
        if self.buttons[r][c]['text'] == '':
            self.buttons[r][c].config(text='F', bg='yellow')
            self.flags.add((r, c))
        elif self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flags.remove((r, c))
        self.check_win()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
