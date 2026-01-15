
import unittest
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassName
from src.models.background import Background, BackgroundName
from src.models.character import Character
from src.models.modifier import Modifier
from src.models.stats import Ability

class TestBuilderContent(unittest.TestCase):
    def test_all_species_load(self):
        """Verify all species templates load without error."""
        for s_name in SpeciesName:
            s_obj = Species.get_template(s_name)
            self.assertEqual(s_obj.name, s_name)
            self.assertGreater(s_obj.speed, 0)
            
    def test_all_classes_load(self):
        """Verify all class templates load."""
        for c_name in ClassName:
            c_obj = CharacterClass.get_template(c_name)
            self.assertEqual(c_obj.name, c_name)
            self.assertGreater(c_obj.hit_die, 0)
            self.assertTrue(len(c_obj.primary_ability) > 0)
            
    def test_all_backgrounds_load(self):
        """Verify all background templates load."""
        for b_name in BackgroundName:
            b_obj = Background.get_template(b_name)
            self.assertEqual(b_obj.name, b_name)
            self.assertEqual(len(b_obj.ability_scores), 3)
            self.assertTrue(b_obj.origin_feat is not None)
            
    def test_asi_application(self):
        """Verify Modifier system correctly boosts stats for Backgrounds."""
        char = Character(name="ASI Test")
        char.stats.get(Ability.STR).score = 10
        char.stats.get(Ability.DEX).score = 10
        
        # Simulate +2 Str, +1 Dex
        mod1 = Modifier(name="Back ASI", value=2, target="Strength", type="bonus")
        mod2 = Modifier(name="Back ASI", value=1, target="Dexterity", type="bonus")
        
        char.stats.modifiers.extend([mod1, mod2])
        
        self.assertEqual(char.stats.get_score(Ability.STR), 12)
        self.assertEqual(char.stats.get_score(Ability.DEX), 11)
        self.assertEqual(char.stats.get_mod(Ability.STR), 1)

if __name__ == "__main__":
    unittest.main()
