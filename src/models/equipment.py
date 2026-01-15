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
    VERSATILE = "Versatile"
    REACH = "Reach"
    AMMUNITION = "Ammunition"
    LOADING = "Loading"
    HEAVY = "Heavy"
    RANGE = "Range" # usually implicit
    TWO_HANDED = "Two-Handed"

class Rarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    VERY_RARE = "Very Rare"
    LEGENDARY = "Legendary"

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
    rarity: Rarity = Rarity.COMMON # Default
    weight: float = 0.0
    cost_gp: float = 0.0
    description: str = ""
    equipped: bool = False
    tool_requirements: Optional[str] = None
    quantity: int = 1

class WeaponMastery(str, Enum):
    CLEAVE = "Cleave"
    GRAZE = "Graze"
    NICK = "Nick"
    PUSH = "Push"
    SAP = "Sap"
    SLOW = "Slow"
    TOPPLE = "Topple"
    VEX = "Vex"

class ArmorCategory(str, Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    SHIELD = "Shield"

class Weapon(Item):
    item_type: ItemType = ItemType.WEAPON
    damage_dice: str = "1d4" # e.g. "1d8"
    damage_type: DamageType = DamageType.SLASHING
    properties: List[WeaponProperty] = []
    mastery: Optional[WeaponMastery] = None 
    range_normal: int = 5
    range_long: Optional[int] = None
    requires_ammo: bool = False

class Armor(Item):
    item_type: ItemType = ItemType.ARMOR
    category: ArmorCategory = ArmorCategory.LIGHT # Default
    ac_base: int = 11 # For shields, this is usually +2 bonus, handled via logic? Or base AC?
    # 5e: Armor sets Base AC. Shield adds +2.
    # We will use ac_base as "Base AC" for armor, and "Bonus AC" for shield (2).
    dex_cap: Optional[int] = None # None = unlimited. 0 = Heavy, 2 = Medium.
    stealth_disadvantage: bool = False
    strength_requirement: int = 0
