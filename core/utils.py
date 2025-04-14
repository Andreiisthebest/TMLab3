import os
import json
import pygame
from typing import Dict, Any, Optional


def load_image(path: str, scale: Optional[float] = None, convert_alpha: bool = True) -> pygame.Surface:
    """Load an image from the assets folder with optional scaling"""
    try:
        if convert_alpha:
            image = pygame.image.load(f"assets/images/{path}").convert_alpha()
        else:
            image = pygame.image.load(f"assets/images/{path}").convert()

        if scale is not None and scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)

        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface if image fails to load
        return pygame.Surface((32, 32), pygame.SRCALPHA)


def load_sound(path: str) -> pygame.mixer.Sound:
    """Load a sound from the assets folder"""
    try:
        return pygame.mixer.Sound(f"assets/sounds/{path}")
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        # Return a silent sound if loading fails
        return pygame.mixer.Sound(buffer=bytearray(44))


def load_font(path: str, size: int) -> pygame.font.Font:
    """Load a font from the assets folder"""
    try:
        return pygame.font.Font(f"assets/fonts/{path}", size)
    except:
        # Fall back to system font if custom font fails to load
        return pygame.font.SysFont(None, size)


def load_json(path: str) -> Dict[str, Any]:
    """Load JSON data from a file"""
    try:
        with open(f"data/{path}", "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading JSON {path}: {e}")
        return {}


def save_json(data: Dict[str, Any], path: str) -> bool:
    """Save data to a JSON file"""
    try:
        os.makedirs(os.path.dirname(f"data/{path}"), exist_ok=True)
        with open(f"data/{path}", "w") as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving JSON {path}: {e}")
        return False


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max"""
    return max(min_value, min(value, max_value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by t"""
    return a + (b - a) * t


def distance(p1: tuple, p2: tuple) -> float:
    """Calculate distance between two points"""
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def rotate_point(origin: tuple, point: tuple, angle: float) -> tuple:
    """Rotate a point around an origin by angle (in radians)"""
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return (qx, qy)