class InputHandler:
    def __init__(self, game_manager):
        self.game = game_manager

    def handle_click(self, row, col):
        board = self.game.board

        tile = board.tiles[row][col]

        # Select piece
        if tile.piece:
            if tile.piece.color == ("white" if self.game.current_player == 1 else "black"):
                self.game.selected_piece = tile.piece
                self.game.valid_moves = tile.piece.get_valid_moves(board)
                return

        # Move piece
        if self.game.selected_piece and (row, col) in self.game.valid_moves:
            self.move_piece(row, col)
            self.switch_turn()

        # Clear selection
        self.game.selected_piece = None
        self.game.valid_moves = []

    def move_piece(self, row, col):
        piece = self.game.selected_piece
        board = self.game.board

        old_row, old_col = piece.row, piece.col

        board.tiles[old_row][old_col].piece = None

        target = board.tiles[row][col].piece
        if target:
            print("Captured!")

        board.tiles[row][col].piece = piece
        piece.row = row
        piece.col = col

    def switch_turn(self):
        self.game.current_player = 2 if self.game.current_player == 1 else 1