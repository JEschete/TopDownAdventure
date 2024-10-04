
# Top-Down Adventure Game

Top-Down Adventure is a high-fantasy action RPG built using Pygame. It features dynamic combat with melee, ranged, and magic attacks. The game includes enemies of various types (melee, archers, tanks, healers, assassins, and bosses), collectible items like potions and coins, and a level-up system that allows players to increase stats such as health, mana, magic damage, and sword damage.

---

## Table of Contents

- [Installation](#installation)
- [Gameplay Overview](#gameplay-overview)
- [Features](#features)
- [Game Files](#game-files)
- [Controls](#controls)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Installation

1. Ensure that you have [Python](https://www.python.org/downloads/) installed on your system.
2. Install [Pygame](https://www.pygame.org/wiki/GettingStarted) using pip:
    ```bash
    pip install pygame
    ```
3. Clone this repository:
    ```bash
    git clone https://github.com/your_username/your_project_name.git
    ```
4. Navigate to the project directory:
    ```bash
    cd your_project_name
    ```
5. Run the game:
    ```bash
    python main.py
    ```

---

## Gameplay Overview

### Objective

The player controls a character in a top-down view, navigating through various enemies, collecting potions and coins, and leveling up to enhance their abilities. The main objective is to defeat enemies while staying alive by managing health, mana, and strategic use of magic.

### Enemy Types

- **Melee:** Standard close-range attackers.
- **Archer:** Ranged attackers that keep distance from the player.
- **Tank:** Slow but with high health.
- **Healer:** Can heal nearby enemies.
- **Assassin:** Fast and deals high damage.
- **Boss:** Large health pool with powerful attacks, appears after defeating enough enemies.

### Items

- **Potions:** Health and mana potions are scattered throughout the game.
- **Coins:** Collect coins to increase your score and gain experience.

### Leveling Up

As you defeat enemies and collect items, you gain experience points (EXP). Once you gain enough EXP, you will have the option to increase one of the following stats:
- **Max Mana**
- **Magic Damage**
- **Max Health**
- **Sword Damage**

---

## Features

- **Dynamic Combat:** Engage in melee combat or cast powerful magic spells. Use strategy to defeat different enemy types.
- **Level Up System:** Earn experience points and increase your stats to improve your combat effectiveness.
- **HUD:** A heads-up display shows player stats like health, mana, level, and score in real-time.
- **Obstacles:** Various environmental obstacles make movement and combat more challenging.
- **Magic Spells:** Use spells like Fireball, Ice Spike, and Lightning Bolt, each with unique colors and effects.

---

## Game Files

The project is composed of multiple modules that handle different aspects of the game:

1. **coin.py** – Defines the `Coin` class.
2. **constants.py** – Contains all constants used across the game, such as colors, screen dimensions, and fonts.
3. **enemy.py** – Defines the `Enemy` class with various enemy behaviors.
4. **game_manager.py** – The main game loop and overall game state management.
5. **helpers.py** – Helper functions for rendering text.
6. **hud_manager.py** – Handles the heads-up display (HUD) for the player’s health, mana, and experience.
7. **input_manager.py** – Manages player input from both keyboard and joystick.
8. **main.py** – The entry point to start the game.
9. **obstacle.py** – Defines the `Obstacle` class for environmental barriers.
10. **player.py** – Defines the `Player` class and player mechanics (movement, combat, leveling up).
11. **potion.py** – Defines the `Potion` class, handling health and mana potions.
12. **projectile.py** – Defines the `Projectile` class for magic attacks.
13. **KnownIssues.txt** – Lists known bugs or issues with the current build.

---

## Controls

### Keyboard Controls

- **Arrow Keys / WASD:** Move the player
- **Spacebar:** Melee attack
- **F:** Magic attack (Hold to charge)
- **Q / E:** Cycle through magic spells
- **P:** Pause the game
- **H:** Display help menu

### Gamepad Controls

- **Left Stick:** Move the player
- **R1:** Melee attack
- **L1:** Magic attack (Hold to charge)
- **L2 / R2:** Cycle through magic spells
- **Options Button:** Pause the game


---

## Future Improvements

- **Character Sprites:** Add sprites for the player, enemies, and items to enhance visual appeal.
- **Sound Effects and Music:** Implement background music, sound effects for combat, and interactions.
- **Multiple Levels:** Introduce multiple levels and environments to explore.
- **Improve Menus:** Fix the menu flickering issues and enhance usability.
- **Multiplayer:** Add support for cooperative multiplayer mode in the future.

---

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.
