# main.py
import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game import Game
from scenes.menu import MenuScene, SettingsMenu
from scenes.gameplay import GameplayScene
from scenes.game_over import GameOverScene


def main():
    """Main entry point for the game."""
    # Create the game instance
    game = Game()

    # Register scenes
    game.register_scene("menu", MenuScene())
    game.register_scene("settings", SettingsMenu())
    game.register_scene("gameplay", GameplayScene())
    game.register_scene("game_over", GameOverScene())

    # Start the game
    game.start("menu")


if __name__ == "__main__":
    main()