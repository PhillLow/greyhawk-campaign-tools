from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import os
import json

class FeatType(str, Enum):
    ORIGIN = "Origin"
    GENERAL = "General"
    FIGHTING_STYLE = "Fighting Style"
    EPIC_BOON = "Epic Boon" # Added Epic Boon mapping

class Feat(BaseModel):
    name: str
    description: str
    prerequisite_level: int = 1
    prerequisite_stat: Optional[str] = None # e.g. "Dexterity 13+"
    type: FeatType = FeatType.ORIGIN
    
    # In a full engine, this would have functional hooks. 
    # For now, it's descriptive.

_FEATS_CACHE = None

def _load_feats():
    global _FEATS_CACHE
    if _FEATS_CACHE is None:
        try:
            path = os.path.join(os.path.dirname(__file__), "generated_feats.json")
            with open(path, "r", encoding="utf-8") as f:
                _FEATS_CACHE = json.load(f)
        except Exception:
            _FEATS_CACHE = {"Origin": [], "General": [], "Fighting Style": [], "Epic Boon": []}

def _get_feats_by_type(feat_type: str, enum_type: FeatType) -> List[Feat]:
    _load_feats()
    feats = []
    for f in _FEATS_CACHE.get(feat_type, []):
        feats.append(Feat(
            name=f["name"],
            description=f["description"],
            type=enum_type,
            prerequisite_level=f.get("prerequisite_level", 1)
        ))
    return feats

class FeatDatabase:
    """Static database of common 2024 feats."""
    
    @staticmethod
    def get_origin_feats() -> List[Feat]:
        """Returns the list of Level 1 Origin Feats."""
        feats = _get_feats_by_type("Origin", FeatType.ORIGIN)
        existing_names = set([f.name for f in feats])
        hardcoded = [
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
        for hc in hardcoded:
            if hc.name not in existing_names:
                feats.append(hc)
        return feats
        
    @staticmethod
    def get_general_feats() -> List[Feat]:
        feats = _get_feats_by_type("General", FeatType.GENERAL)
        existing_names = set([f.name for f in feats])
        hardcoded = [
            Feat(name="War Caster", description="Advantage on Con saves for concentration. Cast spells as Opportunity Attacks.", type=FeatType.GENERAL, prerequisite_level=4),
            Feat(name="Sentinel", description="Creatures provoke OA even if disengaging.", type=FeatType.GENERAL, prerequisite_level=4),
            Feat(name="Sharpshooter", description="Ignore cover, power attack with ranged weapons.", type=FeatType.GENERAL, prerequisite_level=4),
            Feat(name="Great Weapon Master", description="Extra attack on crit/kill, power attack with heavy weapons.", type=FeatType.GENERAL, prerequisite_level=4),
            Feat(name="Resilient", description="+1 Stat and Proficiency in Save.", type=FeatType.GENERAL, prerequisite_level=4)
        ]
        for hc in hardcoded:
            if hc.name not in existing_names:
                feats.append(hc)
        return feats

    @staticmethod
    def get_fighting_style_feats() -> List[Feat]:
        feats = _get_feats_by_type("Fighting Style", FeatType.FIGHTING_STYLE)
        existing_names = set([f.name for f in feats])
        hardcoded = [
            Feat(name="Fighting Style: Archery", description="+2 to attack rolls with Ranged Weapons.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Defense", description="+1 to AC while wearing Armor.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Dueling", description="+2 damage with one-handed melee weapon (no other weapon).", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Great Weapon Fighting", description="Reroll 1s and 2s on damage dice with Two-Handed/Versatile weapons.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Protection", description="Reaction to impose Disadvantage on attack against ally within 5ft (Req Shield).", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Two-Weapon Fighting", description="Add Ability Mod to damage of second attack when you Light/Nick.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Interception", description="Reaction to reduce damage to ally by 1d10+PB (Req Shield/Martial Weapon).", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Thrown Weapon Fighting", description="+2 damage with Thrown weapons.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Unarmed Fighting", description="d6 (or d8) damage with Unarmed Strikes.", type=FeatType.FIGHTING_STYLE),
            Feat(name="Fighting Style: Blind Fighting", description="Blindsight 10ft.", type=FeatType.FIGHTING_STYLE)
        ]
        
        # Ensure 'Fighting Style' prefix is there for dynamically loaded feats
        for i, f in enumerate(feats):
            if not f.name.startswith("Fighting Style:"):
                feats[i].name = f"Fighting Style: {f.name}"
                existing_names.add(feats[i].name)
                
        for hc in hardcoded:
            if hc.name not in existing_names:
                feats.append(hc)
        return feats

    @staticmethod
    def get_epic_boon_feats() -> List[Feat]:
        return _get_feats_by_type("Epic Boon", FeatType.EPIC_BOON)

    @staticmethod
    def get_feat(name: str) -> Optional[Feat]:
        all_feats = FeatDatabase.get_origin_feats() + FeatDatabase.get_general_feats() + FeatDatabase.get_fighting_style_feats() + FeatDatabase.get_epic_boon_feats()
        for f in all_feats:
            if f.name.lower() == name.lower():
                return f
        return None
