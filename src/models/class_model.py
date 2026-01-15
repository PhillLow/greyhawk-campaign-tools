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
        elif name == ClassName.BARBARIAN:
            return cls(
                name=ClassName.BARBARIAN,
                hit_die=12,
                primary_ability=["Strength"],
                skill_choices=["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
                features=[
                    ClassFeature(name="Rage", level=1, description="Advantage on STR checks/saves, resistance to B/P/S damage, bonus rage damage."),
                    ClassFeature(name="Unarmored Defense", level=1, description="AC = 10 + DEX + CON (Shields ok).")
                ]
            )
        elif name == ClassName.BARD:
            return cls(
                name=ClassName.BARD,
                hit_die=8,
                primary_ability=["Charisma"],
                skill_choices=["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"],
                num_skills=3, # Bards get 3
                features=[
                    ClassFeature(name="Bardic Inspiration", level=1, description="Grant inspiration die to ally."),
                    ClassFeature(name="Spellcasting", level=1, description="Cast Bard spells.")
                ]
            )
        elif name == ClassName.CLERIC:
            return cls(
                name=ClassName.CLERIC,
                hit_die=8,
                primary_ability=["Wisdom"],
                skill_choices=["History", "Insight", "Medicine", "Persuasion", "Religion"],
                features=[
                    ClassFeature(name="Spellcasting", level=1, description="Cast Cleric spells."),
                    ClassFeature(name="Divine Order", level=1, description="Choose Protector (Heavy Armor/Martial) or Thaumaturge (Extra Cantrip/Religion).")
                ]
            )
        elif name == ClassName.DRUID:
             return cls(
                name=ClassName.DRUID,
                hit_die=8,
                primary_ability=["Wisdom"],
                skill_choices=["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"],
                features=[
                    ClassFeature(name="Spellcasting", level=1, description="Cast Druid spells."),
                    ClassFeature(name="Primal Order", level=1, description="Choose Warden (Medium Armor/Martial) or Magician (Extra Cantrip/Arcana/Nature).")
                ]
             )
        elif name == ClassName.MONK:
             return cls(
                name=ClassName.MONK,
                hit_die=8,
                primary_ability=["Dexterity", "Wisdom"],
                skill_choices=["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"],
                features=[
                    ClassFeature(name="Martial Arts", level=1, description="Use DEX for Monk weapons/Unarmed. Dmg die scales."),
                    ClassFeature(name="Unarmored Defense", level=1, description="AC = 10 + DEX + WIS.")
                ]
             )
        elif name == ClassName.PALADIN:
             return cls(
                 name=ClassName.PALADIN,
                 hit_die=10,
                 primary_ability=["Strength", "Charisma"],
                 skill_choices=["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"],
                 features=[
                     ClassFeature(name="Lay on Hands", level=1, description="Pool of healing HP = 5 * Level."),
                     ClassFeature(name="Spellcasting", level=1, description="Cast Paladin spells.")
                 ]
             )
        elif name == ClassName.RANGER:
             return cls(
                 name=ClassName.RANGER,
                 hit_die=10,
                 primary_ability=["Dexterity", "Wisdom"],
                 skill_choices=["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
                 num_skills=3, # Rangers get 3
                 features=[
                     ClassFeature(name="Favored Enemy", level=1, description="Cast Hunter's Mark without slot freq=WIS mod."),
                     ClassFeature(name="Spellcasting", level=1, description="Cast Ranger spells.")
                 ]
             )
        elif name == ClassName.ROGUE:
             return cls(
                 name=ClassName.ROGUE,
                 hit_die=8,
                 primary_ability=["Dexterity"],
                 skill_choices=["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Performance", "Persuasion", "Sleight of Hand", "Stealth"],
                 num_skills=4, # Rogues get 4
                 features=[
                     ClassFeature(name="Sneak Attack", level=1, description="Extra damage when you have advantage or ally nearby."),
                     ClassFeature(name="Thieves' Cant", level=1, description="Secret language.")
                 ]
             )
        elif name == ClassName.SORCERER:
             return cls(
                 name=ClassName.SORCERER,
                 hit_die=6,
                 primary_ability=["Charisma"],
                 skill_choices=["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"],
                 features=[
                     ClassFeature(name="Spellcasting", level=1, description="Cast Sorcerer spells."),
                     ClassFeature(name="Innate Sorcery", level=1, description="Advantage on attacks/Save DC bump.")
                 ]
             )
        elif name == ClassName.WARLOCK:
             return cls(
                 name=ClassName.WARLOCK,
                 hit_die=8,
                 primary_ability=["Charisma"],
                 skill_choices=["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"],
                 features=[
                     ClassFeature(name="Pact Magic", level=1, description="Cast Warlock spells (recharge on Short Rest)."),
                     ClassFeature(name="Eldritch Invocations", level=1, description="Learn 1 invocation.")
                 ]
             )
        # Fallback generic
        return cls(name=name, hit_die=8, primary_ability=["Constitution"], skill_choices=["Athletics", "Perception"], num_skills=2)

class ClassLevel(BaseModel):
    """Tracks a character's progression in a single class."""
    character_class: CharacterClass
    level: int = 1
    subclass: Optional[str] = None
