import pygame
import os


class Piece:
    SIZE = 80

    def __init__(self, row, col, color):
        """
        Base class for all chess pieces.

        Args:
            row (int): Board row position
            col (int): Board column position
            color (str): "white" or "black"
        """
        self.row = row
        self.col = col
        self.color = color

        # Get piece class name automatically (rook, bishop, pawn, etc.)
        piece_name = self.__class__.__name__.lower()

        # Example: rook_white.png / rook_black.png
        filename = f"{piece_name}_{self.color}.png"

        # Absolute path to project root:
        # game/game/pieces/piece.py -> go up 4 folders
        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        )

        # Full image path
        image_path = os.path.join(base_path, "assets", "pieces", filename)

        # Load piece image safely
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(
                self.image, (self.SIZE, self.SIZE)
            )
        else:
            # Fallback if image missing
            print(f"Warning: Missing image file -> {image_path}")
            self.image = None

    def move(self, row, col):
        """
        Update piece position.
        """
        self.row = row
        self.col = col

    def draw(self, screen, x, y):
        """
        Draw the piece on the board.
        """
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            # Emergency fallback visual if image is missing
            piece_color = (245, 245, 245) if self.color == "white" else (30, 30, 30)
            outline_color = (0, 0, 0) if self.color == "white" else (255, 255, 255)

            pygame.draw.circle(screen, piece_color, (x + self.SIZE // 2, y + self.SIZE // 2), 25)
            pygame.draw.circle(screen, outline_color, (x + self.SIZE // 2, y + self.SIZE // 2), 25, 2)

    def valid_moves(self, board):
        """
        Override this in child classes (Pawn, Rook, Bishop, etc.)
        Returns a list of valid moves.
        """
        return []