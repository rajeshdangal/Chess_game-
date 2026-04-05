import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 60)

    def draw(self, screen):
        screen.fill((30, 30, 30))

        text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(text, (300, 400))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"
        return None