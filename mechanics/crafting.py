# mechanics/crafting.py
class CraftingSystem:
    """System for crafting upgrades and items."""

    def __init__(self):
        self.recipes = {
            'rail_upgrade': {
                'cost': 500,
                'requirements': {'steel': 5, 'wood': 10},
                'result': {'rail_quality': 1}
            },
            'train_upgrade': {
                'cost': 750,
                'requirements': {'steel': 10, 'coal': 5},
                'result': {'train_speed': 1}
            },
            'station_upgrade': {
                'cost': 1000,
                'requirements': {'steel': 8, 'wood': 15, 'stone': 20},
                'result': {'station_capacity': 1}
            }
        }

        self.player_inventory = {
            'steel': 0,
            'wood': 0,
            'coal': 0,
            'stone': 0
        }

        self.player_upgrades = {
            'rail_quality': 0,
            'train_speed': 0,
            'station_capacity': 0
        }

    def can_craft(self, recipe_name):
        """Check if a recipe can be crafted."""
        if recipe_name not in self.recipes:
            return False

        recipe = self.recipes[recipe_name]

        # Check if player has all required resources
        for resource, amount in recipe['requirements'].items():
            if self.player_inventory.get(resource, 0) < amount:
                return False

        return True

    def craft(self, recipe_name):
        """Craft an item using a recipe."""
        if not self.can_craft(recipe_name):
            return False

        recipe = self.recipes[recipe_name]

        # Deduct resources
        for resource, amount in recipe['requirements'].items():
            self.player_inventory[resource] -= amount

        # Add upgrade
        for upgrade, amount in recipe['result'].items():
            self.player_upgrades[upgrade] = self.player_upgrades.get(upgrade, 0) + amount

        return True

    def add_resource(self, resource_name, amount):
        """Add a resource to the player's inventory."""
        if resource_name in self.player_inventory:
            self.player_inventory[resource_name] += amount
            return True
        return False
