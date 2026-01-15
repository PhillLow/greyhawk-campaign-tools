from pydantic import BaseModel
from enum import Enum
from typing import List, Dict
from src.models.stats import Ability

class BackgroundName(str, Enum):
    ACOLYTE = "Acolyte"
    ARTISAN = "Artisan"
    CHARLATAN = "Charlatan"
    CRIMINAL = "Criminal"
    ENTERTAINER = "Entertainer"
    FARMER = "Farmer"
    GUARD = "Guard"
    GUIDE = "Guide"
    HERMIT = "Hermit"
    MERCHANT = "Merchant"
    NOBLE = "Noble"
    SAGE = "Sage"
    SAILOR = "Sailor"
    SCRIBE = "Scribe"
    SOLDIER = "Soldier"
    WAYFARER = "Wayfarer"

class Background(BaseModel):
    name: BackgroundName
    ability_scores: List[Ability] # The 3 abilities you can boost
    origin_feat: str
    skills: List[str]
    tool_proficiency: str

    @classmethod
    def get_template(cls, name: BackgroundName) -> "Background":
        if name == BackgroundName.ACOLYTE:
             return cls(
                 name=BackgroundName.ACOLYTE,
                 ability_scores=[Ability.INT, Ability.WIS, Ability.CHA],
                 origin_feat="Magic Initiate (Cleric)",
                 skills=["Insight", "Religion"],
                 tool_proficiency="Calligrapher's Supplies"
             )
        elif name == BackgroundName.ARTISAN:
             return cls(
                 name=BackgroundName.ARTISAN,
                 ability_scores=[Ability.STR, Ability.DEX, Ability.INT],
                 origin_feat="Crafter",
                 skills=["Investigation", "Persuasion"],
                 tool_proficiency="Artisan's Tools (One Type)"
             )
        elif name == BackgroundName.CHARLATAN:
             return cls(
                 name=BackgroundName.CHARLATAN,
                 ability_scores=[Ability.DEX, Ability.CON, Ability.CHA],
                 origin_feat="Skilled",
                 skills=["Deception", "Sleight of Hand"],
                 tool_proficiency="Forgery Kit"
             )
        elif name == BackgroundName.CRIMINAL:
             return cls(
                 name=BackgroundName.CRIMINAL,
                 ability_scores=[Ability.DEX, Ability.CON, Ability.INT],
                 origin_feat="Alert",
                 skills=["Sleight of Hand", "Stealth"],
                 tool_proficiency="Thieves' Tools"
             )
        elif name == BackgroundName.ENTERTAINER:
             return cls(
                 name=BackgroundName.ENTERTAINER,
                 ability_scores=[Ability.STR, Ability.DEX, Ability.CHA],
                 origin_feat="Musician",
                 skills=["Acrobatics", "Performance"],
                 tool_proficiency="Musical Instrument"
             )
        elif name == BackgroundName.FARMER:
            return cls(
                name=BackgroundName.FARMER,
                ability_scores=[Ability.STR, Ability.CON, Ability.WIS],
                origin_feat="Tough",
                skills=["Animal Handling", "Nature"],
                tool_proficiency="Carpenter's Tools"
            )
        elif name == BackgroundName.GUARD:
             return cls(
                 name=BackgroundName.GUARD,
                 ability_scores=[Ability.STR, Ability.INT, Ability.WIS],
                 origin_feat="Alert",
                 skills=["Athletics", "Perception"],
                 tool_proficiency="Gaming Set"
             )
        elif name == BackgroundName.GUIDE:
             return cls(
                 name=BackgroundName.GUIDE,
                 ability_scores=[Ability.DEX, Ability.CON, Ability.WIS],
                 origin_feat="Magic Initiate (Druid)",
                 skills=["Stealth", "Survival"],
                 tool_proficiency="Cartographer's Tools"
             )
        elif name == BackgroundName.HERMIT:
             return cls(
                 name=BackgroundName.HERMIT,
                 ability_scores=[Ability.CON, Ability.WIS, Ability.CHA],
                 origin_feat="Healer",
                 skills=["Medicine", "Religion"],
                 tool_proficiency="Herbalism Kit"
             )
        elif name == BackgroundName.MERCHANT:
             return cls(
                 name=BackgroundName.MERCHANT,
                 ability_scores=[Ability.CON, Ability.INT, Ability.CHA], # Check Merchant stats in final
                 origin_feat="Lucky",
                 skills=["Animal Handling", "Persuasion"],
                 tool_proficiency="Navigator's Tools"
             )
        elif name == BackgroundName.NOBLE:
            return cls(
                name=BackgroundName.NOBLE,
                ability_scores=[Ability.STR, Ability.INT, Ability.CHA],
                origin_feat="Skilled",
                skills=["History", "Persuasion"],
                tool_proficiency="Gaming Set"
            )
        elif name == BackgroundName.SAGE:
             return cls(
                 name=BackgroundName.SAGE,
                 ability_scores=[Ability.CON, Ability.INT, Ability.WIS],
                 origin_feat="Magic Initiate (Wizard)",
                 skills=["Arcana", "History"],
                 tool_proficiency="Calligrapher's Supplies"
             )
        elif name == BackgroundName.SAILOR:
             return cls(
                 name=BackgroundName.SAILOR,
                 ability_scores=[Ability.STR, Ability.DEX, Ability.WIS],
                 origin_feat="Tavern Brawler",
                 skills=["Acrobatics", "Perception"],
                 tool_proficiency="Navigator's Tools"
             )
        elif name == BackgroundName.SCRIBE:
             return cls(
                 name=BackgroundName.SCRIBE,
                 ability_scores=[Ability.DEX, Ability.INT, Ability.WIS],
                 origin_feat="Skilled",
                 skills=["Investigation", "Perception"],
                 tool_proficiency="Calligrapher's Supplies"
             )
        elif name == BackgroundName.SOLDIER:
             return cls(
                 name=BackgroundName.SOLDIER,
                 ability_scores=[Ability.STR, Ability.DEX, Ability.CON],
                 origin_feat="Savage Attacker",
                 skills=["Athletics", "Intimidation"],
                 tool_proficiency="Gaming Set"
             )
        elif name == BackgroundName.WAYFARER:
             return cls(
                 name=BackgroundName.WAYFARER,
                 ability_scores=[Ability. DEX, Ability.WIS, Ability.CHA],
                 origin_feat="Lucky",
                 skills=["Insight", "Stealth"],
                 tool_proficiency="Thieves' Tools"
             )
        # Fallback
        return cls(
            name=name,
            ability_scores=[Ability.STR, Ability.DEX, Ability.CON],
            origin_feat="Alert",
            skills=["Perception", "Survival"],
            tool_proficiency="None"
        )
