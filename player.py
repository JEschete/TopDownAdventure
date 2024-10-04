"""
This module defines the Player class for a top-down adventure game using Pygame.
Classes:
    Player: Represents the player character in the game.
Player class:
    Methods:
        __init__(self, x, y):
            Initializes the player with position (x, y) and various attributes.
        update(self, input_manager, obstacles, enemies, coins, projectiles):
            Updates the player's state based on input actions and interactions with the game world.
        move(self, dx, dy, obstacles):
            Moves the player by dx and dy while handling collisions with obstacles.
        collide(self, dx, dy, obstacles):
            Handles collisions with obstacles when the player moves.
        attack(self, enemies):
            Handles the player's attacking logic and damages enemies within attack range.
        get_attack_rect(self):
            Returns the attack area based on the player's facing direction.
        cast_magic(self, projectiles, enemies):
            Handles the magic attack logic, creating a projectile targeting the nearest enemy.
        take_damage(self, amount):
            Reduces the player's health by the specified amount, considering active power-ups.
        increase_score(self, amount):
            Increases the player's score with a multiplier and handles combo logic.
        reset_multiplier(self):
            Resets the score multiplier and combo counter.
        draw(self, surface):
            Draws the player and its attack area if attacking.
        increase_stat(self, stat):
            Increases the specified stat upon leveling up.
        get_state(self):
            Returns the current state of the player for saving.
        set_state(self, state):
            Sets the player's state from a saved state.
        update_power_ups(self):
            Updates power-up timers and effects.
"""

import pygame
import math
from constants import *
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 30
        self.height = 30
        self.color = BLUE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.base_speed = 3
        self.speed = self.base_speed
        self.direction = 'down'  # Default facing down
        self.attacking = False
        self.attack_cooldown = 0
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.mana_recharge_rate = 0.1  # Mana regenerated per frame
        self.invincible = False
        self.invincible_timer = 0

        # Magic attack variables
        self.magic_hold_time = 0
        self.magic_charge_level = 0
        self.mana_recharge_cooldown = 0  # Cooldown before mana starts regenerating
        self.magic_attack_cooldown = 0  # New variable for magic attack cooldown

        # Experience and Leveling
        self.level = 1
        self.experience = 0
        self.next_level_exp = 100
        self.level_up_pending = False  # Flag to pause the game on level up

        # Damage stats
        self.magic_damage = 20
        self.sword_damage = 10

        # Score
        self.score = 0
        self.score_multiplier = 1
        self.combo_counter = 0

        # Health regeneration
        self.health_regen_timer = 0

        # Spells
        self.spells = MAGIC_SPELLS
        self.current_spell_index = 0
        self.current_spell = self.spells[self.current_spell_index]

        # Power-up status
        self.power_ups = {
            'speed': False,
            'damage': False,
            'shield': False,
        }
        self.power_up_timers = {
            'speed': 0,
            'damage': 0,
            'shield': 0,
        }

    def update(self, input_manager, obstacles, enemies, coins, projectiles):
        """Update player based on input actions passed by the InputManager."""
        actions = input_manager.get_actions()
        dx = dy = 0

        # Movement logic based on actions from InputManager
        if actions["move_left"]:
            dx -= self.speed
            self.direction = 'left'
        if actions["move_right"]:
            dx += self.speed
            self.direction = 'right'
        if actions["move_up"]:
            dy -= self.speed
            self.direction = 'up'
        if actions["move_down"]:
            dy += self.speed
            self.direction = 'down'

        # Handle attacking
        if actions["attack"]:
            if self.attack_cooldown == 0:
                self.attacking = True
                self.attack_cooldown = 20
                self.attack(enemies)
        else:
            self.attacking = False

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Move player and handle collisions
        self.move(dx, dy, obstacles)

        # Handle magic
        if actions["magic"]:
            if self.mana > 0:
                self.magic_hold_time += 1
                self.mana -= 0.5  # Consumes mana when magic is used
                self.magic_attack_cooldown = 10
        else:
            # If magic key was released
            if self.magic_hold_time > 0:
                self.cast_magic(projectiles, enemies)
                self.magic_hold_time = 0

        # Update magic attack cooldown
        if self.magic_attack_cooldown > 0:
            self.magic_attack_cooldown -= 1

        # Mana regeneration
        if self.mana < self.max_mana:
            self.mana += self.mana_recharge_rate
            if self.mana > self.max_mana:
                self.mana = self.max_mana

        # Health regeneration (every 3 seconds)
        self.health_regen_timer += 1
        if self.health_regen_timer >= 180:
            self.health_regen_timer = 0
            if self.health < self.max_health:
                self.health += 1

        # Check collisions with coins
        for coin in coins[:]:
            if self.rect.colliderect(coin.rect):
                self.increase_score(10)
                self.experience += 5
                coins.remove(coin)

        # Level up if enough experience
        if self.experience >= self.next_level_exp:
            self.level_up_pending = True

        # Handle spell cycling
        if input_manager.was_pressed("next_spell"):
            self.current_spell_index = (self.current_spell_index + 1) % len(self.spells)
            self.current_spell = self.spells[self.current_spell_index]
        if input_manager.was_pressed("previous_spell"):
            self.current_spell_index = (self.current_spell_index - 1) % len(self.spells)
            self.current_spell = self.spells[self.current_spell_index]

        # Update power-up timers
        self.update_power_ups()

    def move(self, dx, dy, obstacles):
        """Move the player by dx and dy while handling collisions."""
        if dx != 0:
            self.rect.x += dx
            self.collide(dx, 0, obstacles)
        if dy != 0:
            self.rect.y += dy
            self.collide(0, dy, obstacles)
        # Prevent player from going out of bounds
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

    def attack(self, enemies):
        """Handle player attacking logic."""
        attack_rect = self.get_attack_rect()
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                damage = self.sword_damage
                if self.power_ups['damage']:
                    damage *= 2  # Double damage power-up
                enemy.take_damage(damage)
                # Sound effect can be played here if available

    def get_attack_rect(self):
        """Get the attack area based on player direction."""
        sword_length = 90  # Sword attack range

        if self.direction == 'up':
            return pygame.Rect(self.rect.centerx - 5, self.rect.top - sword_length, 10, sword_length)
        elif self.direction == 'down':
            return pygame.Rect(self.rect.centerx - 5, self.rect.bottom, 10, sword_length)
        elif self.direction == 'left':
            return pygame.Rect(self.rect.left - sword_length, self.rect.centery - 5, sword_length, 10)
        elif self.direction == 'right':
            return pygame.Rect(self.rect.right, self.rect.centery - 5, sword_length, 10)

    def cast_magic(self, projectiles, enemies):
        """Handle the magic attack logic."""
        # Calculate the direction based on the player's facing direction
        if self.direction == 'up':
            dx, dy = 0, -1
        elif self.direction == 'down':
            dx, dy = 0, 1
        elif self.direction == 'left':
            dx, dy = -1, 0
        elif self.direction == 'right':
            dx, dy = 1, 0

        # Find nearest enemy to target
        target = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
            if distance < min_distance:
                min_distance = distance
                target = enemy

        # Create a projectile
        magic_damage = self.magic_damage
        spell_color = SPELL_COLORS.get(self.current_spell, PURPLE)
        projectile = Projectile(self.rect.centerx, self.rect.centery, dx, dy, magic_damage, color=spell_color, target_type='enemies', target=target)
        # Append to projectiles list
        projectiles.append(projectile)
        # Sound effect can be played here if available

    def take_damage(self, amount):
        """Reduce player's health by the specified amount."""
        if self.power_ups['shield']:
            amount *= 0.5  # Reduce damage by half if shield is active
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.reset_multiplier()
        # Sound effect can be played here if available

    def increase_score(self, amount):
        """Increase player's score with multiplier and handle combo."""
        self.score += amount * self.score_multiplier
        self.combo_counter += 1
        if self.combo_counter % 5 == 0:
            self.score_multiplier += 0.5  # Increase multiplier every 5 combos

    def reset_multiplier(self):
        """Reset score multiplier and combo counter."""
        self.score_multiplier = 1
        self.combo_counter = 0

    def draw(self, surface):
        """Draw the player and its attack area if attacking."""
        pygame.draw.rect(surface, self.color, self.rect)
        if self.attacking:
            attack_rect = self.get_attack_rect()
            pygame.draw.rect(surface, YELLOW, attack_rect)

    def increase_stat(self, stat):
        """Increase the specified stat upon leveling up."""
        if stat == 'max_mana':
            self.max_mana += 20
            self.mana = self.max_mana
        elif stat == 'magic_damage':
            self.magic_damage += 5
        elif stat == 'max_health':
            self.max_health += 20
            self.health = self.max_health
        elif stat == 'sword_damage':
            self.sword_damage += 5
        # Level up
        self.level += 1
        self.experience = 0
        self.next_level_exp += 50

    def get_state(self):
        """Get the current state of the player for saving."""
        return {
            'position': self.rect.topleft,
            'health': self.health,
            'mana': self.mana,
            'level': self.level,
            'experience': self.experience,
            'score': self.score,
            'current_spell_index': self.current_spell_index,
            'magic_damage': self.magic_damage,
            'sword_damage': self.sword_damage,
            # Add other necessary player attributes
        }

    def set_state(self, state):
        """Set the player's state from a saved state."""
        self.rect.topleft = state['position']
        self.health = state['health']
        self.mana = state['mana']
        self.level = state['level']
        self.experience = state['experience']
        self.score = state['score']
        self.current_spell_index = state['current_spell_index']
        self.current_spell = self.spells[self.current_spell_index]
        self.magic_damage = state.get('magic_damage', self.magic_damage)
        self.sword_damage = state.get('sword_damage', self.sword_damage)
        # Restore other necessary player attributes

    def update_power_ups(self):
        """Update power-up timers and effects."""
        for power, active in self.power_ups.items():
            if active:
                self.power_up_timers[power] -= 1
                if self.power_up_timers[power] <= 0:
                    self.power_ups[power] = False
                    if power == 'speed':
                        self.speed = self.base_speed

