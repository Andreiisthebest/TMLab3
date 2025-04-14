import os

# Game settings
TITLE = "Rail Building Tycoon"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
SAVE_FILE = os.path.join("data", "save.dat")  # Changed to use os.path.join

# Colors
BACKGROUND_COLOR = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
UI_COLOR = (70, 70, 90)
UI_ACCENT = (100, 100, 120)

# Game constants
GRID_SIZE = 32
MAX_LEVELS = 6
BASE_LEVEL_COST = 10000  # Starting budget
COST_INCREMENT = 5000    # Additional cost per level

# Debug settings
DEBUG_MODE = True
SHOW_FPS = True