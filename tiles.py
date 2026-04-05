import pygame

class Tile:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.piece = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.piece :
            self.piece.draw(screen)