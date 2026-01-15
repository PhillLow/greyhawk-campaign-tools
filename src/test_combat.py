
import unittest
from src.models.character import Character
from src.models.stats import Ability
from src.models.item_database import ItemDatabase
from src.models.equipment import Weapon

class TestCombat(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="Fighter")
        self.char.stats.get(Ability.STR).score = 16 # +3
        self.char.stats.get(Ability.DEX).score = 14 # +2
        self.char.classes = [] # No class = prof bonus +2 at level 1? 
        # Actually level is derived from classes, so need one class
        from src.models.class_model import CharacterClass, ClassName, ClassLevel
        ftr = CharacterClass.get_template(ClassName.FIGHTER)
        self.char.classes.append(ClassLevel(character_class=ftr, level=1))
        # Total Level 1 -> Prof Bonus +2.

    def test_weapon_db(self):
        """Verify new weapons exist."""
        dagger = ItemDatabase.get_item("Dagger")
        self.assertIsNotNone(dagger)
        self.assertEqual(dagger.range_normal, 20)
        
        maul = ItemDatabase.get_item("Maul")
        self.assertIsNotNone(maul)
        self.assertEqual(maul.damage_dice, "2d6")

    def test_attack_roll(self):
        """Verify To Hit calculation."""
        # Greatsword (Str)
        gs = ItemDatabase.get_item("Greatsword")
        # Str +3, Prof +2 = +5
        bonus = self.char.calculate_attack_roll(gs)
        self.assertEqual(bonus, 5)
        
        # Longbow (Dex)
        bow = ItemDatabase.get_item("Longbow")
        # Dex +2, Prof +2 = +4
        bonus = self.char.calculate_attack_roll(bow)
        self.assertEqual(bonus, 4)
        
        # Dagger (Finesse - Uses Higher, here Str +3)
        dag = ItemDatabase.get_item("Dagger")
        # Str +3, Prof +2 = +5
        self.assertEqual(self.char.calculate_attack_roll(dag), 5)
        
        # Exhaustion Check
        self.char.exhaustion = 1 # -2 penalty
        # Greatsword: 5 - 2 = 3
        self.assertEqual(self.char.calculate_attack_roll(gs), 3)

    def test_damage_roll(self):
        """Verify Damage Bonus."""
        gs = ItemDatabase.get_item("Greatsword")
        # Str +3. No Prof to damage.
        self.assertEqual(self.char.calculate_damage_roll(gs), 3)
        
        # Off-hand check (defaults to 0 bonus if positive)
        self.assertEqual(self.char.calculate_damage_roll(gs, offhand=True), 0)
        
        # Negative Stat check
        self.char.stats.get(Ability.STR).score = 8 # -1
        # Main hand: -1
        self.assertEqual(self.char.calculate_damage_roll(gs), -1)
        # Off hand: -1 (negative flows through)
        self.assertEqual(self.char.calculate_damage_roll(gs, offhand=True), -1)

if __name__ == "__main__":
    unittest.main()
