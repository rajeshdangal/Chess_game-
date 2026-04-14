import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 8
CELL_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
WHITE = (245, 245, 245)
BLACK = (50, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Knight Movement Prototype")

# Load knight image or draw a simple circle
# You can replace this with an image if you want
def draw_knight(pos):
    x, y = pos
    pygame.draw.circle(screen, BLUE, (y * CELL_SIZE + CELL_SIZE//2, x * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

# Calculate knight moves
def get_knight_moves(x, y):
    moves = [
        (x + 2, y + 1),
        (x + 2, y - 1),
        (x - 2, y + 1),
        (x - 2, y - 1),
        (x + 1, y + 2),
        (x + 1, y - 2),
        (x - 1, y + 2),
        (x - 1, y - 2)
    ]
    return [(mx, my) for mx, my in moves if 0 <= mx < BOARD_SIZE and 0 <= my < BOARD_SIZE]

# Draw board and highlights
def draw_board(knight_pos, valid_moves):
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)
    
    # Highlight valid moves
    for mx, my in valid_moves:
        rect = pygame.Rect(my*CELL_SIZE, mx*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

    # Draw knight
    draw_knight(knight_pos)
    pygame.display.flip()

def main():
    knight_pos = (0, 1)  # Starting position
    valid_moves = get_knight_moves(*knight_pos)

    while True:
        draw_board(knight_pos, valid_moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_pos = (mouse_y // CELL_SIZE, mouse_x // CELL_SIZE)
                if clicked_pos in valid_moves:
                    knight_pos = clicked_pos
                    valid_moves = get_knight_moves(*knight_pos)

if __name__ == "__main__":
    main()