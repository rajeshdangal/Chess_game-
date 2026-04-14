import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)