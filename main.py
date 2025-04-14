#!/usr/bin/env python3
import pygame
import sys
import os
from core.game import Game
from scenes.menu import MenuScene
from scenes.gameplay import GameplayScene
from scenes.game_over import GameOverScene


def initialize_game():
    """Initialize the game with all required scenes"""
    # Create the main game instance
    game = Game()

    # Register all game scenes
    game.add_scene("menu", MenuScene())
    game.add_scene("gameplay", GameplayScene())
    game.add_scene("game_over", GameOverScene())

    return game


def main():
    try:
        # Initialize pygame mixer (for sound)
        pygame.mixer.init()

        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        # Create and run the game
        game = initialize_game()
        game.change_scene("menu")  # Start with the main menu
        game.run()

    except Exception as e:
        # Log any critical errors
        print(f"Critical error: {e}")
        import traceback
        traceback.print_exc()

        # Try to show error message before quitting
        try:
            pygame.init()
            error_font = pygame.font.SysFont(None, 36)
            screen = pygame.display.set_mode((800, 600))
            screen.fill((50, 50, 50))

            lines = [
                "RailBuildingTycoon encountered an error:",
                str(e),
                "",
                "See console for details.",
                "",
                "The game will now close."
            ]

            for i, line in enumerate(lines):
                text = error_font.render(line, True, (255, 100, 100))
                screen.blit(text, (50, 50 + i * 40))

            pygame.display.flip()
            pygame.time.wait(5000)
        except:
            pass

        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()