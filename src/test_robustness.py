
import unittest
from src.models.item_database import ItemDatabase, ItemType
from src.models.spell_database import SpellDatabase, ClassName
from src.models.feat import FeatDatabase, FeatType

class TestRobustness(unittest.TestCase):
    def test_item_database_count(self):
        items = ItemDatabase.get_all_items()
        self.assertTrue(len(items) > 30, f"Expected >30 items, found {len(items)}")
        
        weapons = [i for i in items if i.item_type == ItemType.WEAPON]
        self.assertTrue(len(weapons) > 20, f"Expected >20 weapons, found {len(weapons)}")
        
    def test_spell_database_coverage(self):
        classes = [ClassName.CLERIC, ClassName.DRUID, ClassName.BARD, ClassName.WIZARD, ClassName.SORCERER]
        for c in classes:
            l1_spells = SpellDatabase.get_available_spells(c, level=1)
            self.assertTrue(len(l1_spells) >= 4, f"{c.value} has only {len(l1_spells)} Level 1 spells (Expected >=4)")
            
    def test_feat_database_general(self):
        gen_feats = FeatDatabase.get_general_feats()
        self.assertTrue(len(gen_feats) > 0, "General Feats list is empty")
        self.assertEqual(gen_feats[0].type, FeatType.GENERAL)

if __name__ == "__main__":
    unittest.main()
