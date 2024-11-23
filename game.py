import pygame
import sys
import random  # Add this at the top of your code
import requests
import time

# Wordnik API setup
# API_KEY = 'your_wordnik_api_key'  # Replace this with your actual Wordnik API key
# BASE_URL = 'https://api.wordnik.com/v4/word.json/'

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
font_path = "Poppins-Bold.ttf"  # Change this to your actual font file path
font = pygame.font.Font(font_path, 30)  # Specify the path and size
font_path = "Poppins-Bold.ttf"  # Change this to your actual font file path
small_font2 = pygame.font.Font(font_path, 20)  # Specify the path and size
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
word_cache = {}

def is_valid_word(word):
    """Check if the word exists using Free Dictionary API."""
    global word_cache
    if not word or len(word) < 2:  # Skip single-letter words
        return False

    if word in word_cache:
        return word_cache[word]

    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
        response = requests.get(url)
        word_cache[word] = response.status_code == 200
        return word_cache[word]
    except requests.RequestException as e:
        print(f"API Error: {e}")
        return False  # Assume invalid word on API failure



# Scoring function based on word length
def calculate_score(word, placed_tiles, newly_placed_positions):
    """Calculate the score of a word, considering special tiles."""
    letter_values = {
        "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4,
        "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3,
        "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8,
        "Y": 4, "Z": 10
    }

    word_score = 0
    word_multiplier = 1  # Default multiplier

    print(f"--- Scoring word: {word} ---")
    print(f"Newly placed tiles: {newly_placed_positions}")
    print(f"All placed tiles: {placed_tiles}")

    # Calculate score for newly placed tiles
    for row, col in newly_placed_positions:
        letter = placed_tiles.get((row, col), "")
        letter_score = letter_values.get(letter.upper(), 0)
        print(f"Letter '{letter}' at ({row}, {col}) has base score {letter_score}")

        # Apply special tile bonuses
        if (row, col) in double_letter_tiles:
            letter_score *= 2
            print(f"Double Letter Tile at ({row}, {col}): Score doubled to {letter_score}")
        elif (row, col) in triple_letter_tiles:
            letter_score *= 3
            print(f"Triple Letter Tile at ({row}, {col}): Score tripled to {letter_score}")

        if (row, col) in double_word_tiles:
            word_multiplier *= 2
            print(f"Double Word Tile at ({row}, {col}): Word multiplier now {word_multiplier}")
        elif (row, col) in triple_word_tiles:
            word_multiplier *= 3
            print(f"Triple Word Tile at ({row}, {col}): Word multiplier now {word_multiplier}")
        word_score += letter_score

    # Add scores for other letters in the word (no bonuses applied)
    for row, col in placed_tiles:
        if (row, col) not in newly_placed_positions:
            letter = placed_tiles.get((row, col), "")
            extra_score = letter_values.get(letter.upper(), 0)
            word_score += extra_score
            print(f"Previously placed letter '{letter}' at ({row}, {col}): Score {extra_score}")

    # Apply word multiplier
    print(f"Base score before word multiplier: {word_score}")
    word_score *= word_multiplier
    print(f"Final score after applying word multiplier: {word_score}")

    return word_score



class DraggableTile:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.rect = pygame.Rect(x, y, TILE_SIZE-10, TILE_SIZE-10)
        self.dragging = False
        self.scale = 0.9  # Default scale factor

    def draw(self):
        # Adjust size when dragging
        current_size = TILE_SIZE * self.scale
        self.rect.width = current_size
        self.rect.height = current_size

        # Draw the tile rectangle
        pygame.draw.rect(screen, (223, 124, 53), self.rect, border_radius=5)

        # Render the text surface
        text_surface = font.render(self.letter, True, (50, 50, 50))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Create some sample draggable tiles

# Generate a list of 7 random letters and positions for the tiles
letters = [chr(random.randint(65, 90)) for _ in range(7)]  # Generate random letters from A-Z
tiles = [DraggableTile(letter, 50 + i * (TILE_SIZE+10), 500) for i, letter in enumerate(letters)]

def find_word(placed_tiles, row, col):
    # Check horizontal word
    horizontal_word = ""
    horizontal_start = col
    # Find the starting point of the horizontal word
    while horizontal_start > 0 and (row, horizontal_start - 1) in placed_tiles:
        horizontal_start -= 1
    # Build the horizontal word
    while (row, horizontal_start) in placed_tiles:
        horizontal_word += placed_tiles[(row, horizontal_start)]
        horizontal_start += 1

    # Check vertical word
    vertical_word = ""
    vertical_start = row
    # Find the starting point of the vertical word
    while vertical_start > 0 and (vertical_start - 1, col) in placed_tiles:
        vertical_start -= 1
    # Build the vertical word
    while (vertical_start, col) in placed_tiles:
        vertical_word += placed_tiles[(vertical_start, col)]
        vertical_start += 1

    return horizontal_word, vertical_word


tick_button = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60, 40, 40)
def handle_invalid_word(placed_tiles, tiles, dragged_tile):
    """Handles the return of tiles if an invalid word is formed."""
    # Remove the last placed tile from the board if it's invalid
    if dragged_tile:
        # Remove the tile from the board
        placed_tiles.pop((dragged_tile.rect.y // TILE_SIZE, dragged_tile.rect.x // TILE_SIZE), None)
        
        # Add the tile back to the tray
        tiles.append(dragged_tile)
        
def draw_board():
    screen.fill(Purple)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = LIGHT_PURPLE  # Default tile color
            text = None  # Reset text for each tile
            
            if (row, col) in triple_word_tiles:
                color = RED
                text = "TW"
            elif (row, col) in center:
                color = YELLOW
                text = "C"
            elif (row, col) in triple_letter_tiles:
                color = DARK_BLUE
                text = "TL"
            elif (row, col) in double_letter_tiles:
                color = LIGHT_BLUE
                text = "DL"
            elif (row, col) in double_word_tiles:
                color = PINK
                text = "DW"

            pygame.draw.rect(
                screen, color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                border_radius=7
            )
            pygame.draw.rect(
                screen, Purple,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2, border_radius=7
            )
            
            # Draw special tile text
            if text:
                text_surface = small_font.render(text, True, (200, 200, 200))
                text_rect = text_surface.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

    # Draw tick button
    pygame.draw.rect(screen, (90, 111, 234), tick_button, border_radius=5)
    tick_text = small_font.render("Tick", True, (255, 255, 255))
    screen.blit(tick_text, (tick_button.x + 5, tick_button.y + 8))
running = True
placed_tiles = {}  # Dictionary to store tile positions and letters
# Flag to track if the word has been finalized
# Initialize required variables
word_formed = False  # Flag to check if the word is confirmed
horizontal_word, vertical_word = "", ""  # Words to display after confirmation
dragged_tile = None  # To store the current dragged tile
score=0
while running:
    draw_board()

    # Draw placed tiles (those that are snapped to the board)
    for (row, col), letter in placed_tiles.items():
        rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (223, 124, 53), rect, border_radius=5)

        # Render the letter on the placed tile
        text_surface = font.render(letter, True, (50, 50, 50))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Draw draggable tiles in the player's tray
    for tile in tiles:
        tile.draw()

    # Draw the tick button
    tick_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 40)
    pygame.draw.rect(screen, (0, 255, 0), tick_button, border_radius=5)
    tick_text = small_font.render("Tick", True, (255, 255, 255))
    screen.blit(tick_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 55))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Handle tile dragging (only if the word is not confirmed)
            if not word_formed:
                for tile in tiles:
                    if tile.rect.collidepoint(mouse_x, mouse_y):
                        tile.dragging = True
                        dragged_tile = tile
                        offset_x = tile.rect.x - mouse_x
                        offset_y = tile.rect.y - mouse_y
                        break

            # Handle the tick button click (confirm the word)
            if tick_button.collidepoint(mouse_x, mouse_y) and not word_formed:
                word_formed = True  # Finalize the word
                print("Word confirmed!")
                # Prevent further dragging of tiles after the tick button is pressed
                for tile in tiles:
                    tile.dragging = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged_tile:
                dragged_tile.dragging = False
                dragged_tile.scale = 0.9  # Reset size after dropping

                # Snap to grid
                grid_x = round(dragged_tile.rect.x / TILE_SIZE)
                grid_y = round(dragged_tile.rect.y / TILE_SIZE)
                grid_x = max(0, min(GRID_SIZE - 1, grid_x))
                grid_y = max(0, min(GRID_SIZE - 1, grid_y))

                # Check if the tile is within the board boundaries and not already placed
                if (grid_y, grid_x) not in placed_tiles:
                    # Place tile on the board
                    placed_tiles[(grid_y, grid_x)] = dragged_tile.letter
                    dragged_tile.rect.x = grid_x * TILE_SIZE
                    dragged_tile.rect.y = grid_y * TILE_SIZE

                    # After placing the tile, remove it from the tray only when the word is confirmed
                    if word_formed:
                        tiles.remove(dragged_tile)

                dragged_tile = None

                # Initialize the words to avoid any potential 'None' issues
                horizontal_word, vertical_word = "", ""

                # Find the word formed (passing grid_y and grid_x as row and col)
                horizontal_word, vertical_word = find_word(placed_tiles, grid_y, grid_x)

                # Check if the word is valid
                if is_valid_word(horizontal_word) and len(horizontal_word) > 1:
                    score += calculate_score(horizontal_word, placed_tiles, newly_placed_positions=[(grid_y, grid_x)])
                    word_message = f"Valid Horizontal Word: {horizontal_word}, Score: {score}"
                elif is_valid_word(vertical_word) and len(vertical_word) > 1:
                    score += calculate_score(vertical_word, placed_tiles, newly_placed_positions=[(grid_y, grid_x)])
                    word_message = f"Valid Vertical Word: {vertical_word}, Score: {score}"
                else:
                    word_message = "No valid word formed."

                print(word_message)

            # Display words formed
            # text_surface = small_font.render(f"Words: {horizontal_word}, {vertical_word}", True, (255, 255, 255))
            # screen.blit(text_surface, (10, SCREEN_HEIGHT - 50))

        elif event.type == pygame.MOUSEMOTION:
            if dragged_tile and dragged_tile.dragging and not word_formed:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dragged_tile.rect.x = mouse_x + offset_x
                dragged_tile.rect.y = mouse_y + offset_y

        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1:
                current_letter = event.unicode.upper()

        # Display the words formed only when the word is confirmed
    if word_formed:
        word = horizontal_word if len(horizontal_word) > 1 else vertical_word
        # Display the word and the score
        # text_surface = small_font.render(f"Word: {word}, Score: {score}", True, (0, 0, 0))
        # screen.blit(text_surface, (10, SCREEN_HEIGHT - 50))

        # Display the word validity message
        validity_surface = small_font2.render(word_message, True, (0, 64, 0) if 'Valid' in word_message else (64, 0, 0))
        screen.blit(validity_surface, (10, SCREEN_HEIGHT - 30))
    pygame.display.flip()
    score=0


pygame.quit()
sys.exit()
