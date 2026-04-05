import pygame
from board import Board
from menu import Menu
from viewport import ViewPort

pygame.init()

screen = pygame.display.set_mode((1200, 980))
pygame.display.set_caption("Chess Viewport")

board = Board()
menu = Menu()
viewport = ViewPort(board, menu)

game_state = "menu"
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            result = menu.handle_input(event)
            if result == "start":
                game_state = "game"

    viewport.draw(screen, game_state)
    pygame.display.update()

pygame.quit()
