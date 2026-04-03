import pygame
from tiles import draw_tile
pygame.init()


screen = pygame.display.set_mode((1200,980))
pygame.display.set_caption("chess viewport try")

running = True
screen.fill((255,255,255))
draw_tile(screen)
pygame.display.update()
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
pygame.quit()

