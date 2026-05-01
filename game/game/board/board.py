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

    # =========================================================
    # CREATE BOARD
    # =========================================================
    def create_board(self):
        self.tiles = []

        for row in range(8):
            self.tiles.append([])

            for col in range(8):

                # Light chess board colors
                color = (
                    (240, 217, 181)
                    if (row + col) % 2 == 0
                    else (181, 136, 99)
                )

                tile = Tile(
                    OFFSET_X + col * TILE_SIZE,
                    OFFSET_Y + row * TILE_SIZE,
                    TILE_SIZE,
                    color
                )

                self.tiles[row].append(tile)

        self.setup_pieces()

    # =========================================================
    # SETUP PIECES
    # =========================================================
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

    # =========================================================
    # DRAW
    # =========================================================
    def draw(self, screen, selected_piece=None, valid_moves=None):
        for row in range(8):
            for col in range(8):

                tile = self.tiles[row][col]
                tile.draw(screen)

                # Selected piece
                if (
                    selected_piece
                    and (row, col) == (selected_piece.row, selected_piece.col)
                ):
                    pygame.draw.rect(screen, (0, 255, 0), tile.rect, 3)

                # Valid moves
                if valid_moves and (row, col) in valid_moves:
                    pygame.draw.rect(screen, (0, 0, 255), tile.rect, 3)

    # =========================================================
    # BASIC HELPERS
    # =========================================================
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

    # =========================================================
    # KING LOCATION
    # =========================================================
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.tiles[row][col].piece

                if (
                    piece
                    and piece.color == color
                    and piece.__class__.__name__ == "King"
                ):
                    return (row, col)

        return None

    # =========================================================
    # CHECK IF SQUARE IS ATTACKED
    # =========================================================
    def is_square_under_attack(self, row, col, color):

        enemy_color = "black" if color == "white" else "white"

        for r in range(8):
            for c in range(8):

                piece = self.tiles[r][c].piece

                if piece and piece.color == enemy_color:

                    moves = piece.get_valid_moves(self)

                    if (row, col) in moves:
                        return True

        return False

    # =========================================================
    # CHECK STATE
    # =========================================================
    def is_in_check(self, color):

        king_pos = self.find_king(color)

        if not king_pos:
            return False

        return self.is_square_under_attack(
            king_pos[0],
            king_pos[1],
            color
        )

    # =========================================================
    # SAFE MOVE VALIDATION
    # =========================================================
    def is_valid_move_safe(self, piece, new_row, new_col):

        old_row, old_col = piece.row, piece.col
        captured_piece = self.tiles[new_row][new_col].piece

        # Temporary move
        self.tiles[old_row][old_col].piece = None
        self.tiles[new_row][new_col].piece = piece

        piece.row = new_row
        piece.col = new_col

        in_check = self.is_in_check(piece.color)

        # Undo move
        self.tiles[old_row][old_col].piece = piece
        self.tiles[new_row][new_col].piece = captured_piece

        piece.row = old_row
        piece.col = old_col

        return not in_check

    # =========================================================
    # ONLY KINGS LEFT
    # =========================================================
    def only_kings_left(self):

        pieces = []

        for row in range(8):
            for col in range(8):
                piece = self.tiles[row][col].piece

                if piece:
                    pieces.append(piece.__class__.__name__)

        return len(pieces) == 2 and pieces.count("King") == 2

    # =========================================================
    # MOVE PIECE
    # =========================================================
    def move_piece(self, piece, row, col):

        target_piece = self.tiles[row][col].piece
        capture_happened = target_piece is not None

        # Normal move
        self.tiles[piece.row][piece.col].piece = None
        self.tiles[row][col].piece = piece

        piece.row = row
        piece.col = col

        if hasattr(piece, "has_moved"):
            piece.has_moved = True

        return {
            "capture": capture_happened
        }