import pygame
import sys

# Custom Classes
from board import Board

class Main:
    def __init__(self):
        pygame.init()
        
        # Window Creation
        self.screen_width = 400
        self.screen_height = 400
        self.square_size = self.screen_width // 8
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ChessBuddy")
        
        # Chess Setup
        self.board = Board()
        
        # Load chessboard background image
        self.chessboard_bg = pygame.image.load('../images/Boards/brown.svg')  # Update path to your chessboard image
        self.chessboard_bg = pygame.transform.scale(self.chessboard_bg, (self.screen_width, self.screen_height))


    def draw_board(self):
        # Display the background image
        self.screen.blit(self.chessboard_bg, (0, 0))

        # Draw pieces
        for y, row in enumerate(self.board.board):
            for x, square in enumerate(row):
                if square.piece:
                    piece_image = pygame.transform.scale(square.piece.image, (self.square_size, self.square_size))
                    self.screen.blit(piece_image, (x * self.square_size, y * self.square_size))


    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((0, 0, 0))  # Black background

            self.draw_board()  # Draw the board and pieces

            pygame.display.flip()

if __name__ == "__main__":
    main = Main()
    main.run_game()
