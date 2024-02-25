import pygame

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.has_moved = False
        self.position = None  # Add this line to track the piece's position
        self.value = None
        
        # Visuals
        self.image = pygame.image.load(f'../images/Pieces/{color}_{name}.svg').convert_alpha()

    def get_valid_moves(self, position, board):
        # Implement move validation for the piece
        pass
    

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "Pawn")
        self.value = 1

    def get_valid_moves(self, position, board):
        #print(f" self.has_moved = {self.has_moved}")  # Debugging print statement
        valid_moves = []
        direction = -1 if self.color == "White" else 1  # Adjust direction based on color
        row, col = position

        # Move forward one space
        if board.is_valid_position(row + direction, col) and not board[row + direction, col].piece:
            valid_moves.append((row + direction, col))

            # If it hasn't moved, consider two spaces forward
            if not self.has_moved and board.is_valid_position(row + (2 * direction), col) and not board[row + 2 * direction, col].piece:  # Corrected condition
                valid_moves.append((row + 2 * direction, col))

        # Diagonal capture
        for diag in [-1, 1]:  # Check both left and right diagonals
            if board.is_valid_position(row + direction, col + diag):
                diag_square = board[row + direction, col + diag]
                if diag_square.piece and diag_square.piece.color != self.color:
                    valid_moves.append((row + direction, col + diag))

        return valid_moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "Knight")
        self.value = 3

    def get_valid_moves(self, position, board):
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
        self.value = 3

    def get_valid_moves(self, position, board):
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
        self.value = 5
        self.moved = False

    def get_valid_moves(self, position, board):
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
        self.value = 9

    def get_valid_moves(self, position, board):
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
        self.value = 20
        # Assuming 'moved' tracks if the King has ever moved, for castling or other logic
        # self.moved = False

    def get_valid_moves(self, position, board):
        # Unpack the target position
        row, col = position

        # Directions the King can move: vertical, horizontal, and diagonal
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        valid_moves = []

        # Basic King Movements
        for d_row, d_col in directions:
            target_row, target_col = row + d_row, col + d_col

            # Ensure the move stays within the board boundaries
            if 0 <= target_row < len(board.board) and 0 <= target_col < len(board.board[0]):
                destination_square = board.board[target_row][target_col]
                # Check if the destination square is either empty or contains an opponent's piece
                if destination_square.piece is None or destination_square.piece.color != self.color:
                    valid_moves.append((target_row, target_col))
        
        # Check for the ability to castle
        valid_king_side_castle, king_side_castle_position = self.can_castle_kingside(board)    
        valid_queen_side_castle, queen_side_castle_position = self.can_castle_queenside(board) 
          
        if valid_king_side_castle:
            valid_moves.append(king_side_castle_position)
            
        if valid_queen_side_castle:
            valid_moves.append(queen_side_castle_position)
        
        # print(', '.join(f"({row}, {col})" for row, col in valid_moves))

        return valid_moves

    def can_castle_kingside(self, board):
        # Assuming 'board' is an object with attributes/methods to check for pieces and moves
        # Check if the king has moved
        if self.has_moved:
            return False, None  # The king cannot castle, no end position

        # Define the path and end position for kingside castling based on the king's color
        if self.color == 'White':
            rook_position = (7, 7)  # Assuming H1 for white's rook in traditional setup
            path = [(7, 5), (7, 6)]  # Squares the king passes through for white
            king_end_position = (7, 6)  # G1, white king's ending position after castling
        else:  # 'black'
            rook_position = (0, 7)  # Assuming H8 for black's rook in traditional setup
            path = [(0, 5), (0, 6)]  # Squares the king passes through for black
            king_end_position = (0, 6)  # G8, black king's ending position after castling

        # Check if the path is clear
        for position in path:
            if board.board[position[0]][position[1]].piece is not None:
                return False, None  # Path is not clear, no end position

        # Check if the rook has moved
        rook = board.board[rook_position[0]][rook_position[1]].piece
        if rook is None or rook.has_moved:
            return False, None  # Rook has moved or is not present, no end position

        # If all conditions are met
        print("Can kingside castle")
        return True, king_end_position

    def can_castle_queenside(self, board):
        # Assuming 'board' is an object with attributes/methods to check for pieces and moves
        # Check if the king has moved
        if self.has_moved:
            return False, None  # The king cannot castle, no end position

        # Define the path and end position for queenside castling based on the king's color
        if self.color == 'White':
            rook_position = (7, 0)  # Assuming A1 for white's rook in traditional setup
            path = [(7, 1), (7, 2), (7, 3)]  # Squares the king passes through for white
            king_end_position = (7, 2)  # C1, white king's ending position after castling
        else:  # 'black'
            rook_position = (0, 0)  # Assuming A8 for black's rook in traditional setup
            path = [(0, 1), (0, 2), (0, 3)]  # Squares the king passes through for black
            king_end_position = (0, 2)  # C8, black king's ending position after castling

        # Check if the path is clear
        for position in path:
            if board.board[position[0]][position[1]].piece is not None:
                return False, None  # Path is not clear, no end position

        # Check if the rook has moved
        rook = board.board[rook_position[0]][rook_position[1]].piece
        if rook is None or rook.has_moved:
            return False, None  # Rook has moved or is not present, no end position

        # If all conditions are met
        print("Can queenside castle")
        return True, king_end_position





