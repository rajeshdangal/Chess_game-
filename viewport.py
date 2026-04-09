import pygame

class ViewPort:
    def __init__(self, board, menu):
        self.board = board
        self.menu = menu

    def draw(self, screen, state, selected_piece, valid_moves):
        if state == "menu":
            self.menu.draw(screen)

        elif state == "game":
            screen.fill((255, 255, 255))

            # Draw board + pieces + highlights
            self.board.draw(screen, selected_piece, valid_moves)

        elif state == "pause":
            screen.fill((50, 50, 50))

            font = pygame.font.SysFont(None, 60)
            text = font.render("PAUSED", True, (255, 255, 255))
            screen.blit(text, (500, 400))

            small_font = pygame.font.SysFont(None, 40)

            resume = small_font.render("Press R to Resume", True, (255, 255, 255))
            menu = small_font.render("Press M for Menu", True, (255, 255, 255))
            quit_text = small_font.render("Press ESC to Quit", True, (255, 255, 255))

            screen.blit(resume, (450, 500))
            screen.blit(menu, (450, 550))
            screen.blit(quit_text, (450, 600))