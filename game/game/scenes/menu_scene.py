import pygame
from game.scenes.game_scene import GameScene
from game.save_manager import load_game


class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

        self.base_color = (40, 40, 90)
        self.hover_color = (90, 90, 180)
        self.border_color = (255, 215, 0)
        self.text_color = (255, 255, 255)

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        if hovered:
            glow_rect = self.rect.inflate(12, 12)
            pygame.draw.rect(screen, (255, 215, 0), glow_rect, border_radius=18)

        color = self.hover_color if hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=15)

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class MenuScene:
    def __init__(self, game):
        self.game = game

        self.width = 1300
        self.height = 900

        self.title_font = pygame.font.Font(None, 100)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 42)

        button_width = 280
        button_height = 60
        center_x = (self.width - button_width) // 2
        start_y = 260
        gap = 85

        self.buttons = [
            Button("Play with AI", center_x, start_y, button_width, button_height, "ai"),
            Button("Multiplayer", center_x, start_y + gap, button_width, button_height, "multi"),
            Button("Resume Game", center_x, start_y + gap * 2, button_width, button_height, "resume"),
            Button("Exit", center_x, start_y + gap * 3, button_width, button_height, "exit")
        ]

        self.particles = []
        for i in range(40):
            x = (i * 37) % self.width
            y = (i * 17) % self.height
            speed = (i % 3) + 1
            self.particles.append([x, y, speed])

    def handle_event(self, event):
        for button in self.buttons:
            if button.clicked(event):

                if button.action == "ai":
                    self.game.current_scene = GameScene(self.game)

                elif button.action == "multi":
                    self.game.current_scene = GameScene(self.game)

                elif button.action == "resume":
                    scene = GameScene(self.game)
                    data = load_game(scene.board)

                    if data:
                        scene.turn = data["current_turn"]
                        scene.move_history = data["move_history"]
                        scene.selected_piece = None
                        scene.valid_moves = []
                        self.game.current_scene = scene
                        print("Saved game resumed!")
                    else:
                        print("No saved game found.")

                elif button.action == "exit":
                    pygame.quit()
                    exit()

    def update(self):
        for particle in self.particles:
            particle[1] += particle[2]

            if particle[1] > self.height:
                particle[1] = 0

    def draw_background(self, screen):
        for y in range(self.height):
            color_value = int(20 + (y / self.height) * 40)
            pygame.draw.line(screen, (10, 10, color_value), (0, y), (self.width, y))

        for x, y, speed in self.particles:
            pygame.draw.circle(screen, (255, 215, 0), (x, y), 2)

    def draw_title(self, screen):
        title = self.title_font.render("CHESS MASTER", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.width // 2, 120))
        screen.blit(title, title_rect)

        subtitle = self.subtitle_font.render(
            "Strategy • Intelligence • Victory",
            True,
            (220, 220, 220)
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 180))
        screen.blit(subtitle, subtitle_rect)

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_title(screen)

        for button in self.buttons:
            button.draw(screen, self.button_font)