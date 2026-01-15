
import unittest
from src.models.character import Character
from src.models.item_database import ItemDatabase
from src.engine.crafting import CraftingEngine, CraftingResult
from src.models.background import Background, BackgroundName
from src.models.stats import Ability

class TestCrafting(unittest.TestCase):
    def setUp(self):
        # Create a character with HERMIT background (Herbalism Kit)
        self.char = Character(name="Crafter")
        self.char.background = Background.get_template(BackgroundName.HERMIT) 
        # Hermit gives Herbalism Kit
        self.char.gp = 100 # Rich enough
        
    def test_crafting_cost_time(self):
        potion = ItemDatabase.get_item("Potion of Healing") # 50 gp
        
        cost = CraftingEngine.calculate_cost(potion)
        self.assertEqual(cost, 25.0)
        
        days = CraftingEngine.calculate_days(potion) # 25 / 10 = 2.5
        self.assertEqual(days, 2.5)
        
    def test_can_craft_success(self):
        potion = ItemDatabase.get_item("Potion of Healing")
        can, msg = CraftingEngine.can_craft(self.char, potion)
        self.assertTrue(can, f"Should be able to craft potion. Msg: {msg}")
        
    def test_crafting_failure_gold(self):
        self.char.gp = 0
        potion = ItemDatabase.get_item("Potion of Healing")
        can, msg = CraftingEngine.can_craft(self.char, potion)
        self.assertFalse(can)
        self.assertIn("Insufficient Gold", msg)
        
    def test_crafting_failure_tool(self):
        # Plate Armor needs Smith's Tools. Hermit has Herbalism Kit.
        self.char.gp = 2000 # Enough for Plate
        plate = ItemDatabase.get_item("Plate Armor")
        can, msg = CraftingEngine.can_craft(self.char, plate)
        self.assertFalse(can)
        self.assertIn("Missing Tool Proficiency", msg)
        
    def test_execution(self):
        potion = ItemDatabase.get_item("Potion of Healing")
        start_gp = self.char.gp
        start_inv = len(self.char.inventory)
        
        res = CraftingEngine.craft_item(self.char, potion)
        
        self.assertTrue(res.success)
        self.assertEqual(self.char.gp, start_gp - 25.0)
        self.assertEqual(len(self.char.inventory), start_inv + 1)
        self.assertEqual(self.char.inventory[-1].name, "Potion of Healing")

if __name__ == "__main__":
    unittest.main()
