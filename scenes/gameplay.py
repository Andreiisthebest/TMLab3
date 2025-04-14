# scenes/gameplay.py
import pygame
from mechanics.AI import PathFindingAI
from entities.rail_piece import RailPiece
from entities.train import Train


class GameplayScene:
    """Main gameplay scene."""

    def __init__(self):
        self.game = None
        self.level_number = 1
        self.nodes = []  # Town nodes
        self.rails = []  # Connected rails
        self.trains = []  # Trains on the map
        self.selected_node = None
        self.connecting_mode = False
        self.total_cost = 0
        self.budget = 0
        self.ai = None  # AI for checking optimal solutions
        self.check_button_rect = None
        self.back_button_rect = None

    def enter(self):
        """Initialize the level when the scene is entered."""
        self.level_number = self.game.current_level
        # Load level data from config
        level_data = self.game.config['levels'][self.level_number - 1]
        self.budget = level_data.get('budget', 1000)

        # Clear existing nodes and rails
        self.nodes = []
        self.rails = []
        self.trains = []
        self.total_cost = 0

        # Create town nodes based on level data
        num_nodes = level_data.get('nodes', 3)
        for i in range(num_nodes):
            # Position nodes in a semi-random pattern
            x = 100 + (i * 100) + (i * 20)
            y = 200 + ((-1) ** i * 50)
            self.nodes.append({
                'id': i,
                'pos': (x, y),
                'name': f"Town {chr(65 + i)}",  # Town A, Town B, etc.
                'connected': set()
            })

        # Add a train at the first node
        if self.nodes:
            self.add_train(self.nodes[0])

        # Initialize the AI for checking solutions
        self.ai = PathFindingAI(self.nodes)

    def exit(self):
        """Clean up when leaving the scene."""
        pass

    def add_train(self, node):
        """Add a train at the specified node."""
        train = {
            'node': node['id'],
            'pos': node['pos'],
            'color': (200, 50, 50),
            'cargo': 0,
            'route': []
        }
        self.trains.append(train)

    def handle_event(self, event):
        """Handle user input events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check for node selection
            for node in self.nodes:
                node_rect = pygame.Rect(0, 0, 30, 30)
                node_rect.center = node['pos']

                if node_rect.collidepoint(mouse_pos):
                    if not self.connecting_mode:
                        # Start connecting from this node
                        self.selected_node = node
                        self.connecting_mode = True
                    else:
                        # Try to connect to this node
                        if node != self.selected_node:
                            self.connect_nodes(self.selected_node, node)
                        self.connecting_mode = False
                        self.selected_node = None
                    break

            # Check for button clicks
            if self.check_button_rect and self.check_button_rect.collidepoint(mouse_pos):
                self.check_solution()
            elif self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos):
                self.game.change_scene("menu")

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Cancel connection or go back
                if self.connecting_mode:
                    self.connecting_mode = False
                    self.selected_node = None
                else:
                    self.game.change_scene("menu")

    def connect_nodes(self, node1, node2):
        """Connect two nodes with a rail."""
        # Check if already connected
        if node2['id'] in node1['connected'] or node1['id'] in node2['connected']:
            return False

        # Calculate distance/cost
        x1, y1 = node1['pos']
        x2, y2 = node2['pos']
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        cost = int(distance * 0.5)  # Simple cost calculation

        # Check budget
        if self.total_cost + cost > self.budget:
            return False

        # Add connection
        node1['connected'].add(node2['id'])
        node2['connected'].add(node1['id'])
        self.rails.append({
            'node1': node1['id'],
            'node2': node2['id'],
            'cost': cost
        })
        self.total_cost += cost
        return True

    def check_solution(self):
        """Check if the current solution is optimal."""
        # Check if all nodes are connected (simple check)
        connected_nodes = set()
        if self.nodes:
            # Start from first node and traverse the graph
            queue = [0]  # Start with first node ID
            while queue:
                node_id = queue.pop(0)
                connected_nodes.add(node_id)

                # Add unvisited connected nodes to queue
                node = self.nodes[node_id]
                for connected_id in node['connected']:
                    if connected_id not in connected_nodes:
                        queue.append(connected_id)

        all_connected = len(connected_nodes) == len(self.nodes)

        # Compare with AI solution
        optimal = self.ai.is_solution_optimal(self.rails)
        under_budget = self.total_cost <= self.budget

        if all_connected and optimal and under_budget:
            # Level completed
            self.game.complete_level(self.level_number)
            self.game.change_scene("game_over")
        else:
            # Show feedback (in a real game, you'd want visual feedback)
            if not all_connected:
                print("Not all towns are connected!")
            if not optimal:
                print("Your solution is not optimal!")
            if not under_budget:
                print("You've exceeded the budget!")

    def update(self, dt):
        """Update game state."""
        # Update trains
        for train in self.trains:
            if train['route']:
                # Move train along route
                pass

    def render(self, renderer):
        """Render the gameplay scene."""
        # Draw the level title
        level_data = self.game.config['levels'][self.level_number - 1]
        renderer.draw_text(f"Level {self.level_number}: {level_data.get('name', '')}",
                           36, (0, 0, 0), (renderer.screen.get_width() // 2, 50),
                           centered=True)

        # Draw budget info
        renderer.draw_text(f"Budget: ${self.budget} - Spent: ${self.total_cost}",
                           24, (0, 0, 0), (renderer.screen.get_width() // 2, 90),
                           centered=True)

        # Draw rails
        for rail in self.rails:
            node1 = self.nodes[rail['node1']]
            node2 = self.nodes[rail['node2']]
            renderer.draw_line(node1['pos'], node2['pos'], (100, 100, 100), 5)

            # Draw cost in the middle of the rail
            mid_x = (node1['pos'][0] + node2['pos'][0]) // 2
            mid_y = (node1['pos'][1] + node2['pos'][1]) // 2
            renderer.draw_text(f"${rail['cost']}", 18, (255, 0, 0),
                               (mid_x, mid_y), centered=True)

        # Draw nodes (towns)
        for node in self.nodes:
            color = (0, 200, 0) if node == self.selected_node else (0, 0, 200)
            renderer.draw_circle(node['pos'], 15, color)
            renderer.draw_text(node['name'], 18, (0, 0, 0),
                               (node['pos'][0], node['pos'][1] - 30), centered=True)

        # Draw trains
        for train in self.trains:
            renderer.draw_circle(train['pos'], 10, train['color'])

        # Draw connection line when in connecting mode
        if self.connecting_mode and self.selected_node:
            renderer.draw_line(self.selected_node['pos'], pygame.mouse.get_pos(),
                               (255, 0, 0), 2)

        # Draw UI buttons
        self.check_button_rect = pygame.Rect(0, 0, 150, 40)
        self.check_button_rect.center = (renderer.screen.get_width() - 100,
                                         renderer.screen.get_height() - 50)
        renderer.draw_rect(self.check_button_rect, (0, 180, 0))
        renderer.draw_text("Check Solution", 20, (255, 255, 255),
                           self.check_button_rect.center, centered=True)

        self.back_button_rect = pygame.Rect(0, 0, 100, 40)
        self.back_button_rect.center = (100, renderer.screen.get_height() - 50)
        renderer.draw_rect(self.back_button_rect, (180, 0, 0))
        renderer.draw_text("Back", 20, (255, 255, 255),
                           self.back_button_rect.center, centered=True)