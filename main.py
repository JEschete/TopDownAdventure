"""
This script serves as the entry point for the TopDownAdventure game.
It imports the GameManager class from the game_manager module and initializes
an instance of GameManager to start the game.
Usage:
    Run this script directly to start the game.
Classes:
    GameManager: Manages the game state and controls the game loop.
Functions:
    None
Attributes:
    None
"""

from game_manager import GameManager

if __name__ == "__main__":
    # Start the game by initializing the GameManager
    game = GameManager()
    game.run()
