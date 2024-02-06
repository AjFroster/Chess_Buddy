import pygame

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        
        # Visuals
        self.image = pygame.image.load(f'../images/Pieces/{color}_{name}.svg').convert_alpha()

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement move validation for the piece
        pass

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "Pawn")

    def is_valid_move(self, position, board):
        valid_moves = []
        direction = 1 if self.color == "white" else -1  # Adjust direction based on color
        start_row = 6 if self.color == "white" else 1
        row, col = position

        # Move forward
        if board[row + direction][col] == None:  # Assuming None means the square is empty
            valid_moves.append((row + direction, col))
            # Check if it's the pawn's first move
            if row == start_row and board[row + 2 * direction][col] == None:
                valid_moves.append((row + 2 * direction, col))

        # Capture moves
        for dcol in [-1, 1]:
            if 0 <= col + dcol < 8:  # Ensure the column is within bounds
                target_square = board[row + direction][col + dcol]
                if target_square != None and target_square.color != self.color:  # Enemy piece present
                    valid_moves.append((row + direction, col + dcol))

        return valid_moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "Rook")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement rook-specific move logic
        pass

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "Knight")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement knight-specific move logic
        pass

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "Bishop")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement bishop-specific move logic
        pass

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "Queen")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement queen-specific move logic
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "King")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement king-specific move logic
        pass
