import pygame
import sys

# Custom Classes
from board import Board
from pieces import Pawn

class Main:
    
    def __init__(self):
        pygame.init()
        
        # Window Creation
        self.screen_width = 600
        self.screen_height = 600
        self.square_size = self.screen_width // 8
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ChessBuddy")
        
        # Chess Setup
        self.current_player = 'White' 
        self.board = Board()
        
        # Load chessboard background image
        self.chessboard_bg = pygame.image.load('../images/Boards/brown.png')  # Update path to your chessboard image
        self.chessboard_bg = pygame.transform.scale(self.chessboard_bg, (self.screen_width, self.screen_height))

        self.highlighted_square = None


    def toggle_player_turn(self):
        if self.current_player == 'White':
            self.current_player = 'Black'
        else:
            self.current_player = 'White'
    

    def draw_board(self):
        # Display the background image
        self.screen.blit(self.chessboard_bg, (0, 0))

        # Draw pieces
        for y, row in enumerate(self.board.board):
            for x, square in enumerate(row):
                if square.piece:
                    # Get original image size
                    original_width, original_height = square.piece.image.get_size()

                    # Calculate scaling factor to maintain aspect ratio
                    scale_factor = min(self.square_size / original_width, self.square_size / original_height)

                    # Calculate new size preserving aspect ratio
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)

                    # Scale the image to the new size
                    piece_image = pygame.transform.scale(square.piece.image, (new_width, new_height))

                    # Calculate position to center the piece in the square
                    x_pos = x * self.square_size + (self.square_size - new_width) // 2
                    y_pos = y * self.square_size + (self.square_size - new_height) // 2

                    # Draw the piece on the board
                    self.screen.blit(piece_image, (x_pos, y_pos))

        # Highlight square if one is selected
        if self.highlighted_square:
            self.highlight_square(*self.highlighted_square)


    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                    
                    
            self.screen.fill((0, 0, 0))  # Black background

            self.draw_board()  # Draw the board and pieces
            
            # Check For Selected Square
            if self.highlighted_square:
                self.highlight_square(*self.highlighted_square)

            pygame.display.flip()
    
    
    def handle_mouse_click(self, event):
        # Get mouse click position
        mouse_pos = event.pos

        # Calculate which square is clicked
        clicked_row = mouse_pos[1] // self.square_size  # y value
        clicked_col = mouse_pos[0] // self.square_size  # x value
        print(f"row = {clicked_row}, col = {clicked_col}")

        # Check if a piece is currently highlighted for moving
        if self.highlighted_square:
            # Check if the clicked square is in the available moves list
            if (clicked_row, clicked_col) in self.valid_moves:
                destination_square = self.board.board[clicked_row][clicked_col]
                # Check for opponent's piece in the destination square
                if destination_square.piece and destination_square.piece.color != self.current_player:
                    # Capture logic here: Remove the opponent's piece from the board
                    print(f"Captured {destination_square.piece}")
                    # Implement capturing logic here

                # Move the piece to the new position
                self.move_piece(self.highlighted_square, (clicked_row, clicked_col))
                # After moving, toggle the player's turn
                self.toggle_player_turn()

                # Clear the highlight and available moves after moving
                self.highlighted_square = None
                self.valid_moves = []
            else:
                # Clear the highlight if an invalid move is attempted
                self.highlighted_square = None

        else:
            # If no piece is highlighted, and the clicked square has a piece of the current player
            square = self.board.board[clicked_row][clicked_col]
            if square.piece and square.piece.color == self.current_player:
                # Store the valid moves of the selected piece
                self.valid_moves = square.piece.is_valid_move((clicked_row, clicked_col), board=self.board)
                # Store the clicked square's position to highlight
                self.highlighted_square = (clicked_row, clicked_col)
   
 
            
    def move_piece(self, from_pos, to_pos):
        # Retrieve the piece to move
        piece = self.board.board[from_pos[0]][from_pos[1]].piece
        # Move the piece to the new position
        self.board.board[to_pos[0]][to_pos[1]].piece = piece
        # Clear the old position
        self.board.board[from_pos[0]][from_pos[1]].piece = None

        # If the piece is a Pawn, update its moved attribute
        if isinstance(piece, Pawn) and not piece.moved:
            piece.moved = True
            print(f"Pawn moved to {to_pos}, moved attribute set to True")

        print(f"Moved piece from {from_pos} to {to_pos}")

    
    
    def highlight_square(self, row, col):
        highlight_color_yellow = (255, 255, 0)  # Corrected to yellow
        pygame.draw.rect(self.screen, highlight_color_yellow, (col*self.square_size, row*self.square_size, self.square_size, self.square_size))
        
        # Redraw the piece on the highlighted square
        square = self.board.board[row][col]
        if square.piece:   
                
            piece_image = pygame.transform.scale(square.piece.image, (self.square_size, self.square_size))
            self.screen.blit(piece_image, (col * self.square_size, row * self.square_size))
            
            # Will Highlight all of the pieces valid moves
            highlight_color_red = (255, 0, 0)
            # valid_moves = square.piece.is_valid_move((row, col), board=self.board)
            for move in self.valid_moves:
                move_row, move_col = move
                pygame.draw.rect(self.screen, highlight_color_red, (move_col * self.square_size, move_row * self.square_size, self.square_size, self.square_size))
                
                # If there's a piece on the valid move square, redraw it so it's visible over the red highlight
                move_square = self.board.board[move_row][move_col]
                if move_square.piece:
                    move_piece_image = pygame.transform.scale(move_square.piece.image, (self.square_size, self.square_size))
                    self.screen.blit(move_piece_image, (move_col * self.square_size, move_row * self.square_size))
        else:
            print("No piece on the highlighted square")

if __name__ == "__main__":
    main = Main()
    main.run_game()
