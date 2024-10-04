"""
This module defines the Potion class for a top-down adventure game.
Classes:
    Potion: A class representing a potion sprite in the game.
Constants:
    RED: The color used for health potions.
    BLUE: The color used for mana potions.
    WHITE: The color used for the border of the potion.
Class Potion:
    __init__(self, x, y, potion_type):
        Initializes a new potion instance.
        Parameters:
            x (int): The x-coordinate of the potion.
            y (int): The y-coordinate of the potion.
            potion_type (str): The type of the potion ('health' or 'mana').
    draw(self, surface):
        Draws the potion on the given surface.
        Parameters:
            surface (pygame.Surface): The surface to draw the potion on.
"""

import pygame
from constants import *

class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y, potion_type):
        super().__init__()
        self.width = 20
        self.height = 20
        self.potion_type = potion_type  # 'health' or 'mana'
        self.color = RED if potion_type == 'health' else BLUE
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
