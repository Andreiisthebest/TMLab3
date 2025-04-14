import pygame
import json
import math
from typing import List, Dict, Tuple
from config import GRID_SIZE


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.level_data = self.load_all_levels()
        self.towns = []
        self.rails = []
        self.total_cost = 0

    def load_all_levels(self) -> Dict[int, Dict]:
        """Load all level data from files"""
        levels = {}
        try:
            for i in range(1, 7):  # Assuming 6 levels
                with open(f"data/levels/level_{i}.json") as f:
                    levels[i] = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading levels: {e}")
            # Fallback to generated levels if files don't exist
            levels = self.generate_default_levels()
        return levels

    def generate_default_levels(self) -> Dict[int, Dict]:
        """Generate default levels if files are missing"""
        levels = {}
        for i in range(1, 7):
            levels[i] = {
                "towns": [
                    {"id": 1, "x": 2, "y": 2, "name": "Town A", "population": 1000},
                    {"id": 2, "x": 8, "y": 8, "name": "Town B", "population": 1500}
                ],
                "terrain": [],
                "optimal_path": [(2, 2), (8, 8)],
                "optimal_cost": 1000 * i
            }
        return levels

    def setup_level(self, level_num: int):
        """Initialize a level"""
        if level_num not in self.level_data:
            raise ValueError(f"Level {level_num} doesn't exist")

        self.current_level = level_num
        level = self.level_data[level_num]
        self.towns = level["towns"]
        self.rails = []
        self.total_cost = 0
        return level

    def add_rail(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], rail_type: str = "basic") -> float:
        """Add a rail segment between two points and return its cost"""
        # Calculate distance between points
        x1, y1 = start_pos
        x2, y2 = end_pos
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Calculate cost based on rail type and distance
        cost_per_unit = {
            "basic": 100,
            "advanced": 150,
            "bridge": 300,
            "tunnel": 400
        }.get(rail_type, 100)

        cost = distance * cost_per_unit

        # Add to rails list
        self.rails.append({
            "start": start_pos,
            "end": end_pos,
            "type": rail_type,
            "cost": cost
        })

        self.total_cost += cost
        return cost

    def remove_rail(self, position: Tuple[int, int], threshold: int = GRID_SIZE // 2) -> bool:
        """Remove rail segment near given position"""
        for i, rail in enumerate(self.rails):
            # Check distance to line segment
            if self.point_to_line_distance(position, rail["start"], rail["end"]) < threshold:
                self.total_cost -= rail["cost"]
                self.rails.pop(i)
                return True
        return False

    def point_to_line_distance(self, point: Tuple[int, int], line_start: Tuple[int, int],
                               line_end: Tuple[int, int]) -> float:
        """Calculate distance from point to line segment"""
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end

        # Line length
        line_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if line_len == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        # Project point onto line
        t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (line_len ** 2)
        t = max(0, min(1, t))

        # Nearest point on line
        nearest_x = x1 + t * (x2 - x1)
        nearest_y = y1 + t * (y2 - y1)

        return math.sqrt((x - nearest_x) ** 2 + (y - nearest_y) ** 2)

    def check_level_completion(self) -> Tuple[bool, str]:
        """Check if level is completed with validation logic"""
        if not self.towns or not self.rails:
            return False, "No towns or rails placed"

        # Check if all towns are connected
        connected_towns = set()
        town_positions = [(t["x"], t["y"]) for t in self.towns]

        for rail in self.rails:
            if rail["start"] in town_positions:
                connected_towns.add(rail["start"])
            if rail["end"] in town_positions:
                connected_towns.add(rail["end"])

        if len(connected_towns) != len(self.towns):
            return False, "Not all towns are connected"

        # Check if network is fully connected (all rails are connected)
        if not self.is_network_connected():
            return False, "Rail network is not fully connected"

        return True, "Level completed!"

    def is_network_connected(self) -> bool:
        """Check if all rail segments form a connected network"""
        if not self.rails:
            return False

        # Create a graph of rail connections
        graph = {}
        for rail in self.rails:
            start, end = rail["start"], rail["end"]
            if start not in graph:
                graph[start] = []
            if end not in graph:
                graph[end] = []
            graph[start].append(end)
            graph[end].append(start)

        # BFS to check connectivity
        visited = set()
        queue = [next(iter(graph.keys()))]  # Start with any node

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                queue.extend(n for n in graph.get(node, []) if n not in visited)

        return len(visited) == len(graph)