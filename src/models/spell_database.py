from typing import List
from src.models.spell import Spell, School
from src.models.class_model import ClassName

class SpellDatabase:
    _spells = [
        # Cantrips
        Spell(name="Fire Bolt", level=0, school=School.EVOCATION, casting_time="1 Action", range_area="120 ft", components="V, S", duration="Instantaneous", description="1d10 Fire damage."),
        Spell(name="Light", level=0, school=School.EVOCATION, casting_time="1 Action", range_area="Touch", components="V, M", duration="1 Hour", description="Object sheds bright light."),
        Spell(name="Mage Hand", level=0, school=School.CONJURATION, casting_time="1 Action", range_area="30 ft", components="V, S", duration="1 Minute", description="Spectral hand manipulats objects."),
        Spell(name="Prestidigitation", level=0, school=School.TRANSMUTATION, casting_time="1 Action", range_area="10 ft", components="V, S", duration="1 Hour", description="Minor magical tricks."),
        Spell(name="Sacred Flame", level=0, school=School.EVOCATION, casting_time="1 Action", range_area="60 ft", components="V, S", duration="Instantaneous", description="1d8 Radiant damage (Dex save)."),
        Spell(name="Thaumaturgy", level=0, school=School.TRANSMUTATION, casting_time="1 Action", range_area="30 ft", components="V", duration="1 Minute", description="Minor divine signs."),
        Spell(name="Vicious Mockery", level=0, school=School.ENCHANTMENT, casting_time="1 Action", range_area="60 ft", components="V", duration="Instantaneous", description="1d4 Psychic damage + Disadvantage."),
        Spell(name="Shillelagh", level=0, school=School.TRANSMUTATION, casting_time="Bonus Action", range_area="Touch", components="V, S, M", duration="1 Minute", description="Club becomes magic weapon (Wis)."),
        
        # Level 1
        Spell(name="Magic Missile", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="120 ft", components="V, S", duration="Instantaneous", description="3 darts deal 1d4+1 force each."),
        Spell(name="Shield", level=1, school=School.ABJURATION, casting_time="Reaction", range_area="Self", components="V, S", duration="1 Round", description="+5 AC."),
        Spell(name="Mage Armor", level=1, school=School.ABJURATION, casting_time="1 Action", range_area="Touch", components="V, S, M", duration="8 Hours", description="AC becomes 13 + Dex."),
        Spell(name="Cure Wounds", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="Touch", components="V, S", duration="Instantaneous", description="Heal 2d8 + Mod (2024 buff)."),
        Spell(name="Healing Word", level=1, school=School.EVOCATION, casting_time="Bonus Action", range_area="60 ft", components="V", duration="Instantaneous", description="Heal 1d4 + Mod."),
        Spell(name="Bless", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="30 ft", components="V, S, M", duration="Concentration, 1 Min", description="+1d4 to attacks/saves."),
        Spell(name="Burning Hands", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="15 ft Cone", components="V, S", duration="Instantaneous", description="3d6 Fire damage."),
        Spell(name="Thunderwave", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="15 ft Cube", components="V, S", duration="Instantaneous", description="2d8 Thunder + Push."),
    ]
    
    # Simplified Class Lists (In real app, filter by tag)
    _class_lists = {
        ClassName.WIZARD: ["Fire Bolt", "Light", "Mage Hand", "Prestidigitation", "Magic Missile", "Shield", "Mage Armor", "Burning Hands", "Thunderwave"],
        ClassName.CLERIC: ["Sacred Flame", "Thaumaturgy", "Light", "Cure Wounds", "Healing Word", "Bless", "Shield"], # 2024 Clerics get more
        ClassName.DRUID: ["Shillelagh", "Starry Wisp", "Cure Wounds", "Healing Word", "Thunderwave"],
        ClassName.BARD: ["Vicious Mockery", "Prestidigitation", "Cure Wounds", "Healing Word", "Thunderwave", "Charm Person"],
        ClassName.SORCERER: ["Fire Bolt", "Light", "Magic Missile", "Shield", "Burning Hands"],
        ClassName.WARLOCK: ["Eldritch Blast", "Prestidigitation", "Hex", "Hellish Rebuke"], # TODO add these
    }

    @classmethod
    def get_all_spells(cls) -> List[Spell]:
        return cls._spells
        
    @classmethod
    def get_spell(cls, name: str) -> Spell:
        return next((s for s in cls._spells if s.name.lower() == name.lower()), None)

    @classmethod
    def get_available_spells(cls, class_name: ClassName, level: int = None) -> List[Spell]:
        """Returns spells available to the class, optionally filtered by spell level."""
        allowed_names = cls._class_lists.get(class_name, [])
        spells = [s for s in cls._spells if s.name in allowed_names]
        if level is not None:
            spells = [s for s in spells if s.level == level]
        return spells
