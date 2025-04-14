# entities/train.py
class Train:
    """Represents a train that can travel between nodes."""

    def __init__(self, starting_node, color=(200, 50, 50)):
        self.current_node = starting_node
        self.next_node = None
        self.color = color
        self.speed = 100  # Pixels per second
        self.progress = 0  # Progress between 0-1 for animation
        self.cargo = 0
        self.capacity = 10
        self.route = []  # List of nodes to visit

    def set_route(self, node_list):
        """Set a route for the train to follow."""
        if node_list and node_list[0] == self.current_node:
            self.route = node_list[1:]  # Skip the first node if it's current
            self._start_next_leg()
            return True
        return False

    def _start_next_leg(self):
        """Start movement to the next node in the route."""
        if self.route:
            self.next_node = self.route.pop(0)
            self.progress = 0
        else:
            self.next_node = None

    def update(self, dt):
        """Update train position and state."""
        if not self.next_node:
            return

        # Update progress
        if self.progress < 1.0:
            # Calculate distance
            x1, y1 = self.current_node.position
            x2, y2 = self.next_node.position
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            # Update progress based on speed and distance
            self.progress += (self.speed * dt) / distance

            if self.progress >= 1.0:
                # Reached the destination
                self.current_node = self.next_node
                self._start_next_leg()

    def get_position(self):
        """Get current position for rendering."""
        if not self.next_node:
            return self.current_node.position

        # Interpolate between nodes
        x1, y1 = self.current_node.position
        x2, y2 = self.next_node.position
        x = x1 + (x2 - x1) * self.progress
        y = y1 + (y2 - y1) * self.progress
        return (int(x), int(y))

    def load_cargo(self, amount):
        """Load cargo onto the train."""
        available_space = self.capacity - self.cargo
        loading_amount = min(amount, available_space)
        self.cargo += loading_amount
        return loading_amount

    def unload_cargo(self, amount=None):
        """Unload cargo from the train."""
        if amount is None:
            amount = self.cargo

        unloading_amount = min(amount, self.cargo)
        self.cargo -= unloading_amount
        return unloading_amount

    def draw(self, renderer):
        """Draw the train."""
        position = self.get_position()
        # Draw a simple train shape
        renderer.draw_rect(pygame.Rect(position[0] - 15, position[1] - 10, 30, 20), self.color)

        # Draw cargo indicator
        if self.cargo > 0:
            renderer.draw_text(f"Cargo: {self.cargo}/{self.capacity}", 14, (0, 0, 0),
                               (position[0], position[1] - 20), centered=True)