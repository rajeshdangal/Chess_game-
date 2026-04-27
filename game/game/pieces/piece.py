import pygame

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen, x, y):
        color = (255, 0, 0) if self.color == "white" else (0, 0, 255)
        pygame.draw.circle(screen, color, (x + 40, y + 40), 20)

    def get_valid_moves(self, board):
        return []