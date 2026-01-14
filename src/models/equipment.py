from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

class ItemType(str, Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    GEAR = "Gear"
    POTION = "Potion"

class WeaponProperty(str, Enum):
    LIGHT = "Light"
    FINESSE = "Finesse"
    THROWN = "Thrown"
    TWO_HANDED = "Two-Handed"
    VERSATILE = "Versatile"
    REACH = "Reach"

class DamageType(str, Enum):
    BLUDGEONING = "Bludgeoning"
    PIERCING = "Piercing"
    SLASHING = "Slashing"
    FIRE = "Fire"
    COLD = "Cold"
    # ... expand as needed

class Item(BaseModel):
    name: str
    item_type: ItemType = ItemType.GEAR
    weight: float = 0.0
    cost_gp: float = 0.0
    description: str = ""
    equipped: bool = False

class WeaponMastery(str, Enum):
    CLEAVE = "Cleave"
    GRAZE = "Graze"
    NICK = "Nick"
    PUSH = "Push"
    SAP = "Sap"
    SLOW = "Slow"
    TOPPLE = "Topple"
    VEX = "Vex"

class Weapon(Item):
    item_type: ItemType = ItemType.WEAPON
    damage_dice: str = "1d4" # e.g. "1d8"
    damage_type: DamageType = DamageType.SLASHING
    properties: List[WeaponProperty] = []
    mastery: Optional[WeaponMastery] = None 

class Armor(Item):
    item_type: ItemType = ItemType.ARMOR
    ac_base: int = 11
    dex_cap: Optional[int] = None # None = unlimited. 0 = Heavy, 2 = Medium.
    stealth_disadvantage: bool = False
    strength_requirement: int = 0
