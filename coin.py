"""
This module defines the Coin class for a top-down adventure game.
Classes:
    Coin: A class representing a coin sprite in the game.
Constants:
    GOLD: The color of the coin.
    WHITE: The color used for the coin's outline.
Methods:
    __init__(self, x, y):
        Initializes a Coin instance with a specified position.
    draw(self, surface):
        Draws the coin on the given surface.
"""

import pygame

from constants import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10
        self.color = GOLD
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
        pygame.draw.circle(surface, WHITE, self.rect.center, self.radius, 2)

