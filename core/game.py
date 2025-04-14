# core/game.py
import pygame
from core.renderer import Renderer
from core.events import EventManager
from core.utils import load_config


class Game:
    def __init__(self, config_path="config.py"):
        self.running = False
        self.current_scene = None
        self.scenes = {}
        self.config = load_config(config_path)

        # Initialize PyGame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.config.get('width', 800), self.config.get('height', 600))
        )
        pygame.display.set_caption(self.config.get('title', 'Rail Builder'))

        # Initialize core systems
        self.renderer = Renderer(self.screen)
        self.event_manager = EventManager()
        self.clock = pygame.time.Clock()

        # Game state
        self.current_level = 0
        self.completed_levels = set()
        self.player_data = {
            'name': 'Player',
            'currency': 1000,
            'unlocked_levels': 1
        }

    def register_scene(self, name, scene):
        """Register a scene to the game."""
        self.scenes[name] = scene
        scene.game = self  # Give the scene a reference to the game

    def change_scene(self, scene_name):
        """Change to a different scene."""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
            self.current_scene = self.scenes[scene_name]
            self.current_scene.enter()
            return True
        return False

    def start(self, initial_scene="main_menu"):
        """Start the game loop with the specified initial scene."""
        if not self.change_scene(initial_scene):
            raise ValueError(f"Initial scene '{initial_scene}' not registered.")

        self.running = True
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.event_manager.handle_event(event)
                if self.current_scene:
                    self.current_scene.handle_event(event)

            # Update game state
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            if self.current_scene:
                self.current_scene.update(dt)

            # Render the scene
            self.renderer.clear((200, 200, 200))  # Light gray background
            if self.current_scene:
                self.current_scene.render(self.renderer)
            pygame.display.flip()

    def quit(self):
        """Quit the game."""
        self.running = False
        pygame.quit()

    def load_level(self, level_number):
        """Load a specific level."""
        if level_number <= len(self.config.get('levels', [])) and (
                level_number <= self.player_data['unlocked_levels']):
            self.current_level = level_number
            self.change_scene(f"level_{level_number}")
            return True
        return False

    def complete_level(self, level_number, score=0):
        """Mark a level as completed and unlock the next level."""
        self.completed_levels.add(level_number)
        if level_number == self.player_data['unlocked_levels']:
            self.player_data['unlocked_levels'] = min(
                level_number + 1,
                len(self.config.get('levels', []))
            )
        # Here you could also save scores, etc.
        return self.player_data['unlocked_levels']

    def save_game(self):
        """Save the current game state."""
        # This is a placeholder - implement actual saving logic
        print("Game saved")
        return True

    def load_game(self):
        """Load a saved game state."""
        # This is a placeholder - implement actual loading logic
        print("Game loaded")
        return True