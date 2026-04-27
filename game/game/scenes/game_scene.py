import pygame
from game.board.board import Board

TILE_SIZE = 80
OFFSET_X = 100
OFFSET_Y = 100

class GameScene:
    def __init__(self, game):
        self.game = game
        self.board = Board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = "white"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            col = (x - OFFSET_X) // TILE_SIZE
            row = (y - OFFSET_Y) // TILE_SIZE

            if not (0 <= row < 8 and 0 <= col < 8):
                return

            tile = self.board.tiles[row][col]

            if self.selected_piece:
                if (row, col) in self.valid_moves:
                    self.board.move_piece(self.selected_piece, row, col)
                    self.turn = "black" if self.turn == "white" else "white"

                self.selected_piece = None
                self.valid_moves = []

            elif tile.piece and tile.piece.color == self.turn:
                self.selected_piece = tile.piece
                self.valid_moves = tile.piece.get_valid_moves(self.board)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((200, 200, 200))
        self.board.draw(screen, self.selected_piece, self.valid_moves)
