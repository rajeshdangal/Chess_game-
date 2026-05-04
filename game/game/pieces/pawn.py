from game.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1

        # Move forward 1
        if board.in_bounds(self.row + direction, self.col):
            if board.is_empty(self.row + direction, self.col):
                moves.append((self.row + direction, self.col))

                # Move forward 2 from start
                if not self.has_moved:
                    if board.in_bounds(self.row + 2 * direction, self.col):
                        if board.is_empty(self.row + 2 * direction, self.col):
                            moves.append((self.row + 2 * direction, self.col))

        # Normal diagonal captures
        for dc in [-1, 1]:
            r = self.row + direction
            c = self.col + dc

            if board.in_bounds(r, c):
                if board.has_enemy_piece(r, c, self.color):
                    moves.append((r, c))

        # En passant
        last = board.last_move

        if last:
            last_piece = last["piece"]
            from_row, from_col = last["from"]
            to_row, to_col = last["to"]

            if last_piece.__class__.__name__ == "Pawn":
                if abs(from_row - to_row) == 2:
                    if self.row == to_row and abs(self.col - to_col) == 1:
                        moves.append((self.row + direction, to_col))

        return moves