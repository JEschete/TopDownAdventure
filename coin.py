# --- Start of coin.py ---

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

# --- End of coin.py ---
