from pieces import Pawn, Knight, Bishop, Rook, Queen, King
import pygame

class Square:
    def __init__(self, x, y, color, piece=None):
        # Primary Variables
        self.x = x
        self.y = y
        self.color = color
        self.piece = piece  # Chess piece on the square
        
        # Chess Notation
        self.file = chr(97 + x)  # 'a' to 'h'
        self.rank = str(8 - y)   # '1' to '8'
        self.label = self.file + self.rank  # e.g., 'a1', 'b5', etc.
        
        
class Board:
    def __init__(self):
        self.board = self.setup_board()

    def setup_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Assign squares and place pieces
        for y in range(8):
            for x in range(8):
                color = "White" if (x + y) % 2 == 0 else "Black"
                piece = None

                # Place pawns
                if y == 1: piece = Pawn("Black")
                elif y == 6: piece = Pawn("White")

                # Place other pieces
                if y == 0 or y == 7:
                    color_piece = "Black" if y == 0 else "White"
                    pieces = [Rook(color_piece), Knight(color_piece), Bishop(color_piece), 
                              Queen(color_piece), King(color_piece), 
                              Bishop(color_piece), Knight(color_piece), Rook(color_piece)]
                    piece = pieces[x]

                board[y][x] = Square(x, y, color, piece)

        return board
    
    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece_at_position(self, row, col):
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        else:
            return None

    def __getitem__(self, pos):
        row, col = pos
        return self.board[row][col]
