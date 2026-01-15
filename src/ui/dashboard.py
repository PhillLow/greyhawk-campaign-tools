from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box
from src.models.character import Character

class Dashboard:
    def __init__(self, character: Character):
        self.char = character
        self.console = Console()

    def render(self):
        layout = Layout()
        
        # Split into Header (Top) and Body (Bottom)
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body")
        )
        
        # Split Body into Left (Stats), Center (Combat), Right (Info)
        layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="center", ratio=2),
            Layout(name="right", ratio=2)
        )
        
        # Split Left into Attributes and Inventory
        layout["left"].split_column(
            Layout(name="attributes", ratio=2),
            Layout(name="wealth", ratio=1)
        )
        
        # --- Update Content ---
        layout["header"].update(self._make_header())
        layout["attributes"].update(self._make_stats_column())
        layout["wealth"].update(self._make_wealth_panel())
        layout["center"].update(self._make_combat_column())
        layout["right"].update(self._make_info_column())
        
        self.console.print(layout)

    def _make_header(self) -> Panel:
        summary = f"[b]{self.char.name}[/b] | Level {self.char.level} {self.char.species.name.value} {self.char.character_class.name.value} | {self.char.background.name.value}"
        return Panel(Align.center(summary), style="white on blue")
        
    def _make_wealth_panel(self) -> Panel:
        content = f"[bold gold1]GP: {self.char.gp}[/]\n[bold white]SP: {self.char.sp}[/]\n[bold orange3]CP: {self.char.cp}[/]"
        return Panel(Align.center(content), title="Wealth", border_style="gold1")

    def _make_stats_column(self) -> Panel:
        table = Table(show_header=False, box=None, padding=0)
        table.add_column("Stat", style="bold cyan")
        table.add_column("Score", justify="right")
        table.add_column("Mod", justify="right", style="bold yellow")
        
        stats_order = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        for s in stats_order:
            attr = getattr(self.char.stats, s)
            table.add_row(
                attr.name.value[:3].upper(), 
                str(attr.value), 
                f"{attr.modifier:+}"
            )
            
        return Panel(table, title="Abilities", border_style="cyan")

    def _make_combat_column(self) -> Panel:
        # Top: Vitals
        vitals_table = Table(show_header=True, box=box.SIMPLE, expand=True)
        vitals_table.add_column("HP", justify="center", style="bold red")
        vitals_table.add_column("AC", justify="center", style="bold blue")
        vitals_table.add_column("Init", justify="center")
        vitals_table.add_column("Speed", justify="center")
        vitals_table.add_column("Prof", justify="center")
        
        hp_str = f"{self.char.current_hp}/{self.char.max_hp}"
        if self.char.current_hp <= 0:
            hp_str += "\n[bold red]DOWN[/]"
            
        vitals_table.add_row(
            hp_str,
            str(self.char.armor_class),
            f"{self.char.initiative:+}",
            f"{self.char.species.speed}ft",
            f"+{self.char.proficiency_bonus}"
        )
        
        # Death Saves (Show if damaged or always? Always for now)
        ds_str = f"[green]Success: {self.char.death_save_successes}/3[/]  [red]Fail: {self.char.death_save_failures}/3[/]"
        vitals_table.add_row(ds_str, "", "", "", "")
        
        # Conditions
        if self.char.conditions:
            cond_str = "[bold red]CONDITIONS:[/bold red] " + ", ".join(self.char.conditions)
            vitals_table.add_row(cond_str, "", "", "", "")
        
        # Transformation Status
        if self.char.active_transformation:
            vitals_table.add_row(f"[bold red]{self.char.active_transformation.name}[/]", "", "", "", "")

        # Spell Slots
        content = vitals_table
        
        # We can't easily append text to a table object if we return Panel(table). 
        # So we use a Group or Layout? 
        # Actually, simpler: return Panel(Group(table, text))
        
        from rich.console import Group
        
        elements = [vitals_table]
        
        if self.char.active_transformation:
             elements.append(Align.center(f"[bold red]TRANSFORMED: {self.char.active_transformation.name}[/bold red]"))
             if self.char.active_transformation.hp_value > 0:
                 elements.append(Align.center(f"Temp HP: {self.char.temp_hp}"))
        
        if self.char.max_spell_slots:
            from rich.text import Text
            elements.append(Text("\nSpell Slots:", style="bold purple"))
            slot_text = ""
            for lvl, mx in self.char.max_spell_slots.items():
                cur = self.char.current_spell_slots.get(lvl, 0)
                slot_text += f"Lvl {lvl}: {cur}/{mx}  "
            elements.append(Text(slot_text))
            
        # Attacks Calculator
        from src.models.equipment import Weapon, WeaponProperty, ItemType
        equipped_weapons = [i for i in self.char.inventory if isinstance(i, Weapon) and i.equipped]
        
        if equipped_weapons:
            att_table = Table(title="Attacks", show_header=True, box=box.SIMPLE, expand=True, title_style="bold red")
            att_table.add_column("Weapon", style="white")
            att_table.add_column("To Hit", justify="center", style="bold green")
            att_table.add_column("Damage", justify="center", style="bold yellow")
            att_table.add_column("Props/Mastery", style="dim")
            
            str_mod = self.char.stats.strength.modifier
            dex_mod = self.char.stats.dexterity.modifier
            pb = self.char.proficiency_bonus
            
            for w in equipped_weapons:
                # Use new centralized mechanics methods
                to_hit = self.char.calculate_attack_roll(w)
                dmg_bonus = self.char.calculate_damage_roll(w)
                
                sign = "+" if to_hit >= 0 else ""
                
                # Format Damage: "1d8+3" 
                # If dmg_bonus is 0, just "1d8"
                # If negative, "1d8-1"
                dmg_str = f"{w.damage_dice}"
                if dmg_bonus > 0:
                    dmg_str += f"+{dmg_bonus}"
                elif dmg_bonus < 0:
                    dmg_str += f"{dmg_bonus}"
                    
                dmg_val = f"{dmg_str} {w.damage_type.name[:1]}"
                
                props = ", ".join([p.value for p in w.properties])
                if w.mastery:
                    props += f" | {w.mastery.value}"
                    
                att_table.add_row(w.name, f"{sign}{to_hit}", dmg_val, props)
                
            elements.append(att_table)
            
        return Panel(Group(*elements), title="Combat", border_style="red")

    def _make_info_column(self) -> Panel:
        # Features & Traits
        content = ""
        
        for cls_lvl in self.char.classes:
            c_name = cls_lvl.character_class.name.value
            c_lvl = cls_lvl.level
            content += f"[bold underline]{c_name} (Level {c_lvl})[/]\n"
            
            # Simple check for features available at this level
            available_features = [f for f in cls_lvl.character_class.features if f.level <= c_lvl]
            if not available_features:
                content += "[dim]No features unlocked yet.[/dim]\n"
            for f in available_features:
                 content += f"• [b]{f.name}[/]: {f.description}\n"
            content += "\n"
            
        content += "[bold underline]Species Traits[/]\n"
        for t in self.char.species.traits:
            content += f"• [b]{t.name}[/]: {t.description}\n"
            
        content += "\n[bold underline]Background[/]\n"
        content += f"{self.char.background.name.value}\n"
        
        # Skills
        if self.char.skills:
             content += "\n[bold underline]Skills[/]\n"
             # Sort them
             content += ", ".join(sorted(self.char.skills)) + "\n"
             
        # Feats
        if self.char.feats:
             content += "[bold underline]Feats[/]\n"
             for feat in self.char.feats:
                 content += f"• [b]{feat.name}[/]: {feat.description}\n"
        
        # Spells
        if self.char.spellbook:
            content += "\n[bold underline]Spellbook[/]\n"
            # Group by level
            by_lvl = {}
            for s in self.char.spellbook:
                by_lvl.setdefault(s.level, []).append(s)
            
            for lvl in sorted(by_lvl.keys()):
                label = "Cantrips" if lvl == 0 else f"Level {lvl}"
                content += f"[b]{label}[/]: " + ", ".join([s.name for s in by_lvl[lvl]]) + "\n"
        
        # Companions
        if self.char.companions:
            content += "\n[bold underline]Companions[/]\n"
            for c in self.char.companions:
                content += f"• [b]{c.name}[/] ({c.creature_type}): {c.current_hp}/{c.max_hp} HP\n"
            
        return Panel(content, title="Features & Traits", border_style="green")
