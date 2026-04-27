from game.pieces.piece import Piece

class King(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [
            (-1,0),(1,0),(0,-1),(0,1),
            (-1,-1),(-1,1),(1,-1),(1,1)
        ]

        for dr, dc in directions:
            r = self.row + dr
            c = self.col + dc
            if board.in_bounds(r, c):
                if board.is_empty(r, c) or board.has_enemy_piece(r, c, self.color):
                    moves.append((r, c))

        return moves