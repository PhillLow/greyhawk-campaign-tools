
import unittest
from src.models.spell_database import SpellDatabase
from src.models.class_model import ClassName

class TestWizardSpells(unittest.TestCase):
    def test_wizard_spell_list(self):
        spells = SpellDatabase.get_available_spells(ClassName.WIZARD, level=1)
        names = [s.name for s in spells]
        expected = ["Sleep", "Grease", "Detect Magic", "Charm Person"]
        for e in expected:
            self.assertIn(e, names)
            
    def test_cantrip_availability(self):
        spells = SpellDatabase.get_available_spells(ClassName.WIZARD, level=0)
        self.assertTrue(len(spells) >= 3, "Wizard should have at least 3 cantrips available to choose from.")

if __name__ == "__main__":
    unittest.main()
