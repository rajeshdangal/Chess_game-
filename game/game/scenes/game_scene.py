import pygame
from game.board.board import Board

TILE_SIZE = 80
OFFSET_X = 100
OFFSET_Y = 100


class GameScene:
    def __init__(self, game):
        self.game = game
        self.board = Board()

        self.selected_piece = None
        self.valid_moves = []

        self.turn = "white"

        # =====================================================
        # STATES
        # =====================================================
        self.game_over = False
        self.winner = None
        self.paused = False

        # 16 move rule
        self.no_capture_or_pawn_moves = 0

        # =====================================================
        # FONTS
        # =====================================================
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 40)

        # =====================================================
        # BUTTONS
        # =====================================================
        # Top right pause button
        self.pause_button = pygame.Rect(650, 20, 120, 40)

        # Pause menu
        self.resume_button = pygame.Rect(300, 300, 200, 50)
        self.menu_button = pygame.Rect(300, 380, 200, 50)

        # Game over menu
        self.play_again_button = pygame.Rect(300, 380, 200, 50)
        self.game_over_menu_button = pygame.Rect(300, 460, 200, 50)

    # =====================================================
    # CHECK FOR ANY VALID MOVES
    # =====================================================
    def has_any_valid_moves(self, color):

        for row in range(8):
            for col in range(8):

                piece = self.board.tiles[row][col].piece

                if piece and piece.color == color:

                    moves = piece.get_valid_moves(self.board)

                    for move in moves:

                        if self.board.is_valid_move_safe(
                            piece,
                            move[0],
                            move[1]
                        ):
                            return True

        return False

    # =====================================================
    # HANDLE EVENTS
    # =====================================================
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            # -------------------------------------------------
            # PAUSE BUTTON
            # -------------------------------------------------
            if self.pause_button.collidepoint(event.pos) and not self.game_over:
                self.paused = not self.paused

                if self.paused:
                    self.game.saved_scene = self

                return

            # -------------------------------------------------
            # PAUSE MENU
            # -------------------------------------------------
            if self.paused:

                # Resume
                if self.resume_button.collidepoint(event.pos):
                    self.paused = False
                    return

                # Main Menu
                if self.menu_button.collidepoint(event.pos):
                    from game.scenes.menu_scene import MenuScene
                    self.game.saved_scene = self
                    self.game.current_scene = MenuScene(self.game)
                    return

                return

            # -------------------------------------------------
            # GAME OVER MENU
            # -------------------------------------------------
            if self.game_over:

                # Play Again
                if self.play_again_button.collidepoint(event.pos):
                    self.game.current_scene = GameScene(self.game)
                    return

                # Main Menu
                if self.game_over_menu_button.collidepoint(event.pos):
                    from game.scenes.menu_scene import MenuScene
                    self.game.current_scene = MenuScene(self.game)
                    return

                return

        # Stop gameplay if paused or over
        if self.paused or self.game_over:
            return

        # =====================================================
        # NORMAL GAMEPLAY
        # =====================================================
        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            col = (x - OFFSET_X) // TILE_SIZE
            row = (y - OFFSET_Y) // TILE_SIZE

            # Outside board
            if not (0 <= row < 8 and 0 <= col < 8):
                return

            tile = self.board.tiles[row][col]

            # -------------------------------------------------
            # MOVE SELECTED PIECE
            # -------------------------------------------------
            if self.selected_piece:

                if (row, col) in self.valid_moves:

                    moving_piece = self.selected_piece

                    result = self.board.move_piece(
                        moving_piece,
                        row,
                        col
                    )

                    # 16 move rule reset
                    if (
                        result["capture"]
                        or moving_piece.__class__.__name__ == "Pawn"
                    ):
                        self.no_capture_or_pawn_moves = 0
                    else:
                        self.no_capture_or_pawn_moves += 1

                    # Switch turn
                    self.turn = (
                        "black"
                        if self.turn == "white"
                        else "white"
                    )

                    # =================================================
                    # CHECKMATE
                    # =================================================
                    if (
                        self.board.is_in_check(self.turn)
                        and not self.has_any_valid_moves(self.turn)
                    ):
                        self.game_over = True

                        winner_color = (
                            "White"
                            if self.turn == "black"
                            else "Black"
                        )

                        self.winner = f"Checkmate! {winner_color} Wins!"

                    # =================================================
                    # STALEMATE
                    # =================================================
                    elif (
                        not self.board.is_in_check(self.turn)
                        and not self.has_any_valid_moves(self.turn)
                    ):
                        self.game_over = True
                        self.winner = "Draw - Stalemate"

                    # =================================================
                    # ONLY KINGS LEFT
                    # =================================================
                    elif self.board.only_kings_left():
                        self.game_over = True
                        self.winner = "Draw - Only Kings Left"

                    # =================================================
                    # 16 MOVE RULE
                    # =================================================
                    elif self.no_capture_or_pawn_moves >= 16:
                        self.game_over = True
                        self.winner = "Draw - 16 Move Rule"

                # Reset selection
                self.selected_piece = None
                self.valid_moves = []

            # -------------------------------------------------
            # SELECT NEW PIECE
            # -------------------------------------------------
            elif tile.piece and tile.piece.color == self.turn:

                self.selected_piece = tile.piece

                all_moves = tile.piece.get_valid_moves(self.board)

                # Only legal safe moves
                self.valid_moves = [
                    move for move in all_moves
                    if self.board.is_valid_move_safe(
                        tile.piece,
                        move[0],
                        move[1]
                    )
                ]

    # =====================================================
    # UPDATE
    # =====================================================
    def update(self):
        pass

    # =====================================================
    # DRAW
    # =====================================================
    def draw(self, screen):

        # Background
        screen.fill((220, 220, 220))

        # Board
        self.board.draw(
            screen,
            self.selected_piece,
            self.valid_moves
        )

        # -------------------------------------------------
        # TURN DISPLAY
        # -------------------------------------------------
        turn_text = self.small_font.render(
            f"{self.turn.capitalize()}'s Turn",
            True,
            (0, 0, 0)
        )

        screen.blit(turn_text, (280, 30))

        # -------------------------------------------------
        # CHECK WARNING
        # -------------------------------------------------
        if self.board.is_in_check(self.turn):
            check_text = self.small_font.render(
                "CHECK!",
                True,
                (255, 0, 0)
            )

            screen.blit(check_text, (350, 70))

        # -------------------------------------------------
        # PAUSE BUTTON
        # -------------------------------------------------
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            self.pause_button,
            border_radius=8
        )

        pause_label = "Resume" if self.paused else "Pause"

        pause_text = self.small_font.render(
            pause_label,
            True,
            (255, 255, 255)
        )

        screen.blit(pause_text, (670, 28))

        # =====================================================
        # PAUSE OVERLAY
        # =====================================================
        if self.paused:

            overlay = pygame.Surface((800, 800))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            paused_text = self.font.render(
                "Game Paused",
                True,
                (255, 255, 255)
            )

            screen.blit(paused_text, (250, 200))

            # Resume
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                self.resume_button,
                border_radius=10
            )

            resume_text = self.small_font.render(
                "Resume",
                True,
                (255, 255, 255)
            )

            screen.blit(resume_text, (355, 315))

            # Main Menu
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                self.menu_button,
                border_radius=10
            )

            menu_text = self.small_font.render(
                "Main Menu",
                True,
                (255, 255, 255)
            )

            screen.blit(menu_text, (335, 395))

        # =====================================================
        # GAME OVER OVERLAY
        # =====================================================
        if self.game_over:

            overlay = pygame.Surface((800, 800))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Winner text
            win_text = self.font.render(
                self.winner,
                True,
                (255, 255, 255)
            )

            screen.blit(win_text, (140, 220))

            # Play Again
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                self.play_again_button,
                border_radius=10
            )

            play_again_text = self.small_font.render(
                "Play Again",
                True,
                (255, 255, 255)
            )

            screen.blit(play_again_text, (335, 395))

            # Main Menu
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                self.game_over_menu_button,
                border_radius=10
            )

            menu_text = self.small_font.render(
                "Main Menu",
                True,
                (255, 255, 255)
            )

            screen.blit(menu_text, (335, 475))