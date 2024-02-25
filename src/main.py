import pygame
import sys

# Custom Classes
from board import Board
from pieces import Pawn, Rook, King

class Main:
    
    def __init__(self):
        pygame.init()
        
        self.screen_width = 600
        self.screen_height = 600
        self.square_size = self.screen_width // 8
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ChessBuddy")
        
        self.current_player = 'White'
        self.board = Board()  # Ensure Board() is correctly initialized in board.py
        
        self.chessboard_bg = pygame.image.load('../images/Boards/brown.png').convert_alpha()
        self.chessboard_bg = pygame.transform.scale(self.chessboard_bg, (self.screen_width, self.screen_height))

        self.highlighted_square = None
        self.valid_moves = []

    def toggle_player_turn(self):
        self.current_player = 'Black' if self.current_player == 'White' else 'White'

    def draw_board(self):
        self.screen.blit(self.chessboard_bg, (0, 0))
        
        # Draw pieces and highlight valid moves
        for y, row in enumerate(self.board.board):
            for x, square in enumerate(row):
                piece = square.piece
                if piece:
                    piece_image = pygame.transform.scale(piece.image, (self.square_size, self.square_size))
                    self.screen.blit(piece_image, (x * self.square_size, y * self.square_size))
                
        # Highlight valid moves for the selected piece
        if self.highlighted_square and self.valid_moves:
            for move in self.valid_moves:
                self.highlight_square(move[0], move[1], color=(255, 0, 0))  # Use red color for valid moves
                
                # If there's a piece on the valid move square, redraw it so it's visible over the highlight
                move_square = self.board.board[move[0]][move[1]]
                if move_square.piece:
                    move_piece_image = pygame.transform.scale(move_square.piece.image, (self.square_size, self.square_size))
                    self.screen.blit(move_piece_image, (move[1] * self.square_size, move[0] * self.square_size))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                
            # End Game Logic  
            if self.board.is_king_in_check(self.current_player):
                if self.board.is_checkmate(self.current_player):
                    self.display_checkmate_popup(self.current_player)
                    break
      
            
            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()

    def handle_mouse_click(self, event):
        mouse_pos = event.pos
        clicked_row = mouse_pos[1] // self.square_size
        clicked_col = mouse_pos[0] // self.square_size

        # Convert coordinates to a board position
        clicked_pos = (clicked_row, clicked_col)

        if self.highlighted_square:
            # Check if the clicked position is a valid move
            if clicked_pos in self.valid_moves:
                # Move the piece to the new position
                self.move_piece(self.highlighted_square, clicked_pos)
                self.toggle_player_turn()
            # Whether the move was valid or not, clear the highlights and valid moves
            self.highlighted_square = None
            self.valid_moves = []
        else:
            square = self.board.board[clicked_row][clicked_col]
            if square.piece and square.piece.color == self.current_player:
                print("selected the piece = "+square.piece.name)
                # Highlight the clicked square and calculate valid moves
                self.highlighted_square = clicked_pos
                # Assume a method exists on the piece to calculate its valid moves
                self.valid_moves = square.piece.get_valid_moves(clicked_pos, self.board)
                # This method should return a list of tuples representing valid move positions

    def move_piece(self, from_pos, to_pos):
                
        piece = self.board.board[from_pos[0]][from_pos[1]].piece
        if piece:
            # Update the piece's position and mark it as having moved
            piece.position = to_pos
            piece.has_moved = True  # This should be handled within the piece class if needed

            # Physically move the piece on the board
            self.board.board[to_pos[0]][to_pos[1]].piece = piece
            self.board.board[from_pos[0]][from_pos[1]].piece = None

            print(f"Moved piece from {from_pos} to {to_pos}")
            
            # Check for castling (King moving more than one square)
            if isinstance(piece, King) and abs(to_pos[1] - from_pos[1]) > 1:
                # Determine castling direction
                is_kingside = to_pos[1] > from_pos[1]
                row = from_pos[0]

                if is_kingside:
                    # Move the kingside rook
                    rook_from_pos = (row, 7)  # Assuming the rook is on the H file
                    rook_to_pos = (row, 5)  # Position next to the king after castling
                else:
                    # Move the queenside rook
                    rook_from_pos = (row, 0)  # Assuming the rook is on the A file
                    rook_to_pos = (row, 3)  # Position next to the king after castling

                # Move the rook
                rook = self.board.board[rook_from_pos[0]][rook_from_pos[1]].piece
                if rook:
                    self.board.board[rook_to_pos[0]][rook_to_pos[1]].piece = rook
                    self.board.board[rook_from_pos[0]][rook_from_pos[1]].piece = None
                    rook.position = rook_to_pos
                    rook.has_moved = True
                    print(f"Moved rook from {rook_from_pos} to {rook_to_pos} for castling")
 
    def display_checkmate_popup(self, winner):
        font = pygame.font.Font(None, 74)  # Use a suitable font size
        text = font.render(f"Checkmate! {winner} wins!", 1, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 50))
        
        # Button dimensions and properties
        button_text = pygame.font.Font(None, 50).render("Play Again", True, (255, 255, 255))
        button_rect = pygame.Rect(self.screen_width / 2 - 100, self.screen_height / 2 + 50, 200, 50)
        
        # Main loop for the end game screen
        end_game = True
        while end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Exit the function to prevent further code execution
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Gets the mouse position
                    if button_rect.collidepoint(mouse_pos):
                        # The button was clicked, reset the game
                        self.reset_game()
                        end_game = False
            
            # Drawing the end game screen
            # self.screen.fill((0, 0, 0))  # Clear the screen
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 20))  # Background for text
            self.screen.blit(text, text_rect)
            
            # Drawing the button
            pygame.draw.rect(self.screen, (0, 128, 0), button_rect)  # Button background
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)
            
            pygame.display.flip()

    def reset_game(self):
        # Reset or reinitialize the game state to start a new game
        # This method should reset the board, the player turn, and any other necessary state
        self.board = Board()  # Reinitialize the board or reset its state
        self.current_player = 'White'  # Reset the player turn
        # Add any other necessary state resets here
        self.run_game()


    def highlight_square(self, row, col, color=(255, 255, 0)):  # Default color is yellow for selection
        pygame.draw.rect(self.screen, color, (col*self.square_size, row*self.square_size, self.square_size, self.square_size), 5)

if __name__ == "__main__":
    main = Main()
    main.run_game()
