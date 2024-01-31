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

    def is_valid_move(self, start_pos, end_pos, board):
        # Implement pawn-specific move logic
        pass

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
