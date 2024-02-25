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
                if y == 1:
                    piece = Pawn("Black")
                    piece.position = (y, x)  # Set the piece's position
                elif y == 6:
                    piece = Pawn("White")
                    piece.position = (y, x)  # Set the piece's position

                # Place other pieces
                if y == 0 or y == 7:
                    color_piece = "Black" if y == 0 else "White"
                    pieces = [Rook(color_piece), Knight(color_piece), Bishop(color_piece), 
                              Queen(color_piece), King(color_piece), 
                              Bishop(color_piece), Knight(color_piece), Rook(color_piece)]
                    piece = pieces[x]
                    piece.position = (y, x)  # Set the piece's position

                board[y][x] = Square(x, y, color, piece)  # Assuming Square is correctly implemented

        return board
    
    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece_at_position(self, row, col):
        if self.is_valid_position(row, col):
            return self.board[row][col].piece  # Adjusted to access the piece attribute of the square
        else:
            return None

    def __getitem__(self, pos):
        row, col = pos
        return self.board[row][col]  # Removed the comma, as we're returning the Square object itself
    
    def get_valid_moves_for_piece(self, position):
        piece = self.get_piece_at_position(position[0], position[1])
        if piece:
            return piece.get_valid_moves(position, self)
        return []
    
    def find_king_position(self, color):
        for row in range(8):  # Assuming an 8x8 board
            for col in range(8):
                piece = self.board[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None  # Return None if the king is not found (which should never happen in a valid game)
    
    def is_king_in_check(self, king_color):
        king_pos = self.find_king_position(king_color)
        opponent_color = 'Black' if king_color == 'White' else 'White'
        for row in range(8):  # Assuming an 8x8 board
            for col in range(8):
                piece = self.get_piece_at_position(row, col)
                if piece and piece.color == opponent_color:
                    # Pass 'self' instead of 'self.board' to provide the Board instance
                    if king_pos in piece.get_valid_moves((row, col), self):
                        return True
        return False

    def is_checkmate(self, king_color):
        if not self.is_king_in_check(king_color):
            return False  # The king must be in check for it to be checkmate

        # Find all pieces for the king's color
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at_position(row, col)
                if piece and piece.color == king_color:
                    original_pos = (row, col)
                    valid_moves = self.get_valid_moves_for_piece(original_pos)
                    for move in valid_moves:
                        # Simulate each move
                        captured_piece = self.simulate_move(original_pos, move)
                        if not self.is_king_in_check(king_color):
                            # If the king is not in check after the move, it's not checkmate
                            self.undo_move(original_pos, move, captured_piece)
                            return False
                        # Undo the simulated move
                        self.undo_move(original_pos, move, captured_piece)
        return True  # No moves remove the king from check, thus checkmate

    def simulate_move(self, from_pos, to_pos):
        # Temporarily move a piece to simulate the board's state after the move
        piece = self.get_piece_at_position(from_pos[0], from_pos[1])
        captured_piece = self.get_piece_at_position(to_pos[0], to_pos[1])
        self.board[to_pos[0]][to_pos[1]].piece = piece
        self.board[from_pos[0]][from_pos[1]].piece = None
        if piece:
            piece.position = to_pos
        return captured_piece

    def undo_move(self, from_pos, to_pos, captured_piece):
        # Revert a move during simulation
        piece = self.get_piece_at_position(to_pos[0], to_pos[1])
        self.board[from_pos[0]][from_pos[1]].piece = piece
        self.board[to_pos[0]][to_pos[1]].piece = captured_piece
        if piece:
            piece.position = from_pos
        if captured_piece:
            captured_piece.position = to_pos

