"""
Projectile class represents a projectile in the game.
Attributes:
    radius (int): Radius of the projectile.
    color (tuple): Color of the projectile.
    rect (pygame.Rect): Rect object representing the projectile's position and size.
    dx (float): Change in x-direction per update.
    dy (float): Change in y-direction per update.
    speed (int): Speed of the projectile.
    damage (int): Damage dealt by the projectile.
    target_type (str): Type of target ('enemies' or 'player').
    target (pygame.sprite.Sprite): Specific target sprite.
Methods:
    __init__(x, y, dx, dy, damage, color=CYAN, target_type='enemies', target=None):
        Initializes the projectile with given parameters.
    update(obstacles, player, enemies):
        Updates the projectile's position and checks for collisions.
    draw(surface):
        Draws the projectile on the given surface.
"""

import pygame
import math
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, damage, color=CYAN, target_type='enemies', target=None):
        super().__init__()
        self.radius = 5
        self.color = color
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.dx = dx
        self.dy = dy
        self.speed = 5
        self.damage = damage
        self.target_type = target_type  # 'enemies' or 'player'
        self.target = target

    def update(self, obstacles, player, enemies):
        if self.target_type == 'enemies':
            if self.target and self.target.health > 0:
                # Adjust direction towards the target
                dx = self.target.rect.centerx - self.rect.centerx
                dy = self.target.rect.centery - self.rect.centery
                distance = math.hypot(dx, dy)
                if distance != 0:
                    self.dx = dx / distance
                    self.dy = dy / distance
            else:
                # Continue in last known direction
                pass

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        # Check collision with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True  # Remove projectile

        # Check collision with targets
        if self.target_type == 'enemies':
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.damage)
                    return True  # Remove projectile
        elif self.target_type == 'player':
            if self.rect.colliderect(player.rect):
                player.take_damage(self.damage)
                return True  # Remove projectile

        # Remove projectile if it goes off-screen
        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.top < HUD_HEIGHT or self.rect.bottom > HEIGHT):
            return True

        return False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)

