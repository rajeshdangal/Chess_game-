import pygame
import os


class Piece:
    SIZE = 80

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

<<<<<<< HEAD
    def draw(self, screen, x, y):

        # White and Black pieces
        piece_color = (245, 245, 245) if self.color == "white" else (30, 30, 30)

        # Outline for visibility
        outline_color = (0, 0, 0) if self.color == "white" else (255, 255, 255)

        # Draw main piece
        pygame.draw.circle(screen, piece_color, (x + 40, y + 40), 25)

        # Draw border
        pygame.draw.circle(screen, outline_color, (x + 40, y + 40), 25, 2)
=======
        piece_name = self.__class__.__name__.lower()
        filename = f"{piece_name}_{color}.png"

        # 🔥 FIXED PATH (absolute based on project)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        path = os.path.join(base_path, "assets", "pieces", filename)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
>>>>>>> 49c4671 (changed the board)
