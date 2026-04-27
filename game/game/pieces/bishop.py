from game.pieces.piece import Piece

class Bishop(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1,-1),(-1,1),(1,-1),(1,1)]

        for dr, dc in directions:
            r, c = self.row, self.col
            while True:
                r += dr
                c += dc
                if not board.in_bounds(r, c):
                    break
                if board.is_empty(r, c):
                    moves.append((r, c))
                elif board.has_enemy_piece(r, c, self.color):
                    moves.append((r, c))
                    break
                else:
                    break
        return moves