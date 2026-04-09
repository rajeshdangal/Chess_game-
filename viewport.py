import pygame

class ViewPort:
    def __init__(self, board, menu):
        self.board = board
        self.menu = menu

    def draw(self, screen, state):
        if state == "menu":
            self.menu.draw(screen)

        elif state == "game":
            screen.fill((255, 255, 255))
            self.board.draw(screen)

        elif state == "pause":
            # draw game in background
            screen.fill((255, 255, 255))
            self.board.draw(screen)

            # dark overlay
            overlay = pygame.Surface((1200, 980))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # text
            font = pygame.font.SysFont(None, 60)

            text1 = font.render("PAUSED", True, (255, 255, 255))
            text2 = font.render("R = Resume", True, (255, 255, 255))
            text3 = font.render("M = Menu", True, (255, 255, 255))

            screen.blit(text1, (500, 300))
            screen.blit(text2, (450, 400))
            screen.blit(text3, (450, 470))