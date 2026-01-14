from pydantic import BaseModel, Field, computed_field
from typing import Dict, Optional
from enum import Enum
import math

class Ability(str, Enum):
    STR = "Strength"
    DEX = "Dexterity"
    CON = "Constitution"
    INT = "Intelligence"
    WIS = "Wisdom"
    CHA = "Charisma"

class Skill(str, Enum):
    ACROBATICS = "Acrobatics"
    ANIMAL_HANDLING = "Animal Handling"
    ARCANA = "Arcana"
    ATHLETICS = "Athletics"
    DECEPTION = "Deception"
    HISTORY = "History"
    INSIGHT = "Insight"
    INTIMIDATION = "Intimidation"
    INVESTIGATION = "Investigation"
    MEDICINE = "Medicine"
    NATURE = "Nature"
    PERCEPTION = "Perception"
    PERFORMANCE = "Performance"
    PERSUASION = "Persuasion"
    RELIGION = "Religion"
    SLEIGHT_OF_HAND = "Sleight of Hand"
    STEALTH = "Stealth"
    SURVIVAL = "Survival"

class AbilityScore(BaseModel):
    name: Ability
    score: int = Field(..., ge=1, le=30)
    override: Optional[int] = None

    @computed_field
    def value(self) -> int:
        """Returns the effective score (base or override)."""
        return self.override if self.override is not None else self.score

    @computed_field
    def modifier(self) -> int:
        """Calculates the 2024 PHB modifier: floor((score - 10) / 2)."""
        # Note: In Python, // operator implements floor division for integers correctly handling negatives
        return (self.value - 10) // 2

class Stats(BaseModel):
    """Container for all 6 ability scores."""
    strength: AbilityScore = AbilityScore(name=Ability.STR, score=10)
    dexterity: AbilityScore = AbilityScore(name=Ability.DEX, score=10)
    constitution: AbilityScore = AbilityScore(name=Ability.CON, score=10)
    intelligence: AbilityScore = AbilityScore(name=Ability.INT, score=10)
    wisdom: AbilityScore = AbilityScore(name=Ability.WIS, score=10)
    charisma: AbilityScore = AbilityScore(name=Ability.CHA, score=10)

    def get(self, ability: Ability) -> AbilityScore:
        mapping = {
            Ability.STR: self.strength,
            Ability.DEX: self.dexterity,
            Ability.CON: self.constitution,
            Ability.INT: self.intelligence,
            Ability.WIS: self.wisdom,
            Ability.CHA: self.charisma
        }
        return mapping[ability]
