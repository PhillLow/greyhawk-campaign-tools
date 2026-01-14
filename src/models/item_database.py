from src.models.equipment import Item, Weapon, Armor, ItemType, WeaponProperty, WeaponMastery, DamageType

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
            mastery=WeaponMastery.NICK
        ))
        items.append(Weapon(
            name="Greatsword", 
            cost_gp=50, 
            weight=6, 
            damage_dice="2d6", 
            damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.TWO_HANDED],
            mastery=WeaponMastery.GRAZE
        ))
        items.append(Weapon(
            name="Longbow", 
            cost_gp=50, 
            weight=2, 
            damage_dice="1d8", 
            damage_type=DamageType.PIERCING,
            properties=[WeaponProperty.TWO_HANDED], # Ammunition property implied for now
            mastery=WeaponMastery.SLOW
        ))
        items.append(Weapon(
            name="Longsword", 
            cost_gp=15, 
            weight=3, 
            damage_dice="1d8", 
            damage_type=DamageType.SLASHING,
            properties=[WeaponProperty.VERSATILE],
            mastery=WeaponMastery.SAP
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
            stealth_disadvantage=True
        ))
        
        # --- GEAR ---
        items.append(Item(name="Potion of Healing", item_type=ItemType.POTION, cost_gp=50, weight=0.5, description="Restores 2d4+2 HP."))
        
        return items

    @staticmethod
    def get_item(name: str) -> Item | None:
        for item in ItemDatabase.get_all_items():
            if item.name.lower() == name.lower():
                return item
        return None
