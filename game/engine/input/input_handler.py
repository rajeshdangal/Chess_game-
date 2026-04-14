class InputHandler:
    def __init__(self, scene):
        self.scene = scene

    def handle_click(self, row, col):
        board = self.scene.board
        tile = board.tiles[row][col]

        # Select piece
        if tile.piece:
            if tile.piece.color == ("white" if self.scene.current_player == 1 else "black"):
                self.scene.selected_piece = tile.piece
                self.scene.valid_moves = tile.piece.get_valid_moves(board)
                return

        # Move
        if self.scene.selected_piece and (row, col) in self.scene.valid_moves:
            self.move_piece(row, col)
            self.switch_turn()

        self.scene.selected_piece = None
        self.scene.valid_moves = []

    def move_piece(self, row, col):
        piece = self.scene.selected_piece
        board = self.scene.board

        old_row, old_col = piece.row, piece.col
        board.tiles[old_row][old_col].piece = None

        board.tiles[row][col].piece = piece
        piece.row = row
        piece.col = col

        if hasattr(piece, "has_moved"):
            piece.has_moved = True

    def switch_turn(self):
        self.scene.current_player = 2 if self.scene.current_player == 1 else 1