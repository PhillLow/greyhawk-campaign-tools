from pydantic import BaseModel
from enum import Enum
from typing import List, Dict
from src.models.stats import Ability

class BackgroundName(str, Enum):
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
        if name == BackgroundName.FARMER:
            return cls(
                name=BackgroundName.FARMER,
                ability_scores=[Ability.STR, Ability.CON, Ability.WIS],
                origin_feat="Tough",
                skills=["Animal Handling", "Nature"],
                tool_proficiency="Carpenter's Tools"
            )
        elif name == BackgroundName.NOBLE:
            return cls(
                name=BackgroundName.NOBLE,
                ability_scores=[Ability.STR, Ability.CHA, Ability.INT], # Approximation
                origin_feat="Skilled",
                skills=["History", "Persuasion"],
                tool_proficiency="Gaming Set"
            )
        # Fallback
        return cls(
            name=name,
            ability_scores=[Ability.STR, Ability.DEX, Ability.CON],
            origin_feat="Alert",
            skills=["Perception", "Survival"],
            tool_proficiency="None"
        )
