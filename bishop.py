from piece import Piece

class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def get_valid_moves(self, board):
        moves = []
        
        # Bishop moves: diagonally in 4 directions
        directions = [
            (-1, -1),  # up-left
            (-1, 1),   # up-right
            (1, -1),   # down-left
            (1, 1)     # down-right
        ]
        
        for dr, dc in directions:
            # Bishop can move any number of squares along diagonal
            for step in range(1, 8):
                new_row = self.row + (dr * step)
                new_col = self.col + (dc * step)
                
                # Check if within board boundaries
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                # If square is empty, add move and continue
                if board.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                # If enemy piece, add move then stop in this direction
                elif board.has_enemy_piece(new_row, new_col, self.color):
                    moves.append((new_row, new_col))
                    break
                # If own piece, stop in this direction
                else:
                    break
        
        return moves