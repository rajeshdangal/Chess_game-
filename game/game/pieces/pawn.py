from game.pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.has_moved = False

    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1

        if board.is_empty(self.row + direction, self.col):
            moves.append((self.row + direction, self.col))

        if not self.has_moved:
            if (board.is_empty(self.row + direction, self.col) and
                board.is_empty(self.row + 2*direction, self.col)):
                moves.append((self.row + 2*direction, self.col))

        for dc in [-1, 1]:
            r = self.row + direction
            c = self.col + dc
            if board.has_enemy_piece(r, c, self.color):
                moves.append((r, c))

        return moves
