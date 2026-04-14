import pygame
from game.board.tile import Tile
from game.pieces.pawn import Pawn

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

                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)

                tile = Tile(
                    OFFSET_X + col * TILE_SIZE,
                    OFFSET_Y + row * TILE_SIZE,
                    TILE_SIZE,
                    color
                )

                self.tiles[row].append(tile)

        self.setup_pawns()

    def setup_pawns(self):
        # Black pawns
        for col in range(8):
            pawn = Pawn(1, col, "black")
            self.tiles[1][col].piece = pawn

        # White pawns
        for col in range(8):
            pawn = Pawn(6, col, "white")
            self.tiles[6][col].piece = pawn

    # ----------------------------
    # DRAW
    # ----------------------------
    def draw(self, screen, selected_piece=None, valid_moves=None):
        for row in range(8):
            for col in range(8):
                tile = self.tiles[row][col]

                tile.draw(screen)

                # Highlight selected
                if selected_piece and (row, col) == (selected_piece.row, selected_piece.col):
                    pygame.draw.rect(screen, (0, 255, 0), tile.rect, 3)

                # Highlight valid moves
                if valid_moves and (row, col) in valid_moves:
                    pygame.draw.rect(screen, (0, 0, 255), tile.rect, 3)

    # ----------------------------
    # LOGIC HELPERS
    # ----------------------------
    def is_empty(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.tiles[row][col].piece is None
        return False

    def has_enemy_piece(self, row, col, color):
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.tiles[row][col].piece
            return piece is not None and piece.color != color
        return False

    # ----------------------------
    # SERIALIZATION (SAVE)
    # ----------------------------
    def to_dict(self):
        data = []

        for row in range(8):
            row_data = []
            for col in range(8):
                piece = self.tiles[row][col].piece

                if piece:
                    row_data.append({
                        "type": piece.__class__.__name__,
                        "color": piece.color,
                        "row": piece.row,
                        "col": piece.col,
                        "has_moved": getattr(piece, "has_moved", False)
                    })
                else:
                    row_data.append(None)

            data.append(row_data)

        return data

    # ----------------------------
    # DESERIALIZATION (LOAD)
    # ----------------------------
    def from_dict(self, data):
        self.create_board()  # reset board

        for row in range(8):
            for col in range(8):

                piece_data = data[row][col]

                if piece_data:
                    piece = self.create_piece(piece_data)
                    self.tiles[row][col].piece = piece

    # ----------------------------
    # FACTORY (CREATE PIECES)
    # ----------------------------
    def create_piece(self, data):
        piece_type = data["type"]
        color = data["color"]
        row = data["row"]
        col = data["col"]

        if piece_type == "Pawn":
            piece = Pawn(row, col, color)
            piece.has_moved = data.get("has_moved", False)
            return piece

        # Later:
        # if piece_type == "Rook": return Rook(...)
        # if piece_type == "Knight": return Knight(...)

        return None