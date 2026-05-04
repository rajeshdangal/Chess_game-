import random

PIECE_VALUES = {
    "Pawn": 100,
    "Knight": 320,
    "Bishop": 330,
    "Rook": 500,
    "Queen": 900,
    "King": 20000
}


class ChessAI:
    def __init__(self, color):
        self.color = color

    def get_all_legal_moves(self, board):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = board.tiles[row][col].piece

                if piece and piece.color == self.color:
                    legal_moves = board.get_legal_moves(piece)

                    for move_row, move_col in legal_moves:
                        moves.append((piece, move_row, move_col))

        return moves

    def choose_move(self, board):
        moves = self.get_all_legal_moves(board)

        if not moves:
            return None

        best_score = -999999
        best_moves = []

        for piece, row, col in moves:
            target_piece = board.tiles[row][col].piece
            score = 0

            if target_piece:
                score += PIECE_VALUES.get(target_piece.__class__.__name__, 0)

            # Prefer center squares
            if row in [3, 4] and col in [3, 4]:
                score += 25

            # Small random variety
            score += random.randint(0, 10)

            if score > best_score:
                best_score = score
                best_moves = [(piece, row, col)]
            elif score == best_score:
                best_moves.append((piece, row, col))

        return random.choice(best_moves)