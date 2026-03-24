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
    lineages: dict = {} # Map of LineageName -> {'speed_bonus': int, 'darkvision_override': int, 'extra_traits': List[dict], 'extra_spells': List[dict]}
    
    def apply_lineage(self, lineage_name: str):
        if lineage_name in self.lineages:
            lin = self.lineages[lineage_name]
            self.speed += lin.get('speed_bonus', 0)
            if lin.get('darkvision_override', 0) > self.darkvision:
                self.darkvision = lin['darkvision_override']
                
            for t in lin.get('extra_traits', []):
                self.traits.append(Trait(**t))
                
            for s in lin.get('extra_spells', []):
                self.free_spells.append(SpeciesSpell(**s))

    @classmethod
    def get_template(cls, name: SpeciesName) -> "Species":
        """Factory for default species templates (2024 Rules)."""
        if name == SpeciesName.HUMAN:
            return cls(
                name=SpeciesName.HUMAN,
                speed=30,
                traits=[
                    dict(name="Resourceful", description="You gain Heroic Inspiration each day."),
                    dict(name="Skillful", description="You gain proficiency in one skill of your choice."),
                    dict(name="Versatile", description="You gain an Origin Feat of your choice.")
                ]
            )
        elif name == SpeciesName.ELF:
             return cls(
                name=SpeciesName.ELF,
                speed=30,
                darkvision=60,
                traits=[
                    dict(name="Trance", description="You don't need sleep, and magic can't put you to sleep. Long rest in 4 hours."),
                    dict(name="Keen Senses", description="Proficiency in Perception."),
                    dict(name="Fey Ancestry", description="Advantage on saves vs Charmed.")
                ],
                lineages={
                    "Drow": {
                        "darkvision_override": 120,
                        "extra_spells": [
                            dict(name="Dancing Lights", level_required=1, count=99),
                            dict(name="Faerie Fire", level_required=3, count=1),
                            dict(name="Darkness", level_required=5, count=1)
                        ]
                    },
                    "High Elf": {
                        "extra_spells": [
                            dict(name="Prestidigitation", level_required=1, count=99),
                            dict(name="Detect Magic", level_required=3, count=1),
                            dict(name="Misty Step", level_required=5, count=1)
                        ]
                    },
                    "Wood Elf": {
                        "speed_bonus": 5,
                        "extra_spells": [
                            dict(name="Druidcraft", level_required=1, count=99),
                            dict(name="Longstrider", level_required=3, count=1),
                            dict(name="Pass without Trace", level_required=5, count=1)
                        ]
                    }
                }
            )
        elif name == SpeciesName.DWARF:
             return cls(
                name=SpeciesName.DWARF,
                speed=30,
                darkvision=120,
                traits=[
                    dict(name="Dwarven Resilience", description="Resistance to Poison damage."),
                    dict(name="Dwarven Toughness", description="+1 HP per level."),
                    dict(name="Stonecunning", description="Tremorsense 60ft as Bonus Action.")
                ]
            )
        elif name == SpeciesName.HALFLING:
            return cls(
                name=SpeciesName.HALFLING,
                speed=30,
                traits=[
                    dict(name="Brave", description="Advantage on saves vs Frightened."),
                    dict(name="Halfling Nimbleness", description="Move through space of creatures larger than you."),
                    dict(name="Lucky", description="Reroll 1s on d20 tests.")
                ]
            )
        elif name == SpeciesName.DRAGONBORN:
            return cls(
                name=SpeciesName.DRAGONBORN,
                speed=30,
                darkvision=60,
                traits=[
                    dict(name="Breath Weapon", description="Exhale magical energy in an area."),
                    dict(name="Draconic Flight", description="Level 5: Temporary Wings for 10 mins.")
                ],
                lineages={
                    "Black (Acid)": {"extra_traits": [dict(name="Damage Resistance", description="Acid Resistance")]},
                    "Blue (Lightning)": {"extra_traits": [dict(name="Damage Resistance", description="Lightning Resistance")]},
                    "Brass (Fire)": {"extra_traits": [dict(name="Damage Resistance", description="Fire Resistance")]},
                    "Bronze (Lightning)": {"extra_traits": [dict(name="Damage Resistance", description="Lightning Resistance")]},
                    "Copper (Acid)": {"extra_traits": [dict(name="Damage Resistance", description="Acid Resistance")]},
                    "Gold (Fire)": {"extra_traits": [dict(name="Damage Resistance", description="Fire Resistance")]},
                    "Green (Poison)": {"extra_traits": [dict(name="Damage Resistance", description="Poison Resistance")]},
                    "Red (Fire)": {"extra_traits": [dict(name="Damage Resistance", description="Fire Resistance")]},
                    "Silver (Cold)": {"extra_traits": [dict(name="Damage Resistance", description="Cold Resistance")]},
                    "White (Cold)": {"extra_traits": [dict(name="Damage Resistance", description="Cold Resistance")]}
                }
            )
        elif name == SpeciesName.GNOME:
            return cls(
                name=SpeciesName.GNOME,
                speed=30,
                darkvision=60,
                traits=[
                    dict(name="Gnomish Cunning", description="Advantage on Int, Wis, Cha saves vs magic.")
                ],
                lineages={
                    "Forest Gnome": {
                        "extra_spells": [
                            dict(name="Minor Illusion", level_required=1, count=99),
                            dict(name="Speak with Animals", level_required=1, count=1) 
                        ]
                    },
                    "Rock Gnome": {
                        "extra_spells": [
                            dict(name="Mending", level_required=1, count=99),
                            dict(name="Prestidigitation", level_required=1, count=99)
                        ],
                        "extra_traits": [
                            dict(name="Tinker", description="Use Prestidigitation to create tiny clockwork devices.")
                        ]
                    }
                }
            )
        elif name == SpeciesName.ORC:
            return cls(
                name=SpeciesName.ORC,
                speed=30,
                darkvision=120,
                traits=[
                    dict(name="Adrenaline Rush", description="Dash as Bonus Action + Temp HP."),
                    dict(name="Relentless Endurance", description="Drop to 1 HP instead of 0 once per Long Rest.")
                ]
            )
        elif name == SpeciesName.TIEFLING:
             return cls(
                name=SpeciesName.TIEFLING,
                speed=30,
                darkvision=60,
                traits=[
                    dict(name="Otherworldly Presence", description="Know Thaumaturgy cantrip.")
                ],
                free_spells=[
                    dict(name="Thaumaturgy", level_required=1, count=99)
                ],
                lineages={
                    "Abyssal": {
                        "extra_traits": [dict(name="Abyssal Legacy", description="Resistance to Poison damage.")],
                        "extra_spells": [
                            dict(name="Poison Spray", level_required=1, count=99),
                            dict(name="Ray of Sickness", level_required=3, count=1),
                            dict(name="Hold Person", level_required=5, count=1)
                        ]
                    },
                    "Chthonic": {
                        "extra_traits": [dict(name="Chthonic Legacy", description="Resistance to Necrotic damage.")],
                        "extra_spells": [
                            dict(name="Chill Touch", level_required=1, count=99),
                            dict(name="False Life", level_required=3, count=1),
                            dict(name="Ray of Enfeeblement", level_required=5, count=1)
                        ]
                    },
                    "Infernal": {
                        "extra_traits": [dict(name="Infernal Legacy", description="Resistance to Fire damage.")],
                        "extra_spells": [
                            dict(name="Fire Bolt", level_required=1, count=99),
                            dict(name="Hellish Rebuke", level_required=3, count=1),
                            dict(name="Darkness", level_required=5, count=1)
                        ]
                    }
                }
            )
        elif name == SpeciesName.GOLIATH:
             return cls(
                 name=SpeciesName.GOLIATH,
                 speed=35,
                 traits=[
                     dict(name="Powerful Build", description="Advantage ending Grappled condition. Count as one size larger for carrying."),
                     dict(name="Large Form", description="Level 5: Become Large as Bonus Action for 10 mins.")
                 ],
                 lineages={
                     "Cloud Giant": {"extra_traits": [dict(name="Cloud's Jaunt", description="Bonus Action teleport 30ft.")]},
                     "Fire Giant": {"extra_traits": [dict(name="Fire's Burn", description="Add 1d10 Fire damage to hit.")]},
                     "Frost Giant": {"extra_traits": [dict(name="Frost's Chill", description="Add 1d6 Cold damage to hit, reduce speed 10ft.")]},
                     "Hill Giant": {"extra_traits": [dict(name="Hill's Tumble", description="Knock Large or smaller creature Prone on hit.")]},
                     "Stone Giant": {"extra_traits": [dict(name="Stone's Endurance", description="Reaction roll 1d12+CON to reduce damage taken.")]},
                     "Storm Giant": {"extra_traits": [dict(name="Storm's Thunder", description="Reaction 1d8 Thunder damage to attacker.")]}
                 }
             )
        elif name == SpeciesName.AASIMAR:
             return cls(
                 name=SpeciesName.AASIMAR,
                 speed=30,
                 darkvision=60,
                 traits=[
                     dict(name="Celestial Revelation", description="Transform to gain flight or damage bonus."),
                     dict(name="Healing Hands", description="Heal HP equal to level."),
                     dict(name="Light Bearer", description="Know Light cantrip.")
                 ]
             )
        # Fallback
        return cls(name=name)
