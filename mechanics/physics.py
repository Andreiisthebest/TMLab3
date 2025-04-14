# mechanics/physics.py
import math


class PhysicsEngine:
    """Simple physics engine for the game."""

    def __init__(self):
        self.gravity = 9.8
        self.friction = 0.1

    def calculate_distance(self, pos1, pos2):
        """Calculate distance between two points."""
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_direction(self, pos1, pos2):
        """Calculate direction vector from pos1 to pos2."""
        x1, y1 = pos1
        x2, y2 = pos2
        dx = x2 - x1
        dy = y2 - y1
        magnitude = math.sqrt(dx * dx + dy * dy)

        if magnitude == 0:
            return (0, 0)

        return (dx / magnitude, dy / magnitude)

    def calculate_cost(self, distance, terrain_factor=1.0):
        """Calculate cost based on distance and terrain."""
        base_cost = distance * 0.5
        return int(base_cost * terrain_factor)