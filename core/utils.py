# core/utils.py
import importlib.util
import os
import pygame

def load_config(path):
    """Load a configuration file."""
    try:
        # Handle both module paths and file paths
        if path.endswith('.py'):
            # Load as Python file
            spec = importlib.util.spec_from_file_location("config", path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            return config_module.CONFIG
        else:
            # Load as module
            config_module = importlib.import_module(path)
            return config_module.CONFIG
    except (ImportError, AttributeError) as e:
        print(f"Error loading configuration: {e}")
        # Return default config
        return {
            'title': 'Rail Builder',
            'width': 800,
            'height': 600,
            'levels': [
                {'name': 'Level 1', 'nodes': 3, 'budget': 500},
                {'name': 'Level 2', 'nodes': 4, 'budget': 700},
                {'name': 'Level 3', 'nodes': 5, 'budget': 900},
                {'name': 'Level 4', 'nodes': 6, 'budget': 1200},
                {'name': 'Level 5', 'nodes': 7, 'budget': 1500},
                {'name': 'Level 6', 'nodes': 8, 'budget': 2000},
            ]
        }

def load_image(path, scale=None):
    """Load an image from a file."""
    try:
        image = pygame.image.load(path)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Create a placeholder image
        surf = pygame.Surface((64, 64))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf