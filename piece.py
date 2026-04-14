import pygame

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen):
        color = (25, 55, 55) if self.color == "white" else (0, 0, 0)

        pygame.draw.circle(
            screen,
            color,
            (self.col * 80 + 140, self.row * 80 + 140),
            20
        )