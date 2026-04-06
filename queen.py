import pygame
from piece import Piece

class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def draw(self, screen):
        # Queen color: same as pawn (white or black)
        color = (230, 230, 230) if self.color == "white" else (20, 20, 20)

        # Draw a slightly bigger circle to differentiate queen from pawns
        pygame.draw.circle(
            screen,
            color,
            (self.col * 80 + 140, self.row * 80 + 140),  # center of tile
            30  # bigger radius than pawn
        )

        # Optional: draw a smaller inner circle for decoration (like a crown)
        pygame.draw.circle(
            screen,
            (200, 0, 200),  # purple accent for queen
            (self.col * 80 + 140, self.row * 80 + 140),
            12
        )

    def get_valid_moves(self, board):
        moves = []

        # Queen moves in 8 directions (straight + diagonal)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc

            # move continuously in this direction
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                elif board.has_enemy_piece(new_row, new_col, self.color):
                    moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += dr
                new_col += dc

        return moves