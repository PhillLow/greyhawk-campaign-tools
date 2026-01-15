
import unittest
from src.models.character import Character
from src.models.species import Species, SpeciesName
from src.models.modifier import Modifier
from src.models.class_model import CharacterClass, ClassName, ClassLevel

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="Test Hero")
        # Add a class to have Hit Dice
        wiz = CharacterClass.get_template(ClassName.WIZARD)
        self.char.classes.append(ClassLevel(character_class=wiz, level=4)) # Setup level 4 Wizard
        self.char.stats.constitution.score = 14 # +2 Mod
        
        # Init Hit Dice (manually since builder usually does it)
        # perform_long_rest generally initializes them if missing or we do it manual
        self.char.perform_long_rest()
        
    def test_exhaustion_mechanics(self):
        """Verify 2024 Exhaustion Rules (6 levels, -2 penalty, -5 speed)."""
        self.char.exhaustion = 0
        self.assertEqual(self.char.exhaustion_penalty, 0)
        self.assertEqual(self.char.get_roll_modifier("d20_test"), 0)
        
        # Level 1
        self.char.exhaustion = 1
        self.assertEqual(self.char.exhaustion_penalty, -2)
        self.assertEqual(self.char.get_roll_modifier("attack"), -2)
        self.assertEqual(self.char.speed_penalty, -5)
        
        # Level 3
        self.char.exhaustion = 3
        self.assertEqual(self.char.exhaustion_penalty, -6)
        self.assertEqual(self.char.speed_penalty, -15)
        
    def test_modifiers(self):
        """Verify generic modifier injection."""
        base_str = self.char.stats.get_score(self.char.stats.strength.name)
        self.assertEqual(base_str, 10)
        
        # Add +2 Bonus
        mod = Modifier(name="Gauntlets", value=2, target="Strength", type="bonus")
        self.char.stats.modifiers.append(mod)
        
        new_str = self.char.stats.get_score(self.char.stats.strength.name)
        self.assertEqual(new_str, 12)
        
        # Add Set 19
        mod_set = Modifier(name="Belt", value=19, target="Strength", type="set")
        self.char.stats.modifiers.append(mod_set)
        
        final_str = self.char.stats.get_score(self.char.stats.strength.name)
        # 19 (Set) + 2 (Bonus) = 21 (usually 5e logic is Set replaces Base, Bonuses add on top)
        self.assertEqual(final_str, 21)

    def test_short_rest_hit_dice(self):
        """Verify Hit Die spending."""
        # Max HP (Lvl 4 Wiz, Con +2) -> (6+2) + (4+2)*3 = 8 + 18 = 26
        # Let's say we are damaged
        self.char.current_hp = 10
        self.char.current_hit_dice["Wizard"] = 4
        
        # Roll 1 die
        healed = self.char.roll_hit_die("Wizard")
        
        # Verify die spent
        self.assertEqual(self.char.current_hit_dice["Wizard"], 3)
        
        # Verify healing (min 1+2=3, max 6+2=8)
        self.assertTrue(healed >= 3)
        self.assertTrue(self.char.current_hp > 10)
        
    def test_long_rest(self):
        """Verify Long Rest resets."""
        self.char.exhaustion = 2
        self.char.current_hp = 1
        self.char.current_hit_dice["Wizard"] = 1 # Spent 3
        
        self.char.perform_long_rest()
        
        # Check Exhaustion reduced by 1
        self.assertEqual(self.char.exhaustion, 1)
        
        # Check HP full
        self.assertEqual(self.char.current_hp, self.char.max_hp)
        
        # Check Hit Dice Regain (Half max = 2)
        # 1 + 2 = 3. Cap is 4.
        self.assertEqual(self.char.current_hit_dice["Wizard"], 3) 

    def test_derived_stats(self):
        """Verify AC, Speed, Initiative logic."""
        # Setup Dex 14 (+2)
        self.char.stats.dexterity.score = 14
        
        # Base AC: 10 + 2 = 12
        self.assertEqual(self.char.armor_class, 12)
        
        # Equip Leather (11 + Dex)
        from src.models.item_database import ItemDatabase
        leather = ItemDatabase.get_item("Leather Armor")
        shield = ItemDatabase.get_item("Shield")
        
        self.char.inventory.append(leather.model_copy())
        self.char.inventory.append(shield.model_copy())
        
        self.char.equip_item("Leather Armor")
        # 11 + 2 = 13
        self.assertEqual(self.char.armor_class, 13)
        
        # Equip Shield
        self.char.equip_item("Shield")
        # 13 + 2 = 15
        self.assertEqual(self.char.armor_class, 15)
        
        # Equip Plate (18, No Dex) - Should replace Leather but KEEP Shield
        plate = ItemDatabase.get_item("Plate Armor")
        self.char.inventory.append(plate.model_copy())
        self.char.equip_item("Plate Armor")
        
        # Plate (18) + Shield (2) = 20
        self.assertEqual(self.char.armor_class, 20)
        
        # Verify Leather is unequipped
        is_leather_equipped = next((i.equipped for i in self.char.inventory if i.name == "Leather Armor"), False)
        self.assertFalse(is_leather_equipped)
        
        # Verify Shield IS equipped
        is_shield_equipped = next((i.equipped for i in self.char.inventory if i.name == "Shield"), False)
        self.assertTrue(is_shield_equipped)

if __name__ == "__main__":
    unittest.main()
