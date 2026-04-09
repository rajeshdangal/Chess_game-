import pygame
from board import Board
from menu import Menu
from viewport import ViewPort
from database_manager import DatabaseManager

class GameManager:
    def __init__(self):
        self.board = Board()
        self.menu = Menu()
        self.viewport = ViewPort(self.board, self.menu)
        self.db = DatabaseManager()

        self.state = "menu"
        self.running = True

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
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    self.db.save(self.board)

                elif event.key == pygame.K_l:
                    data = self.db.load()
                    if data:
                        self.board.from_dict(data["board"])

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

    def draw(self, screen):
        self.viewport.draw(screen, self.state)