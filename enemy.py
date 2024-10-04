"""
Enemy class representing different types of enemies in the game.
Attributes:
    width (int): Width of the enemy sprite.
    height (int): Height of the enemy sprite.
    type (str): Type of the enemy (e.g., 'melee', 'archer', 'tank', 'healer', 'assassin', 'boss').
    color (tuple): Color of the enemy sprite.
    speed (float): Speed of the enemy.
    health (int): Current health of the enemy.
    max_health (int): Maximum health of the enemy.
    exp_value (int): Experience value awarded to the player upon defeating the enemy.
    attack_cooldown (int): Cooldown period between attacks for certain enemy types.
    heal_cooldown (int): Cooldown period between heals for healer type enemies.
    rect (pygame.Rect): Rectangular area representing the enemy's position and size.
Methods:
    __init__(self, x, y, enemy_type='melee'):
        Initializes the enemy with the given position and type.
    update(self, player, obstacles, projectiles):
        Updates the enemy's behavior based on its type and interactions with the player, obstacles, and projectiles.
    move_towards_player(self, player, obstacles):
        Moves the enemy towards the player, considering obstacles.
    archer_behavior(self, player, obstacles, projectiles):
        Defines the behavior for archer type enemies, including movement and attacking.
    healer_behavior(self):
        Defines the behavior for healer type enemies, including healing nearby enemies.
    assassin_behavior(self, player, obstacles):
        Defines the behavior for assassin type enemies, including movement and attacking.
    move(self, dx, dy, obstacles):
        Moves the enemy by the given deltas, considering collisions with obstacles.
    collide(self, dx, dy, obstacles):
        Handles collisions with obstacles when the enemy moves.
    shoot_arrow(self, player, projectiles):
        Shoots a projectile towards the player.
    take_damage(self, amount):
        Reduces the enemy's health by the given amount.
    draw(self, surface):
        Draws the enemy on the given surface.
    draw_health_bar(self, surface):
        Draws the health bar above the enemy.
"""

import pygame
import random
import math
from constants import *
from projectile import Projectile



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='melee'):
        super().__init__()
        self.width = 30
        self.height = 30
        self.type = enemy_type
        if self.type == 'melee':
            self.color = RED
            self.speed = 2
            self.health = 50
            self.max_health = 50
            self.exp_value = 50
        elif self.type == 'archer':
            self.color = ORANGE
            self.speed = 1.5
            self.health = 30
            self.max_health = 30
            self.exp_value = 70
            self.attack_cooldown = random.randint(60, 120)
        elif self.type == 'tank':
            self.color = BROWN
            self.speed = 1
            self.health = 100
            self.max_health = 100
            self.exp_value = 100
        elif self.type == 'healer':
            self.color = GREEN
            self.speed = 1.5
            self.health = 40
            self.max_health = 40
            self.exp_value = 60
            self.heal_cooldown = 0
        elif self.type == 'assassin':
            self.color = MAGENTA
            self.speed = 3
            self.health = 30
            self.max_health = 30
            self.exp_value = 80
        elif self.type == 'boss':
            self.color = DARK_RED
            self.speed = 1
            self.health = 500
            self.max_health = 500
            self.exp_value = 500
            self.attack_cooldown = 0

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.attack_cooldown = 0

    def update(self, player, obstacles, projectiles):
        # Calculate distance to player
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        if self.type == 'melee' or self.type == 'tank' or self.type == 'boss':
            if distance < 200:
                # Move towards player
                self.move_towards_player(player, obstacles)

                # Collision with player
                if self.rect.colliderect(player.rect):
                    if self.attack_cooldown == 0:
                        damage = 5 if self.type == 'melee' else 10  # Tanks and boss do more damage
                        player.take_damage(damage)
                        self.attack_cooldown = 30  # Cooldown frames

            # Update attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

        elif self.type == 'archer':
            self.archer_behavior(player, obstacles, projectiles)

        elif self.type == 'healer':
            self.healer_behavior()

        elif self.type == 'assassin':
            self.assassin_behavior(player, obstacles)

    def move_towards_player(self, player, obstacles):
        dx = dy = 0
        if player.rect.centerx > self.rect.centerx:
            dx = self.speed
        if player.rect.centerx < self.rect.centerx:
            dx = -self.speed
        if player.rect.centery > self.rect.centery:
            dy = self.speed
        if player.rect.centery < self.rect.centery:
            dy = -self.speed

        # Normalize movement to avoid faster diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        # Update position with collision
        self.move(dx, dy, obstacles)

    def archer_behavior(self, player, obstacles, projectiles):
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        if distance < 300:
            # Move away from player if too close
            if distance < 150:
                dx = dy = 0
                if player.rect.centerx > self.rect.centerx:
                    dx = -self.speed
                if player.rect.centerx < self.rect.centerx:
                    dx = self.speed
                if player.rect.centery > self.rect.centery:
                    dy = -self.speed
                if player.rect.centery < self.rect.centery:
                    dy = self.speed

                if dx != 0 and dy != 0:
                    dx *= 0.7071
                    dy *= 0.7071

                self.move(dx, dy, obstacles)

            # Attack player
            if self.attack_cooldown == 0:
                self.shoot_arrow(player, projectiles)
                self.attack_cooldown = random.randint(60, 120)  # Random cooldown between shots

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def healer_behavior(self):
        # Healer heals nearby enemies
        if self.heal_cooldown == 0:
            # Logic to heal nearby enemies
            self.heal_cooldown = 120  # Cooldown before next heal
        else:
            self.heal_cooldown -= 1

    def assassin_behavior(self, player, obstacles):
        # Assassin moves quickly towards the player and attacks
        self.move_towards_player(player, obstacles)
        if self.rect.colliderect(player.rect):
            if self.attack_cooldown == 0:
                damage = 15  # High damage
                player.take_damage(damage)
                self.attack_cooldown = 60  # Cooldown frames
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def move(self, dx, dy, obstacles):
        if dx != 0:
            self.rect.x += dx
            self.collide(dx, 0, obstacles)
        if dy != 0:
            self.rect.y += dy
            self.collide(0, dy, obstacles)
        # Prevent enemy from moving out of bounds
        self.rect.clamp_ip(pygame.Rect(10, HUD_HEIGHT + 10, WIDTH - 20, HEIGHT - HUD_HEIGHT - 20))

    def collide(self, dx, dy, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dx > 0:  # Moving right
                    self.rect.right = obstacle.rect.left
                if dx < 0:  # Moving left
                    self.rect.left = obstacle.rect.right
                if dy > 0:  # Moving down
                    self.rect.bottom = obstacle.rect.top
                if dy < 0:  # Moving up
                    self.rect.top = obstacle.rect.bottom

    def shoot_arrow(self, player, projectiles):
        # Shoot a projectile towards the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        norm = math.hypot(dx, dy)
        if norm != 0:
            dx /= norm
            dy /= norm
        arrow = Projectile(self.rect.centerx, self.rect.centery, dx, dy, 10, color=DARK_RED, target_type='player')
        projectiles.append(arrow)

    def take_damage(self, amount):
        self.health -= amount

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw health bar above enemy
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, self.rect.width * health_ratio, 5))

