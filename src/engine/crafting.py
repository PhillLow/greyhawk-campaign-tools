
from src.models.character import Character
from src.models.equipment import Item

class CraftingResult:
    def __init__(self, success: bool, message: str, time_days: float = 0, cost_gp: float = 0):
        self.success = success
        self.message = message
        self.time_days = time_days
        self.cost_gp = cost_gp

class CraftingEngine:
    PROGRESS_PER_DAY_GP = 10.0 # 2024 PHB Baseline assumption (or 5e XGE)
    
    @staticmethod
    def calculate_cost(item: Item) -> float:
        """Crafting materials cost half the market value."""
        return item.cost_gp / 2.0
    
    @staticmethod
    def calculate_days(item: Item) -> float:
        """Days = Crafting Cost / Progress per Day."""
        cost = CraftingEngine.calculate_cost(item)
        days = cost / CraftingEngine.PROGRESS_PER_DAY_GP
        return max(days, 0.5) # Minimum half day
        
    @staticmethod
    def can_craft(char: Character, item: Item) -> tuple[bool, str]:
        """Check prerequisites: Tools and Gold."""
        # 1. Cost
        cost = CraftingEngine.calculate_cost(item)
        if char.gp < cost:
            return False, f"Insufficient Gold. Need {cost} GP, have {char.gp} GP."
            
        # 2. Tool Proficiency
        req_tool = item.tool_requirements
        if req_tool:
            # Check background tool
            bg_tool = char.background.tool_proficiency
            # Also check generic "proficiencies" list if we add one later.
            # Simplified string match
            if req_tool.lower() not in bg_tool.lower() and "all" not in bg_tool.lower():
                # Feat check? Crafter feat?
                has_crafter = any(f.name == "Crafter" for f in char.feats)
                if not has_crafter:
                    return False, f"Missing Tool Proficiency: {req_tool}. (Have: {bg_tool})"
        
        return True, "Ready via Standard Crafting."

    @staticmethod
    def craft_item(char: Character, item: Item) -> CraftingResult:
        can, msg = CraftingEngine.can_craft(char, item)
        if not can:
            return CraftingResult(False, msg)
            
        cost = CraftingEngine.calculate_cost(item)
        days = CraftingEngine.calculate_days(item)
        
        # Deduct Gold
        char.gp -= cost
        
        # Add Item
        # We need a copy of the item, not reference to DB
        new_item = item.model_copy()
        new_item.equipped = False
        char.inventory.append(new_item)
        
        # Apply "Crafter" feat bonus? (2024: Crafter gives discount or speed?)
        # Let's assume standard for now.
        
        return CraftingResult(True, f"Crafted {item.name} in {days} days.", time_days=days, cost_gp=cost)
