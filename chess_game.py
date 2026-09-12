import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=500, height=500, bg="#c8a951", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Game state
        self.board = [
            ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
            ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
            ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        ]
        
        self.piece_colors = []
        for row in self.board:
            colors_row = []
            for piece in row:
                if piece == "":
                    colors_row.append("")
                elif piece == "pawn":
                    colors_row.append("white_pawn")
                elif piece == "knight":
                    colors_row.append("white_knight")
                elif piece == "bishop":
                    colors_row.append("white_bishop")
                elif piece == "rook":
                    colors_row.append("white_rook")
                elif piece == "queen":
                    colors_row.append("white_queen")
                elif piece == "king":
                    colors_row.append("white_king")
            self.piece_colors.append(colors_row)
        
        self.current_turn = "white"
        self.selected_piece = None
        self.selected_pos = None
        self.game_over = False
        
        # Piece symbols (using Unicode)
        self.piece_symbols = {
            "white_pawn": "♟", "white_knight": "♞", "white_bishop": "♝", 
            "white_rook": "♜", "white_queen": "♛", "white_king": "♚",
            "black_pawn": "♙", "black_knight": "♘", "black_bishop": "♗", 
            "black_rook": "♖", "black_queen": "♕", "black_king": "♔"
        }
        
        # Square size
        self.square_size = 500 // 8
        
        # Bind clicks
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Draw initial board
        self.draw_board()
        self.draw_pieces()
        
        # Status label
        self.status_label = tk.Label(root, text="White to move", font=("Arial", 14), fg="#333", bg="#f0e6d2")
        self.status_label.pack()
    
    def get_square_color(self, row, col):
        if (row + col) % 2 == 0:
            return "#d8b465"
        else:
            return "#a97745"
    
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.get_square_color(row, col)
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#8b5a2b", width=1)
    
    def draw_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "":
                    color_key = f"{piece}_color" if False else piece
                    # Determine display color
                    if piece.startswith("white"):
                        display_color = "white"
                    elif piece.startswith("black"):
                        display_color = "black"
                    else:
                        continue
                    
                    symbol = self.piece_symbols.get(f"{piece}", "♟")
                    x1 = col * self.square_size + self.square_size // 4
                    y1 = row * self.square_size + self.square_size // 4
                    x2 = x1 + self.square_size // 2
                    y2 = y1 + self.square_size // 2
                    
                    # Draw piece text
                    self.canvas.create_text(
                        x1 + self.square_size // 4, y1 + self.square_size // 4,
                        text=symbol, font=("Segoe UI Emoji", 36), tag="piece",
                        fill="#333" if display_color == "white" else "#fff"
                    )
    
    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        if piece == "":
            return False
        
        # Check color
        if (piece.startswith("white") and self.current_turn != "white") or \
           (piece.startswith("black") and self.current_turn != "black"):
            return False
        
        # Basic movement validation
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        if piece == "pawn":
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col)
        elif piece == "rook":
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece == "knight":
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        elif piece == "bishop":
            return row_diff == col_diff and row_diff > 0
        elif piece == "queen":
            return (row_diff == col_diff or row_diff == 0 or col_diff == 0) and row_diff > 0
        elif piece == "king":
            return row_diff <= 1 and col_diff <= 1
        
        return False
    
    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        direction = -1 if piece.startswith("white") else 1
        start_row = 6 if piece.startswith("white") else 1
        
        # Forward one square
        if from_col == to_col and to_row == from_row + direction and self.board[to_row][to_col] == "":
            return True
        
        # Forward two squares from start position
        if from_col == to_col and from_row == start_row and to_row == from_row + 2 * direction and \
           self.board[from_row + direction][to_col] == "" and self.board[to_row][to_col] == "":
            return True
        
        # Capture diagonally
        if abs(to_col - from_col) == 1 and to_row == from_row + direction and self.board[to_row][to_col] != "":
            target = self.board[to_row][to_col]
            if (target.startswith("white") and self.current_turn == "black") or \
               (target.startswith("black") and self.current_turn == "white"):
                return True
        
        return False
    
    def is_valid_rook_move(self, from_row, from_col, to_row, to_col):
        # Must move in straight line
        if from_row != to_row and from_col != to_col:
            return False
        
        # Check path is clear
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        r, c = from_row + row_step, from_col + col_step
        while r != to_row or c != to_col:
            if self.board[r][c] != "":
                return False
            r += row_step
            c += col_step
        
        # Check target
        target = self.board[to_row][to_col]
        if target == "":
            return True
        if (target.startswith("white") and self.current_turn == "black") or \
           (target.startswith("black") and self.current_turn == "white"):
            return True
        
        return False
    
    def on_click(self, event):
        if self.game_over:
            return
        
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if self.selected_piece is None:
            # Select piece
            piece = self.get_piece_at(row, col)
            if piece != "" and ((piece.startswith("white") and self.current_turn == "white") or
                               (piece.startswith("black") and self.current_turn == "black")):
                self.selected_piece = piece
                self.selected_pos = (row, col)
                # Highlight possible moves
                self.highlight_moves(row, col)
        else:
            # Deselect or move
            if self.selected_pos == (row, col):
                # Deselect
                self.selected_piece = None
                self.selected_pos = None
                self.canvas.delete("highlight")
            elif self.is_valid_move(self.selected_pos[0], self.selected_pos[1], row, col):
                # Make move
                self.make_move(self.selected_pos[0], self.selected_pos[1], row, col)
                self.selected_piece = None
                self.selected_pos = None
                self.canvas.delete("highlight")
                self.switch_turn()
            else:
                # Invalid move, deselect
                self.selected_piece = None
                self.selected_pos = None
                self.canvas.delete("highlight")
    
    def highlight_moves(self, row, col):
        piece = self.board[row][col]
        rows = range(8)
        cols = range(8)
        
        for r in rows:
            for c in cols:
                if self.is_valid_move(row, col, r, c):
                    x1 = c * self.square_size + self.square_size // 2
                    y1 = r * self.square_size + self.square_size // 2
                    self.canvas.create_oval(x1 - 15, y1 - 15, x1 + 15, y1 + 15, 
                                           fill="yellow", stipple="gray25", outline="", tags="highlight")
    
    def make_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""
        
        # Handle pawn promotion
        if piece == "pawn" and (to_row == 0 or to_row == 7):
            self.board[to_row][to_col] = "queen"  # Simple promotion to queen
        
        # Check for check
        self.check_game_status()
    
    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.status_label.config(text=f"{self.current_turn.capitalize()} to move")
        self.draw_pieces()
    
    def check_game_status(self):
        # Simple check detection - just for show
        pass
    
    def on_restart(self):
        self.board = [
            ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
            ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
            ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        ]
        self.current_turn = "white"
        self.selected_piece = None
        self.selected_pos = None
        self.game_over = False
        self.status_label.config(text="White to move")
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    
    # Menu
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New Game", command=game.on_restart)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)
    
    root.mainloop()