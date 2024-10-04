# --- Start of helpers.py ---

import sys
import pygame
from constants import *

def draw_text(surface, text, pos, color=WHITE, font=FONT):
    img = font.render(text, True, color)
    surface.blit(img, pos)

# The help_menu function is now integrated into GameManager.show_help_menu()

# --- End of helpers.py ---
