# mechanics/interactions.py
class InteractionSystem:
    """System for handling interactions between entities."""

    def __init__(self, game):
        self.game = game
        self.active_interactions = []

    def interact(self, entity1, entity2, interaction_type):
        """Create an interaction between two entities."""
        if interaction_type == "trade":
            return self._handle_trade(entity1, entity2)
        elif interaction_type == "quest":
            return self._handle_quest(entity1, entity2)
        elif interaction_type == "dialog":
            return self._handle_dialog(entity1, entity2)
        return False

    def _handle_trade(self, buyer, seller):
        """Handle trading between entities."""
        # Simple implementation - could be expanded
        if hasattr(buyer, 'currency') and hasattr(seller, 'price'):
            if buyer.currency >= seller.price:
                buyer.currency -= seller.price
                return True
        return False

    def _handle_quest(self, player, npc):
        """Handle quest interactions."""
        if hasattr(npc, 'quest') and npc.quest:
            if npc.quest.is_completed():
                npc.quest.complete(player)
                return True
        return False

    def _handle_dialog(self, player, npc):
        """Handle dialog interactions."""
        if hasattr(npc, 'talk'):
            message = npc.talk()
            # Could add dialog system here
            return message
        return None

    def update(self, dt):
        """Update all active interactions."""
        completed_interactions = []
        for interaction in self.active_interactions:
            interaction.update(dt)
            if interaction.is_complete():
                completed_interactions.append(interaction)

        # Remove completed interactions
        for interaction in completed_interactions:
            self.active_interactions.remove(interaction)