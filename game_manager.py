"""
game_manager.py
This module contains the GameManager class, which is responsible for managing the overall game state, including player, enemies, obstacles, potions, coins, projectiles, and various game states such as 'playing', 'paused', 'game_over', and 'level_up'. It also handles input, updates game entities, and manages the drawing of the game screen.
Classes:
    GameManager: Manages the overall game state and game entities.
GameManager Methods:
    __init__: Initializes the game manager and sets up initial game entities and state.
    setup_obstacles: Sets up game obstacles like walls and trees.
    add_random_tree: Adds a tree obstacle at a random location.
    update: Updates the game state, including player, enemies, and other objects.
    handle_level_up: Handles the level-up state where the player chooses a stat to increase.
    update_enemies: Updates all enemies and handles respawns and deaths.
    spawn_enemy: Spawns an enemy at a random location.
    spawn_boss: Spawns the boss enemy.
    update_potions: Handles potions spawning and player picking up potions.
    update_coins: Handles coins spawning and player collecting coins.
    update_projectiles: Updates all projectiles.
    draw: Draws all game entities and the HUD.
    draw_title_screen: Draws the title screen.
    show_help_menu: Displays the help menu.
    save_game: Saves the current game state.
    load_game: Loads a saved game state.
    run: Main game loop.
"""

import pygame
import sys
import random
from constants import *
from player import Player
from enemy import Enemy
from obstacle import Obstacle
from potion import Potion
from coin import Coin
from projectile import Projectile
from input_manager import InputManager
from hud_manager import HUDManager
from helpers import draw_text
import pickle  # For save/load functionality



class GameManager:
    def __init__(self):
        # Initialize player
        self.player = Player(WIDTH // 2, HUD_HEIGHT + (HEIGHT - HUD_HEIGHT) // 2)

        # Initialize other game entities
        self.enemies = []
        self.obstacles = []
        self.potions = []
        self.coins = []
        self.projectiles = []  # Initialize an empty list for projectiles

        # Game state
        self.enemy_respawn_timer = 0
        self.enemies_defeated = 0
        self.boss_spawned = False
        self.potion_spawn_timer = 0
        self.coin_spawn_timer = 0

        # Managers
        self.input_manager = InputManager()
        self.hud_manager = HUDManager(self.player)

        # Set up obstacles
        self.setup_obstacles()

        # Game state management
        self.state = 'title'  # Possible states: 'title', 'playing', 'paused', 'game_over', 'level_up'
        self.previous_state = None  # To keep track of the state before menus

    def setup_obstacles(self):
        """Set up game obstacles like walls and trees."""
        self.walls = [
            Obstacle(0, HUD_HEIGHT, WIDTH, 10, DARK_GREEN),  # Top wall
            Obstacle(0, HEIGHT - 10, WIDTH, 10, DARK_GREEN),  # Bottom wall
            Obstacle(0, HUD_HEIGHT, 10, HEIGHT - HUD_HEIGHT, DARK_GREEN),  # Left wall
            Obstacle(WIDTH - 10, HUD_HEIGHT, 10, HEIGHT - HUD_HEIGHT, DARK_GREEN)  # Right wall
        ]
        self.obstacles.extend(self.walls)
        # Add trees to obstacles
        for _ in range(20):
            self.add_random_tree()

    def add_random_tree(self):
        """Add a tree obstacle at a random location."""
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
            tree = Obstacle(x, y, TILE_SIZE, TILE_SIZE)
            if not any(tree.rect.colliderect(ob.rect) for ob in self.obstacles):
                self.obstacles.append(tree)
                break

    def update(self, events):
        """Update the game state, including player, enemies, and other objects."""
        self.input_manager.handle_input(events)
        actions = self.input_manager.get_actions()

        if self.state == 'playing':
            if actions["pause"]:
                self.state = 'paused'
                return

            if actions["help"]:
                self.show_help_menu(previous_state='playing')
                return

            # Update entities
            self.player.update(self.input_manager, self.obstacles, self.enemies, self.coins, self.projectiles)
            self.update_enemies()
            self.update_potions()
            self.update_coins()
            self.update_projectiles()

            # Check for level up
            if self.player.level_up_pending:
                self.state = 'level_up'

            # Check for game over
            if self.player.health <= 0:
                self.state = 'game_over'

        elif self.state == 'paused':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or self.input_manager.actions.get("pause"):
                        self.state = 'playing'
                    elif event.key == pygame.K_h or self.input_manager.actions.get("help"):
                        self.show_help_menu(previous_state='paused')
                    elif event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()

        elif self.state == 'level_up':
            self.handle_level_up(events)

        elif self.state == 'title':
            # Handle input in the title menu
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = 'playing'
                    elif event.key == pygame.K_h:
                        self.show_help_menu(previous_state='title')
            # No need to update entities in the title menu

        elif self.state == 'game_over':
            # Handle input in the game over menu
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__init__()  # Restart the game
                        self.state = 'playing'
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def handle_level_up(self, events):
        """Handle the level-up state where the player chooses a stat to increase."""
        self.draw()
        self.hud_manager.draw_level_up_menu(SCREEN)
        pygame.display.flip()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.increase_stat('max_mana')
                    self.state = 'playing'
                    self.player.level_up_pending = False
                elif event.key == pygame.K_2:
                    self.player.increase_stat('magic_damage')
                    self.state = 'playing'
                    self.player.level_up_pending = False
                elif event.key == pygame.K_3:
                    self.player.increase_stat('max_health')
                    self.state = 'playing'
                    self.player.level_up_pending = False
                elif event.key == pygame.K_4:
                    self.player.increase_stat('sword_damage')
                    self.state = 'playing'
                    self.player.level_up_pending = False

    def update_enemies(self):
        """Update all enemies and handle respawns and deaths."""
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.obstacles, self.projectiles)
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.enemies_defeated += 1
                self.player.increase_score(enemy.exp_value)

        # Boss spawn logic
        if self.enemies_defeated >= 20 and not self.boss_spawned:
            self.spawn_boss()
            self.boss_spawned = True

        # Respawn logic if necessary
        if not self.boss_spawned:
            self.enemy_respawn_timer += 1
            if self.enemy_respawn_timer >= 180:
                self.enemy_respawn_timer = 0
                self.spawn_enemy()

    def spawn_enemy(self):
        """Spawn an enemy at a random location."""
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
            enemy_type = random.choice(['melee', 'archer', 'tank', 'healer', 'assassin'])
            enemy = Enemy(x, y, enemy_type=enemy_type)
            collision = False
            for obstacle in self.obstacles:
                if enemy.rect.colliderect(obstacle.rect):
                    collision = True
                    break
            if not collision and not enemy.rect.colliderect(self.player.rect):
                self.enemies.append(enemy)
                break

    def spawn_boss(self):
        """Spawn the boss enemy."""
        boss = Enemy(WIDTH // 2, HEIGHT // 2, enemy_type='boss')
        self.enemies.append(boss)

    def update_potions(self):
        """Handle potions spawning and player picking up potions."""
        if not self.potions:
            self.potion_spawn_timer += 1
            if self.potion_spawn_timer >= random.randint(300, 600):
                self.potion_spawn_timer = 0
                while True:
                    x = random.randint(50, WIDTH - 50)
                    y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
                    potion_type = random.choice(['health', 'mana'])
                    potion = Potion(x, y, potion_type)
                    collision = False
                    if potion.rect.colliderect(self.player.rect):
                        collision = True
                    for obstacle in self.obstacles:
                        if potion.rect.colliderect(obstacle.rect):
                            collision = True
                            break
                    if not collision:
                        self.potions.append(potion)
                        break
        else:
            for potion in self.potions[:]:
                if self.player.rect.colliderect(potion.rect):
                    if potion.potion_type == 'health':
                        self.player.health += 30
                        if self.player.health > self.player.max_health:
                            self.player.health = self.player.max_health
                    else:
                        self.player.mana += 50
                        if self.player.mana > self.player.max_mana:
                            self.player.mana = self.player.max_mana
                    self.potions.remove(potion)

    def update_coins(self):
        """Handle coins spawning and player collecting coins."""
        self.coin_spawn_timer += 1
        if self.coin_spawn_timer >= random.randint(200, 400):
            self.coin_spawn_timer = 0
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
                coin = Coin(x, y)
                collision = False
                if coin.rect.colliderect(self.player.rect):
                    collision = True
                for obstacle in self.obstacles:
                    if coin.rect.colliderect(obstacle.rect):
                        collision = True
                        break
                if not collision:
                    self.coins.append(coin)
                    break

    def update_projectiles(self):
        """Update all projectiles."""
        for projectile in self.projectiles[:]:
            remove = projectile.update(self.obstacles, self.player, self.enemies)
            if remove:
                self.projectiles.remove(projectile)

    def draw(self):
        """Draw all game entities and the HUD."""
        if self.state == 'title':
            self.draw_title_screen()
        elif self.state == 'playing' or self.state == 'level_up':
            SCREEN.fill(BLACK)
            for obstacle in self.obstacles:
                obstacle.draw(SCREEN)
            for potion in self.potions:
                potion.draw(SCREEN)
            for coin in self.coins:
                coin.draw(SCREEN)
            for enemy in self.enemies:
                enemy.draw(SCREEN)
            self.player.draw(SCREEN)
            self.hud_manager.draw_hud(SCREEN)  # HUD is drawn through the HUDManager
            for projectile in self.projectiles:
                projectile.draw(SCREEN)
        elif self.state == 'paused':
            # Draw the game screen behind the pause message
            SCREEN.fill(BLACK)
            for obstacle in self.obstacles:
                obstacle.draw(SCREEN)
            for potion in self.potions:
                potion.draw(SCREEN)
            for coin in self.coins:
                coin.draw(SCREEN)
            for enemy in self.enemies:
                enemy.draw(SCREEN)
            self.player.draw(SCREEN)
            self.hud_manager.draw_hud(SCREEN)
            for projectile in self.projectiles:
                projectile.draw(SCREEN)
            self.hud_manager.draw_pause(SCREEN)
        elif self.state == 'game_over':
            SCREEN.fill(BLACK)
            self.hud_manager.draw_game_over(SCREEN, self.enemies_defeated, self.player.score)

    def draw_title_screen(self):
        """Draw the title screen."""
        SCREEN.fill(BLACK)
        draw_text(SCREEN, "Top-Down Adventure", (WIDTH // 2 - 150, HEIGHT // 2 - 100), WHITE, FONT_LARGE)
        draw_text(SCREEN, "Press ENTER to Start", (WIDTH // 2 - 100, HEIGHT // 2), WHITE)
        draw_text(SCREEN, "Press H for Help", (WIDTH // 2 - 80, HEIGHT // 2 + 50), WHITE)

    def show_help_menu(self, previous_state):
        """Display the help menu."""
        self.previous_state = previous_state
        help_lines = [
            "Controls:",
            "- Move: Arrow Keys/WASD or Left Stick",
            "- Melee Attack: Spacebar or R1",
            "- Magic Attack: F or L1 (Hold to charge)",
            "- Cycle Magic: Q/E or L2/R2",
            "- Pause: P or Options button",
            "",
            "Game Mechanics:",
            "- Defeat enemies to gain experience and level up.",
            "- Collect coins for score and experience.",
            "- Use potions to restore health or mana.",
            "- Mana regenerates over time.",
            "- Be strategic with magic usage to manage mana.",
            "",
            "Level Up Choices:",
            "- On leveling up, choose a stat to increase.",
            "- Options: Max Mana, Magic Damage, Max Health, Sword Damage.",
        ]
        in_help = True
        while in_help:
            SCREEN.fill(BLACK)
            draw_text(SCREEN, "Help", (WIDTH // 2 - 50, 100), WHITE, FONT_LARGE)
            for i, line in enumerate(help_lines):
                draw_text(SCREEN, line, (WIDTH // 2 - 300, 200 + i * 25), WHITE)
            draw_text(SCREEN, "Press ESC to Return", (WIDTH // 2 - 100, HEIGHT - 100), YELLOW)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_help = False
                        self.state = self.previous_state

    def save_game(self):
        """Save the current game state."""
        game_state = {
            'player': self.player.get_state(),
            'enemies_defeated': self.enemies_defeated,
            'score': self.player.score,
            # Add other necessary game state data
        }
        with open('savegame.pkl', 'wb') as f:
            pickle.dump(game_state, f)
        print("Game saved.")

    def load_game(self):
        """Load a saved game state."""
        try:
            with open('savegame.pkl', 'rb') as f:
                game_state = pickle.load(f)
            self.player.set_state(game_state['player'])
            self.enemies_defeated = game_state['enemies_defeated']
            self.player.score = game_state['score']
            # Restore other game state data
            print("Game loaded.")
        except FileNotFoundError:
            print("No saved game found.")

    def run(self):
        """Main game loop."""
        running = True
        while running:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            self.update(events)
            self.draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()


