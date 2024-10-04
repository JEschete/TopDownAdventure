"""
This module defines the Obstacle class for the TopDownAdventure game.
Classes:
    Obstacle: A class representing a rectangular obstacle in the game.
Usage Example:
    obstacle = Obstacle(x=100, y=150, width=50, height=50)
    obstacle.draw(surface)
Attributes:
    rect (pygame.Rect): The rectangle representing the obstacle's position and size.
    color (tuple): The color of the obstacle, default is GREEN.
Methods:
    __init__(x, y, width, height, color=GREEN): Initializes the Obstacle with position, size, and color.
    draw(surface): Draws the obstacle on the given surface.
"""

import pygame
from constants import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
