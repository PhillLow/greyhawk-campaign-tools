from pydantic import BaseModel, Field, computed_field
from typing import Dict, Optional, List, Any
from src.models.modifier import Modifier
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
    
    modifiers: List[Modifier] = []

    def get_score(self, ability: Ability) -> int:
        """Calculates final score applying modifiers."""
        base_obj = self.get(ability)
        base = base_obj.score
        
        # Check for internal overrides first (legacy support)
        if base_obj.override is not None:
            return base_obj.override
            
        # Filter external modifiers
        # Target should match the Ability value e.g. "Strength"
        relevant = [m for m in self.modifiers if m.target.lower() == ability.value.lower()]
        
        # Apply SET (override) modifiers
        # If multiple sets exist, usually the highest one applies (e.g. 19 vs 21)
        sets = [m for m in relevant if m.type == "set"]
        if sets:
            # Assumes value is int
            base = max([int(m.value) for m in sets])
            
        # Apply BONUS modifiers
        bonuses = [int(m.value) for m in relevant if m.type == "bonus"]
        return base + sum(bonuses)

    def get_mod(self, ability: Ability) -> int:
        """Calculates modifier from the dynamic score."""
        return (self.get_score(ability) - 10) // 2

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
