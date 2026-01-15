
import unittest
from src.models.character import Character
from src.models.class_model import CharacterClass, ClassLevel, ClassName
from src.models.stats import Ability, AbilityScore
from src.models.equipment import Armor, ArmorCategory

class TestCompliance(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="TestChar")
        self.char.classes = []

    def set_stats(self, dex=10, con=10, wis=10, str=10):
        self.char.stats.dexterity = AbilityScore(name=Ability.DEX, score=dex)
        self.char.stats.constitution = AbilityScore(name=Ability.CON, score=con)
        self.char.stats.wisdom = AbilityScore(name=Ability.WIS, score=wis)
        self.char.stats.strength = AbilityScore(name=Ability.STR, score=str)

    def add_class(self, name: ClassName, level: int = 1):
        tmpl = CharacterClass.get_template(name)
        self.char.classes.append(ClassLevel(character_class=tmpl, level=level))

    def test_monk_ac(self):
        # Monk: Dex 16 (+3), Wis 16 (+3). AC = 10 + 3 + 3 = 16
        self.set_stats(dex=16, wis=16)
        self.add_class(ClassName.MONK)
        
        self.assertEqual(self.char.armor_class, 16)
        
        # With Armor: Padded (11+Dex) = 11+3 = 14. Should override? 
        # Actually AC method picks armor if equipped.
        armor = Armor(name="Leather", ac_base=11, category=ArmorCategory.LIGHT)
        self.char.inventory.append(armor)
        self.char.equip_item("Leather")
        
        # Light armor = 11 + 3 = 14. Unarmored Defense doesn't apply.
        self.assertEqual(self.char.armor_class, 14)
        
    def test_monk_ac_shield(self):
        # Monk: Dex 16 (+3), Wis 16 (+3) -> 16
        self.set_stats(dex=16, wis=16)
        self.add_class(ClassName.MONK)
        
        # Equip Shield (+2)
        shield = Armor(name="Shield", ac_base=2, category=ArmorCategory.SHIELD)
        self.char.inventory.append(shield)
        self.char.equip_item("Shield")
        
        # Monk Unarmored doesn't work with Shield.
        # Fallback to Standard Unarmored (10+Dex) + Shield = 10 + 3 + 2 = 15.
        # (Monk AC would be 10+3+3+2 = 18 if allowed, but it's not)
        self.assertEqual(self.char.armor_class, 15)

    def test_barbarian_ac(self):
        # Barb: Dex 14 (+2), Con 16 (+3). AC = 10 + 2 + 3 = 15
        self.set_stats(dex=14, con=16)
        self.add_class(ClassName.BARBARIAN)
        
        self.assertEqual(self.char.armor_class, 15)
        
        # With Shield (+2). Barb Unarmored WORKS with Shield.
        # AC = 15 + 2 = 17.
        shield = Armor(name="Shield", ac_base=2, category=ArmorCategory.SHIELD)
        self.char.inventory.append(shield)
        self.char.equip_item("Shield")
        
        self.assertEqual(self.char.armor_class, 17)

    def test_grapple_dc_monk(self):
        # Monk: Dex 18 (+4), Str 10 (+0), Prof +2.
        # DC = 8 + Max(Str, Dex) + Prof = 8 + 4 + 2 = 14
        self.set_stats(dex=18, str=10)
        self.add_class(ClassName.MONK)
        
        self.assertEqual(self.char.grapple_save_dc, 14)
        
    def test_grapple_dc_fighter(self):
        # Fighter: Dex 18 (+4), Str 10 (+0).
        # DC = 8 + Str + Prof = 8 + 0 + 2 = 10 (Fighters don't swap)
        self.set_stats(dex=18, str=10)
        self.add_class(ClassName.FIGHTER)
        
        self.assertEqual(self.char.grapple_save_dc, 10)

if __name__ == "__main__":
    unittest.main()
