from piece import Piece

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.has_moved = False

    def get_valid_moves(self, board):
        moves = []

        direction = -1 if self.color == "white" else 1

        # forward 1
        if board.is_empty(self.row + direction, self.col):
            moves.append((self.row + direction, self.col))

        # forward 2 (first move)
        if not self.has_moved:
            if board.is_empty(self.row + 2 * direction, self.col):
                moves.append((self.row + 2 * direction, self.col))

        # capture diagonally
        for dc in [-1, 1]:
            new_row = self.row + direction
            new_col = self.col + dc

            if board.has_enemy_piece(new_row, new_col, self.color):
                moves.append((new_row, new_col))

        return moves