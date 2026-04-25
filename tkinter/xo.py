import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("300x350")
        
        self.player = "X"
        self.buttons = []
        
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(root, text="", font=('Arial', 20, 'bold'), 
                                width=5, height=2,
                                command=lambda r=i, c=j: self.handle_click(r, c))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def handle_click(self, r, c):
        button = self.buttons[r][c]
        
        if button["text"] == "":
            button["text"] = self.player
            
            if self.player == "X":
                button.config(fg="blue")
            else:
                button.config(fg="red")
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.player} wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()
            else:
                self.player = "O" if self.player == "X" else "X"

    def check_winner(self):
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                return True
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                return True
        
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return True
            
        return False

    def check_draw(self):
        for row in self.buttons:
            for btn in row:
                if btn["text"] == "":
                    return False
        return True

    def reset_game(self):
        for row in self.buttons:
            for btn in row:
                btn.config(text="")
        self.player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()