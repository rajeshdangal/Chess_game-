import pygame
from board import Board
from menu import Menu
from viewport import ViewPort
from database_manager import DatabaseManager
from input_handler import InputHandler

class GameManager:
    def __init__(self):
        self.board = Board()
        self.menu = Menu()
        self.viewport = ViewPort(self.board, self.menu)
        self.db = DatabaseManager()

        self.input_handler = InputHandler(self)

        self.state = "menu"
        self.running = True

        # Turn system
        self.current_player = 1  # 1 = white, 2 = black

        # Selection system
        self.selected_piece = None
        self.valid_moves = []

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        # -------- MENU --------
        if self.state == "menu":
            result = self.menu.handle_input(event)

            if result == "two_player":
                self.board = Board()
                self.viewport.board = self.board
                self.state = "game"

            elif result == "ai":
                self.board = Board()
                self.viewport.board = self.board
                self.state = "game"

            elif result == "exit":
                self.running = False

        # -------- GAME --------
        elif self.state == "game":

            # Mouse input → selection + movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = self.get_tile_from_mouse(x, y)

                if 0 <= row < 8 and 0 <= col < 8:
                    self.input_handler.handle_click(row, col)

            # Keyboard input
            if event.type == pygame.KEYDOWN:

                # Save game
                if event.key == pygame.K_s:
                    self.db.save(self.board)

                # Load game
                elif event.key == pygame.K_l:
                    data = self.db.load()
                    if data:
                        self.board.from_dict(data["board"])

                # Pause
                elif event.key == pygame.K_ESCAPE:
                    self.state = "pause"

        # -------- PAUSE --------
        elif self.state == "pause":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    self.state = "game"

                elif event.key == pygame.K_m:
                    self.state = "menu"

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def get_tile_from_mouse(self, x, y):
        tile_size = 80
        offset_x = 100
        offset_y = 100

        col = (x - offset_x) // tile_size
        row = (y - offset_y) // tile_size

        return row, col

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def draw(self, screen):
        self.viewport.draw(
            screen,
            self.state,
            self.selected_piece,
            self.valid_moves
        )