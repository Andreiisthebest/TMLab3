# scenes/menu.py
import pygame
from core.game import Game


class MenuScene:
    """Main menu scene for the game."""

    def __init__(self):
        self.game = None  # Will be set when registered with the game
        self.buttons = []
        self.selected_button = 0
        self.button_rects = []

    def enter(self):
        """Called when this scene becomes active."""
        # Create buttons for Play, Load, Settings, Quit
        self.buttons = [
            {"text": "Play", "action": self.start_game},
            {"text": "Load Game", "action": self.load_game},
            {"text": "Settings", "action": self.open_settings},
            {"text": "Quit", "action": self.quit_game}
        ]
        self.selected_button = 0

    def exit(self):
        """Called when this scene is no longer active."""
        pass

    def handle_event(self, event):
        """Handle an event."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_button]["action"]()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if any button was clicked
            for i, button_rect in enumerate(self.button_rects):
                if button_rect.collidepoint(event.pos):
                    self.buttons[i]["action"]()
                    break

    def update(self, dt):
        """Update the scene state."""
        pass

    def render(self, renderer):
        """Render the scene."""
        # Draw the title
        title_rect = renderer.draw_text("Rail Builder", 48, (0, 0, 0),
                                        (renderer.screen.get_width() // 2, 100),
                                        centered=True)

        # Draw the buttons
        self.button_rects = []
        button_y = 200
        for i, button in enumerate(self.buttons):
            color = (100, 100, 255) if i == self.selected_button else (150, 150, 150)
            button_rect = pygame.Rect(0, 0, 200, 50)
            button_rect.center = (renderer.screen.get_width() // 2, button_y)
            renderer.draw_rect(button_rect, color)

            text_rect = renderer.draw_text(button["text"], 24, (0, 0, 0),
                                           button_rect.center, centered=True)
            self.button_rects.append(button_rect)
            button_y += 70

    def start_game(self):
        """Start a new game."""
        self.game.load_level(1)
        self.game.change_scene("gameplay")

    def load_game(self):
        """Load a saved game."""
        success = self.game.load_game()
        if success:
            self.game.change_scene("gameplay")

    def open_settings(self):
        """Open the settings menu."""
        # Implement settings scene if needed
        pass

    def quit_game(self):
        """Quit the game."""
        self.game.quit()


class SettingsMenu:
    """Settings menu scene."""

    def __init__(self):
        self.game = None
        self.settings = {
            "Sound Volume": 50,
            "Music Volume": 50,
            "Fullscreen": False
        }
        self.selected_setting = 0

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % len(self.settings)
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % len(self.settings)
            elif event.key == pygame.K_LEFT:
                self._adjust_setting(-1)
            elif event.key == pygame.K_RIGHT:
                self._adjust_setting(1)
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def _adjust_setting(self, direction):
        setting_name = list(self.settings.keys())[self.selected_setting]
        setting_value = self.settings[setting_name]

        if setting_name.endswith("Volume"):
            # Adjust volume by 5%
            new_value = max(0, min(100, setting_value + direction * 5))
            self.settings[setting_name] = new_value
        elif setting_name == "Fullscreen":
            self.settings[setting_name] = not setting_value

    def update(self, dt):
        pass

    def render(self, renderer):
        renderer.draw_text("Settings", 48, (0, 0, 0),
                           (renderer.screen.get_width() // 2, 100), centered=True)

        y = 200
        for i, (setting_name, setting_value) in enumerate(self.settings.items()):
            color = (100, 100, 255) if i == self.selected_setting else (0, 0, 0)

            renderer.draw_text(setting_name, 24, color,
                               (renderer.screen.get_width() // 2 - 150, y))

            if setting_name.endswith("Volume"):
                # Draw volume bar
                bar_rect = pygame.Rect(renderer.screen.get_width() // 2, y, 200, 24)
                renderer.draw_rect(bar_rect, (200, 200, 200), 1)
                filled_rect = pygame.Rect(bar_rect.left, bar_rect.top,
                                          bar_rect.width * setting_value / 100,
                                          bar_rect.height)
                renderer.draw_rect(filled_rect, (0, 200, 0))
            elif setting_name == "Fullscreen":
                text = "ON" if setting_value else "OFF"
                renderer.draw_text(text, 24, (0, 150, 0) if setting_value else (150, 0, 0),
                                   (renderer.screen.get_width() // 2 + 100, y))

            y += 60

        renderer.draw_text("Press ESC to return to the main menu", 20, (100, 100, 100),
                           (renderer.screen.get_width() // 2, renderer.screen.get_height() - 50),
                           centered=True)