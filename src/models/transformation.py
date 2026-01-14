from pydantic import BaseModel, Field
from typing import Optional

class Transformation(BaseModel):
    """Represents a temporary form (Wild Shape, Polymorph)."""
    name: str
    description: str = ""
    
    # Overrides (None means use Character's base)
    ac_override: Optional[int] = None
    speed_override: Optional[int] = None
    
    # Stat Overrides
    strength_score: Optional[int] = None
    dexterity_score: Optional[int] = None
    constitution_score: Optional[int] = None
    
    # HP Rules
    # 2024 Wild Shape: Keeps HP, gains Temp HP.
    # Polymorph: Replaces HP.
    replaces_hp: bool = False
    hp_value: int = 0 # Temp HP grant OR Replacement HP
    
    @staticmethod
    def get_template(name: str) -> 'Transformation':
        if name == "Wolf":
            return Transformation(
                name="Wolf",
                speed_override=40,
                ac_override=13, # Natural Armor
                strength_score=12,
                dexterity_score=15,
                constitution_score=12,
                hp_value=11 # Temp HP? Or irrelevant if just form stats.
            )
        elif name == "Brown Bear":
            return Transformation(
                name="Brown Bear",
                speed_override=40,
                ac_override=11,
                strength_score=19,
                dexterity_score=10,
                constitution_score=16,
                hp_value=34
            )
        return Transformation(name=name)
