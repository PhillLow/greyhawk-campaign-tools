
import unittest
import os
import shutil
from src.models.character import Character
from src.models.equipment import Weapon, Armor, ItemType, DamageType, ArmorCategory
from src.engine.persistence import PersistenceManager
from src.models.spell import Spell, School

class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Clean saves dir
        if os.path.exists("saves"):
            shutil.rmtree("saves")
        self.pm = PersistenceManager()

    def tearDown(self):
        if os.path.exists("saves"):
            shutil.rmtree("saves")

    def test_item_subclass_persistence(self):
        char = Character(name="Hero")
        
        # Add a Weapon
        sword = Weapon(name="Excalibur", damage_dice="1d12", damage_type=DamageType.SLASHING)
        char.inventory.append(sword)
        
        # Add Armor
        plate = Armor(name="Plate", ac_base=18, category=ArmorCategory.HEAVY)
        char.inventory.append(plate)
        
        # Save
        self.pm.save_character(char)
        
        # Load
        loaded = self.pm.load_character("Hero")
        
        # Verify
        self.assertEqual(len(loaded.inventory), 2)
        
        item1 = loaded.inventory[0]
        # Check if it's a Weapon (has damage_dice)
        # Pydantic might load it as generic Item if not configured correctly.
        # But even if generic Item, does it have extra fields in `__dict__` or just dropped?
        # Standard Pydantic behavior: if model is List[Item], it validates as Item. 
        # If Item doesn't have `damage_dice` field, it drops it. 
        
        # We expect this to FAIL if we haven't set up Union.
        # But let's check what happens.
        
        # If it's a dict, we can check keys. If it's model, check attr.
        # It should be a model.
        
        # If Pydantic "downcasted" to Item, it won't have `damage_dice`.
        if hasattr(item1, "damage_dice"):
             self.assertEqual(item1.damage_dice, "1d12")
        else:
             self.fail(f"Item 1 lost Weapon attributes! Is type: {type(item1)}")
             
        item2 = loaded.inventory[1]
        if hasattr(item2, "ac_base"):
             self.assertEqual(item2.ac_base, 18)
        else:
             self.fail("Item 2 lost Armor attributes!")

    def test_spellbook_persistence(self):
        char = Character(name="Wizard")
        spell = Spell(name="Fireball", level=3, school=School.EVOCATION, 
                      casting_time="1 Action", range_area="150ft", 
                      components="V,S,M", duration="Instant", description="Boom")
        char.spellbook.append(spell)
        
        self.pm.save_character(char)
        loaded = self.pm.load_character("Wizard")
        
        self.assertEqual(len(loaded.spellbook), 1)
        self.assertEqual(loaded.spellbook[0].name, "Fireball")
        self.assertEqual(loaded.spellbook[0].school, School.EVOCATION)

if __name__ == "__main__":
    unittest.main()
