import pygame
from engine.core.state_manager import Scene
from game.board.board import Board
from engine.input.input_handler import InputHandler
from engine.systems.save_system import SaveSystem
from game.scenes.pause_scene import PauseScene


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.board = Board()
        self.input_handler = InputHandler(self)
        self.save_system = SaveSystem()

        self.current_player = 1
        self.selected_piece = None
        self.valid_moves = []

    def handle_event(self, event):

        # -------------------------
        # KEYBOARD INPUT
        # -------------------------
        if event.type == pygame.KEYDOWN:

            # Pause game
            if event.key == pygame.K_ESCAPE:
                self.game.current_scene = PauseScene(self.game, self)
                return

            # Save game
            elif event.key == pygame.K_s:
                self.save_system.save(self)

            # Load game
            elif event.key == pygame.K_l:
                data = self.save_system.load()
                if data:
                    self.board.from_dict(data["board"])
                    self.current_player = data["player"]

        # -------------------------
        # MOUSE INPUT
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = self.get_tile_from_mouse(x, y)

            if 0 <= row < 8 and 0 <= col < 8:
                self.input_handler.handle_click(row, col)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.board.draw(screen, self.selected_piece, self.valid_moves)

    def get_tile_from_mouse(self, x, y):
        tile_size = 80
        offset_x = 100
        offset_y = 100

        col = (x - offset_x) // tile_size
        row = (y - offset_y) // tile_size

        return row, col