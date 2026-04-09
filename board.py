import pygame
from tiles import Tile
from pawn import Pawn

class Board:
    def __init__(self):
        self.tiles = []
        self.create_board()

    def create_board(self):
        tile_size = 80
        offset_x = 100
        offset_y = 100

        # Create tiles
        for row in range(8):
            self.tiles.append([])
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)

                tile = Tile(
                    offset_x + col * tile_size,
                    offset_y + row * tile_size,
                    tile_size,
                    color
                )

                self.tiles[row].append(tile)

        # Black pawns
        for col in range(8):
            pawn = Pawn(1, col, "black")
            self.tiles[1][col].piece = pawn

        # White pawns
        for col in range(8):
            pawn = Pawn(6, col, "white")
            self.tiles[6][col].piece = pawn

    # ✅ THIS MUST BE INSIDE THE CLASS
    def draw(self, screen, selected_piece=None, valid_moves=None):
        for row in range(8):
            for col in range(8):
                tile = self.tiles[row][col]

                tile.draw(screen)

                # Highlight selected piece
                if selected_piece and (row, col) == (selected_piece.row, selected_piece.col):
                    pygame.draw.rect(screen, (0, 255, 0), tile.rect, 3)

                # Highlight valid moves
                if valid_moves and (row, col) in valid_moves:
                    pygame.draw.rect(screen, (0, 0, 255), tile.rect, 3)

    def is_empty(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.tiles[row][col].piece is None
        return False

    def has_enemy_piece(self, row, col, color):
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.tiles[row][col].piece
            return piece is not None and piece.color != color
        return False