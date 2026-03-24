import unittest
from src.models.item_database import ItemDatabase

class TestGameplayToolbox(unittest.TestCase):
    def test_poisons_loaded(self):
        items = ItemDatabase.get_all_items()
        
        assassins_blood = next((i for i in items if i.name == "Assassin's Blood"), None)
        self.assertIsNotNone(assassins_blood, "Assassin's Blood poison was not successfully parsed or loaded into the DB.")
        self.assertEqual(assassins_blood.cost_gp, 150)
        self.assertIn("[Ingested]", assassins_blood.description)

        purple_worm = next((i for i in items if i.name == "Purple Worm Poison"), None)
        self.assertIsNotNone(purple_worm, "Purple Worm Poison was not loaded.")
        self.assertEqual(purple_worm.cost_gp, 2000)
        self.assertIn("[Injury]", purple_worm.description)

if __name__ == "__main__":
    unittest.main()
