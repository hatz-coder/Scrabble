import pygame
import sys

pygame.init()  # Initialize Pygame

icon = pygame.image.load("app_icon.png")
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GRID_SIZE = 15
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
Purple = (197, 197, 210)
LightPurple = (231, 231, 241)
LIGHT_PURPLE = (150, 123, 182)
LIGHT_BLUE = (104, 163, 196)
RED = (192, 77, 77)
DARK_BLUE = (4, 103, 157)
YELLOW = (255, 235, 123)
PINK = (229, 163, 164)

pygame.display.set_caption("Scrabble Go")
font = pygame.font.SysFont("Poppins Bold", TILE_SIZE//1)
small_font = pygame.font.SysFont("Poppins Bold", TILE_SIZE // 2)
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Define special tile positions (same as in your original code)
# [Add code for triple_word_tiles, double_word_tiles, triple_letter_tiles, double_letter_tiles, and center]
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

class DraggableTile:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.dragging = False

    def draw(self):
        # Draw the tile rectangle
        pygame.draw.rect(screen, (223, 124, 53), self.rect, border_radius=5)
        
        # Render the text surface
        text_surface = font.render(self.letter, True, (50, 50, 50))
        
        # Get the text's rectangle and set its center to match the tile's center
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Blit the text surface at the calculated position
        screen.blit(text_surface, text_rect)
# Create some sample draggable tiles
tiles = [DraggableTile('A', 100, 500), DraggableTile('B', 150, 500), DraggableTile('C', 200, 500)]

def draw_board():
    screen.fill(Purple)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = LIGHT_PURPLE  # Default tile color
            if (row, col) in triple_word_tiles:
                color = RED
                text="TW"
            elif (row, col) in center:
                color = YELLOW
                text="C"
            elif (row, col) in triple_letter_tiles:
                color = DARK_BLUE
                text="TL"
            elif (row, col) in double_letter_tiles:
                color = LIGHT_BLUE
                text="DL"
            elif (row, col) in double_word_tiles:
                color = PINK
                text="DW"
            pygame.draw.rect(screen, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), border_radius=7)
            pygame.draw.rect(screen, Purple, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2, border_radius=7)
            
            if text:
                text_surface = small_font.render(text, True, (200, 200, 200))  # Adjust color as needed
                text_rect = text_surface.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)
            text = ''
running = True
dragged_tile = None

while running:
    draw_board()

    for tile in tiles:
        tile.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for tile in tiles:
                if tile.rect.collidepoint(mouse_x, mouse_y):
                    tile.dragging = True
                    dragged_tile = tile
                    offset_x = tile.rect.x - mouse_x
                    offset_y = tile.rect.y - mouse_y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_tile:
                dragged_tile.dragging = False
                dragged_tile = None
        elif event.type == pygame.MOUSEMOTION:
            if dragged_tile and dragged_tile.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dragged_tile.rect.x = mouse_x + offset_x
                dragged_tile.rect.y = mouse_y + offset_y
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1:
                current_letter = event.unicode.upper()

    pygame.display.flip()

pygame.quit()
sys.exit()
