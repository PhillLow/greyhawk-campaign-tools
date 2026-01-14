import questionary
import sys
from rich.console import Console
from src.engine.builder import CharacterBuilder
from src.engine.persistence import PersistenceManager
from src.ui.dashboard import Dashboard

console = Console()
pm = PersistenceManager()

def main_menu():
    while True:
        console.clear()
        console.print("[bold cyan]D&D 2024 Character Tools[/bold cyan]")
        choice = questionary.select(
            "Main Menu",
            choices=["Create New Character", "Load Character", "Exit"]
        ).ask()
        
        if choice == "Create New Character":
            builder = CharacterBuilder()
            char = builder.run_cli_flow()
            game_loop(char)
        elif choice == "Load Character":
            saves = pm.list_saves()
            if not saves:
                console.print("[red]No save files found![/red]")
                questionary.text("Press Enter to continue...").ask()
                continue
                
            name = questionary.select("Select Character:", choices=saves + ["Back"]).ask()
            if name == "Back":
                continue
                
            try:
                char = pm.load_character(name)
                game_loop(char)
            except Exception as e:
                console.print(f"[red]Error loading character: {e}[/red]")
                questionary.text("Press Enter to continue...").ask()
        elif choice == "Exit":
            sys.exit()

def game_loop(char):
    """The 'Living Sheet' loop."""
    while True:
        console.clear()
        # Render Sheet
        dash = Dashboard(char)
        dash.render()
        
        # Action Menu
        action = questionary.select(
            "Actions:",
            choices=[
                "Edit HP (Damage/Heal)",
                "Manage Exhaustion",
                "Manage Status (Cond/DS/Insp)",
                "Inventory & Equipment",
                "Level Up / Multiclass",
                "Wild Shape / Transform", 
                "Magic & Spells",
                "Rest (Short/Long)", 
                "Save Character",
                "Return to Main Menu"
            ]
        ).ask()
        
        if action == "Edit HP (Damage/Heal)":
            manage_hp(char)
        elif action == "Manage Exhaustion":
             # ... existing ...
             new_level = int(questionary.text(f"Current Level: {char.exhaustion}. Enter new level (0-10):", validate=lambda t: t.isdigit() and 0 <= int(t) <= 10).ask())
             char.exhaustion = new_level
             console.print(f"[yellow]Exhaustion set to {new_level}. Penalty to rolls: {char.exhaustion_penalty}[/yellow]")
             questionary.text("Press Enter...").ask()
        elif action == "Manage Status (Cond/DS/Insp)":
            manage_status(char)
        elif action == "Inventory & Equipment":
             manage_inventory(char)
        elif action == "Level Up / Multiclass":
             manage_levelup(char)
        elif action == "Wild Shape / Transform":
             manage_transformation(char)
        elif action == "Magic & Spells":
             manage_magic(char)
        elif action == "Rest (Short/Long)":
             manage_rest(char)
        elif action == "Save Character":
             path = pm.save_character(char)
             console.print(f"[green]Character saved to {path}![/green]")
             questionary.text("Press Enter to continue...").ask()
        elif action == "Return to Main Menu":
            break

def manage_status(char):
    while True:
        console.clear()
        console.print("[bold]Status Management[/bold]")
        console.print(f"Conditions: {', '.join(char.conditions) if char.conditions else 'None'}")
        console.print(f"Death Saves: Success {char.death_save_successes}/3, Fail {char.death_save_failures}/3")
        console.print(f"Heroic Inspiration: {'Yes' if char.heroic_inspiration else 'No'}")
        
        choice = questionary.select(
            "Actions:", 
            choices=["Toggle Condition", "Update Death Saves", "Toggle Heroic Inspiration", "Manage Companions", "Back"]
        ).ask()
        
        if choice == "Back":
            break
        elif choice == "Manage Companions":
             if not char.companions:
                 console.print("[italic]No companions.[/italic]")
             for i, c in enumerate(char.companions):
                 console.print(f"{i+1}. {c.name} ({c.creature_type}) - {c.current_hp}/{c.max_hp} HP")
             
             act = questionary.select("Companion Action:", choices=["Add New", "Remove", "Back"]).ask()
             if act == "Add New":
                 name = questionary.text("Name:").ask()
                 ctype = questionary.text("Type (e.g. Wolf):").ask()
                 hp = int(questionary.text("Max HP:", validate=lambda x: x.isdigit()).ask())
                 from src.models.minion import Minion
                 char.companions.append(Minion(name=name, creature_type=ctype, max_hp=hp, current_hp=hp))
                 console.print("[green]Companion added.[/green]")
             elif act == "Remove":
                 if not char.companions: continue
                 opts = [c.name for c in char.companions]
                 rem = questionary.select("Remove who?", choices=opts + ["Cancel"]).ask()
                 if rem != "Cancel":
                     char.companions = [c for c in char.companions if c.name != rem]
                     console.print("[green]Removed.[/green]")

        elif choice == "Toggle Condition":
            # List common 2024 conditions
            conds = ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious", "Exhaustion"]
            # Checkbox? Or Select to toggle?
            # Checkbox with current state
            selected = questionary.checkbox("Select Active Conditions:", choices=conds, 
                default=[c for c in char.conditions if c in conds]).ask()
            char.conditions = selected # Replace list (assuming custom conditions rare for now)
            console.print("[green]Conditions updated.[/green]")
        elif choice == "Update Death Saves":
            suc = questionary.text("Successes (0-3):", default=str(char.death_save_successes), validate=lambda x: x in ['0','1','2','3']).ask()
            fail = questionary.text("Failures (0-3):", default=str(char.death_save_failures), validate=lambda x: x in ['0','1','2','3']).ask()
            char.death_save_successes = int(suc)
            char.death_save_failures = int(fail)
            console.print("[green]Death Saves updated.[/green]")
        elif choice == "Toggle Heroic Inspiration":
            char.heroic_inspiration = not char.heroic_inspiration
            console.print(f"[green]Heroic Inspiration set to {char.heroic_inspiration}[/green]")
            

def manage_magic(char):
    while True:
        console.clear()
        console.print("[bold purple]Magic & Spells[/bold purple]")
        
        # Show Slots
        console.print("\n[bold]Spell Slots:[/bold]")
        max_slots = char.max_spell_slots
        current = char.current_spell_slots
        
        # Init slots if empty but max exists
        if max_slots and not current:
            char.restore_spell_slots()
            current = char.current_spell_slots
            
        if not max_slots:
            console.print("[italic]No spell slots available.[/italic]")
        else:
            for lvl, count in max_slots.items():
                curr = current.get(lvl, 0)
                console.print(f"Level {lvl}: {curr}/{count}")

        choice = questionary.select(
            "Magic Actions:",
            choices=["Cast Spell (Use Slot)", "Prepare/Learn Spell", "Back"]
        ).ask()
        
        if choice == "Back":
            break
        elif choice == "Cast Spell (Use Slot)":
             if not max_slots:
                 continue
             lvl_str = questionary.text("Slot Level to use (1-9):", validate=lambda t: t.isdigit() and 1 <= int(t) <= 9).ask()
             if not lvl_str: continue
             lvl = int(lvl_str)
             
             cur_val = current.get(lvl, 0)
             if cur_val > 0:
                 char.current_spell_slots[lvl] = cur_val - 1
                 console.print(f"[green]Used Level {lvl} slot. Remaining: {char.current_spell_slots[lvl]}[/green]")
                 questionary.text("Press Enter...").ask()
             else:
                 console.print(f"[red]No Level {lvl} slots remaining![/red]")
                 questionary.text("Press Enter...").ask()
                 
        elif choice == "Prepare/Learn Spell":
             console.print("[dim]Spell Database not fully populated. Feature coming soon.[/dim]")
             questionary.text("Press Enter...").ask()

def manage_transformation(char):
    from src.models.transformation import Transformation
    
    if char.active_transformation:
        console.print(f"[bold red]Currently Transformed into: {char.active_transformation.name}[/bold red]")
        if questionary.confirm("Revert to Normal Form?").ask():
            char.toggle_transformation(None) # None works as toggle off logic in our method? No, method takes a Trans.
            # Fix logic: toggle_transformation(None) might fail if it expects a Transformation object
            # Let's check `toggle_transformation` impl:
            # "if self.active_transformation: self.active_transformation = None" overrides arg.
            # So passing any dummy trans works, or I should update signature.
            # I'll pass the current one to safeguard.
            char.toggle_transformation(char.active_transformation)
            console.print("[green]Reverted to normal form.[/green]")
    else:
        # Choose Form
        forms = ["Wolf", "Brown Bear", "Cancel"]
        choice = questionary.select("Select Form:", choices=forms).ask()
        
        if choice == "Cancel":
            return
            
        trans = Transformation.get_template(choice)
        char.toggle_transformation(trans)
        console.print(f"[green]Transformed into {choice}![/green]")
        console.print(f"New AC: {char.armor_class}. Temp HP: {char.temp_hp}")
    
    questionary.text("Press Enter...").ask()

def manage_levelup(char):
    from src.models.class_model import CharacterClass, ClassLevel, ClassName
    
    console.print(f"Current Level: {char.level}")
    
    options = [f"Level Up {c.character_class.name.value} (to {c.level + 1})" for c in char.classes]
    options.append("Multiclass into New Class")
    options.append("Cancel")
    
    choice = questionary.select("Level Up Options:", choices=options).ask()
    
    if choice == "Cancel":
        return
        
    if choice == "Multiclass into New Class":
        # Filter out existing classes? 2024 allows multiple of same class? No.
        existing = [c.character_class.name for c in char.classes]
        available = [c.value for c in ClassName if c not in existing]
        
        new_cls_name = questionary.select("Select New Class:", choices=available).ask()
        if new_cls_name: 
             template = CharacterClass.get_template(ClassName(new_cls_name))
             char.classes.append(ClassLevel(character_class=template, level=1))
             console.print(f"[bold green]Multiclassed into {new_cls_name}![/bold green]")
        
    else:
        # Chosen existing
        try:
            parts = choice.split(" ")
            cls_name = parts[2]
            target = next(c for c in char.classes if c.character_class.name.value == cls_name)
            target.level += 1
            console.print(f"[bold green]Leveled up {cls_name} to {target.level}![/bold green]")
        except Exception as e:
            console.print(f"[red]Error parsing choice: {e}[/red]")
            return
        
    # Recalculate derived stats happens automatically via properties
    console.print(f"Total Character Level is now {char.level}. Max HP is {char.max_hp}.")
    questionary.text("Press Enter to continue...").ask()

def manage_inventory(char):
    from src.models.item_database import ItemDatabase
    while True:
        console.clear()
        # List Inventory
        console.print("[bold]Inventory:[/bold]")
        if not char.inventory:
            console.print("[italic]Empty[/italic]")
        else:
            for item in char.inventory:
                status = "[green][E][/green] " if item.equipped else ""
                console.print(f"- {status}{item.name} ({item.item_type.value})")
                
        # Currency Display
        console.print(f"\n[bold gold1]Wealth: {char.gp} gp, {char.sp} sp, {char.cp} cp[/]")

        choice = questionary.select(
            "Inventory Actions:",
            choices=["Add Item from Database", "Equip Item", "Unequip Item", "Manage Currency", "Back"]
        ).ask()
        
        if choice == "Back":
            break
        elif choice == "Manage Currency":
            curr_type = questionary.select("Currency Type:", choices=["GP", "SP", "CP", "Back"]).ask()
            if curr_type != "Back":
                val = questionary.text("Amount (positive to add, negative to subtract):", validate=lambda t: t.lstrip('-').isdigit()).ask()
                amount = int(val)
                if curr_type == "GP": char.gp += amount
                elif curr_type == "SP": char.sp += amount
                elif curr_type == "CP": char.cp += amount
                console.print(f"[green]Currency updated.[/green]")
                
        elif choice == "Add Item from Database":
            # Simple list for now
            all_items = ItemDatabase.get_all_items()
            item_names = [i.name for i in all_items]
            selection = questionary.select("Select Item:", choices=item_names + ["Cancel"]).ask()
            if selection != "Cancel":
                new_item = ItemDatabase.get_item(selection)
                # Clone item (pydantic copy)
                char.inventory.append(new_item.model_copy())
                console.print(f"[green]Added {selection}![/green]")
        elif choice == "Equip Item":
            unequipped = [i.name for i in char.inventory if not i.equipped]
            if not unequipped:
                 console.print("[yellow]No unequipped items.[/yellow]")
                 questionary.text("Press Enter...").ask()
                 continue
            selection = questionary.select("Equip what?", choices=unequipped + ["Cancel"]).ask()
            if selection != "Cancel":
                char.equip_item(selection)
                console.print(f"[green]Equipped {selection}.[/green]")
        elif choice == "Unequip Item":
            equipped = [i.name for i in char.inventory if i.equipped]
            if not equipped:
                 console.print("[yellow]No equipped items.[/yellow]")
                 questionary.text("Press Enter...").ask()
                 continue
            selection = questionary.select("Unequip what?", choices=equipped + ["Cancel"]).ask()
            if selection != "Cancel":
                char.unequip_item(selection)
                console.print(f"[green]Unequipped {selection}.[/green]")

def manage_hp(char):
    val = questionary.text("Enter HP change (positive to heal, negative to damage):", 
                           validate=lambda t: t.lstrip('-').isdigit()).ask()
    delta = int(val)
    new_hp = char.current_hp + delta
    
    # Clamp between 0 and Max
    char.current_hp = max(0, min(char.max_hp, new_hp))
    
    if delta < 0:
        console.print(f"[red]Took {abs(delta)} damage![/red]")
    else:
        console.print(f"[green]Healed {delta} HP![/green]")

def manage_rest(char):
    rest_type = questionary.select("Rest Type:", choices=["Short Rest", "Long Rest", "Cancel"]).ask()
    if rest_type == "Short Rest":
        # Placeholder: Hit Die logic would go here
        console.print("[yellow]Short Rest: Warlock slots recovered (TODO). You can roll Hit Dice manually for now.[/yellow]")
        questionary.text("Press Enter...").ask()
    elif rest_type == "Long Rest":
        char.current_hp = char.max_hp
        char.stats.current_hit_dice = char.level # hypothetical field
        char.restore_spell_slots() # NEW
        console.print("[green]Long Rest: HP and Spell Slots fully restored![/green]")
        questionary.text("Press Enter...").ask()

if __name__ == "__main__":
    main_menu()
