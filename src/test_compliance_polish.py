
import unittest
from src.models.character import Character
from src.models.species import Species, SpeciesName
from src.models.equipment import Item, ItemType
from src.models.spell import Spell, School

class TestCompliancePolish(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="PolishTester")

    def test_species_spells_tiefling(self):
        # Tiefling grants spells at lvl 3 and 5
        self.char.species = Species.get_template(SpeciesName.TIEFLING)
        self.char.classes = [] # No classes needed for species traits usually, but level matters.
        # Check level calculation (Character defaults level 1 if no classes)
        
        # Level 1: No spells (Hellish Rebuke is Lvl 3)
        self.char.perform_long_rest()
        self.assertNotIn("Hellish Rebuke", self.char.free_casts)
        
        # Level Up to 3
        # Mocking classes to increase level
        from src.models.class_model import CharacterClass, ClassName, ClassLevel
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        self.char.classes.append(ClassLevel(character_class=fighter, level=3))
        
        self.char.perform_long_rest()
        
        self.assertIn("Hellish Rebuke", self.char.free_casts)
        self.assertEqual(self.char.free_casts["Hellish Rebuke"], 1)
        
        # Level 5
        self.char.classes[0].level = 5
        self.char.perform_long_rest()
        self.assertIn("Darkness", self.char.free_casts)

    def test_item_quantity(self):
        arrow = Item(name="Arrow", item_type=ItemType.GEAR, quantity=20)
        self.assertEqual(arrow.quantity, 20)
        arrow.quantity -= 1
        self.assertEqual(arrow.quantity, 19)

    def test_spell_ritual_flag(self):
        s = Spell(name="Test Ritual", level=1, school=School.DIVINATION, casting_time="1A", range="Self", components="V", duration="1m", description="Test", ritual=True)
        self.assertTrue(s.ritual)
        
if __name__ == "__main__":
    unittest.main()
