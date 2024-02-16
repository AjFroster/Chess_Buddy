import pygame

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.has_moved = False
        
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
        direction = -1 if self.color == "White" else 1  # Adjust direction based on color
        row, col = position

        # Move forward one space
        if board.is_valid_position(row + direction, col) and not board[row + direction, col].piece:
            valid_moves.append((row + direction, col))

            # If it hasn't moved, consider two spaces forward
            if not self.has_moved and board.is_valid_position(row + (2 * direction), col) and not board[row + 2 * direction, col].piece:
                valid_moves.append((row + 2 * direction, col))

        return valid_moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "Knight")

    def is_valid_move(self, position, board):
        valid_moves = []
        row, col = position
        # Knight move patterns (2 in one direction, 1 in the perpendicular direction)
        move_offsets = [
            (-2, -1), (-2, +1),
            (-1, -2), (-1, +2),
            (+1, -2), (+1, +2),
            (+2, -1), (+2, +1),
        ]

        for offset in move_offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if within the board
                target_square = board.board[new_row][new_col]
                # Check if the target square is empty or contains an opponent's piece
                if not target_square.piece or target_square.piece.color != self.color:
                    valid_moves.append((new_row, new_col))

        return valid_moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "Bishop")

    def is_valid_move(self, position, board):
        valid_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Diagonal directions

        for direction in directions:
            step = 1
            while True:
                end_row = position[0] + step * direction[0]
                end_col = position[1] + step * direction[1]

                # Check bounds of the board
                if not (0 <= end_row < len(board.board) and 0 <= end_col < len(board.board[0])):
                    break

                if board[(end_row, end_col)].piece is None:
                    # The square is empty, add as a valid move
                    valid_moves.append((end_row, end_col))
                else:
                    # Square is occupied, check if it's an opponent's piece
                    if board[(end_row, end_col)].piece.color != self.color:
                        valid_moves.append((end_row, end_col))
                    # Block further moves in this direction
                    break

                step += 1

        return valid_moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "Rook")

    def is_valid_move(self, position, board):
        valid_moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Horizontal and vertical directions

        for direction in directions:
            step = 1
            while True:
                end_row = position[0] + step * direction[0]
                end_col = position[1] + step * direction[1]

                # Check bounds of the board
                if not (0 <= end_row < len(board.board) and 0 <= end_col < len(board.board[0])):
                    break

                if board[(end_row, end_col)].piece is None:
                    # The square is empty, add as a valid move
                    valid_moves.append((end_row, end_col))
                else:
                    # Square is occupied, check if it's an opponent's piece
                    if board[(end_row, end_col)].piece.color != self.color:
                        valid_moves.append((end_row, end_col))
                    # Block further moves in this direction
                    break

                step += 1

        return valid_moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "Queen")

    def is_valid_move(self, position, board):
        valid_moves = []
        # Combine directions from Rook and Bishop
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), # Horizontal and vertical
                      (-1, -1), (-1, 1), (1, -1), (1, 1)] # Diagonal

        for direction in directions:
            step = 1
            while True:
                end_row = position[0] + step * direction[0]
                end_col = position[1] + step * direction[1]

                # Check bounds of the board
                if not (0 <= end_row < len(board.board) and 0 <= end_col < len(board.board[0])):
                    break

                # Accessing board using tuple indexing, assuming a __getitem__ method in Board class
                if board[(end_row, end_col)].piece is None:
                    # The square is empty, add as a valid move
                    valid_moves.append((end_row, end_col))
                else:
                    # Square is occupied, check if it's an opponent's piece
                    if board[(end_row, end_col)].piece.color != self.color:
                        valid_moves.append((end_row, end_col))
                    # Block further moves in this direction
                    break

                step += 1

        return valid_moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "King")

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement king-specific move logic
        pass
