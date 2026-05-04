import pygame
from game.board.tile import Tile

from game.pieces.pawn import Pawn
from game.pieces.rook import Rook
from game.pieces.knight import Knight
from game.pieces.bishop import Bishop
from game.pieces.queen import Queen
from game.pieces.king import King

TILE_SIZE = 80
OFFSET_X = 250
OFFSET_Y = 120

LIGHT_TILE = (238, 238, 210)
DARK_TILE = (118, 150, 86)

SELECT_COLOR = (246, 246, 105)
LAST_MOVE_COLOR = (205, 210, 106)
MOVE_DOT_COLOR = (80, 80, 80)


class Board:
    def __init__(self):
        self.tiles = []
        self.create_board()

    def create_board(self):
        self.tiles = []

        for row in range(8):
            self.tiles.append([])
            for col in range(8):
                color = LIGHT_TILE if (row + col) % 2 == 0 else DARK_TILE

                tile = Tile(
                    OFFSET_X + col * TILE_SIZE,
                    OFFSET_Y + row * TILE_SIZE,
                    TILE_SIZE,
                    color
                )
                self.tiles[row].append(tile)

        self.setup_pieces()

    def setup_pieces(self):
        for col in range(8):
            self.tiles[1][col].piece = Pawn(1, col, "black")
            self.tiles[6][col].piece = Pawn(6, col, "white")

        self.tiles[0][0].piece = Rook(0, 0, "black")
        self.tiles[0][7].piece = Rook(0, 7, "black")
        self.tiles[7][0].piece = Rook(7, 0, "white")
        self.tiles[7][7].piece = Rook(7, 7, "white")

        self.tiles[0][1].piece = Knight(0, 1, "black")
        self.tiles[0][6].piece = Knight(0, 6, "black")
        self.tiles[7][1].piece = Knight(7, 1, "white")
        self.tiles[7][6].piece = Knight(7, 6, "white")

        self.tiles[0][2].piece = Bishop(0, 2, "black")
        self.tiles[0][5].piece = Bishop(0, 5, "black")
        self.tiles[7][2].piece = Bishop(7, 2, "white")
        self.tiles[7][5].piece = Bishop(7, 5, "white")

        self.tiles[0][3].piece = Queen(0, 3, "black")
        self.tiles[7][3].piece = Queen(7, 3, "white")

        self.tiles[0][4].piece = King(0, 4, "black")
        self.tiles[7][4].piece = King(7, 4, "white")

    def draw(self, screen, selected_piece=None, valid_moves=None, last_move=None, dragging_piece=None):
        for row in range(8):
            for col in range(8):
                tile = self.tiles[row][col]
                tile.draw(screen)

                if last_move:
                    start, end = last_move
                    if (row, col) == start or (row, col) == end:
                        pygame.draw.rect(screen, LAST_MOVE_COLOR, tile.rect)

                piece = tile.piece
                if piece and piece != dragging_piece:
                    piece.draw(screen, tile.rect.x, tile.rect.y)

                if selected_piece and (row, col) == (selected_piece.row, selected_piece.col):
                    pygame.draw.rect(screen, SELECT_COLOR, tile.rect, 4)

                if valid_moves and (row, col) in valid_moves:
                    pygame.draw.circle(screen, MOVE_DOT_COLOR, tile.rect.center, 12)

    def is_empty(self, row, col):
        return self.in_bounds(row, col) and self.tiles[row][col].piece is None

    def has_enemy_piece(self, row, col, color):
        if self.in_bounds(row, col):
            piece = self.tiles[row][col].piece
            return piece and piece.color != color
        return False

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def move_piece(self, piece, row, col):
        captured_piece = self.tiles[row][col].piece

        self.tiles[piece.row][piece.col].piece = None
        self.tiles[row][col].piece = piece
        piece.row = row
        piece.col = col

        if hasattr(piece, "has_moved"):
            piece.has_moved = True

        return captured_piece

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.tiles[row][col].piece
                if piece and piece.color == color and piece.__class__.__name__ == "King":
                    return row, col
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)

        if not king_pos:
            return True

        king_row, king_col = king_pos
        enemy_color = "black" if color == "white" else "white"

        for row in range(8):
            for col in range(8):
                piece = self.tiles[row][col].piece

                if piece and piece.color == enemy_color:
                    moves = piece.get_valid_moves(self)

                    if (king_row, king_col) in moves:
                        return True

        return False

    def is_move_safe(self, piece, new_row, new_col):
        old_row = piece.row
        old_col = piece.col
        captured_piece = self.tiles[new_row][new_col].piece

        self.tiles[old_row][old_col].piece = None
        self.tiles[new_row][new_col].piece = piece
        piece.row = new_row
        piece.col = new_col

        safe = not self.is_in_check(piece.color)

        self.tiles[old_row][old_col].piece = piece
        self.tiles[new_row][new_col].piece = captured_piece
        piece.row = old_row
        piece.col = old_col

        return safe

    def get_legal_moves(self, piece):
        legal_moves = []

        for row, col in piece.get_valid_moves(self):
            if self.is_move_safe(piece, row, col):
                legal_moves.append((row, col))

        return legal_moves

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.tiles[row][col].piece

                if piece and piece.color == color:
                    if self.get_legal_moves(piece):
                        return False

        return True