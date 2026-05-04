import pygame
from game.save_manager import save_game, load_game
from game.board.board import Board
from game.ai.chess_ai import ChessAI

TILE_SIZE = 80
OFFSET_X = 250
OFFSET_Y = 120
SIDE_PANEL_X = 20


class GameScene:
    def __init__(self, game, ai_enabled=True):
        self.game = game
        self.board = Board()

        self.selected_piece = None
        self.valid_moves = []
        self.last_move = None

        self.dragging = False
        self.dragging_piece = None
        self.drag_pos = (0, 0)

        self.animating = False
        self.animation_piece = None
        self.animation_start = (0, 0)
        self.animation_end = (0, 0)
        self.animation_progress = 0
        self.animation_speed = 0.15

        self.turn = "white"
        self.move_history = []

        self.ai_enabled = ai_enabled
        self.ai = ChessAI("black", depth=2)

        self.game_over = False
        self.winner = None

        self.captured_white = []
        self.captured_black = []

        self.turn_font = pygame.font.Font(None, 42)
        self.win_font = pygame.font.Font(None, 70)
        self.captured_font = pygame.font.Font(None, 30)

        self.pause_button = pygame.Rect(SIDE_PANEL_X + 25, 700, 70, 70)
        self.restart_button = pygame.Rect(SIDE_PANEL_X + 120, 700, 70, 70)

    def restart_game(self):
        self.board = Board()
        self.selected_piece = None
        self.valid_moves = []
        self.last_move = None
        self.dragging = False
        self.dragging_piece = None
        self.drag_pos = (0, 0)
        self.animating = False
        self.animation_piece = None
        self.animation_progress = 0
        self.turn = "white"
        self.move_history = []
        self.game_over = False
        self.winner = None
        self.captured_white = []
        self.captured_black = []

    def pause_game(self):
        save_game(self.board, self.turn, self.move_history)

        from game.scenes.menu_scene import MenuScene
        self.game.current_scene = MenuScene(self.game)

    def start_animation(self, piece, old_row, old_col, new_row, new_col):
        self.animating = True
        self.animation_piece = piece
        self.animation_start = (
            OFFSET_X + old_col * TILE_SIZE,
            OFFSET_Y + old_row * TILE_SIZE
        )
        self.animation_end = (
            OFFSET_X + new_col * TILE_SIZE,
            OFFSET_Y + new_row * TILE_SIZE
        )
        self.animation_progress = 0

    def finish_move(self, piece, old_row, old_col, row, col):
        captured_piece = self.board.move_piece(piece, row, col)

        if captured_piece:
            if captured_piece.color == "white":
                self.captured_white.append(captured_piece)
            else:
                self.captured_black.append(captured_piece)

        self.last_move = ((old_row, old_col), (row, col))

        self.move_history.append({
            "piece": piece.__class__.__name__,
            "color": piece.color,
            "from": [old_row, old_col],
            "to": [row, col],
            "captured": captured_piece.__class__.__name__ if captured_piece else None
        })

    def check_game_status(self):
        if self.board.is_checkmate(self.turn):
            self.game_over = True
            self.winner = "White" if self.turn == "black" else "Black"
        elif self.board.is_stalemate(self.turn):
            self.game_over = True
            self.winner = "Draw"

    def make_ai_move(self):
        move = self.ai.choose_move(self.board)

        if move is None:
            self.check_game_status()
            return

        piece, row, col = move
        old_row = piece.row
        old_col = piece.col

        self.finish_move(piece, old_row, old_col, row, col)
        self.start_animation(piece, old_row, old_col, row, col)

        self.turn = "white"
        self.check_game_status()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_game()

            if event.key == pygame.K_s:
                save_game(self.board, self.turn, self.move_history)

            if event.key == pygame.K_l:
                data = load_game(self.board)
                if data:
                    self.turn = data["current_turn"]
                    self.move_history = data["move_history"]
                    self.selected_piece = None
                    self.valid_moves = []
                    self.last_move = None
                    self.dragging = False
                    self.dragging_piece = None
                    self.animating = False
                    self.animation_piece = None
                    self.game_over = False
                    self.winner = None
                    self.captured_white = []
                    self.captured_black = []

            if event.key == pygame.K_r:
                self.restart_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.pause_button.collidepoint(event.pos):
                self.pause_game()
                return

            if self.restart_button.collidepoint(event.pos):
                self.restart_game()
                return

        if self.game_over or self.animating:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            col = (x - OFFSET_X) // TILE_SIZE
            row = (y - OFFSET_Y) // TILE_SIZE

            if not (0 <= row < 8 and 0 <= col < 8):
                return

            tile = self.board.tiles[row][col]

            if (
                tile.piece
                and tile.piece.color == self.turn
                and (not self.ai_enabled or self.turn == "white")
            ):
                self.selected_piece = tile.piece
                self.valid_moves = self.board.get_legal_moves(tile.piece)
                self.dragging = True
                self.dragging_piece = tile.piece
                self.drag_pos = event.pos

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.drag_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging and self.dragging_piece:
                x, y = event.pos
                col = (x - OFFSET_X) // TILE_SIZE
                row = (y - OFFSET_Y) // TILE_SIZE

                if (0 <= row < 8 and 0 <= col < 8) and (row, col) in self.valid_moves:
                    piece = self.dragging_piece
                    old_row = piece.row
                    old_col = piece.col

                    self.finish_move(piece, old_row, old_col, row, col)
                    self.start_animation(piece, old_row, old_col, row, col)

                    self.turn = "black" if self.turn == "white" else "white"
                    self.check_game_status()

                self.dragging = False
                self.dragging_piece = None
                self.selected_piece = None
                self.valid_moves = []

    def update(self):
        if self.animating:
            self.animation_progress += self.animation_speed

            if self.animation_progress >= 1:
                self.animation_progress = 1
                self.animating = False
                self.animation_piece = None

                if self.turn == "black" and self.ai_enabled and not self.game_over:
                    self.make_ai_move()

    def draw_captured_pieces(self, screen):
        panel_x = SIDE_PANEL_X
        panel_y = OFFSET_Y
        panel_w = 210
        panel_h = 560

        pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_w, panel_h), border_radius=14)

        title_black = self.captured_font.render("Black Captured", True, (255, 215, 0))
        title_white = self.captured_font.render("White Captured", True, (255, 215, 0))

        screen.blit(title_black, (panel_x + 20, panel_y + 30))
        screen.blit(title_white, (panel_x + 20, panel_y + 285))

        spacing = 40

        for index, piece in enumerate(self.captured_black):
            x = panel_x + 20 + (index % 4) * spacing
            y = panel_y + 75 + (index // 4) * spacing
            small_image = pygame.transform.scale(piece.image, (34, 34))
            screen.blit(small_image, (x, y))

        for index, piece in enumerate(self.captured_white):
            x = panel_x + 20 + (index % 4) * spacing
            y = panel_y + 330 + (index // 4) * spacing
            small_image = pygame.transform.scale(piece.image, (34, 34))
            screen.blit(small_image, (x, y))

    def draw_icon_button(self, screen, rect, icon_type):
        mouse = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse)

        if hovered:
            pygame.draw.rect(screen, (255, 215, 0), rect.inflate(10, 10), border_radius=20)

        color = (90, 90, 180) if hovered else (40, 40, 90)

        pygame.draw.rect(screen, color, rect, border_radius=18)
        pygame.draw.rect(screen, (255, 215, 0), rect, 2, border_radius=18)

        icon_color = (255, 255, 255)

        if icon_type == "pause":
            bar_w = 10
            bar_h = 34
            gap = 10
            center_x = rect.centerx
            center_y = rect.centery

            left_bar = pygame.Rect(center_x - gap - bar_w, center_y - bar_h // 2, bar_w, bar_h)
            right_bar = pygame.Rect(center_x + gap, center_y - bar_h // 2, bar_w, bar_h)

            pygame.draw.rect(screen, icon_color, left_bar, border_radius=3)
            pygame.draw.rect(screen, icon_color, right_bar, border_radius=3)

        elif icon_type == "restart":
            center = rect.center
            radius = 22

            pygame.draw.arc(
                screen,
                icon_color,
                (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                0.6,
                5.3,
                5
            )

            arrow_points = [
                (center[0] + 18, center[1] - 22),
                (center[0] + 31, center[1] - 17),
                (center[0] + 22, center[1] - 6)
            ]
            pygame.draw.polygon(screen, icon_color, arrow_points)

    def draw(self, screen):
        screen.fill((40, 40, 40))

        hidden_piece = self.dragging_piece or self.animation_piece
        check_color = self.turn if self.board.is_in_check(self.turn) else None

        self.board.draw(
            screen,
            self.selected_piece,
            self.valid_moves,
            self.last_move,
            hidden_piece,
            check_color
        )

        self.draw_captured_pieces(screen)

        self.draw_icon_button(screen, self.pause_button, "pause")
        self.draw_icon_button(screen, self.restart_button, "restart")

        if self.animating and self.animation_piece:
            sx, sy = self.animation_start
            ex, ey = self.animation_end

            x = sx + (ex - sx) * self.animation_progress
            y = sy + (ey - sy) * self.animation_progress

            self.animation_piece.draw(screen, x, y)

        if self.dragging and self.dragging_piece:
            x, y = self.drag_pos
            self.dragging_piece.draw(screen, x - TILE_SIZE // 2, y - TILE_SIZE // 2)

        if self.game_over:
            if self.winner == "Draw":
                message = "Draw by Stalemate"
            else:
                message = f"Checkmate! {self.winner} Wins!"
            text_surface = self.win_font.render(message, True, (255, 215, 0))
        else:
            if check_color:
                message = f"{self.turn.capitalize()} is in Check!"
            else:
                message = f"{self.turn.capitalize()}'s Turn"
            text_surface = self.turn_font.render(message, True, (255, 215, 0))

        text_rect = text_surface.get_rect(center=(OFFSET_X + 4 * TILE_SIZE, 60))
        screen.blit(text_surface, text_rect)