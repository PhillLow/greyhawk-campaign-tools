from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Dict
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassLevel, ClassName
from src.models.background import Background, BackgroundName
from src.models.stats import Stats
from src.models.equipment import Item, Weapon, Armor
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
    exhaustion: int = Field(0, ge=0, le=10) 
    
    # Death Saves
    death_save_successes: int = 0
    death_save_failures: int = 0
    
    # Conditions
    conditions: List[str] = []
    
    # Companions
    companions: List[Minion] = []
    
    @computed_field
    def exhaustion_penalty(self) -> int:
        return -1 * self.exhaustion

    # Inventory
    inventory: List[Item] = []
    
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
    
    @property
    def max_spell_slots(self) -> Dict[int, int]:
        """Calculates max spell slots based on class levels (2024 Multiclass Table)."""
        # Simplified standard progression for full casters
        # Level: [1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th]
        slots_table = {
            1: [2, 0, 0, 0, 0, 0, 0, 0, 0],
            2: [3, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [4, 2, 0, 0, 0, 0, 0, 0, 0],
            4: [4, 3, 0, 0, 0, 0, 0, 0, 0],
            5: [4, 3, 2, 0, 0, 0, 0, 0, 0],
            # ... abbreviated for this task ...
            # I will use a simple formula or partial table for the demo up to lvl 5
            # Real app needs full table.
        }
        
        # Calculate Caster Level
        total_caster_level = 0
        for c in self.classes:
            if c.character_class.name in [ClassName.WIZARD, ClassName.CLERIC, ClassName.DRUID, ClassName.SORCERER, ClassName.BARD, ClassName.CLERIC]:
                total_caster_level += c.level
            elif c.character_class.name in [ClassName.PALADIN, ClassName.RANGER]:
                total_caster_level += c.level // 2
            # Warlock is different (Pact Magic). Handling standard slots first.
            
        # Default fallback
        lvl = max(1, min(5, total_caster_level)) # Cap at 5 for demo table presence
        current_counts = slots_table.get(lvl, [2, 0, 0, 0, 0, 0, 0, 0, 0])
        
        return {i+1: count for i, count in enumerate(current_counts) if count > 0}

    def restore_spell_slots(self):
        """Restores all slots to max."""
        self.current_spell_slots = self.max_spell_slots.copy()
    
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
        """Dex Mod + Bonuses."""
        # TODO: Add Alert feat check
        return self.stats.dexterity.modifier

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
        
        # Find equipped armor
        equipped_armor = next((i for i in self.inventory if isinstance(i, Armor) and i.equipped), None)
        
        if equipped_armor:
            ac = equipped_armor.ac_base
            if equipped_armor.dex_cap is None:
                # Light Armor / No Cap
                ac += dex_mod
            else:
                # Medium/Heavy with Cap
                ac += min(dex_mod, equipped_armor.dex_cap)
            return ac
            
        # Unarmored
        return base_ac + dex_mod

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

        # If Armor, unequip other armor
        if isinstance(item, Armor):
             for i in self.inventory:
                 if isinstance(i, Armor) and i.equipped:
                     i.equipped = False
                     
        item.equipped = True

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
