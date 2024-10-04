"""
This module provides helper functions for the TopDownAdventure game.
Functions:
    draw_text(surface, text, pos, color=WHITE, font=FONT):
        Renders and draws text on the given surface at the specified position.
Constants:
    WHITE: Default color for the text.
    FONT: Default font for rendering the text.
"""

import sys
import pygame
from constants import *

def draw_text(surface, text, pos, color=WHITE, font=FONT):
    img = font.render(text, True, color)
    surface.blit(img, pos)

# The help_menu function is now integrated into GameManager.show_help_menu()
# This file should be depreciated and integrated somewhere else. 
