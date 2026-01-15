
import unittest
import importlib

class TestImports(unittest.TestCase):
    def test_main_import(self):
        """Verifies src.main imports without syntax errors."""
        try:
            import src.main
            importlib.reload(src.main)
        except Exception as e:
            self.fail(f"Failed to import src.main: {e}")

    def test_builder_import(self):
        """Verifies src.engine.builder imports without syntax errors."""
        try:
            import src.engine.builder
            importlib.reload(src.engine.builder)
        except Exception as e:
            self.fail(f"Failed to import src.engine.builder: {e}")

    def test_models_import(self):
        """Verifies core models import."""
        modules = [
            "src.models.character",
            "src.models.species",
            "src.models.class_model",
            "src.models.background",
            "src.models.equipment",
            "src.models.spell",
        ]
        for m in modules:
            try:
                mod = importlib.import_module(m)
                importlib.reload(mod)
            except Exception as e:
                self.fail(f"Failed to import {m}: {e}")

if __name__ == "__main__":
    unittest.main()
