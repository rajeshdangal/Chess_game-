import pygame
from engine.core.state_manager import Scene
from game.scenes.game_scene import GameScene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 50)
        self.selected = 0
        self.options = ["Two Player", "Play vs AI", "Exit"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.game.current_scene = GameScene(self.game)

                elif self.selected == 2:
                    self.game.running = False

    def draw(self, screen):
        screen.fill((30, 30, 30))

        title = self.font.render("Chess Menu", True, (255, 255, 255))
        screen.blit(title, (450, 200))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            screen.blit(text, (450, 300 + i * 60))