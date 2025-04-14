import pygame
import pickle
import os
from .events import EventHandler
from .renderer import Renderer
from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_LEVELS, SAVE_FILE, BASE_LEVEL_COST, COST_INCREMENT


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rail Building Tycoon")

        self.clock = pygame.time.Clock()
        self.running = False
        self.dt = 0

        # Initialize core systems
        self.event_handler = EventHandler()
        self.renderer = Renderer(self.screen)

        # Game state
        self.current_scene = None
        self.scenes = {}
        self.player_data = {
            "current_level": 1,
            "completed_levels": [],
            "money": 0,
            "unlocked_items": ["basic_rail"]
        }

    def run(self):
        self.load_game()
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0

            # Process events
            self.event_handler.process_events()
            if self.event_handler.quit:
                self.running = False

            # Update current scene
            if self.current_scene:
                self.current_scene.update(self.dt)

                # Render
                self.renderer.clear()
                self.current_scene.render(self.renderer)
                self.renderer.present()

        self.save_game()
        self.cleanup()

    def load_game(self):
        """Load saved game data"""
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'rb') as f:
                    self.player_data = pickle.load(f)
            else:
                # Create new save file if it doesn't exist
                self.save_game()
        except (EOFError, pickle.PickleError) as e:
            print(f"Error loading save file: {e}")
            # Reset to default data
            self.player_data = {
                "current_level": 1,
                "completed_levels": [],
                "money": 0,
                "unlocked_items": ["basic_rail"]
            }
            self.save_game()

    def save_game(self):
        """Save game data"""
        try:
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
            with open(SAVE_FILE, 'wb') as f:
                pickle.dump(self.player_data, f)
        except Exception as e:
            print(f"Error saving game: {e}")

    def unlock_next_level(self):
        """Progress to the next level"""
        if self.player_data["current_level"] not in self.player_data["completed_levels"]:
            self.player_data["completed_levels"].append(self.player_data["current_level"])

        if self.player_data["current_level"] < MAX_LEVELS:
            self.player_data["current_level"] += 1
            self.save_game()
            return True
        return False

    def get_level_budget(self, level):
        """Calculate budget for a specific level"""
        return BASE_LEVEL_COST + (level - 1) * COST_INCREMENT

    def change_scene(self, scene_name, *args, **kwargs):
        """Switch to a different game scene with optional arguments"""
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter(*args, **kwargs)

    def add_scene(self, name, scene):
        """Add a scene to the game"""
        self.scenes[name] = scene
        scene.game = self

    def cleanup(self):
        """Clean up resources"""
        pygame.quit()