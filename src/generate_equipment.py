import os
import sys
import json
import re

def parse_cost(cost_str):
    cost_str = cost_str.strip().upper()
    if cost_str == '—': return 0.0
    val_str = re.sub(r'[^\d.]', '', cost_str)
    if not val_str: return 0.0
    val = float(val_str)
    if 'CP' in cost_str: return val / 100.0
    if 'SP' in cost_str: return val / 10.0
    if 'EP' in cost_str: return val / 2.0
    if 'PP' in cost_str: return val * 10.0
    return val # GP

def parse_weight(weight_str):
    weight_str = weight_str.strip()
    if weight_str == '—': return 0.0
    
    try:
        if "/" in weight_str:
            parts = weight_str.replace(" lb.", "").split("/")
            if len(parts) == 2:
                return float(parts[0]) / float(parts[1])
    except Exception:
        pass
        
    val_str = re.sub(r'[^\d.]', '', weight_str)
    if not val_str: return 0.0
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def extract_equipment():
    filepath = "dnd-5e-srd-markdown/equipment.md"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    sections = content.split("## Armor")
    weapon_text = sections[0]
    armor_text = sections[1].split("## Adventuring Gear")[0]
    
    pattern = r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>'
    
    db = {"Weapons": [], "Armor": [], "Items": []}
    
    # Parse Weapons
    for match in re.findall(pattern, weapon_text, re.DOTALL):
        name = match[0].strip()
        damage_raw = match[1].strip()
        props_raw = match[2].strip()
        mastery = match[3].strip() if match[3].strip() != '—' else None
        weight = parse_weight(match[4])
        cost = parse_cost(match[5])
        
        dmg_split = damage_raw.split(" ", 1)
        dice = dmg_split[0]
        dmg_type = dmg_split[1].strip() if len(dmg_split) > 1 else "None"
        
        props = [p.strip() for p in props_raw.split(",")] if props_raw != '—' else []
        
        db["Weapons"].append({
            "name": name,
            "damage_dice": dice,
            "damage_type": dmg_type.upper(),
            "properties": props,
            "mastery": mastery.upper() if mastery else None,
            "weight": weight,
            "cost_gp": cost
        })
        
    # Parse Armor
    for match in re.findall(pattern, armor_text, re.DOTALL):
        name = match[0].strip()
        ac_raw = match[1].strip()
        str_req = match[2].strip()
        stealth = match[3].strip()
        weight = parse_weight(match[4])
        cost = parse_cost(match[5])
        
        ac_base = 11
        dex_cap = None
        category = "Light"
        
        if "+ Dex modifier (max 2)" in ac_raw:
            category = "Medium"
            dex_cap = 2
            ac_base = int(ac_raw.split(" ")[0])
        elif "+ Dex modifier" in ac_raw:
            category = "Light"
            ac_base = int(ac_raw.split(" ")[0])
        elif "Shield" in name:
            category = "Shield"
            ac_base = 2
        else:
            category = "Heavy"
            dex_cap = 0
            try:
                ac_base = int(ac_raw)
            except:
                ac_base = 10
                
        str_val = 0
        if "Str" in str_req:
            str_val = int(str_req.replace("Str ", ""))
            
        stealth_disadv = (stealth == "Disadvantage")
        
        db["Armor"].append({
            "name": name,
            "category": category.upper(),
            "ac_base": ac_base,
            "dex_cap": dex_cap,
            "strength_requirement": str_val,
            "stealth_disadvantage": stealth_disadv,
            "weight": weight,
            "cost_gp": cost
        })

    out_path = "src/models/generated_equipment.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(db, f, indent=4)
         
    print(f"Generated {len(db['Weapons'])} weapons and {len(db['Armor'])} armors.")

if __name__ == "__main__":
    extract_equipment()
