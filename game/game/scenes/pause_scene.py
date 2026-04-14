import pygame
from engine.core.state_manager import Scene

class PauseScene(Scene):
    def __init__(self, game, previous_scene):
        super().__init__(game)
        self.previous_scene = previous_scene

        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                # Resume
                self.game.current_scene = self.previous_scene

            elif event.key == pygame.K_m:
                # Back to menu
                from game.scenes.menu_scene import MenuScene
                self.game.current_scene = MenuScene(self.game)

            elif event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self):
        pass

    def draw(self, screen):
        # Draw previous game screen first
        self.previous_scene.draw(screen)

        # Dark overlay
        overlay = pygame.Surface((1000, 800))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Pause text
        text = self.font.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, (450, 300))

        resume = self.small_font.render("Press R to Resume", True, (255, 255, 255))
        menu = self.small_font.render("Press M for Menu", True, (255, 255, 255))

        screen.blit(resume, (420, 400))
        screen.blit(menu, (420, 450))