# --- Start of potion.py ---

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

# --- End of potion.py ---
