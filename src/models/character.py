from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Dict, Union
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassLevel, ClassName
from src.models.background import Background, BackgroundName
from src.models.stats import Stats, Ability
from src.models.equipment import Item, Weapon, Armor, ArmorCategory, WeaponProperty
from src.models.spell import Spell
from src.models.feat import Feat

from src.models.transformation import Transformation
from src.models.minion import Minion

class Character(BaseModel):
    name: str = "New Character"
    # level: int = Field(1, ge=1, le=20) # REMOVED, now computed
    species: Species = Species.get_template(SpeciesName.HUMAN)
    
    # Multiclassing Support
    classes: List[ClassLevel] = [] 
    
    # Transformation
    active_transformation: Optional[Transformation] = None
    
    background: Background = Background.get_template(BackgroundName.FARMER)
    
    # Core Stats
    stats: Stats = Stats()
    
    # Features & Feats
    feats: List[Feat] = []
    
    # Skills
    skills: List[str] = []
    
    # Status
    current_hp: int = 10
    max_hp_override: Optional[int] = None
    temp_hp: int = 0
    heroic_inspiration: bool = False
    exhaustion: int = Field(0, ge=0, le=6) # 2024: Max 6 levels
    
    # Hit Dice
    # We store current dice count. Max is based on Level.
    # For now assuming 1 die type per class or using primary. 
    # Real 2024 multiclassing tracks dice BY CLASS.
    # Simplified: store dict {ClassName: count} or simple int for primary.
    # Let's use specific tracking:
    current_hit_dice: Dict[str, int] = Field(default_factory=dict)
    
    # Death Saves
    death_save_successes: int = 0
    death_save_failures: int = 0
    
    # Conditions
    conditions: List[str] = []
    
    # Companions
    companions: List[Minion] = []
    
    @computed_field
    def exhaustion_penalty(self) -> int:
        """2024 Rules: -2 per level."""
        return -2 * self.exhaustion
        
    @computed_field
    def speed_penalty(self) -> int:
        """2024 Rules: -5 ft per level."""
        return -5 * self.exhaustion

    def get_roll_modifier(self, check_type: str = "d20_test") -> int:
        """
        Global modifier for d20 tests (Attacks, Saves, Ability Checks).
        Includes Exhaustion penalty.
        """
        mod = 0
        # Exhaustion applies to ALL d20 tests
        if check_type in ["d20_test", "attack", "save", "check"]:
            mod += self.exhaustion_penalty
        return mod

    # Inventory
    inventory: List[Union[Weapon, Armor, Item]] = []
    
    # Currency
    gp: int = 10
    sp: int = 0
    cp: int = 0
    
    gold: float = 0.0 # Deprecate this one or map it? I'll leave it for now to avoid breakages but 'gp' is better.
    
    # Magic
    spellbook: List[Spell] = [] 
    
    # Slots: {1: 4, 2: 3, ...}
    # We will track CURRENT slots. Max is computed.
    current_spell_slots: Dict[int, int] = Field(default_factory=dict)
    current_pact_slots: int = 0
    
    # Species Spells (Free Casts)
    # Map: Spell Name -> Remaining Uses
    free_casts: Dict[str, int] = Field(default_factory=dict)
    
    @property
    def max_spell_slots(self) -> Dict[int, int]:
        """Calculates max spell slots based on class levels (2024 Multiclass Table)."""
        eff_lvl = 0
        for cl in self.classes:
            name = cl.character_class.name
            if name in [ClassName.BARD, ClassName.CLERIC, ClassName.DRUID, ClassName.SORCERER, ClassName.WIZARD]:
                eff_lvl += cl.level
            elif name in [ClassName.PALADIN, ClassName.RANGER]:
                eff_lvl += (cl.level + 1) // 2 # Round up? 2024 checks needed. 
                # Verification: Paladin/Ranger now get Spellcasting at Lvl 1. 2014 was Lvl 2 (Half, round down).
                # 2024: They are half casters. Lvl 1 = 2 slots? No, Lvl 1 is long rest reset?
                # Actually, simplified: Use (Level+1)//2 for now (Round Up).
                pass
            # Warlock is Pact Magic (Separate)
            
        if eff_lvl == 0:
            return {}
            
        # Standard Slot Table (Full Caster)
        # Level: [1, 2, 3, 4, 5, 6, 7, 8, 9]
        table = [
            [2, 0, 0, 0, 0, 0, 0, 0, 0], # Lvl 1
            [3, 0, 0, 0, 0, 0, 0, 0, 0], # Lvl 2
            [4, 2, 0, 0, 0, 0, 0, 0, 0], # Lvl 3
            [4, 3, 0, 0, 0, 0, 0, 0, 0], # Lvl 4
            [4, 3, 2, 0, 0, 0, 0, 0, 0], # Lvl 5
            [4, 3, 3, 0, 0, 0, 0, 0, 0], # Lvl 6
            [4, 3, 3, 1, 0, 0, 0, 0, 0], # Lvl 7
            [4, 3, 3, 2, 0, 0, 0, 0, 0], # Lvl 8
            [4, 3, 3, 3, 1, 0, 0, 0, 0], # Lvl 9
            [4, 3, 3, 3, 2, 0, 0, 0, 0], # Lvl 10
            [4, 3, 3, 3, 2, 1, 0, 0, 0], # Lvl 11
            [4, 3, 3, 3, 2, 1, 0, 0, 0], # 12
            [4, 3, 3, 3, 2, 1, 1, 0, 0], # 13
            [4, 3, 3, 3, 2, 1, 1, 0, 0], # 14
            [4, 3, 3, 3, 2, 1, 1, 1, 0], # 15
            [4, 3, 3, 3, 2, 1, 1, 1, 0], # 16
            [4, 3, 3, 3, 2, 1, 1, 1, 1], # 17
            [4, 3, 3, 3, 3, 1, 1, 1, 1], # 18
            [4, 3, 3, 3, 3, 2, 1, 1, 1], # 19
            [4, 3, 3, 3, 3, 2, 2, 1, 1], # 20
        ]
        
        idx = min(eff_lvl, 20) - 1
        if idx < 0: return {}
        
        row = table[idx]
        slots = {}
        for i, count in enumerate(row):
            if count > 0:
                slots[i+1] = count
                
        return slots

    @property
    def max_pact_slots(self) -> tuple[int, int]:
        """Returns (slot_level, slot_count) for Warlock."""
        warlock_lvl = sum(c.level for c in self.classes if c.character_class.name == ClassName.WARLOCK)
        if warlock_lvl == 0: return (0, 0)
        
        # 2024 Warlock Table Simplification
        # 1: 1x1, 2: 2x1, 3: 2x2, 4: 2x2, ...
        # Lvl: 11 -> 3x5
        # Slot Level caps at 5.
        
        slot_lvl = 1
        if warlock_lvl >= 9: slot_lvl = 5
        elif warlock_lvl >= 7: slot_lvl = 4
        elif warlock_lvl >= 5: slot_lvl = 3
        elif warlock_lvl >= 3: slot_lvl = 2
        
        count = 1
        if warlock_lvl >= 11: count = 3
        elif warlock_lvl >= 17: count = 4
        elif warlock_lvl >= 2: count = 2
        
        return (slot_lvl, count)

    def restore_spell_slots(self):
        """Restores all slots to max."""
        self.current_spell_slots = self.max_spell_slots.copy()
        # Restore Pact
        _, count = self.max_pact_slots
        self.current_pact_slots = count
        
    def perform_long_rest(self):
        """2024 Long Rest Logic."""
        self.current_hp = self.max_hp
        self.restore_spell_slots()
        
        # Recover Hit Dice (Half of Max, min 1)
        # Simplified: Recover all for now or track max
        # TODO: Implement "Half Max" logic properly scanning classes
        # For now, reset to full for demo simplicity or iterate classes
        for cls in self.classes:
            name = cls.character_class.name.value
            max_hd = cls.level
            current = self.current_hit_dice.get(name, 0)
            regain = max(1, max_hd // 2)
            self.current_hit_dice[name] = min(max_hd, current + regain)

        # Reduce Exhaustion
        if self.exhaustion > 0:
            self.exhaustion -= 1
            
        if self.species.name == SpeciesName.HUMAN:
            self.heroic_inspiration = True
            
        # Reset Free Casts (Species Spells)
        if self.species.free_spells:
            for s in self.species.free_spells:
                if self.level >= s.level_required:
                    self.free_casts[s.name] = s.count
            
    def perform_short_rest(self):
        # 2024: Pact Magic restores on Short Rest
        _, count = self.max_pact_slots
        self.current_pact_slots = count
        # Also Wizard Arcane Recovery etc. (Not implemented yet)
        """Logic for short rest (resetting cooldowns) is mostly per-class."""
        # Warlock slots, Fighter Second Wind etc would go here.
        pass
        
    def roll_hit_die(self, class_name: str = None) -> int:
        """Spends a hit die to heal."""
        if not self.classes: return 0
        
        # Default to primary class if None
        target_cls = None
        if class_name:
             target_cls = next((c for c in self.classes if c.character_class.name.value == class_name), None)
        else:
             target_cls = self.classes[0]
             
        if not target_cls: return 0
        
        cname = target_cls.character_class.name.value
        current = self.current_hit_dice.get(cname, 0)
        
        if current <= 0:
            return 0 # No dice
            
        # Spend
        self.current_hit_dice[cname] = current - 1
        
        # Roll
        import random
        die_size = target_cls.character_class.hit_die
        roll = random.randint(1, die_size)
        con_mod = self.stats.get_mod(Ability.CON) # Use new stats method
        
        heal = max(0, roll + con_mod) # Minimum 0? actually minimum 1 usually in 5e? 
        # 2024 PHB: "roll the die and add your Constitution modifier... regain HP equal to the total (minimum of 0)"
        
        self.current_hp = min(self.max_hp, self.current_hp + heal)
        return heal

    @property
    def grapple_save_dc(self) -> int:
        """2024 Rules: 8 + Str Mod + Prof."""
        # Monk Exception: uses Dex if higher? Need to check Monk specifically
        # For now standard formula
        base = 8
        str_mod = self.stats.get_mod(Ability.STR)
        
        # Monk Exception (2024): Use Dex if higher
        is_monk = any(c.character_class.name == ClassName.MONK for c in self.classes)
        if is_monk:
            dex_mod = self.stats.get_mod(Ability.DEX)
            mod = max(str_mod, dex_mod)
        else:
            mod = str_mod
            
        return base + mod + self.proficiency_bonus
    
    @property
    def level(self) -> int:
        """Total character level."""
        if not self.classes:
            return 1 # Default for new char
        return sum(c.level for c in self.classes)

    @property
    def character_class(self) -> CharacterClass:
        """Primary Class (for backward compat)."""
        if not self.classes:
             # Return a default Fighter if no classes
             return CharacterClass.get_template(ClassName.FIGHTER)
        return self.classes[0].character_class

    @computed_field
    def proficiency_bonus(self) -> int:
        """Calculates PB based on total character level (2024 Rules)."""
        return (self.level - 1) // 4 + 2

    @computed_field
    def max_hp(self) -> int:
        """Dynamic HP Calc for Multiclassing."""
        if self.max_hp_override:
             return self.max_hp_override
             
        if not self.classes:
            return 10 # Default fallback
            
        con_mod = self.stats.constitution.modifier
        total_hp = 0
        
        # Primary Class (Level 1 rules: Max Die)
        primary = self.classes[0]
        # First level of primary class gives Max Die
        total_hp += primary.character_class.hit_die + con_mod
        
        # Remaining levels in Primary
        avg_primary = (primary.character_class.hit_die // 2) + 1
        total_hp += (max(0, avg_primary + con_mod) * (primary.level - 1))
        
        # Secondary Classes (Always Avg Die)
        for cls in self.classes[1:]:
            avg = (cls.character_class.hit_die // 2) + 1
            total_hp += (max(0, avg + con_mod) * cls.level)
            
        return total_hp

    @computed_field
    def initiative(self) -> int:
        """Dex Mod + Bonuses (Modifiers)."""
        base = self.stats.dexterity.modifier
        # Check for Modifiers to "Initiative"
        relevant = [m.value for m in self.stats.modifiers if m.target.lower() == "initiative" and m.type == "bonus"]
        return base + sum(relevant)

    @computed_field
    def speed(self) -> int:
        """Calculates Speed (Species + modifiers - Exhaustion)."""
        base = self.species.speed
        
        # Modifiers
        relevant = [m.value for m in self.stats.modifiers if m.target.lower() == "speed" and m.type == "bonus"]
        
        # Exhaustion
        total = base + sum(relevant) + self.speed_penalty
        return max(5, total) # Minimum 5ft typically

    @computed_field
    def armor_class(self) -> int:
        """Calculates AC. Transformation overrides everything else."""
        # 1. Check Transformation
        if self.active_transformation and self.active_transformation.ac_override:
            return self.active_transformation.ac_override
            
        base_ac = 10
        dex_mod = self.stats.dexterity.modifier
        if self.active_transformation and self.active_transformation.dexterity_score is not None:
             # Recalculate mod locally (simple version)
             dex_mod = (self.active_transformation.dexterity_score - 10) // 2
        
        # Find equipped armor (Body) and Shield
        equipped_armor = next((i for i in self.inventory if isinstance(i, Armor) and i.equipped and i.category != ArmorCategory.SHIELD), None)
        equipped_shield = next((i for i in self.inventory if isinstance(i, Armor) and i.equipped and i.category == ArmorCategory.SHIELD), None)
        
        ac = base_ac
        
        if equipped_armor:
            ac = equipped_armor.ac_base
            if equipped_armor.dex_cap is None:
                # Light Armor / No Cap
                ac += dex_mod
            else:
                # Medium/Heavy with Cap
                ac += min(dex_mod, equipped_armor.dex_cap)
        else:
             # Unarmored Defense Check
             ac = base_ac + dex_mod
             
             # Monk: 10 + Dex + Wis (No Shield)
             # Barbarian: 10 + Dex + Con (Shield OK)
             
             has_monk = any(c.character_class.name == ClassName.MONK for c in self.classes)
             has_barb = any(c.character_class.name == ClassName.BARBARIAN for c in self.classes)
             
             if has_monk and not equipped_shield:
                 wis_mod = self.stats.get_mod(Ability.WIS)
                 monk_ac = 10 + dex_mod + wis_mod
                 ac = max(ac, monk_ac)
                 
             if has_barb: # Shield allowed for Barb
                 con_mod = self.stats.get_mod(Ability.CON)
                 barb_ac = 10 + dex_mod + con_mod
                 ac = max(ac, barb_ac)
             
        # Add Shield
        if equipped_shield:
            ac += equipped_shield.ac_base # usually 2
            
        return ac

    def equip_item(self, item_name: str):
        # Prevent equipping if transformed?
        if self.active_transformation:
            print("Cannot equip items while transformed.")
            return
            
        """Equips an item by name, handling Armor exclusivity."""
        # Find item
        item = next((i for i in self.inventory if i.name == item_name), None)
        if not item:
            return

        # If Armor, unequip other armor of same category group (Body vs Shield)
        if isinstance(item, Armor):
             is_shield = (item.category == ArmorCategory.SHIELD)
             for i in self.inventory:
                 if isinstance(i, Armor) and i.equipped:
                     # Check conflict
                     other_is_shield = (i.category == ArmorCategory.SHIELD)
                     
                     if is_shield and other_is_shield:
                         i.equipped = False # Replace Shield
                     elif not is_shield and not other_is_shield:
                         i.equipped = False # Replace Body Armor
                      
        item.equipped = True

    def get_equipped_weapons(self) -> List[Weapon]:
        return [i for i in self.inventory if isinstance(i, Weapon) and i.equipped]

    def calculate_attack_roll(self, weapon: Weapon) -> int:
        """Calculates 'To Hit' bonus."""
        # 1. Ability Mod
        str_mod = self.stats.get_mod(Ability.STR)
        dex_mod = self.stats.get_mod(Ability.DEX)
        
        mod = str_mod
        if WeaponProperty.FINESSE in weapon.properties:
            mod = max(str_mod, dex_mod)
        elif weapon.range_normal > 5 and WeaponProperty.THROWN not in weapon.properties:
             # Ranged weapons (bows) use Dex
             mod = dex_mod
             
        # 2. Proficiency
        # Simplification: Assume proficient if Class allows. 
        # For now, just ADD prof bonus for all.
        mod += self.proficiency_bonus
        
        # 3. Global Modifiers (Exhaustion, Bless, Magic Items)
        mod += self.get_roll_modifier("attack")
        
        # 4. Conditions (Return tuple? Or just handle Advantage/Disadvantage elsewhere?)
        # Since this method returns an INT (bonus), we cannot easily return "Advantage" state here 
        # without changing signature.
        # However, we can simply NOTE it in a printed listing or handle it in the UI.
        # But for 'bonus', some conditions might apply e.g. -2?
        # 2024: Exhaustion is already handled (-2 per level).
        # Prone/Poisoned/Invisible affects 'Advantage/Disadvantage', not the flat number.
        # So we won't change the number here.
        # We will add a helper `get_advantage_state(check_type)`?
        
        return mod

    def get_advantage_state(self, check_type: str = "attack") -> str:
        """Returns 'advantage', 'disadvantage', or 'normal'."""
        adv = 0
        if check_type == "attack":
            if "Invisible" in self.conditions: adv += 1
            if "Poisoned" in self.conditions: adv -= 1
            if "Prone" in self.conditions: adv -= 1
            if "Restrained" in self.conditions: adv -= 1
            
        if adv > 0: return "advantage"
        if adv < 0: return "disadvantage"
        return "normal"
        
    def calculate_damage_roll(self, weapon: Weapon, offhand: bool = False) -> int:
        """Calculates Damage Bonus."""
        # 1. Ability Mod
        str_mod = self.stats.get_mod(Ability.STR)
        dex_mod = self.stats.get_mod(Ability.DEX)
        
        stat_bonus = str_mod
        if WeaponProperty.FINESSE in weapon.properties:
            stat_bonus = max(str_mod, dex_mod)
        elif weapon.range_normal > 5 and WeaponProperty.THROWN not in weapon.properties:
             stat_bonus = dex_mod
             
        # Offhand logic (negative logic: remove stat bonus unless negative?)
        if offhand:
             # Normal dual wielding: No stat bonus to damage (unless negative)
             # Fighting Style "Two-Weapon Fighting" allows it. (Not tracked yet)
             # Simplification: if offhand, bonus is min(0, stat_bonus). 
             if stat_bonus > 0:
                 stat_bonus = 0
                 
        # 2. Magic Bonus (TODO: Check if weapon is +1 etc)
        magic_bonus = 0
        
        # 3. Global Damage Modifiers (e.g. Rage)
        global_dmg = 0
        # TODO: Scan modifiers for "damage" target
             
        return stat_bonus + magic_bonus + global_dmg

    def toggle_transformation(self, trans: Transformation):
        if self.active_transformation:
            # Revert
            self.active_transformation = None
        else:
            # Apply
            self.active_transformation = trans
            # Apply HP effects
            if trans.replaces_hp:
                # Polymorph style: swap HP (TODO: save original HP)
                # For simplified CLI, just set Temp HP
                pass
            if trans.hp_value > 0:
                self.temp_hp = trans.hp_value

    def unequip_item(self, item_name: str):
        item = next((i for i in self.inventory if i.name == item_name), None)
        if item:
            item.equipped = False
