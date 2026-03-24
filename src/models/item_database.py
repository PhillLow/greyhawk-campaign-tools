import os
import json
import re
from src.models.equipment import Item, Weapon, Armor, ItemType, WeaponProperty, WeaponMastery, DamageType, ArmorCategory

_EQUIPMENT_CACHE = None

def _load_equipment():
    global _EQUIPMENT_CACHE
    if _EQUIPMENT_CACHE is None:
        try:
            path = os.path.join(os.path.dirname(__file__), "generated_equipment.json")
            with open(path, "r", encoding="utf-8") as f:
                _EQUIPMENT_CACHE = json.load(f)
        except Exception:
            _EQUIPMENT_CACHE = {"Weapons": [], "Armor": [], "Items": []}


class ItemDatabase:
    """Catalog of standard 2024 PHB items, dynamically loaded from AST."""
    
    @staticmethod
    def get_all_items() -> list[Item]:
        _load_equipment()
        items = []
        
        for w_data in _EQUIPMENT_CACHE.get("Weapons", []):
            try:
                props = []
                r_norm = 5
                r_long = None
                r_ammo = False
                for p in w_data.get("properties", []):
                    p_upper = p.upper()
                    if "TWO-HANDED" in p_upper: props.append(WeaponProperty.TWO_HANDED)
                    elif "LIGHT" in p_upper: props.append(WeaponProperty.LIGHT)
                    elif "FINESSE" in p_upper: props.append(WeaponProperty.FINESSE)
                    elif "THROWN" in p_upper: props.append(WeaponProperty.THROWN)
                    elif "VERSATILE" in p_upper: props.append(WeaponProperty.VERSATILE)
                    elif "REACH" in p_upper: props.append(WeaponProperty.REACH)
                    elif "LOADING" in p_upper: props.append(WeaponProperty.LOADING)
                    elif "HEAVY" in p_upper: props.append(WeaponProperty.HEAVY)
                    
                    if "AMMUNITION" in p_upper: 
                        props.append(WeaponProperty.AMMUNITION)
                        r_ammo = True
                        
                    if "RANGE" in p_upper:
                        m = re.search(r'RANGE\s+(\d+)(?:/(\d+))?', p_upper)
                        if m:
                            r_norm = int(m.group(1))
                            if m.group(2): r_long = int(m.group(2))
                
                mastery_val = None
                m_str = w_data.get("mastery")
                if m_str:
                    try: mastery_val = WeaponMastery(m_str.capitalize())
                    except: pass
                    
                dmg_type_val = DamageType.BLUDGEONING
                dt_str = w_data.get("damage_type", "BLUDGEONING")
                if dt_str:
                    try: dmg_type_val = DamageType(dt_str.capitalize())
                    except: pass
                    
                items.append(Weapon(
                    name=w_data["name"],
                    cost_gp=w_data.get("cost_gp", 0.0),
                    weight=w_data.get("weight", 0.0),
                    damage_dice=w_data.get("damage_dice", "1d4"),
                    damage_type=dmg_type_val,
                    properties=props,
                    mastery=mastery_val,
                    range_normal=r_norm,
                    range_long=r_long,
                    requires_ammo=r_ammo
                ))
            except Exception as e:
                pass
                
        for a_data in _EQUIPMENT_CACHE.get("Armor", []):
            try:
                cat_str = a_data.get("category", "LIGHT").capitalize()
                try: cat_val = ArmorCategory(cat_str)
                except: cat_val = ArmorCategory.LIGHT
                
                tool_req = None
                if a_data["name"].lower() == "plate armor":
                    tool_req = "Smith's Tools"
                
                items.append(Armor(
                    name=a_data["name"],
                    cost_gp=a_data.get("cost_gp", 0.0),
                    weight=a_data.get("weight", 0.0),
                    ac_base=a_data.get("ac_base", 10),
                    category=cat_val,
                    dex_cap=a_data.get("dex_cap"),
                    strength_requirement=a_data.get("strength_requirement", 0),
                    stealth_disadvantage=a_data.get("stealth_disadvantage", False),
                    tool_requirements=tool_req
                ))
            except Exception as e:
                pass
                
        existing_names = set(i.name.lower() for i in items)
        
        if "shield" not in existing_names:
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
            
        items.append(Item(name="Potion of Healing", item_type=ItemType.POTION, cost_gp=50, weight=0.5, 
                          description="Restores 2d4+2 HP.", tool_requirements="Herbalism Kit"))
                          
        # Load Magic Items (Wondrous Items, Rings, etc.)
        try:
            magic_path = os.path.join(os.path.dirname(__file__), "generated_magic_items.json")
            if os.path.exists(magic_path):
                with open(magic_path, "r", encoding="utf-8") as f:
                    magics = json.load(f)
                    for m in magics:
                        # Prevent collision if magic item overlaps standard
                        if m["name"].lower() not in existing_names:
                            from src.models.equipment import Rarity
                            r_str = m.get("rarity", "Uncommon").upper()
                            r_enum = Rarity.UNCOMMON
                            if "COMMON" in r_str: r_enum = getattr(Rarity, r_str.replace(" ", "_"), Rarity.UNCOMMON)

                            items.append(Item(
                                name=m["name"],
                                item_type=ItemType.GEAR,
                                description=m.get("description", ""),
                                rarity=r_enum,
                                weight=1.0 # arbitrary default for magic items unlisted
                            ))
                            existing_names.add(m["name"].lower())
        except Exception:
            pass

        # Load Poisons
        try:
            poison_path = os.path.join(os.path.dirname(__file__), "generated_poisons.json")
            if os.path.exists(poison_path):
                with open(poison_path, "r", encoding="utf-8") as f:
                    poisons = json.load(f)
                    for p in poisons:
                        if p["name"].lower() not in existing_names:
                            items.append(Item(
                                name=p["name"],
                                item_type=ItemType.GEAR,
                                cost_gp=p.get("cost_gp", 0),
                                weight=0.1,
                                description=f"[{p.get('type', 'Ingested')}] " + p.get("description", "")
                            ))
                            existing_names.add(p["name"].lower())
        except Exception:
            pass

        return items

    @staticmethod
    def get_item(name: str) -> Item | None:
        for item in ItemDatabase.get_all_items():
            if item.name.lower() == name.lower():
                return item
        return None
