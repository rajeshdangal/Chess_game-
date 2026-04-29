import pygame
import os

class Piece:
    SIZE = 80

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        piece_name = self.__class__.__name__.lower()
        filename = f"{piece_name}_{color}.png"

        # 🔥 FIXED PATH (absolute based on project)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        path = os.path.join(base_path, "assets", "pieces", filename)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))