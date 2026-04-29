import pygame
from game.board.board import Board

TILE_SIZE = 80
OFFSET_X = 100
OFFSET_Y = 100


class GameScene:
    def __init__(self, game):
        self.game = game
        self.board = Board()

        self.selected_piece = None
        self.valid_moves = []

        self.turn = "white"

        # Game over system
        self.game_over = False
        self.winner = None

        self.font = pygame.font.Font(None, 60)

    # ----------------------------
    # HANDLE EVENTS
    # ----------------------------
    def handle_event(self, event):

        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            col = (x - OFFSET_X) // TILE_SIZE
            row = (y - OFFSET_Y) // TILE_SIZE

            if not (0 <= row < 8 and 0 <= col < 8):
                return

            tile = self.board.tiles[row][col]

            # If piece already selected
            if self.selected_piece:

                # Move if valid
                if (row, col) in self.valid_moves:

                    result = self.board.move_piece(self.selected_piece, row, col)

                    # Check winner
                    if result:
                        self.game_over = True
                        self.winner = result
                    else:
                        # Switch turn
                        self.turn = "black" if self.turn == "white" else "white"

                # Reset selection
                self.selected_piece = None
                self.valid_moves = []

            # Select piece
            elif tile.piece and tile.piece.color == self.turn:
                self.selected_piece = tile.piece
                self.valid_moves = tile.piece.get_valid_moves(self.board)

    # ----------------------------
    # UPDATE
    # ----------------------------
    def update(self):
        pass

    # ----------------------------
    # DRAW
    # ----------------------------
    def draw(self, screen):
        screen.fill((200, 200, 200))

        # Draw board
        self.board.draw(screen, self.selected_piece, self.valid_moves)

        # Show turn
        turn_text = self.font.render(f"{self.turn.capitalize()}'s Turn", True, (0, 0, 0))
        screen.blit(turn_text, (250, 30))

        # Game Over Screen
        if self.game_over:
            overlay = pygame.Surface((800, 800))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            win_text = self.font.render(self.winner, True, (255, 255, 255))
            screen.blit(win_text, (250, 350))