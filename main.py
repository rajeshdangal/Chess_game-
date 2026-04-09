import pygame
from game_manager import GameManager

pygame.init()

screen = pygame.display.set_mode((1200, 980))
pygame.display.set_caption("Chess Viewport")

game = GameManager()

while game.running:
    for event in pygame.event.get():
        game.handle_events(event)

    game.draw(screen)
    pygame.display.update()

pygame.quit()