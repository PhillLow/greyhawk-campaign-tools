import unittest
from src.models.character import Character
from src.models.class_model import CharacterClass, ClassName, ClassLevel
from src.models.item_database import ItemDatabase
from src.models.feat import FeatDatabase, FeatType
from src.models.equipment import WeaponMastery

class TestFeatures(unittest.TestCase):
    def setUp(self):
        self.char = Character(name="Test Fighter")
        ftr = CharacterClass.get_template(ClassName.FIGHTER)
        self.char.classes = [ClassLevel(character_class=ftr, level=1)]
        
    def test_fighter_defaults(self):
        """Verify Fighter gets 3 masteries and correct features."""
        ftr = self.char.classes[0].character_class
        self.assertEqual(ftr.num_weapon_masteries, 3)
        self.assertTrue(any(f.name == "Fighting Style" for f in ftr.features))
        self.assertTrue(any(f.name == "Weapon Mastery" for f in ftr.features))

    def test_weapon_mastery_logic(self):
        """Verify mastery only activates if selected."""
        dagger = ItemDatabase.get_item("Dagger") # Has Nick
        longsword = ItemDatabase.get_item("Longsword") # Has Sap
        
        # Initially, no masteries selected
        self.assertIsNone(self.char.get_active_mastery(dagger))
        self.assertIsNone(self.char.get_active_mastery(longsword))
        
        # Select Dagger
        self.char.weapon_masteries.append("Dagger")
        
        # Dagger should now be active
        self.assertEqual(self.char.get_active_mastery(dagger), WeaponMastery.NICK)
        
        # Longsword still inactive
        self.assertIsNone(self.char.get_active_mastery(longsword))
        
        # Case Insensitive check
        self.char.weapon_masteries.append("longsword")
        self.assertEqual(self.char.get_active_mastery(longsword), WeaponMastery.SAP)

    def test_fighting_styles(self):
        """Verify Fighting Style feats exist in DB."""
        styles = FeatDatabase.get_fighting_style_feats()
        self.assertTrue(len(styles) > 0)
        self.assertTrue(all(f.type == FeatType.FIGHTING_STYLE for f in styles))
        
        archery = FeatDatabase.get_feat("Fighting Style: Archery")
        self.assertIsNotNone(archery)

if __name__ == "__main__":
    unittest.main()
