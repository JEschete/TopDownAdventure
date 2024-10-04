"""
This module sets up the constants and initial configurations for the Top-Down Adventure game.
Modules:
    pygame: A set of Python modules designed for writing video games.
Constants:
    WIDTH (int): The width of the game screen.
    HEIGHT (int): The height of the game screen.
    HUD_HEIGHT (int): The height of the Heads-Up Display (HUD).
    SCREEN (pygame.Surface): The display surface for the game.
    FPS (int): Frames per second for the game loop.
    WHITE (tuple): RGB color value for white.
    GREEN (tuple): RGB color value for green.
    DARK_GREEN (tuple): RGB color value for dark green.
    RED (tuple): RGB color value for red.
    DARK_RED (tuple): RGB color value for dark red.
    BLUE (tuple): RGB color value for blue.
    BLACK (tuple): RGB color value for black.
    GRAY (tuple): RGB color value for gray.
    YELLOW (tuple): RGB color value for yellow.
    CYAN (tuple): RGB color value for cyan.
    MAGENTA (tuple): RGB color value for magenta.
    ORANGE (tuple): RGB color value for orange.
    GOLD (tuple): RGB color value for gold.
    BROWN (tuple): RGB color value for brown.
    PURPLE (tuple): RGB color value for purple.
    FONT (pygame.font.Font): The default font for the game.
    FONT_LARGE (pygame.font.Font): The large font for the game.
    TILE_SIZE (int): The size of each tile in the game.
    MAGIC_SPELLS (list): List of available magic spells.
    SPELL_COLORS (dict): Dictionary mapping each spell to its corresponding color.
"""

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

