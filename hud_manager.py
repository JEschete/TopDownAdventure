"""
HUDManager class is responsible for managing and drawing the Heads-Up Display (HUD) elements on the game screen.
Attributes:
    player (Player): The player object containing health, mana, experience, and other attributes.
Methods:
    __init__(player):
        Initializes the HUDManager with the player object.
    draw_hud(surface):
        Draws the HUD elements on the given surface, including health bar, mana bar, experience bar, and various text elements.
    draw_game_over(surface, enemies_defeated, score):
        Draws the Game Over screen with the number of enemies defeated and the player's score.
    draw_pause(surface):
        Draws the Pause screen with options to resume, get help, save, and load the game.
    draw_level_up_menu(surface):
        Draws the Level Up menu with options to increase various player stats.
"""

import pygame
from constants import *
from helpers import draw_text

class HUDManager:
    def __init__(self, player):
        self.player = player

    def draw_hud(self, surface):
        # Draw HUD background
        pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, HUD_HEIGHT))

        # Health Bar
        bar_width = 200
        bar_height = 15
        pygame.draw.rect(surface, RED, (10, 10, bar_width, bar_height))
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(surface, GREEN, (10, 10, bar_width * health_ratio, bar_height))

        # Mana Bar
        pygame.draw.rect(surface, DARK_RED, (10, 40, bar_width, bar_height))
        mana_ratio = self.player.mana / self.player.max_mana
        pygame.draw.rect(surface, BLUE, (10, 40, bar_width * mana_ratio, bar_height))

        # Experience Bar
        pygame.draw.rect(surface, GRAY, (10, 70, bar_width, bar_height))
        exp_ratio = self.player.experience / self.player.next_level_exp
        pygame.draw.rect(surface, YELLOW, (10, 70, bar_width * exp_ratio, bar_height))

        # Text for Health, Mana, and Level
        surface.blit(FONT.render(f"Health: {int(self.player.health)}", True, WHITE), (220, 10))  # Health Text
        surface.blit(FONT.render(f"Mana: {int(self.player.mana)}", True, WHITE), (220, 40))  # Mana Text
        surface.blit(FONT.render(f"Level: {self.player.level}", True, WHITE), (220, 70))  # Level Text

        # Draw Score
        surface.blit(FONT.render(f"Score: {self.player.score}", True, WHITE), (WIDTH - 200, 10))  # Score Text

        # Display current spell
        spell_text = f"Spell: {self.player.current_spell}"
        surface.blit(FONT.render(spell_text, True, WHITE), (WIDTH - 200, 40))

        # Display score multiplier
        multiplier_text = f"Multiplier: x{self.player.score_multiplier}"
        surface.blit(FONT.render(multiplier_text, True, WHITE), (WIDTH - 200, 70))

    def draw_game_over(self, surface, enemies_defeated, score):
        # Draw Game Over screen
        surface.fill(BLACK)
        draw_text(surface, "Game Over", (WIDTH // 2 - 80, HEIGHT // 2 - 100), RED, FONT_LARGE)
        draw_text(surface, f"Enemies Defeated: {enemies_defeated}", (WIDTH // 2 - 100, HEIGHT // 2 - 50), WHITE)
        draw_text(surface, f"Score: {score}", (WIDTH // 2 - 50, HEIGHT // 2 - 20), WHITE)
        draw_text(surface, "Press ENTER to Play Again", (WIDTH // 2 - 120, HEIGHT // 2 + 20), WHITE)
        draw_text(surface, "Press ESC to Quit", (WIDTH // 2 - 80, HEIGHT // 2 + 50), WHITE)

    def draw_pause(self, surface):
        # Draw Pause screen
        draw_text(surface, "Paused", (WIDTH // 2 - 50, HEIGHT // 2 - 100), WHITE, FONT_LARGE)
        draw_text(surface, "Press P to Resume", (WIDTH // 2 - 100, HEIGHT // 2), WHITE)
        draw_text(surface, "Press H for Help", (WIDTH // 2 - 90, HEIGHT // 2 + 50), WHITE)
        draw_text(surface, "Press S to Save", (WIDTH // 2 - 80, HEIGHT // 2 + 100), WHITE)
        draw_text(surface, "Press L to Load", (WIDTH // 2 - 80, HEIGHT // 2 + 150), WHITE)

    def draw_level_up_menu(self, surface):
        # Draw Level Up menu
        surface.fill(BLACK)
        draw_text(surface, "Level Up!", (WIDTH // 2 - 80, HEIGHT // 2 - 150), YELLOW, FONT_LARGE)
        draw_text(surface, "Choose a stat to increase:", (WIDTH // 2 - 150, HEIGHT // 2 - 100), WHITE)
        draw_text(surface, "1. Increase Max Mana", (WIDTH // 2 - 100, HEIGHT // 2 - 50), WHITE)
        draw_text(surface, "2. Increase Magic Damage", (WIDTH // 2 - 100, HEIGHT // 2), WHITE)
        draw_text(surface, "3. Increase Max Health", (WIDTH // 2 - 100, HEIGHT // 2 + 50), WHITE)
        draw_text(surface, "4. Increase Sword Damage", (WIDTH // 2 - 100, HEIGHT // 2 + 100), WHITE)
