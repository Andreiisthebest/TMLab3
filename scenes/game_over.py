# scenes/game_over.py
import pygame


class GameOverScene:
    """Scene shown when a level is completed."""

    def __init__(self):
        self.game = None

    def enter(self):
        """Initialize the scene."""
        pass

    def exit(self):
        """Clean up when leaving the scene."""
        pass

    def handle_event(self, event):
        """Handle user input events."""
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            # Go to next level or back to menu
            next_level = self.game.current_level + 1
            if next_level <= len(self.game.config.get('levels', [])):
                self.game.load_level(next_level)
                self.game.change_scene("gameplay")
            else:
                self.game.change_scene("menu")

    def update(self, dt):
        """Update game state."""
        pass

    def render(self, renderer):
        """Render the game over scene."""
        # Draw completion message
        renderer.draw_text("Level Complete!", 48, (0, 150, 0),
                           (renderer.screen.get_width() // 2, 200), centered=True)

        # Draw next level prompt
        next_level = self.game.current_level + 1
        if next_level <= len(self.game.config.get('levels', [])):
            renderer.draw_text("Press any key to continue to the next level",
                               24, (0, 0, 0),
                               (renderer.screen.get_width() // 2, 300),
                               centered=True)
        else:
            renderer.draw_text("Congratulations! You've completed all levels!",
                               24, (0, 0, 0),
                               (renderer.screen.get_width() // 2, 300),
                               centered=True)
            renderer.draw_text("Press any key to return to the main menu",
                               24, (0, 0, 0),
                               (renderer.screen.get_width() // 2, 350),
                               centered=True)