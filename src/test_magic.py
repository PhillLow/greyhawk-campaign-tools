
import unittest
from src.models.character import Character
from src.models.class_model import CharacterClass, ClassName, ClassLevel

class TestMagic(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="Mage")
        self.char.classes = [] # Reset
        
    def add_class(self, name: ClassName, level: int):
        tmpl = CharacterClass.get_template(name)
        self.char.classes.append(ClassLevel(character_class=tmpl, level=level))
        
    def test_single_class_wizard(self):
        # Wizard 5
        self.add_class(ClassName.WIZARD, 5)
        slots = self.char.max_spell_slots
        # Lvl 5: 4 Lvl 1, 3 Lvl 2, 2 Lvl 3
        self.assertEqual(slots.get(1), 4)
        self.assertEqual(slots.get(2), 3)
        self.assertEqual(slots.get(3), 2)
        
    def test_multiclass_caster(self):
        # Wizard 3 / Cleric 2 -> Effective 5
        self.add_class(ClassName.WIZARD, 3)
        self.add_class(ClassName.CLERIC, 2)
        slots = self.char.max_spell_slots
        self.assertEqual(slots.get(3), 2) # Same as above
        
    def test_half_caster(self):
        # Ranger 5 -> Effective 3 ((5+1)//2 = 3)
        self.add_class(ClassName.RANGER, 5)
        slots = self.char.max_spell_slots
        # Lvl 3: 4 Lvl 1, 2 Lvl 2
        self.assertEqual(slots.get(1), 4)
        self.assertEqual(slots.get(2), 2)
        self.assertIsNone(slots.get(3))
        
    def test_warlock(self):
        # Warlock 2
        self.add_class(ClassName.WARLOCK, 2)
        # Regular slots: 0
        self.assertEqual(self.char.max_spell_slots, {})
        # Pact slots: (Lvl 1, Count 2)
        self.assertEqual(self.char.max_pact_slots, (1, 2))
        
    def test_sorc_warlock_mix(self):
        # Sorc 1 / Warlock 1
        self.add_class(ClassName.SORCERER, 1)
        self.add_class(ClassName.WARLOCK, 1)
        
        # Regular: Sorc 1 -> 2 Lvl 1 slots
        self.assertEqual(self.char.max_spell_slots, {1: 2})
        
        # Pact: Warlock 1 -> (Lvl 1, Count 1)
        self.assertEqual(self.char.max_pact_slots, (1, 1))

if __name__ == "__main__":
    unittest.main()
