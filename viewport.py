class ViewPort:
    def __init__(self, board, menu):
        self.board = board
        self.menu = menu

    def draw(self, screen, state):
        if state == "menu":
            self.menu.draw(screen)

        elif state == "game":
            screen.fill((255, 255, 255))
            self.board.draw(screen)