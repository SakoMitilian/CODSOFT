import tkinter as tk
from tkinter import messagebox

# Initialize the board
board = [[" " for _ in range(3)] for _ in range(3)]

def check_winner(player):
    # Check rows, columns, and diagonals to find a winner (3 matching symbols)
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player: #for diagonals
        return True
    return False

def check_draw():
    return all(cell != " " for row in board for cell in row)

def minimax(depth, is_maximizing):
    if check_winner("O"):
        return 1
    elif check_winner("X"):
        return -1
    elif check_draw():
        return 0
    
    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = " "
                    score = minimax(depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def make_move(row, col):
    if board[row][col] == " ":
        board[row][col] = "X"
        buttons[row][col].config(text="X")
        if check_winner("X"):
            messagebox.showinfo("Game Over", "Player wins!")
            reset_game()
            return
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
            return
        
        # AI's turn
        move = best_move()
        if move:
            board[move[0]][move[1]] = "O"
            buttons[move[0]][move[1]].config(text="O")
            if check_winner("O"):
                messagebox.showinfo("Game Over", "AI wins!")
                reset_game()
                return
            elif check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_game()

def reset_game():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="")

# to Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# to Create buttons for the Tic-Tac-Toe board
buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text=" ", width=10, height=3,
                                       command=lambda r=row, c=col: make_move(r, c))
        buttons[row][col].grid(row=row, column=col)

# Start the game
root.mainloop()
