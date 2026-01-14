import json
import os
from src.models.character import Character

SAVE_DIR = "saves"

class PersistenceManager:
    def __init__(self):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    def save_character(self, character: Character) -> str:
        """Saves character to JSON. Returns filename."""
        filename = f"{character.name.replace(' ', '_').lower()}.json"
        filepath = os.path.join(SAVE_DIR, filename)
        
        with open(filepath, "w") as f:
            f.write(character.model_dump_json(indent=2))
            
        return filepath

    def load_character(self, name: str) -> Character:
        """Loads character by filename (without extension) or full name."""
        filename = f"{name.replace(' ', '_').lower()}.json"
        filepath = os.path.join(SAVE_DIR, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No save file found for '{name}'")
            
        with open(filepath, "r") as f:
            data = f.read()
            return Character.model_validate_json(data)

    def list_saves(self) -> list[str]:
        """Returns list of character names from save files."""
        if not os.path.exists(SAVE_DIR):
            return []
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        # Convert filename back to readable name? Or just return filenames.
        # returning filenames for simplicity
        return [f.replace(".json", "") for f in files]
