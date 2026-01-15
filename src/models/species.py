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

class SpeciesSpell(BaseModel):
    name: str
    level_required: int = 1
    count: int = 1 # Per Long Rest
    recharge: str = "Long Rest"

class Species(BaseModel):
    name: SpeciesName
    speed: int = 30
    darkvision: int = 0
    traits: List[Trait] = []
    free_spells: List[SpeciesSpell] = []
    
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
        elif name == SpeciesName.HALFLING:
            return cls(
                name=SpeciesName.HALFLING,
                speed=30,
                traits=[
                    Trait(name="Brave", description="Advantage on saves vs Frightened."),
                    Trait(name="Halfling Nimbleness", description="Move through space of creatures larger than you."),
                    Trait(name="Lucky", description="Reroll 1s on d20 tests.")
                ]
            )
        elif name == SpeciesName.DRAGONBORN:
            return cls(
                name=SpeciesName.DRAGONBORN,
                speed=30,
                darkvision=60,
                traits=[
                    Trait(name="Breath Weapon", description="Exhale magical energy in an area."),
                    Trait(name="Damage Resistance", description="Resistance to damage type associated with ancestry."),
                    Trait(name="Darkvision", description="60ft.")
                ]
            )
        elif name == SpeciesName.GNOME:
            return cls(
                name=SpeciesName.GNOME,
                speed=30,
                darkvision=60,
                traits=[
                    Trait(name="Gnomish Cunning", description="Advantage on Int, Wis, Cha saves vs magic."),
                    Trait(name="Darkvision", description="60ft.")
                ]
            )
        elif name == SpeciesName.ORC:
            return cls(
                name=SpeciesName.ORC,
                speed=30,
                darkvision=120,
                traits=[
                    Trait(name="Adrenaline Rush", description="Dash as Bonus Action + Temp HP."),
                    Trait(name="Relentless Endurance", description="Drop to 1 HP instead of 0 once per Long Rest."),
                    Trait(name="Darkvision", description="120ft.")
                ]
            )
        elif name == SpeciesName.TIEFLING:
             return cls(
                name=SpeciesName.TIEFLING,
                speed=30,
                darkvision=60,
                traits=[
                    Trait(name="Infernal Legacy", description="Know Thaumaturgy. Cast Hellish Rebuke (Lvl 3) and Darkness (Lvl 5)."),
                    Trait(name="Otherworldly Presence", description="Know Thaumaturgy cantrip."),
                    Trait(name="Darkvision", description="60ft.")
                ],
                free_spells=[
                    SpeciesSpell(name="Hellish Rebuke", level_required=3, count=1),
                    SpeciesSpell(name="Darkness", level_required=5, count=1)
                ]
            )
        elif name == SpeciesName.GOLIATH:
             return cls(
                 name=SpeciesName.GOLIATH,
                 speed=35,
                 traits=[
                     Trait(name="Little Giant", description="Powerful Build + Athletics proficiency."),
                     Trait(name="Stone's Endurance", description="Reaction to reduce damage.")
                 ]
             )
        elif name == SpeciesName.AASIMAR:
             return cls(
                 name=SpeciesName.AASIMAR,
                 speed=30,
                 darkvision=60,
                 traits=[
                     Trait(name="Celestial Revelation", description="Transform to gain flight or damage bonus."),
                     Trait(name="Healing Hands", description="Heal HP equal to level."),
                     Trait(name="Light Bearer", description="Know Light cantrip.")
                 ]
             )
        # Fallback
        return cls(name=name)
