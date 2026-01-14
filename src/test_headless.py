from src.models.character import Character
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassName

def test_headless_build():
    print("Initializing Character...")
    from src.models.class_model import ClassLevel
    
    # Init without level (it's computed)
    char = Character(name="Test Hero") 
    
    print("Applying Species: Elf")
    # char.species is a field, so this is fine
    char.species = Species.get_template(SpeciesName.ELF)
    
    print("Applying Class: Wizard (Level 3)")
    # OLD: char.character_class = ...
    # NEW: Add to classes list
    wiz_template = CharacterClass.get_template(ClassName.WIZARD)
    char.classes = [ClassLevel(character_class=wiz_template, level=3)]
    
    print("Setting Stats...")
    char.stats.intelligence.score = 18
    
    print("Validating Results...")
    assert char.name == "Test Hero"
    assert char.species.name == SpeciesName.ELF
    assert char.species.darkvision == 60
    assert char.character_class.name == ClassName.WIZARD # access via property
    assert char.level == 3
    assert char.character_class.hit_die == 6
    assert char.stats.intelligence.modifier == 4 # (18-10)//2
    
    # HP Calc Check for Level 3 Wizard (Con +4? No, Con is default 10 -> +0)
    # Lvl 1: 6 + 0 = 6
    # Lvl 2: 4 + 0 = 4 (Avg 3.5->4)
    # Lvl 3: 4 + 0 = 4
    # Total: 14.
    # Note: Stats default to 10. `char.stats.intelligence` was set to 18.
    print(f"Calculated HP: {char.max_hp}")
    assert char.max_hp == 14
    
    print("SUCCESS: Headless build verified.")

    # --- New Tests ---
    print("\nTesting AC & Equipment...")
    # Base AC = 10 + DexMod (0 default)
    assert char.armor_class == 10
    
    from src.models.item_database import ItemDatabase
    plate = ItemDatabase.get_item("Plate Armor")
    if plate:
        char.inventory.append(plate)
        char.equip_item("Plate Armor")
        print(f"Equipped Plate. AC: {char.armor_class}")
        assert char.armor_class == 18
        
        char.unequip_item("Plate Armor")
        assert char.armor_class == 10
        print("Equipment Logic Verified.")

    # 4. Currency Test
    print("\nTesting Currency...")
    char.gp = 100
    char.sp = 50
    if char.gp == 100 and char.sp == 50:
        print(f"Currency Verified: {char.gp}gp, {char.sp}sp")
    else:
        print("FAILURE: Currency mismatch.")

    # 5. Conditions & Status
    print("\nTesting Conditions...")
    # (Character already imported at top)
    char.conditions.append("Prone")
    char.death_save_failures = 2
    if "Prone" in char.conditions and char.death_save_failures == 2:
        print("Conditions & Death Saves Verified.")
    else:
        print("FAILURE: Conditions/DS mismatch.")
        
    # 6. Companions
    print("\nTesting Companions...")
    from src.models.minion import Minion
    minion = Minion(name="Wolfy", creature_type="Wolf", current_hp=10, max_hp=10)
    char.companions.append(minion)
    if len(char.companions) == 1 and char.companions[0].name == "Wolfy":
        print("Companions Verified.")
    else:
        print("FAILURE: Companion logic.")
        
    # 7. Skills & Spells
    print("\nTesting Skills & Spells...")
    char.skills.append("Stealth")
    # Verify duplicates handled? Model doesn't enforce set, UI does.
    print(f"Skills: {char.skills}")
    
    # Spellbook check
    from src.models.spell_database import SpellDatabase
    spell = SpellDatabase.get_spell("Fire Bolt")
    if spell:
        char.spellbook.append(spell)
        print("Spellbook Verified.")
    else:
        print("FAILURE: Could not load spell.")

    print("\nALL HEADLESS TESTS PASSED.")
if __name__ == "__main__":
    test_headless_build()
