# entities/rail_piece.py
class RailPiece:
    """Represents a rail connection between two nodes."""

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.cost = self._calculate_cost()
        self.built = False

    def _calculate_cost(self):
        """Calculate the cost of building this rail piece."""
        # Calculate distance between nodes
        x1, y1 = self.start_node.position
        x2, y2 = self.end_node.position
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # Base cost on distance
        base_cost = int(distance * 0.5)

        # Apply terrain multiplier if applicable
        terrain_multiplier = 1.0
        # Add terrain logic here in future versions

        return int(base_cost * terrain_multiplier)

    def build(self):
        """Mark this rail as built."""
        self.built = True
        self.start_node.connect(self.end_node)
        self.end_node.connect(self.start_node)
        return self.cost

    def demolish(self):
        """Remove this rail."""
        if self.built:
            self.built = False
            self.start_node.disconnect(self.end_node)
            self.end_node.disconnect(self.start_node)
            return self.cost // 2  # Refund half the cost
        return 0

    def draw(self, renderer):
        """Draw this rail piece."""
        color = (100, 100, 100) if self.built else (200, 200, 200)
        width = 5 if self.built else 2
        renderer.draw_line(self.start_node.position, self.end_node.position, color, width)

        if self.built:
            # Draw the cost in the middle of the rail
            mid_x = (self.start_node.position[0] + self.end_node.position[0]) // 2
            mid_y = (self.start_node.position[1] + self.end_node.position[1]) // 2
            renderer.draw_text(f"${self.cost}", 18, (255, 0, 0), (mid_x, mid_y), centered=True)
