import unittest
from src.models.character import Character
from src.models.class_model import CharacterClass, ClassLevel, ClassName

class TestClassProgression(unittest.TestCase):
    def test_fighter_progression(self):
        char = Character(name="Boromir")
        fighter_cls = CharacterClass.get_template(ClassName.FIGHTER)
        
        # Level 1 Fighter
        char.classes = [ClassLevel(character_class=fighter_cls, level=1)]
        features_lvl1 = char.active_features
        feat_names_lvl1 = [f.name for f in features_lvl1]
        
        self.assertIn("Fighting Style", feat_names_lvl1)
        self.assertIn("Second Wind", feat_names_lvl1)
        self.assertIn("Weapon Mastery", feat_names_lvl1)
        self.assertNotIn("Action Surge", feat_names_lvl1)
        
        # Level up to 2
        char.classes[0].level = 2
        features_lvl2 = char.active_features
        feat_names_lvl2 = [f.name for f in features_lvl2]
        
        self.assertIn("Action Surge", feat_names_lvl2)
        self.assertIn("Tactical Mind", feat_names_lvl2)
        
        # Level up to 5
        char.classes[0].level = 5
        feat_names_lvl5 = [f.name for f in char.active_features]
        self.assertIn("Extra Attack", feat_names_lvl5)
        
    def test_multiclass_progression(self):
        char = Character(name="Gish")
        fighter_cls = CharacterClass.get_template(ClassName.FIGHTER)
        wizard_cls = CharacterClass.get_template(ClassName.WIZARD)
        
        char.classes = [
            ClassLevel(character_class=fighter_cls, level=2),
            ClassLevel(character_class=wizard_cls, level=1)
        ]
        
        feat_names = [f.name for f in char.active_features]
        
        # Fighter 2
        self.assertIn("Action Surge", feat_names)
        self.assertNotIn("Extra Attack", feat_names) # Level 5 fighter
        
        # Wizard 1
        self.assertIn("Spellcasting", feat_names)
        self.assertIn("Arcane Recovery", feat_names)

if __name__ == "__main__":
    unittest.main()
