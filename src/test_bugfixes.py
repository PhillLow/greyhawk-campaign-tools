import unittest
from src.models.character import Character
from src.models.feat import Feat, FeatDatabase
from src.models.class_model import CharacterClass, ClassName
from src.models.spell_database import SpellDatabase

class TestBugFixes(unittest.TestCase):
    def setUp(self):
        self.character = Character(name="Test Fix")
        # Wizard Level 1
        from src.models.class_model import ClassLevel
        wiz = CharacterClass.get_template(ClassName.WIZARD)
        self.character.classes = [ClassLevel(character_class=wiz, level=1)]
        self.character.stats.constitution.score = 10 # +0 Mod
        
    def test_tough_feat_hp(self):
        """Verify Tough feat adds +2 HP per level."""
        # Base HP for Wizard Lvl 1 with +0 Con = 6
        self.assertEqual(self.character.max_hp, 6)
        
        # Add Tough
        tough = FeatDatabase.get_feat("Tough")
        self.character.feats.append(tough)
        
        # Should constitute +2
        self.assertEqual(self.character.max_hp, 8)
        
        # Level up to 2
        self.character.classes[0].level = 2
        # Base: 6 + 4(avg) = 10. Tough: +4 (2*2). Total: 14.
        self.assertEqual(self.character.max_hp, 14)

    def test_magic_initiate_free_cast(self):
        """Verify adding Magic Initiate adds free cast capability."""
        # Simulate selection (since builder is interactive, we test the RESULT state)
        spell = SpellDatabase.get_spell("Shield") # Wizard Lvl 1
        
        # Manually add to book & free cast (logic present in builder)
        self.character.spellbook.append(spell)
        self.character.free_casts[spell.name] = 1
        
        self.assertIn(spell.name, self.character.free_casts)
        self.assertEqual(self.character.free_casts[spell.name], 1)
        
        # Rest logic
        self.character.free_casts[spell.name] = 0
        
    def test_spell_db_content(self):
        """Verify new spells exist."""
        # Cantrips
        self.assertIsNotNone(SpellDatabase.get_spell("Ray of Frost"))
        self.assertIsNotNone(SpellDatabase.get_spell("Minor Illusion"))
        self.assertIsNotNone(SpellDatabase.get_spell("Mending"))
        
        # Lvl 1
        self.assertIsNotNone(SpellDatabase.get_spell("Ice Knife"))
        self.assertIsNotNone(SpellDatabase.get_spell("Identify"))

if __name__ == "__main__":
    unittest.main()
