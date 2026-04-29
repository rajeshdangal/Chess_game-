import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen, x, y):

        # White and Black pieces
        piece_color = (245, 245, 245) if self.color == "white" else (30, 30, 30)

        # Outline for visibility
        outline_color = (0, 0, 0) if self.color == "white" else (255, 255, 255)

        # Draw main piece
        pygame.draw.circle(screen, piece_color, (x + 40, y + 40), 25)

        # Draw border
        pygame.draw.circle(screen, outline_color, (x + 40, y + 40), 25, 2)