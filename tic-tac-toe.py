import tkinter as tk
from tkinter import messagebox as message

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("YAJ tic tac toe")
        self.board = [[" "]*3 for _ in range(3)]
        self.current_player = "X"

        self.buttons = [[None]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text="", width=10, height=3,
                                               command=lambda i=i, j=j: self.make_move(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_winner(self.current_player):
                message.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_tie():
                message.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def check_tie(self):
        return all(all(cell != " " for cell in row) for row in self.board)

    def reset_game(self):
        self.board = [[" "]*3 for _ in range(3)]
        self.current_player = "X"

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
