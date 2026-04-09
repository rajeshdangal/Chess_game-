import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)
        self.selected = 0  # 0 = Two Player, 1 = AI, 2 = Exit

        self.options = ["Two Player", "Play vs AI", "Exit"]

    def draw(self, screen):
        screen.fill((30, 30, 30))

        title = self.font.render("Chess Menu", True, (255, 255, 255))
        screen.blit(title, (450, 200))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            screen.blit(text, (450, 300 + i * 60))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    return "two_player"
                elif self.selected == 1:
                    return "ai"
                elif self.selected == 2:
                    return "exit"

        return None