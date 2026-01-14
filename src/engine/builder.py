import questionary
from src.models.character import Character
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassName
from src.models.background import Background, BackgroundName
from src.models.feat import FeatDatabase
from rich.console import Console

console = Console()

class CharacterBuilder:
    def __init__(self):
        self.character = Character()

    def run_cli_flow(self) -> Character:
        """Runs the interactive CLI to build a character."""
        console.print("[bold green]Welcome to the D&D 2024 Character Builder[/bold green]")
        
        # 1. Name
        self.character.name = questionary.text("What is your character's name?").ask()
        
        # 2. Species
        species_choice = questionary.select(
            "Select your Species:",
            choices=[s.value for s in SpeciesName]
        ).ask()
        self.character.species = Species.get_template(SpeciesName(species_choice))
        
        # 3. Class (Primary)
        class_choice = questionary.select(
            "Select your Class:",
            choices=[c.value for c in ClassName]
        ).ask()
        
        from src.models.class_model import ClassLevel
        primary_class_template = CharacterClass.get_template(ClassName(class_choice))
        self.character.classes = [ClassLevel(character_class=primary_class_template, level=1)]
        
        # 4. Background (2024 Rules)
        bg_choice = questionary.select(
            "Select your Background:",
            choices=[b.value for b in BackgroundName]
        ).ask()
        self.character.background = Background.get_template(BackgroundName(bg_choice))
        # Grant Origin Feat
        origin_feat = FeatDatabase.get_feat(self.character.background.origin_feat)
        if origin_feat:
            self.character.feats.append(origin_feat)
        
        # Grant Background Skills
        self.character.skills.extend(self.character.background.skills)
        console.print(f"[dim]Background grants: {self.character.background.origin_feat} feat and Skills: {', '.join(self.character.background.skills)}[/dim]")
        
        # 4b. Class Skills
        cls_def = primary_class_template
        avail_skills = [s for s in cls_def.skill_choices if s not in self.character.skills]
        
        if avail_skills:
            num = cls_def.num_skills
            console.print(f"\n[bold]Select {num} Class Skills:[/bold]")
            s_choices = questionary.checkbox(
                "Skills:",
                choices=avail_skills,
                validate=lambda c: True if len(c) == num else f"Please select exactly {num} skills."
            ).ask()
            self.character.skills.extend(s_choices)
        
        # 5. Core Stats (Manual + Background Bonus)
        console.print("\n[bold]Roll for Stats! (Manual Entry)[/bold]")
        stats_map = {
            "str": "strength", "dex": "dexterity", "con": "constitution",
            "int": "intelligence", "wis": "wisdom", "cha": "charisma"
        }
        for short, full in stats_map.items():
            val = questionary.text(
                f"Enter {full.title()} score:",
                validate=lambda text: text.isdigit() and 1 <= int(text) <= 30
            ).ask()
            getattr(self.character.stats, full).score = int(val)

        # 6. Spell Selection (if caster)
        # Check primary class
        primary_cls_name = self.character.character_class.name
        # Simple list of caster classes for CLI flow
        casters = [ClassName.WIZARD, ClassName.CLERIC, ClassName.DRUID, ClassName.BARD, ClassName.SORCERER, ClassName.WARLOCK]
        
        if primary_cls_name in casters:
            console.print(f"\n[bold purple]Select Starting Spells for {primary_cls_name.value}[/bold purple]")
            from src.models.spell_database import SpellDatabase
            
            # Cantrips
            # Rule of thumb: 3 Cantrips at lvl 1 (varies, but simple for now)
            cantrips_avail = SpellDatabase.get_available_spells(primary_cls_name, level=0)
            if cantrips_avail:
                cantrip_names = [s.name for s in cantrips_avail]
                choices = questionary.checkbox(
                    "Select 3 Cantrips:",
                    choices=cantrip_names,
                    validate=lambda c: True if len(c) <= 3 else "Select at most 3 cantrips."
                ).ask()
                for name in choices:
                    s = SpellDatabase.get_spell(name)
                    if s: self.character.spellbook.append(s)
            
            # Level 1 Spells
            # Wizard: 6 in book. Cleric: All prepared? 
            # Simplified: Select 4 to start.
            lvl1_avail = SpellDatabase.get_available_spells(primary_cls_name, level=1)
            if lvl1_avail:
                l1_names = [s.name for s in lvl1_avail]
                choices = questionary.checkbox(
                    "Select up to 6 Level 1 Spells:",
                    choices=l1_names,
                    validate=lambda c: True if len(c) <= 6 else "Max 6 spells."
                ).ask()
                for name in choices:
                    s = SpellDatabase.get_spell(name)
                    if s: self.character.spellbook.append(s)
                    
            console.print(f"[green]Added {len(self.character.spellbook)} spells to spellbook.[/green]")

        console.print("[bold blue]Character Created![/bold blue]")
        return self.character
