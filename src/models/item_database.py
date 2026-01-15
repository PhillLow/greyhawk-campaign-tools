from src.models.equipment import Item, Weapon, Armor, ItemType, WeaponProperty, WeaponMastery, DamageType, ArmorCategory

class ItemDatabase:
    """Catalog of standard 2024 PHB items."""
    
    @staticmethod
    def get_all_items() -> list[Item]:
        items = []
        
        # --- WEAPONS ---
        items.append(Weapon(
            name="Dagger", 
            cost_gp=2, 
            weight=1, 
            damage_dice="1d4", 
            damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT, WeaponProperty.THROWN],
            mastery=WeaponMastery.NICK,
            range_normal=20,
            range_long=60
        ))
        items.append(Weapon(
            name="Greatsword", 
            cost_gp=50, 
            weight=6, 
            damage_dice="2d6", 
            damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.TWO_HANDED],
            mastery=WeaponMastery.GRAZE,
            range_normal=5
        ))
        items.append(Weapon(
            name="Longbow", 
            cost_gp=50, 
            weight=2, 
            damage_dice="1d8", 
            damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.TWO_HANDED, WeaponProperty.AMMUNITION],
            mastery=WeaponMastery.SLOW,
            range_normal=150,
            range_long=600,
            requires_ammo=True
        ))
        items.append(Weapon(
            name="Longsword", 
            cost_gp=15, 
            weight=3, 
            damage_dice="1d8", 
            damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.VERSATILE],
            mastery=WeaponMastery.SAP,
            range_normal=5
        ))
        
        # Simple Melee
        items.append(Weapon(
            name="Club", cost_gp=0.1, weight=2, damage_dice="1d4", damage_type=DamageType.BLUDGEONING,
            properties=[WeaponProperty.LIGHT], mastery=WeaponMastery.SLOW, range_normal=5
        ))
        items.append(Weapon(
            name="Handaxe", cost_gp=5, weight=2, damage_dice="1d6", damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.LIGHT, WeaponProperty.THROWN], mastery=WeaponMastery.VEX, range_normal=20, range_long=60
        ))
        items.append(Weapon(
            name="Quarterstaff", cost_gp=0.2, weight=4, damage_dice="1d6", damage_type=DamageType.BLUDGEONING,
            properties=[WeaponProperty.VERSATILE], mastery=WeaponMastery.TOPPLE, range_normal=5
        ))
        items.append(Weapon(
            name="Spear", cost_gp=1, weight=3, damage_dice="1d6", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.THROWN, WeaponProperty.VERSATILE], mastery=WeaponMastery.SAP, range_normal=20, range_long=60
        ))
        
        # Simple Ranged
        items.append(Weapon(
            name="Shortbow", cost_gp=25, weight=2, damage_dice="1d6", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.AMMUNITION, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.VEX, 
            range_normal=80, range_long=320, requires_ammo=True
        ))
        items.append(Weapon(
            name="Light Crossbow", cost_gp=25, weight=5, damage_dice="1d8", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.AMMUNITION, WeaponProperty.LOADING, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.SLOW, 
            range_normal=80, range_long=320, requires_ammo=True
        ))
        items.append(Weapon(
            name="Dart", cost_gp=0.05, weight=0.25, damage_dice="1d4", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.FINESSE, WeaponProperty.THROWN], mastery=WeaponMastery.VEX, 
            range_normal=20, range_long=60
        ))
        items.append(Weapon(
            name="Sling", cost_gp=0.1, weight=0, damage_dice="1d4", damage_type=DamageType.BLUDGEONING,
            properties=[WeaponProperty.AMMUNITION], mastery=WeaponMastery.SLOW, 
            range_normal=30, range_long=120, requires_ammo=True
        ))
        
        # Martial Melee
        items.append(Weapon(
            name="Greataxe", cost_gp=30, weight=7, damage_dice="1d12", damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.TWO_HANDED, WeaponProperty.HEAVY], mastery=WeaponMastery.CLEAVE, range_normal=5
        ))
        items.append(Weapon(
            name="Maul", cost_gp=10, weight=10, damage_dice="2d6", damage_type=DamageType.BLUDGEONING,
            properties=[WeaponProperty.TWO_HANDED, WeaponProperty.HEAVY], mastery=WeaponMastery.TOPPLE, range_normal=5
        ))
        items.append(Weapon(
            name="Rapier", cost_gp=25, weight=2, damage_dice="1d8", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.FINESSE], mastery=WeaponMastery.VEX, range_normal=5
        ))
        items.append(Weapon(
            name="Shortsword", cost_gp=10, weight=2, damage_dice="1d6", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT], mastery=WeaponMastery.VEX, range_normal=5
        ))
        items.append(Weapon(
            name="Scimitar", cost_gp=25, weight=3, damage_dice="1d6", damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.FINESSE, WeaponProperty.LIGHT], mastery=WeaponMastery.NICK, range_normal=5
        ))
        items.append(Weapon(
            name="Flail", cost_gp=10, weight=2, damage_dice="1d8", damage_type=DamageType.BLUDGEONING, 
            properties=[], mastery=WeaponMastery.SAP, range_normal=5
        ))
        items.append(Weapon(
            name="Glaive", cost_gp=20, weight=6, damage_dice="1d10", damage_type=DamageType.SLASHING, 
            properties=[WeaponProperty.HEAVY, WeaponProperty.REACH, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.GRAZE, range_normal=5
        ))
        items.append(Weapon(
            name="Halberd", cost_gp=20, weight=6, damage_dice="1d10", damage_type=DamageType.SLASHING, 
            properties=[WeaponProperty.HEAVY, WeaponProperty.REACH, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.CLEAVE, range_normal=5
        ))
        items.append(Weapon(
            name="Lance", cost_gp=10, weight=6, damage_dice="1d12", damage_type=DamageType.PIERCING, 
            properties=[WeaponProperty.REACH, WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.TOPPLE, range_normal=5
        ))
        items.append(Weapon(
            name="Maul", cost_gp=10, weight=10, damage_dice="2d6", damage_type=DamageType.BLUDGEONING, 
            properties=[WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.TOPPLE, range_normal=5
        ))
        items.append(Weapon(
            name="Morningstar", cost_gp=15, weight=4, damage_dice="1d8", damage_type=DamageType.PIERCING, 
            properties=[], mastery=WeaponMastery.SAP, range_normal=5
        ))
        items.append(Weapon(
            name="Pike", cost_gp=5, weight=18, damage_dice="1d10", damage_type=DamageType.PIERCING, 
            properties=[WeaponProperty.HEAVY, WeaponProperty.REACH, WeaponProperty.TWO_HANDED], mastery=WeaponMastery.PUSH, range_normal=5
        ))
        items.append(Weapon(
            name="Trident", cost_gp=5, weight=4, damage_dice="1d8", damage_type=DamageType.PIERCING, 
            properties=[WeaponProperty.THROWN, WeaponProperty.VERSATILE], mastery=WeaponMastery.TOPPLE, range_normal=20, range_long=60
        ))
        items.append(Weapon(
            name="War Pick", cost_gp=5, weight=2, damage_dice="1d8", damage_type=DamageType.PIERCING, 
            properties=[WeaponProperty.VERSATILE], mastery=WeaponMastery.SAP, range_normal=5
        ))
        items.append(Weapon(
            name="Warhammer", cost_gp=15, weight=2, damage_dice="1d8", damage_type=DamageType.BLUDGEONING, 
            properties=[WeaponProperty.VERSATILE], mastery=WeaponMastery.PUSH, range_normal=5
        ))
        items.append(Weapon(
            name="Whip", cost_gp=2, weight=3, damage_dice="1d4", damage_type=DamageType.SLASHING, 
            properties=[WeaponProperty.FINESSE, WeaponProperty.REACH], mastery=WeaponMastery.SLOW, range_normal=5
        ))
        
        # Martial Ranged
        items.append(Weapon(
            name="Heavy Crossbow", cost_gp=50, weight=18, damage_dice="1d10", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.AMMUNITION, WeaponProperty.HEAVY, WeaponProperty.LOADING, WeaponProperty.TWO_HANDED], 
            mastery=WeaponMastery.PUSH, range_normal=100, range_long=400, requires_ammo=True
        ))
        items.append(Weapon(
            name="Hand Crossbow", cost_gp=75, weight=3, damage_dice="1d6", damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.AMMUNITION, WeaponProperty.LIGHT, WeaponProperty.LOADING], 
            mastery=WeaponMastery.VEX, range_normal=30, range_long=120, requires_ammo=True
        ))
        
        # --- ARMOR ---
        items.append(Armor(
            name="Leather Armor", 
            cost_gp=10, 
            weight=10, 
            ac_base=11, 
            dex_cap=None, 
            strength_requirement=0,
            stealth_disadvantage=False
        ))
        items.append(Armor(
            name="Scale Mail", 
            cost_gp=50, 
            weight=45, 
            ac_base=14, 
            dex_cap=2, 
            strength_requirement=0,
            stealth_disadvantage=True
        ))
        items.append(Armor(
            name="Plate Armor", 
            cost_gp=1500, 
            weight=65, 
            ac_base=18, 
            dex_cap=0, 
            strength_requirement=15,
            stealth_disadvantage=True,
            tool_requirements="Smith's Tools"
        ))
        items.append(Armor(
            name="Shield",
            cost_gp=10,
            weight=6,
            ac_base=2,
            category=ArmorCategory.SHIELD,
            dex_cap=None,
            strength_requirement=0,
            stealth_disadvantage=False
        ))
        
        # --- GEAR ---
        items.append(Item(name="Potion of Healing", item_type=ItemType.POTION, cost_gp=50, weight=0.5, 
                          description="Restores 2d4+2 HP.", tool_requirements="Herbalism Kit"))
        
        return items

    @staticmethod
    def get_item(name: str) -> Item | None:
        for item in ItemDatabase.get_all_items():
            if item.name.lower() == name.lower():
                return item
        return None
