from pydantic import BaseModel
from typing import Any, Optional

class Modifier(BaseModel):
    """
    Represents a modification to a statistic, roll, or property.
    e.g. +2 to Strength, Advantage on Stealth, -2 to d20 Tests (Exhaustion).
    """
    name: str # e.g. "Exhaustion Level 1", "Gauntlets of Ogre Power"
    value: Any # +2, -5, "Advantage", 19 (for set score)
    target: str # "strength", "d20_test", "speed", "ac"
    type: str = "bonus" # "bonus" (add), "set" (override), "multiplier"
    source: Optional[str] = None # "Race", "Item", "Condition"
