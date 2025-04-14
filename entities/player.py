class Player:
    """Player entity representing the game's player state."""

    def __init__(self, name="Player"):
        self.name = name
        self.score = 0
        self.currency = 1000
        self.completed_levels = set()
        self.unlocked_levels = 1  # Start with only the first level unlocked

    def complete_level(self, level_number, score=0):
        """Mark a level as completed and add score."""
        self.completed_levels.add(level_number)
        self.score += score
        # Unlock the next level if it's just the next one
        if level_number + 1 > self.unlocked_levels:
            self.unlocked_levels = level_number + 1

    def add_currency(self, amount):
        """Add currency to the player's wallet."""
        self.currency += amount

    def can_afford(self, cost):
        """Check if the player can afford a purchase."""
        return self.currency >= cost

    def spend(self, amount):
        """Spend currency if possible."""
        if self.can_afford(amount):
            self.currency -= amount
            return True
        return False
