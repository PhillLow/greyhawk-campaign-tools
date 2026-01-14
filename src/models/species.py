from pydantic import BaseModel
from enum import Enum
from typing import List

class SpeciesName(str, Enum):
    HUMAN = "Human"
    ELF = "Elf"
    DWARF = "Dwarf"
    HALFLING = "Halfling"
    DRAGONBORN = "Dragonborn"
    GNOME = "Gnome"
    ORC = "Orc"
    TIEFLING = "Tiefling"
    GOLIATH = "Goliath"
    AASIMAR = "Aasimar"

class Trait(BaseModel):
    name: str
    description: str

class Species(BaseModel):
    name: SpeciesName
    speed: int = 30
    darkvision: int = 0
    traits: List[Trait] = []
    
    @classmethod
    def get_template(cls, name: SpeciesName) -> "Species":
        """Factory for default species templates (2024 Rules)."""
        if name == SpeciesName.HUMAN:
            return cls(
                name=SpeciesName.HUMAN,
                speed=30,
                traits=[
                    Trait(name="Resourceful", description="You gain Heroic Inspiration each day."),
                    Trait(name="Skillful", description="You gain proficiency in one skill of your choice."),
                    Trait(name="Versatile", description="You gain an Origin Feat of your choice.")
                ]
            )
        elif name == SpeciesName.ELF:
             return cls(
                name=SpeciesName.ELF,
                speed=30,
                darkvision=60,
                traits=[
                    Trait(name="Trance", description="You don't need sleep, and magic can't put you to sleep. Long rest in 4 hours."),
                    Trait(name="Keen Senses", description="Proficiency in Perception."),
                    Trait(name="Fey Ancestry", description="Advantage on saves vs Charmed.")
                ]
            )
        elif name == SpeciesName.DWARF:
             return cls(
                name=SpeciesName.DWARF,
                speed=30,
                darkvision=60,
                traits=[
                    Trait(name="Dwarven Resilience", description="Resistance to Poison damage."),
                    Trait(name="Dwarven Toughness", description="+1 HP per level.")
                ]
            )
        # Fallback
        return cls(name=name)
