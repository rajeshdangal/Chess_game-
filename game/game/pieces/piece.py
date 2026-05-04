import pygame
import os
import sys


class Piece:
    SIZE = 80

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.has_moved = False

        piece_name = self.__class__.__name__.lower()
        filename = f"{piece_name}_{color}.png"

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__)
                    )
                )
            )

        path = os.path.join(base_path, "assets", "pieces", filename)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(
            self.image,
            (self.SIZE, self.SIZE)
        )

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def get_valid_moves(self, board):
        return []