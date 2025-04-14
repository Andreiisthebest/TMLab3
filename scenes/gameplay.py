import pygame
import os
import json
import math
from config import GRID_SIZE, WHITE, GREEN, RED, BLUE, YELLOW, UI_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class GameplayScene:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 6
        self.budget = 0
        self.total_cost = 0
        self.ui_font = None
        self.small_font = None
        self.camera_offset = [0, 0]
        self.dragging = False
        self.drag_start = None
        self.rail_start_pos = None
        self.entities = []
        self.rails = []
        self.level_data = None
        self.completed = False
        self.rail_removal_mode = False

    def on_enter(self, level=1):
        self.current_level = level
        self.level_data = self.load_or_create_level(level)
        self.budget = self.calculate_level_budget(level)
        self.total_cost = 0
        self.ui_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.completed = False
        self.rail_removal_mode = False
        self.initialize_entities()

    def calculate_level_budget(self, level):
        """Calculate budget with increasing difficulty"""
        base_cost = 8000 + (level * 2000)  # More budget for harder levels
        terrain_penalty = sum(1 for t in self.level_data.get("terrain", []) if t["type"] == "mountain") * 500
        return base_cost - terrain_penalty

    def load_or_create_level(self, level_num):
        """Load level data or create default if not exists"""
        if not os.path.exists("data/levels"):
            os.makedirs("data/levels")

        level_path = f"data/levels/level_{level_num}.json"

        if not os.path.exists(level_path):
            level_data = self.generate_level_data(level_num)
            with open(level_path, 'w') as f:
                json.dump(level_data, f, indent=2)
            return level_data
        else:
            with open(level_path, 'r') as f:
                return json.load(f)

    def generate_level_data(self, level_num):
        """Generate unique levels with increasing difficulty"""
        levels = [
            # Level 1 - Basic 2 towns (very easy)
            {
                "towns": [
                    {"id": 1, "x": 5, "y": 5, "name": "Start", "population": 1000},
                    {"id": 2, "x": 15, "y": 5, "name": "End", "population": 1500}
                ],
                "optimal_cost": 1000,
                "terrain": []
            },
            # Level 2 - Triangle with one obstacle
            {
                "towns": [
                    {"id": 1, "x": 5, "y": 5, "name": "Alpha", "population": 1000},
                    {"id": 2, "x": 15, "y": 5, "name": "Beta", "population": 1500},
                    {"id": 3, "x": 10, "y": 12, "name": "Gamma", "population": 2000}
                ],
                "optimal_cost": 2200,
                "terrain": [
                    {"type": "mountain", "x": 10, "y": 7, "width": 2, "height": 2}
                ]
            },
            # Level 3 - Square with obstacles
            {
                "towns": [
                    {"id": 1, "x": 5, "y": 5, "name": "North", "population": 1000},
                    {"id": 2, "x": 15, "y": 5, "name": "East", "population": 1500},
                    {"id": 3, "x": 15, "y": 15, "name": "South", "population": 2000},
                    {"id": 4, "x": 5, "y": 15, "name": "West", "population": 2500}
                ],
                "optimal_cost": 3500,
                "terrain": [
                    {"type": "water", "x": 8, "y": 8, "width": 4, "height": 4},
                    {"type": "mountain", "x": 5, "y": 10, "width": 2, "height": 1}
                ]
            },
            # Level 4 - Cross with complex terrain
            {
                "towns": [
                    {"id": 1, "x": 10, "y": 5, "name": "Top", "population": 1000},
                    {"id": 2, "x": 5, "y": 10, "name": "Left", "population": 1500},
                    {"id": 3, "x": 15, "y": 10, "name": "Right", "population": 2000},
                    {"id": 4, "x": 10, "y": 15, "name": "Bottom", "population": 2500}
                ],
                "optimal_cost": 4500,
                "terrain": [
                    {"type": "mountain", "x": 8, "y": 8, "width": 4, "height": 4},
                    {"type": "water", "x": 5, "y": 5, "width": 2, "height": 2},
                    {"type": "water", "x": 13, "y": 13, "width": 2, "height": 2}
                ]
            },
            # Level 5 - Hexagon with challenging terrain
            {
                "towns": [
                    {"id": 1, "x": 10, "y": 5, "name": "Top", "population": 1000},
                    {"id": 2, "x": 5, "y": 8, "name": "Top-Left", "population": 1500},
                    {"id": 3, "x": 5, "y": 12, "name": "Bottom-Left", "population": 2000},
                    {"id": 4, "x": 10, "y": 15, "name": "Bottom", "population": 2500},
                    {"id": 5, "x": 15, "y": 12, "name": "Bottom-Right", "population": 3000},
                    {"id": 6, "x": 15, "y": 8, "name": "Top-Right", "population": 3500}
                ],
                "optimal_cost": 6000,
                "terrain": [
                    {"type": "mountain", "x": 7, "y": 7, "width": 6, "height": 6},
                    {"type": "water", "x": 10, "y": 10, "width": 2, "height": 2}
                ]
            },
            # Level 6 - Complex layout with multiple obstacles
            {
                "towns": [
                    {"id": 1, "x": 5, "y": 5, "name": "Mountain", "population": 1000},
                    {"id": 2, "x": 15, "y": 5, "name": "Valley", "population": 1500},
                    {"id": 3, "x": 5, "y": 10, "name": "Forest", "population": 2000},
                    {"id": 4, "x": 15, "y": 10, "name": "River", "population": 2500},
                    {"id": 5, "x": 5, "y": 15, "name": "Mine", "population": 3000},
                    {"id": 6, "x": 15, "y": 15, "name": "Port", "population": 3500}
                ],
                "optimal_cost": 8000,
                "terrain": [
                    {"type": "mountain", "x": 8, "y": 5, "width": 4, "height": 2},
                    {"type": "mountain", "x": 8, "y": 13, "width": 4, "height": 2},
                    {"type": "water", "x": 5, "y": 7, "width": 2, "height": 6},
                    {"type": "water", "x": 13, "y": 7, "width": 2, "height": 6}
                ]
            }
        ]
        return levels[level_num - 1] if level_num <= len(levels) else levels[-1]

    def initialize_entities(self):
        """Initialize towns and terrain without any connections"""
        self.entities = []
        self.rails = []

        # Add terrain first (so towns render on top)
        for terrain in self.level_data.get("terrain", []):
            self.entities.append({
                "type": "terrain",
                "terrain_type": terrain["type"],
                "x": terrain["x"],
                "y": terrain["y"],
                "width": terrain.get("width", 1),
                "height": terrain.get("height", 1)
            })

        # Add towns
        for town in self.level_data["towns"]:
            self.entities.append({
                "type": "town",
                "id": town["id"],
                "x": town["x"],
                "y": town["y"],
                "name": town["name"],
                "color": GREEN,
                "connected": False
            })

    def update(self, dt):
        events = self.game.event_handler.events

        # Toggle rail removal mode with Shift key
        if self.game.event_handler.keys.get(pygame.K_LSHIFT, False):
            self.rail_removal_mode = True
        else:
            self.rail_removal_mode = False

        # Handle camera panning
        mouse_pos = self.game.event_handler.mouse_pos
        if self.game.event_handler.mouse_buttons["middle"] or (
                self.game.event_handler.mouse_buttons["right"] and not self.dragging
        ):
            if not self.dragging:
                self.dragging = True
                self.drag_start = mouse_pos
            else:
                dx, dy = mouse_pos[0] - self.drag_start[0], mouse_pos[1] - self.drag_start[1]
                self.camera_offset[0] += dx
                self.camera_offset[1] += dy
                self.drag_start = mouse_pos
        else:
            self.dragging = False

        # Handle rail placement/removal
        if not self.completed and self.game.event_handler.mouse_buttons["left"] and not self.dragging:
            grid_pos = self.screen_to_grid(mouse_pos)

            if self.rail_removal_mode:
                # Remove rail closest to click
                self.remove_rail_near(grid_pos)
            else:
                # Handle rail placement
                clicked_town = None
                for entity in self.entities:
                    if entity["type"] == "town":
                        town_pos = (entity["x"], entity["y"])
                        if self.points_distance(grid_pos, town_pos) < 1.5:
                            clicked_town = entity
                            break

                if clicked_town:
                    if not self.rail_start_pos:
                        # Start new rail from this town
                        self.rail_start_pos = (clicked_town["x"], clicked_town["y"])
                        clicked_town["color"] = YELLOW
                    else:
                        # Complete rail to this town
                        start_pos = self.rail_start_pos
                        end_pos = (clicked_town["x"], clicked_town["y"])

                        if start_pos != end_pos:
                            # Check if connection already exists
                            if not self.rail_exists(start_pos, end_pos):
                                # Calculate rail cost with terrain penalties
                                cost = self.calculate_rail_cost(start_pos, end_pos)

                                if self.total_cost + cost <= self.budget:
                                    self.rails.append({
                                        "start": start_pos,
                                        "end": end_pos,
                                        "cost": cost,
                                        "color": (139, 69, 19)
                                    })
                                    self.total_cost += cost

                                    # Mark towns as connected
                                    for entity in self.entities:
                                        if (entity["x"], entity["y"]) in [start_pos, end_pos]:
                                            entity["connected"] = True
                                            entity["color"] = BLUE

                        # Reset selection
                        for entity in self.entities:
                            if (entity["x"], entity["y"]) == self.rail_start_pos:
                                entity["color"] = BLUE if entity["connected"] else GREEN
                        self.rail_start_pos = None

        # Check level completion
        if not self.completed and self.game.event_handler.keys.get(pygame.K_RETURN, False):
            if self.check_level_completion():
                self.completed = True
                # Unlock next level
                if self.current_level < self.max_levels:
                    self.game.player_data["current_level"] = self.current_level + 1
                    self.game.save_game()

        # Handle back to menu
        if self.game.event_handler.keys.get(pygame.K_ESCAPE, False):
            self.game.change_scene("menu")

    def rail_exists(self, pos1, pos2):
        """Check if rail already exists between two positions (in any direction)"""
        for rail in self.rails:
            if (rail["start"] == pos1 and rail["end"] == pos2) or \
                    (rail["start"] == pos2 and rail["end"] == pos1):
                return True
        return False

    def calculate_rail_cost(self, start_pos, end_pos):
        """Calculate rail cost with terrain penalties"""
        base_cost = self.points_distance(start_pos, end_pos) * 100

        # Check if rail crosses difficult terrain
        terrain_penalty = 0
        for terrain in self.level_data.get("terrain", []):
            if terrain["type"] == "mountain":
                # Simple check - if either end is in mountain, add penalty
                if (start_pos[0] == terrain["x"] and start_pos[1] == terrain["y"]) or \
                        (end_pos[0] == terrain["x"] and end_pos[1] == terrain["y"]):
                    terrain_penalty += 200

        return int(base_cost + terrain_penalty)

    def remove_rail_near(self, grid_pos):
        """Remove rail closest to click position"""
        closest_rail = None
        min_distance = float('inf')

        for i, rail in enumerate(self.rails):
            # Calculate distance to rail segment
            dist = self.point_to_line_distance(
                grid_pos, rail["start"], rail["end"])

            if dist < min_distance and dist < 1.0:  # Within 1 grid unit
                min_distance = dist
                closest_rail = i

        if closest_rail is not None:
            # Refund cost
            self.total_cost -= self.rails[closest_rail]["cost"]

            # Check if towns should be marked as disconnected
            start_pos = self.rails[closest_rail]["start"]
            end_pos = self.rails[closest_rail]["end"]
            self.rails.pop(closest_rail)

            # Check if towns are still connected via other rails
            for pos in [start_pos, end_pos]:
                connected = False
                for rail in self.rails:
                    if pos in [rail["start"], rail["end"]]:
                        connected = True
                        break

                if not connected:
                    for entity in self.entities:
                        if entity["type"] == "town" and (entity["x"], entity["y"]) == pos:
                            entity["connected"] = False
                            entity["color"] = GREEN

    def point_to_line_distance(self, point, line_start, line_end):
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

    def check_level_completion(self):
        """Check if all towns are properly connected"""
        # First check if all towns are connected
        all_connected = all(town["connected"] for town in self.entities if town["type"] == "town")
        if not all_connected:
            return False

        # Then check if the network is fully connected
        return self.is_network_connected()

    def is_network_connected(self):
        """Check if all towns are reachable from each other"""
        if not self.rails or not any(town["type"] == "town" for town in self.entities):
            return False

        # Create a graph of connections
        graph = {}
        town_positions = [(t["x"], t["y"]) for t in self.entities if t["type"] == "town"]

        for pos in town_positions:
            graph[pos] = []

        for rail in self.rails:
            graph[rail["start"]].append(rail["end"])
            graph[rail["end"]].append(rail["start"])

        # BFS to check connectivity
        visited = set()
        start_pos = town_positions[0]
        queue = [start_pos]

        while queue:
            pos = queue.pop(0)
            if pos not in visited:
                visited.add(pos)
                queue.extend(n for n in graph[pos] if n not in visited)

        return len(visited) == len(town_positions)

    def points_distance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def screen_to_grid(self, screen_pos):
        x = (screen_pos[0] - self.camera_offset[0]) / GRID_SIZE
        y = (screen_pos[1] - self.camera_offset[1]) / GRID_SIZE
        return (x, y)

    def grid_to_screen(self, grid_pos):
        x = grid_pos[0] * GRID_SIZE + self.camera_offset[0]
        y = grid_pos[1] * GRID_SIZE + self.camera_offset[1]
        return (x, y)

    def render(self, renderer):
        # Draw grid
        self.draw_grid(renderer)

        # Draw terrain
        for entity in self.entities:
            if entity["type"] == "terrain":
                pos = self.grid_to_screen((entity["x"], entity["y"]))
                width = entity["width"] * GRID_SIZE
                height = entity["height"] * GRID_SIZE

                if entity["terrain_type"] == "mountain":
                    renderer.draw_rect((100, 100, 100), pygame.Rect(pos[0], pos[1], width, height))
                elif entity["terrain_type"] == "water":
                    renderer.draw_rect((70, 70, 200), pygame.Rect(pos[0], pos[1], width, height))

        # Draw rails
        for rail in self.rails:
            start = self.grid_to_screen(rail["start"])
            end = self.grid_to_screen(rail["end"])
            renderer.draw_line(rail["color"], start, end, 5)

        # Draw towns
        for entity in self.entities:
            if entity["type"] == "town":
                pos = self.grid_to_screen((entity["x"], entity["y"]))
                renderer.draw_circle(entity["color"], pos, GRID_SIZE // 2)
                text = self.small_font.render(entity["name"], True, WHITE)
                text_rect = text.get_rect(center=(pos[0], pos[1] - GRID_SIZE))
                renderer.draw_text_surface(text, text_rect)

        # Draw UI
        self.draw_ui(renderer)

        # Draw rail placement preview
        if self.rail_start_pos and not self.rail_removal_mode:
            mouse_grid_pos = self.screen_to_grid(self.game.event_handler.mouse_pos)
            start = self.grid_to_screen(self.rail_start_pos)
            end = self.grid_to_screen(mouse_grid_pos)
            renderer.draw_line((200, 200, 200), start, end, 3)

        # Draw removal mode indicator
        if self.rail_removal_mode:
            text = self.small_font.render("RAIL REMOVAL MODE (Hold Shift)", True, RED)
            renderer.draw_text_surface(text, (SCREEN_WIDTH // 2 - 150, 10))

        # Draw completion message
        if self.completed:
            msg = f"Level {self.current_level} Completed!"
            text = self.ui_font.render(msg, True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            renderer.draw_text_surface(text, text_rect)

            next_msg = "Press ESC to return to menu"
            text = self.small_font.render(next_msg, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            renderer.draw_text_surface(text, text_rect)

    def draw_grid(self, renderer):
        color = (100, 100, 100)
        start_x = max(0, int(-self.camera_offset[0] // GRID_SIZE))
        start_y = max(0, int(-self.camera_offset[1] // GRID_SIZE))
        end_x = start_x + (SCREEN_WIDTH // GRID_SIZE) + 2
        end_y = start_y + (SCREEN_HEIGHT // GRID_SIZE) + 2

        for x in range(start_x, end_x):
            screen_x = x * GRID_SIZE + self.camera_offset[0]
            if 0 <= screen_x <= SCREEN_WIDTH:
                renderer.draw_line(color, (screen_x, 0), (screen_x, SCREEN_HEIGHT), 1)

        for y in range(start_y, end_y):
            screen_y = y * GRID_SIZE + self.camera_offset[1]
            if 0 <= screen_y <= SCREEN_HEIGHT:
                renderer.draw_line(color, (0, screen_y), (SCREEN_WIDTH, screen_y), 1)

    def draw_ui(self, renderer):
        # Budget info
        remaining = self.budget - self.total_cost
        budget_text = f"Budget: ${remaining}"
        text_surface = self.ui_font.render(budget_text, True,
                                           GREEN if remaining >= 0 else RED)
        renderer.draw_text_surface(text_surface, (10, 10))

        # Level info
        level_text = f"Level: {self.current_level}/{self.max_levels}"
        text_surface = self.ui_font.render(level_text, True, WHITE)
        renderer.draw_text_surface(text_surface, (10, 50))

        # Cost info
        cost_text = f"Cost: ${self.total_cost}"
        text_surface = self.ui_font.render(cost_text, True, WHITE)
        renderer.draw_text_surface(text_surface, (10, 90))

        # Instructions
        instructions = [
            "Left click: Connect towns",
            "Right click: Pan camera",
            "Hold Shift + Click: Remove rail",
            "Enter: Check completion",
            "ESC: Return to menu"
        ]

        for i, text in enumerate(instructions):
            text_surface = self.small_font.render(text, True, WHITE)
            renderer.draw_text_surface(text_surface, (SCREEN_WIDTH - 400, 10 + i * 30))