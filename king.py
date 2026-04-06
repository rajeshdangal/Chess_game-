from piece import Piece

class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.has_moved = False

    def get_valid_moves(self, board):
        moves = []
        
        # King moves: one square in any direction
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),  # Up and diagonals
            (0, -1),           (0, 1),    # Left and right
            (1, -1),  (1, 0),  (1, 1)     # Down and diagonals
        ]
        
        for dr, dc in king_moves:
            new_row = self.row + dr
            new_col = self.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty(new_row, new_col) or board.has_enemy_piece(new_row, new_col, self.color):
                    moves.append((new_row, new_col))
        
        return moves