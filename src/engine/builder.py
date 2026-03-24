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

    def _handle_feat_selection(self, feat_name: str):
        """Checks if a feat requires sub-selection (like Magic Initiate) and prompts user."""
        if "Magic Initiate" in feat_name:
            # Format: "Magic Initiate (Class)" or just "Magic Initiate"
            # Extract class
            target_cls = None
            if "(" in feat_name:
                target_cls = feat_name.split("(")[1].replace(")", "")
            else:
                # Prompt if generic? 2024 usually specifies.
                # If undefined, ask user.
                # For now assume defined or fallback.
                pass
                
            if target_cls:
                console.print(f"\n[bold purple]Magic Initiate ({target_cls}): Select Spells[/bold purple]")
                from src.models.spell_database import SpellDatabase
                from src.models.class_model import ClassName
                
                try:
                    c_enum = ClassName(target_cls)
                    
                    # 2 Cantrips
                    cantrips = SpellDatabase.get_available_spells(c_enum, level=0)
                    c_names = [s.name for s in cantrips]
                    c_choice = questionary.checkbox(
                        f"Select 2 {target_cls} Cantrips:",
                        choices=c_names,
                        validate=lambda c: True if len(c) == 2 else "Select exactly 2."
                    ).ask()
                    
                    for n in c_choice:
                        s = SpellDatabase.get_spell(n)
                        if s: self.character.spellbook.append(s)
                        
                    # 1 Level 1 Spell
                    lvl1 = SpellDatabase.get_available_spells(c_enum, level=1)
                    l1_names = [s.name for s in lvl1]
                    l1_choice = questionary.select(
                        f"Select 1 Level 1 {target_cls} Spell:",
                        choices=l1_names
                    ).ask()
                    
                    s_l1 = SpellDatabase.get_spell(l1_choice)
                    if s_l1:
                        self.character.spellbook.append(s_l1)
                        # Add Free Cast
                        self.character.free_casts[s_l1.name] = 1
                        console.print(f"[green]Learned {l1_choice} (Free Cast x1/LR) and cantrips.[/green]")
                        
                except ValueError:
                    console.print(f"[yellow]Could not parse class {target_cls} for Magic Initiate.[/yellow]")

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
        
        # 2a. Lineage / Legacy Selection
        if self.character.species.lineages:
            lineage_choice = questionary.select(
                f"Choose your {self.character.species.name.value} Lineage/Ancestry/Legacy:",
                choices=list(self.character.species.lineages.keys())
            ).ask()
            self.character.species.apply_lineage(lineage_choice)
            console.print(f"[green]Applied {lineage_choice} traits.[/green]")
        
        # 2b. Human Bonus Feat
        if self.character.species.name == SpeciesName.HUMAN:
            console.print("\n[bold]Human Heritage:[/bold] You get one additional Origin Feat.")
            all_origin = [f for f in FeatDatabase.get_origin_feats()] # Assuming we want to show all to pick from
            # Exclude background ones? Not necessarily, but duplicates are usually wasted.
            origin_names = [f.name for f in all_origin]
            
            human_feat_choice = questionary.select(
                "Select Bonus Origin Feat:",
                choices=origin_names
            ).ask()
            
            feat = FeatDatabase.get_feat(human_feat_choice)
            if feat:
                self.character.feats.append(feat)
                console.print(f"[green]Added Human Bonus Feat: {feat.name}[/green]")
                self._handle_feat_selection(feat.name)
        
        # 3. Class (Primary)
        class_choice = questionary.select(
            "Select your Class:",
            choices=[c.value for c in ClassName]
        ).ask()
        
        from src.models.class_model import ClassLevel
        primary_class_template = CharacterClass.get_template(ClassName(class_choice))
        self.character.classes = [ClassLevel(character_class=primary_class_template.model_dump(), level=1)]
        
        # 4. Background (2024 Rules)
        bg_choice = questionary.select(
            "Select your Background:",
            choices=[b.value for b in BackgroundName]
        ).ask()
        self.character.background = Background.get_template(BackgroundName(bg_choice))
        # Grant Origin Feat
        # Logic to handle "Magic Initiate (Wizard)" etc.
        feat_name_full = self.character.background.origin_feat
        origin_feat = FeatDatabase.get_feat(feat_name_full)
        
        # If not found, try splitting (e.g. "Magic Initiate (Wizard)" -> "Magic Initiate")
        if not origin_feat and "(" in feat_name_full:
            base_name = feat_name_full.split("(")[0].strip()
            origin_feat = FeatDatabase.get_feat(base_name)
            
        if origin_feat:
            # We add the generic feat object, but we trigger selection with the FULL name
            # So the handler knows which class to pick for Magic Initiate
            # Ideally we'd rename the feat instance to the full name too for the sheet.
            feat_clone = origin_feat.model_copy()
            feat_clone.name = feat_name_full # Update name to be specific
            
            self.character.feats.append(feat_clone)
            self._handle_feat_selection(feat_name_full)
        
        # Grant Background Skills
        self.character.skills.extend(self.character.background.skills)
        console.print(f"[dim]Background grants: {self.character.background.origin_feat} feat and Skills: {', '.join(self.character.background.skills)}[/dim]")
        
        # 4b. Class Features (Fighting Style)
        # Check if primary class has Fighting Style
        cls_def = primary_class_template
        fs_feature = next((f for f in cls_def.features if f.name == "Fighting Style"), None)
        if fs_feature:
            console.print("\n[bold]Class Feature: Fighting Style[/bold]")
            styles = FeatDatabase.get_fighting_style_feats()
            style_names = [s.name for s in styles]
            
            fs_choice = questionary.select(
                "Choose your Fighting Style:",
                choices=style_names
            ).ask()
            
            fs_feat = FeatDatabase.get_feat(fs_choice)
            if fs_feat:
                self.character.feats.append(fs_feat)
                console.print(f"[green]Added Fighting Style: {fs_feat.name}[/green]")
        
        # 4c. Weapon Mastery Selection
        if cls_def.num_weapon_masteries > 0:
            console.print(f"\n[bold]Weapon Mastery[/bold]: Select {cls_def.num_weapon_masteries} weapons to master.")
            from src.models.item_database import ItemDatabase
            # Show all weapons or filter?
            # 2024: "You choose... from the weapons in the Equipment chapter"
            # We'll just list all weapons in our DB.
            all_weapons = [i for i in ItemDatabase.get_all_items() if i.item_type.value == "Weapon"]
            # Unique names
            w_names = sorted(list(set(w.name for w in all_weapons)))
            
            mastery_choices = questionary.checkbox(
                f"Select {cls_def.num_weapon_masteries} Weapons:",
                choices=w_names,
                validate=lambda c: True if len(c) == cls_def.num_weapon_masteries else f"Please select exactly {cls_def.num_weapon_masteries} weapons."
            ).ask()
            
            self.character.weapon_masteries.extend(mastery_choices)
            console.print(f"[green]Masteries learned: {', '.join(mastery_choices)}[/green]")
        
        # 4d. Class Skills
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
        
        # 5. Core Stats (Point Buy / Standard / Manual)
        console.print("\n[bold]Ability Scores[/bold]")
        method = questionary.select("Choose Generation Method:", choices=["Point Buy (27 pts)", "Standard Array (15,14,13,12,10,8)", "Manual Entry"]).ask()
        
        from src.models.stats import Ability
        base_scores = {a: 8 for a in Ability}
        
        if method == "Manual Entry":
            stats_map = {
                "str": Ability.STR, "dex": Ability.DEX, "con": Ability.CON,
                "int": Ability.INT, "wis": Ability.WIS, "cha": Ability.CHA
            }
            for short, enum_val in stats_map.items():
                val = questionary.text(
                    f"Enter {enum_val.value} score:",
                    validate=lambda text: text.isdigit() and 1 <= int(text) <= 30
                ).ask()
                self.character.stats.get(enum_val).score = int(val)
                
        elif method == "Standard Array (15,14,13,12,10,8)":
            array = [15, 14, 13, 12, 10, 8]
            for ability in Ability:
                val = int(questionary.select(
                    f"Assign score for {ability.value}:",
                    choices=[str(x) for x in array]
                ).ask())
                self.character.stats.get(ability).score = val
                array.remove(val)
                
        elif method == "Point Buy (27 pts)":
            points = 27
            scores = {a: 8 for a in Ability}
            costs = {8:0, 9:1, 10:2, 11:3, 12:4, 13:5, 14:7, 15:9}
            
            while points > 0:
                console.clear()
                console.print(f"Points Remaining: [bold cyan]{points}[/bold cyan]")
                for a, s in scores.items():
                    console.print(f"{a.value}: {s}")
                
                # Check which can still be improved
                opts = []
                for a in Ability:
                    curr = scores[a]
                    if curr < 15:
                        cost_diff = costs[curr+1] - costs[curr]
                        if points >= cost_diff:
                            opts.append(f"{a.value} (+1, cost {cost_diff})")
                
                if not opts:
                    console.print("[yellow]No more increases possible.[/yellow]")
                    break
                    
                opts.append("Finish")
                
                choice = questionary.select("Upgrade Ability:", choices=opts).ask()
                if choice == "Finish": 
                    break
                
                # Apply
                target_name = choice.split(" ")[0] # "Strength"
                target_enum = next(a for a in Ability if a.value == target_name)
                curr = scores[target_enum]
                cost = costs[curr+1] - costs[curr]
                scores[target_enum] += 1
                points -= cost
            
            # Save to character
            for a, s in scores.items():
                self.character.stats.get(a).score = s

        # 6. Background ASI (2024 Rules)
        console.print("\n[bold]Background Ability Adjustments[/bold]")
        allowed = self.character.background.ability_scores # List[Ability]
        allowed_names = [a.value for a in allowed]
        
        console.print(f"Background {self.character.background.name.value} allows boosting: {', '.join(allowed_names)}")
        
        asi_choice = questionary.select(
            "Select ASI Pattern:",
            choices=["+2 to One, +1 to Another", "+1 to Three"]
        ).ask()
        
        from src.models.modifier import Modifier
        
        if asi_choice == "+1 to Three":
            # Must pick 3 unique from allowed (which are usually 3 anyway)
            # If standard 3 are given, typically just those 3.
            # But technically you choose to boost 3.
            # Assuming background gives exactly 3 options usually.
            for a in allowed:
                mod = Modifier(name="Background ASI", value=1, target=a.value, type="bonus")
                self.character.stats.modifiers.append(mod)
                console.print(f"[green]+1 {a.value}[/green]")
        else:
            # +2 / +1
            plus2 = questionary.select("Select Ability for +2:", choices=allowed_names).ask()
            remain = [n for n in allowed_names if n != plus2]
            plus1 = questionary.select("Select Ability for +1:", choices=remain).ask()
            
            self.character.stats.modifiers.append(Modifier(name="Background ASI", value=2, target=plus2, type="bonus"))
            self.character.stats.modifiers.append(Modifier(name="Background ASI", value=1, target=plus1, type="bonus"))
            console.print(f"[green]+2 {plus2}, +1 {plus1}[/green]")

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
            
            # Filter already known spells (e.g. from Magic Initiate)
            known_names = {s.name for s in self.character.spellbook}
            cantrips_avail = [s for s in cantrips_avail if s.name not in known_names]
            
            if cantrips_avail:
                cantrip_names = [s.name for s in cantrips_avail]
                choices = questionary.checkbox(
                    "Select 3 Cantrips:",
                    choices=cantrip_names,
                    validate=lambda c: True if len(c) == 3 else "Select exactly 3 cantrips."
                ).ask()
                for name in choices:
                    s = SpellDatabase.get_spell(name)
                    if s: self.character.spellbook.append(s)
            
            # Level 1 Spells
            # Wizard: 6 in book. Cleric: All prepared? 
            # Simplified: Select 4 to start.
            lvl1_avail = SpellDatabase.get_available_spells(primary_cls_name, level=1)
            
            # Filter known
            lvl1_avail = [s for s in lvl1_avail if s.name not in known_names]
            
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

        # Sync HP
        self.character.current_hp = self.character.max_hp
        console.print(f"[bold]HP Initialized to {self.character.current_hp}/{self.character.max_hp}[/bold]")

        console.print("[bold blue]Character Created![/bold blue]")
        return self.character
