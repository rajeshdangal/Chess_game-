from game.pieces.piece import Piece

class Knight(Piece):
    def get_valid_moves(self, board):
        moves = []
        steps = [
            (-2,-1),(-2,1),(2,-1),(2,1),
            (-1,-2),(-1,2),(1,-2),(1,2)
        ]

        for dr, dc in steps:
            r = self.row + dr
            c = self.col + dc
            if board.in_bounds(r, c):
                if board.is_empty(r, c) or board.has_enemy_piece(r, c, self.color):
                    moves.append((r, c))

        return moves
