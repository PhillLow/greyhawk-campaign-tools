from pydantic import BaseModel
from typing import Optional, List

class Feat(BaseModel):
    name: str
    description: str
    prerequisite_level: int = 1
    prerequisite_stat: Optional[str] = None # e.g. "Dexterity 13+"
    
    # In a full engine, this would have functional hooks. 
    # For now, it's descriptive.

class FeatDatabase:
    """Static database of common 2024 feats."""
    
    @staticmethod
    def get_origin_feats() -> List[Feat]:
        """Returns the list of Level 1 Origin Feats."""
        return [
            Feat(name="Alert", description="Initiative +PB. Swap initiative with ally."),
            Feat(name="Crafter", description="Tool proficiencies, faster crafting."),
            Feat(name="Healer", description="Reroll healing dice. Stabilize to 1 HP."),
            Feat(name="Lucky", description="Luck points to gain advantage/disadvantage."),
            Feat(name="Magic Initiate", description="Two cantrips and one level 1 spell."),
            Feat(name="Musician", description="Grant Heroic Inspiration after rest."),
            Feat(name="Savage Attacker", description="Advantage on damage rolls."),
            Feat(name="Skilled", description="Gain 3 skill proficiencies."),
            Feat(name="Tough", description="+2 HP per level."),
            Feat(name="Tavern Brawler", description="Unarmed damage d4, push 5ft.")
        ]

    @staticmethod
    def get_feat(name: str) -> Optional[Feat]:
        all_feats = FeatDatabase.get_origin_feats() # + General Feats later
        for f in all_feats:
            if f.name.lower() == name.lower():
                return f
        return None
