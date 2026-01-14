from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class ClassName(str, Enum):
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"

class ClassFeature(BaseModel):
    name: str
    level: int
    description: str

class CharacterClass(BaseModel):
    name: ClassName
    hit_die: int = Field(..., description="Die size, e.g. 8 for d8")
    primary_ability: List[str]
    features: List[ClassFeature] = []
    skill_choices: List[str] = []
    num_skills: int = 2

    @classmethod
    def get_template(cls, name: ClassName) -> "CharacterClass":
        if name == ClassName.FIGHTER:
            return cls(
                name=ClassName.FIGHTER,
                hit_die=10,
                primary_ability=["Strength", "Dexterity"],
                # 2024 Fighter Skills
                skill_choices=["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
                num_skills=2,
                features=[
                    ClassFeature(name="Fighting Style", level=1, description="Choose a Fighting Style feat."),
                    ClassFeature(name="Second Wind", level=1, description="Regain 1d10+Level HP as a Bonus Action.")
                ]
            )
        elif name == ClassName.WIZARD:
             return cls(
                name=ClassName.WIZARD,
                hit_die=6,
                primary_ability=["Intelligence"],
                # 2024 Wizard Skills
                skill_choices=["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
                num_skills=2,
                features=[
                    ClassFeature(name="Spellcasting", level=1, description="Cast Wizard spells."),
                    ClassFeature(name="Arcane Recovery", level=1, description="Recover spell slots on Short Rest.")
                ]
            )
        # Fallback generic
        return cls(name=name, hit_die=8, primary_ability=["Constitution"], skill_choices=["Athletics", "Perception"], num_skills=2)

class ClassLevel(BaseModel):
    """Tracks a character's progression in a single class."""
    character_class: CharacterClass
    level: int = 1
    subclass: Optional[str] = None
