from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
import os
import json

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

_CLASS_FEATURES_CACHE = None

def _get_class_features(class_name: str) -> list[dict]:
    global _CLASS_FEATURES_CACHE
    if _CLASS_FEATURES_CACHE is None:
        try:
            path = os.path.join(os.path.dirname(__file__), "generated_class_features.json")
            with open(path, "r", encoding="utf-8") as f:
                _CLASS_FEATURES_CACHE = json.load(f)
        except Exception:
            _CLASS_FEATURES_CACHE = {}
    return _CLASS_FEATURES_CACHE.get(class_name.upper(), [])

class CharacterClass(BaseModel):
    name: ClassName
    hit_die: int = Field(..., description="Die size, e.g. 8 for d8")
    primary_ability: List[str]
    features: List[ClassFeature] = []
    skill_choices: List[str] = []
    num_skills: int = 2
    num_weapon_masteries: int = 0

    @classmethod
    def get_template(cls, name: ClassName) -> "CharacterClass":
        feats = _get_class_features(name.value)
        if name == ClassName.FIGHTER:
            return cls(
                name=ClassName.FIGHTER,
                hit_die=10,
                primary_ability=["Strength", "Dexterity"],
                skill_choices=["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Perception", "Survival"],
                num_skills=2,
                num_weapon_masteries=3,
                features=feats
            )
        elif name == ClassName.WIZARD:
             return cls(
                name=ClassName.WIZARD,
                hit_die=6,
                primary_ability=["Intelligence"],
                skill_choices=["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"],
                num_skills=2,
                features=feats
            )
        elif name == ClassName.BARBARIAN:
            return cls(
                name=ClassName.BARBARIAN,
                hit_die=12,
                primary_ability=["Strength"],
                num_skills=2,
                num_weapon_masteries=2,
                features=feats
            )
        elif name == ClassName.BARD:
            return cls(
                name=ClassName.BARD,
                hit_die=8,
                primary_ability=["Charisma"],
                skill_choices=["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"],
                num_skills=3,
                features=feats
            )
        elif name == ClassName.CLERIC:
            return cls(
                name=ClassName.CLERIC,
                hit_die=8,
                primary_ability=["Wisdom"],
                skill_choices=["History", "Insight", "Medicine", "Persuasion", "Religion"],
                features=feats
            )
        elif name == ClassName.DRUID:
             return cls(
                name=ClassName.DRUID,
                hit_die=8,
                primary_ability=["Wisdom"],
                skill_choices=["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
                features=feats
             )
        elif name == ClassName.MONK:
             return cls(
                name=ClassName.MONK,
                hit_die=8,
                primary_ability=["Dexterity", "Wisdom"],
                num_skills=2,
                num_weapon_masteries=2,
                features=feats
             )
        elif name == ClassName.PALADIN:
             return cls(
                 name=ClassName.PALADIN,
                 hit_die=10,
                 primary_ability=["Strength", "Charisma"],
                 num_skills=2,
                 num_weapon_masteries=2,
                 features=feats
             )
        elif name == ClassName.RANGER:
             return cls(
                 name=ClassName.RANGER,
                 hit_die=10,
                 primary_ability=["Dexterity", "Wisdom"],
                 skill_choices=["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
                 num_skills=3,
                 num_weapon_masteries=2,
                 features=feats
             )
        elif name == ClassName.ROGUE:
             return cls(
                 name=ClassName.ROGUE,
                 hit_die=8,
                 primary_ability=["Dexterity"],
                 skill_choices=["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"],
                 num_skills=4,
                 num_weapon_masteries=2,
                 features=feats
             )
        elif name == ClassName.SORCERER:
             return cls(
                 name=ClassName.SORCERER,
                 hit_die=6,
                 primary_ability=["Charisma"],
                 skill_choices=["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"],
                 features=feats
             )
        elif name == ClassName.WARLOCK:
             return cls(
                 name=ClassName.WARLOCK,
                 hit_die=8,
                 primary_ability=["Charisma"],
                 skill_choices=["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"],
                 features=feats
             )
        # Fallback generic
        return cls(name=name, hit_die=8, primary_ability=["Constitution"], skill_choices=["Athletics", "Perception"], num_skills=2, features=feats)

class ClassLevel(BaseModel):
    """Tracks a character's progression in a single class."""
    character_class: CharacterClass
    level: int = 1
    subclass: Optional[str] = None
