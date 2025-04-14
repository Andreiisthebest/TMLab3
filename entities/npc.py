# entities/npc.py
class NPC:
    """Non-player character for quests and interactions."""

    def __init__(self, name, position, dialogue=None):
        self.name = name
        self.position = position
        self.dialogue = dialogue or ["Hello there!"]
        self.current_dialogue = 0
        self.quest = None

    def talk(self):
        """Get the current dialogue."""
        message = self.dialogue[self.current_dialogue]
        self.current_dialogue = (self.current_dialogue + 1) % len(self.dialogue)
        return message

    def assign_quest(self, quest):
        """Assign a quest to this NPC."""
        self.quest = quest

    def draw(self, renderer):
        """Draw the NPC."""
        # Draw a simple character
        renderer.draw_circle(self.position, 15, (0, 150, 150))
        renderer.draw_text(self.name, 16, (0, 0, 0),
                           (self.position[0], self.position[1] - 25), centered=True)