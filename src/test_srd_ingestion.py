import os
import unittest
from src.engine.srd_parser import parse_markdown_to_tree

class TestSrdIngestion(unittest.TestCase):
    def test_srd_ingestion_basic(self):
        """Verify that the parser can load the character creation file and build an AST tree."""
        filepath = "dnd-5e-srd-markdown/character-creation.md"
        
        # Adjust path if running from inner directory
        if not os.path.exists(filepath):
            filepath = os.path.join("..", filepath)
            
        if not os.path.exists(filepath):
            self.fail(f"SRD repository not found at {filepath}")
            
        root = parse_markdown_to_tree(filepath)
        
        # We should have at least the main H1 tag
        self.assertGreaterEqual(len(root.subsections), 1)
        
        # Search for H1 "Character Creation"
        h1_section = root.get_subsection("Character Creation")
        self.assertIsNotNone(h1_section)
        
        # Check if it loaded the inner steps
        h2_section = h1_section.get_subsection("Create Your Character")
        self.assertIsNotNone(h2_section)

        h3_section = h2_section.get_subsection("Step 1: Choose Class")
        self.assertIsNotNone(h3_section)
        self.assertIn("Choose a class, and write it on your character sheet", h3_section.get_text())

if __name__ == "__main__":
    unittest.main()
