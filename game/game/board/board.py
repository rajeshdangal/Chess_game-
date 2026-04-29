import pygame
from game.board.tile import Tile

from game.pieces.pawn import Pawn
from game.pieces.rook import Rook
from game.pieces.knight import Knight
from game.pieces.bishop import Bishop
from game.pieces.queen import Queen
from game.pieces.king import King

TILE_SIZE = 80
OFFSET_X = 100
OFFSET_Y = 100


class Board:
    def __init__(self):
        self.tiles = []
        self.create_board()

    # ----------------------------
    # CREATE BOARD
    # ----------------------------
    def create_board(self):
        self.tiles = []

        for row in range(8):
            self.tiles.append([])
            for col in range(8):

                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)

                tile = Tile(
                    OFFSET_X + col * TILE_SIZE,
                    OFFSET_Y + row * TILE_SIZE,
                    TILE_SIZE,
                    color
                )

                self.tiles[row].append(tile)

        self.setup_pieces()

    # ----------------------------
    # SETUP ALL PIECES
    # ----------------------------
    def setup_pieces(self):

        # Pawns
        for col in range(8):
            self.tiles[1][col].piece = Pawn(1, col, "black")
            self.tiles[6][col].piece = Pawn(6, col, "white")

        # Rooks
        self.tiles[0][0].piece = Rook(0, 0, "black")
        self.tiles[0][7].piece = Rook(0, 7, "black")
        self.tiles[7][0].piece = Rook(7, 0, "white")
        self.tiles[7][7].piece = Rook(7, 7, "white")

        # Knights
        self.tiles[0][1].piece = Knight(0, 1, "black")
        self.tiles[0][6].piece = Knight(0, 6, "black")
        self.tiles[7][1].piece = Knight(7, 1, "white")
        self.tiles[7][6].piece = Knight(7, 6, "white")

        # Bishops
        self.tiles[0][2].piece = Bishop(0, 2, "black")
        self.tiles[0][5].piece = Bishop(0, 5, "black")
        self.tiles[7][2].piece = Bishop(7, 2, "white")
        self.tiles[7][5].piece = Bishop(7, 5, "white")

        # Queens
        self.tiles[0][3].piece = Queen(0, 3, "black")
        self.tiles[7][3].piece = Queen(7, 3, "white")

        # Kings
        self.tiles[0][4].piece = King(0, 4, "black")
        self.tiles[7][4].piece = King(7, 4, "white")

    # ----------------------------
    # DRAW
    # ----------------------------
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

    # ----------------------------
    # HELPERS
    # ----------------------------
    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        if self.in_bounds(row, col):
            return self.tiles[row][col].piece is None
        return False

    def has_enemy_piece(self, row, col, color):
        if self.in_bounds(row, col):
            piece = self.tiles[row][col].piece
            return piece is not None and piece.color != color
        return False

    # ----------------------------
    # MOVE PIECE + KING CAPTURE
    # ----------------------------
    def move_piece(self, piece, row, col):

        target_piece = self.tiles[row][col].piece

        # If king is captured → game over
        if target_piece and target_piece.__class__.__name__ == "King":
            self.tiles[piece.row][piece.col].piece = None
            self.tiles[row][col].piece = piece

            piece.row = row
            piece.col = col

            return f"Congratulations {piece.color.capitalize()} Wins!"

        # Normal move
        self.tiles[piece.row][piece.col].piece = None
        self.tiles[row][col].piece = piece

        piece.row = row
        piece.col = col

        if hasattr(piece, "has_moved"):
            piece.has_moved = True

        return None