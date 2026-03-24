import unittest
from unittest.mock import MagicMock, patch
from src.engine.builder import CharacterBuilder
from src.models.species import SpeciesName
from src.models.class_model import ClassName
from src.models.background import BackgroundName

class TestBuilderIntegration(unittest.TestCase):
    @patch('src.engine.builder.questionary')
    def test_wizard_sage_duplicate_spells(self, mock_questionary):
        """
        Simulate creating a Human Wizard with Sage background.
        Sage grants Magic Initiate (Wizard).
        We select 'Ray of Frost' via Magic Initiate.
        We verify that 'Ray of Frost' is EXCLUDED from the Wizard class cantrip selection.
        """
        # Setup Mocks
        def mock_ask(return_val):
            m = MagicMock()
            m.ask.return_value = return_val
            return m

        # Sequence of expected calls and their return values
        # Note: This list must match the EXACT order of questionary calls in run_cli_flow
        
        # 1. Name
        mock_questionary.text.return_value = mock_ask("Gandalf")
        
        # 2. Species -> Human
        mock_questionary.select.side_effect = [
            # Species
            mock_ask(SpeciesName.HUMAN.value),
            # Human Bonus Feat
            mock_ask("Tough"),
            # Class
            mock_ask(ClassName.WIZARD.value),
            # Background
            mock_ask(BackgroundName.SAGE.value),
            
            # --- Inside _handle_feat_selection for Magic Initiate (Wizard) ---
            # It asks for 1 Level 1 Spell (Select)
            mock_ask("Shield"),
            
            # --- Back to Main Flow ---
            # 5. Stats Method
            mock_ask("Standard Array (15,14,13,12,10,8)"),
            
            # 5a. Assign Stats (6 calls)
            mock_ask("15"), mock_ask("14"), mock_ask("13"), mock_ask("12"), mock_ask("10"), mock_ask("8"),
            
            # 6. Background ASI
            mock_ask("+1 to Three"),
        ]

        # Checkbox calls are tricky because they happen in specific places
        # We need to distinguish between Magic Initiate Cantrips and Class Cantrips
        
        # Let's map side effects for checkbox based on the prompt text?
        # Or just sequence them.
        
        # Sequence:
        # 1. Magic Initiate Cantrips (in _handle_feat_selection)
        # 2. Class Skills (Wizard)
        # 3. Class Cantrips (Wizard)
        # 4. Class Lvl 1 Spells (Wizard)
        
        mock_questionary.checkbox.side_effect = [
            # 1. Magic Initiate Cantrips
            mock_ask(["Ray of Frost", "Light"]),
            
            # 2. Class Skills (Select 2)
            mock_ask(["Arcana", "History"]), # Wait, Sage gives Arcana/History. Wizard list might differ. 
            # Sage: Arcana, History. Wizard Choices: Arcana, History, Insight, Invest, Med, Rel.
            # If we limit choices, builder might filter.
            # Let's pick "Insight", "Investigation".
            
            # 3. Class Cantrips (Select 3) 
            # THIS is where we verify the bug. We want to check the 'choices' passed here.
            # We'll return dummy data to let flow finish.
            mock_ask(["Mage Hand", "Prestidigitation", "Minor Illusion"]),
            
            # 4. Class Lvl 1 Spells (Select 6)
            mock_ask(["Magic Missile", "Mage Armor", "Sleep", "Detect Magic", "Identify", "Grease"]),
            
            # 5. Weapon Mastery (Wizard gets 0? No, wait, Wizard has 0 masteries. So this won't be called.)
        ]
        
        # Run the builder
        builder = CharacterBuilder()
        char = builder.run_cli_flow()
        
        # Verify Verification
        # Find the call to checkbox for Class Cantrips
        # It's the 3rd call to checkbox.
        
        # Magic Initiate Call
        call_args_mi = mock_questionary.checkbox.call_args_list[0]
        # Class Skills Call
        call_args_skills = mock_questionary.checkbox.call_args_list[1]
        # Class Cantrips Call
        call_args_cantrips = mock_questionary.checkbox.call_args_list[2]
        
        _, kwargs = call_args_cantrips
        choices_offered = kwargs['choices']
        prompt_text = args = call_args_cantrips[0][0] # "Select 3 Cantrips:"
        
        print(f"Prompt: {prompt_text}")
        print(f"Choices Offered: {choices_offered}")
        
        # ASSERTION: "Ray of Frost" and "Light" should NOT be in choices_offered
        self.assertNotIn("Ray of Frost", choices_offered, "Ray of Frost (Magic Initiate) should not be offered again.")
        self.assertNotIn("Light", choices_offered, "Light (Magic Initiate) should not be offered again.")

if __name__ == "__main__":
    unittest.main()
