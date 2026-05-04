import random
import math

PIECE_VALUES = {
    "Pawn": 100,
    "Knight": 320,
    "Bishop": 330,
    "Rook": 500,
    "Queen": 900,
    "King": 20000
}


class ChessAI:
    def __init__(self, color, depth=2):
        self.color = color
        self.depth = depth
        self.enemy_color = "white" if color == "black" else "black"

    def get_all_legal_moves(self, board, color):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = board.tiles[row][col].piece

                if piece and piece.color == color:
                    legal_moves = board.get_legal_moves(piece)

                    for move_row, move_col in legal_moves:
                        moves.append((piece, move_row, move_col))

        return moves

    def evaluate_board(self, board):
        score = 0

        for row in range(8):
            for col in range(8):
                piece = board.tiles[row][col].piece

                if piece:
                    value = PIECE_VALUES.get(piece.__class__.__name__, 0)

                    # small center bonus
                    if row in [3, 4] and col in [3, 4]:
                        value += 20

                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value

        return score

    def simulate_move(self, board, piece, row, col):
        old_row = piece.row
        old_col = piece.col
        captured_piece = board.tiles[row][col].piece

        board.tiles[old_row][old_col].piece = None
        board.tiles[row][col].piece = piece
        piece.row = row
        piece.col = col

        return old_row, old_col, captured_piece

    def undo_move(self, board, piece, old_row, old_col, row, col, captured_piece):
        board.tiles[row][col].piece = captured_piece
        board.tiles[old_row][old_col].piece = piece
        piece.row = old_row
        piece.col = old_col

    def minimax(self, board, depth, alpha, beta, maximizing, color):
        if depth == 0 or board.is_checkmate("white") or board.is_checkmate("black"):
            return self.evaluate_board(board)

        moves = self.get_all_legal_moves(board, color)

        if not moves:
            return self.evaluate_board(board)

        next_color = "white" if color == "black" else "black"

        if maximizing:
            max_eval = -math.inf

            for piece, row, col in moves:
                old_row, old_col, captured_piece = self.simulate_move(board, piece, row, col)

                eval_score = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    next_color
                )

                self.undo_move(board, piece, old_row, old_col, row, col, captured_piece)

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = math.inf

            for piece, row, col in moves:
                old_row, old_col, captured_piece = self.simulate_move(board, piece, row, col)

                eval_score = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    next_color
                )

                self.undo_move(board, piece, old_row, old_col, row, col, captured_piece)

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break

            return min_eval

    def choose_move(self, board):
        moves = self.get_all_legal_moves(board, self.color)

        if not moves:
            return None

        best_score = -math.inf
        best_moves = []

        for piece, row, col in moves:
            old_row, old_col, captured_piece = self.simulate_move(board, piece, row, col)

            score = self.minimax(
                board,
                self.depth - 1,
                -math.inf,
                math.inf,
                False,
                self.enemy_color
            )

            self.undo_move(board, piece, old_row, old_col, row, col, captured_piece)

            if score > best_score:
                best_score = score
                best_moves = [(piece, row, col)]
            elif score == best_score:
                best_moves.append((piece, row, col))

        return random.choice(best_moves)