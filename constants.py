# --- Start of constants.py ---

import pygame

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 960
HUD_HEIGHT = 140
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Adventure")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)

# Fonts
FONT = pygame.font.SysFont('Arial', 20)
FONT_LARGE = pygame.font.SysFont('Arial', 40)

# Game variables
TILE_SIZE = 40

# Magic spells
MAGIC_SPELLS = ['Fireball', 'Ice Spike', 'Lightning Bolt']
SPELL_COLORS = {'Fireball': RED, 'Ice Spike': CYAN, 'Lightning Bolt': YELLOW}

# --- End of constants.py ---
