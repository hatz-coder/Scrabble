import pygame
import sys

pygame.init() # Initialize Pygame

icon = pygame.image.load("app_icon.png")
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GRID_SIZE = 15
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
Purple = (197, 197, 210)
LightPurple = (231, 231, 241)
GREEN = (34, 139, 34)
LIGHT_PURPLE = (150, 123, 182)
LIGHT_BLUE = (104, 163, 196)
RED = (192, 77, 77)
DARK_BLUE = (4, 103, 157)
YELLOW = (255, 235, 123)
PINK=(229, 163, 164)

# Set up the screen
pygame.display.set_caption("Scrabble Go")

# Font for text rendering
font = pygame.font.SysFont("Poppin", TILE_SIZE)

# Board data structure
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
triple_word_tiles = [
    (0, 0), (0, 7), (0, 14),  # Top row
    (7, 0), (7, 14),          # Middle rows
    (14, 0), (14, 7), (14, 14)  # Bottom row
]
double_word_tiles = [
    (1, 1), (2, 2), (3, 3), (4, 4), (13, 1), (12, 2), (11, 3), (10, 4),  # Top left and bottom left to center
    (1, 13), (2, 12), (3, 11), (4, 10), (13, 13), (12, 12), (11, 11), (10, 10)  # Top right and bottom right to center
]
triple_letter_tiles = [
    (1, 5), (1, 9), (5, 1), (5, 13), (9, 1), (9, 13), (13, 5), (13, 9)  # Around the board in symmetric positions
]
center = [
    (7, 7) 
]
double_letter_tiles = [
    (0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12),
    (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8),
    (14, 3), (14, 11)
]
print("triple_word_tiles",triple_word_tiles)
# Draw the board grid
def draw_board():
    screen.fill(Purple)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = LIGHT_PURPLE  # Default tile color

            # Change color for special tiles
            if (row, col) in triple_word_tiles:
                color = RED  # TWS tiles in red
            elif (row, col) in center:
                color = YELLOW
            elif (row, col) in triple_letter_tiles:
                color = DARK_BLUE  # DWS tiles in yellow
            elif (row, col) in double_letter_tiles:
                color = LIGHT_BLUE  # DLS tiles in light blue
            elif (row, col) in double_word_tiles:
                color = PINK  # DLS tiles in light blue
            # rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect( screen, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),border_radius=7)
            pygame.draw.rect( screen, Purple, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2,border_radius=7)

# Main loop
running = True
current_letter = 'A'  # Placeholder for demo purposes

while running:

    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // TILE_SIZE
            row = y // TILE_SIZE

            # Place a tile if the spot is empty
            if board[row][col] == '':
                board[row][col] = current_letter

        elif event.type == pygame.KEYDOWN:
            # Update the current letter with the key pressed (for demo purposes)
            if event.unicode.isalpha() and len(event.unicode) == 1:
                current_letter = event.unicode.upper()

    pygame.display.flip()

pygame.quit()
sys.exit()
