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
        Spell(name="Starry Wisp", level=0, school=School.EVOCATION, casting_time="1 Action", range_area="60 ft", components="V, S", duration="Instantaneous", description="1d8 Radiant + Light. (2024 New)"),
        Spell(name="Eldritch Blast", level=0, school=School.EVOCATION, casting_time="1 Action", range_area="120 ft", components="V, S", duration="Instantaneous", description="1d10 Force damage."),
        Spell(name="Guidance", level=0, school=School.DIVINATION, casting_time="1 Action", range_area="Touch", components="V, S", duration="Concentration, 1 Min", description="+1d4 to check."),
        Spell(name="Resistance", level=0, school=School.ABJURATION, casting_time="1 Action", range_area="Touch", components="V, S", duration="Concentration, 1 Min", description="+1d4 to save."),
        
        # Level 1
        Spell(name="Magic Missile", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="120 ft", components="V, S", duration="Instantaneous", description="3 darts deal 1d4+1 force each."),
        Spell(name="Shield", level=1, school=School.ABJURATION, casting_time="Reaction", range_area="Self", components="V, S", duration="1 Round", description="+5 AC."),
        Spell(name="Mage Armor", level=1, school=School.ABJURATION, casting_time="1 Action", range_area="Touch", components="V, S, M", duration="8 Hours", description="AC becomes 13 + Dex."),
        Spell(name="Cure Wounds", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="Touch", components="V, S", duration="Instantaneous", description="Heal 2d8 + Mod (2024 buff)."),
        Spell(name="Healing Word", level=1, school=School.EVOCATION, casting_time="Bonus Action", range_area="60 ft", components="V", duration="Instantaneous", description="Heal 1d4 + Mod."),
        Spell(name="Bless", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="30 ft", components="V, S, M", duration="Concentration, 1 Min", description="+1d4 to attacks/saves."),
        Spell(name="Burning Hands", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="15 ft Cone", components="V, S", duration="Instantaneous", description="3d6 Fire damage."),
        Spell(name="Thunderwave", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="15 ft Cube", components="V, S", duration="Instantaneous", description="2d8 Thunder + Push."),
        Spell(name="Charm Person", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="30 ft", components="V, S", duration="1 Hour", description="Charm humanoid."),
        Spell(name="Hex", level=1, school=School.ENCHANTMENT, casting_time="Bonus Action", range_area="90 ft", components="V, S, M", duration="Concentration, 1 Hour", description="Extra 1d6 Necrotic + Disadvantage on checks."),
        Spell(name="Hellish Rebuke", level=1, school=School.EVOCATION, casting_time="Reaction", range_area="60 ft", components="V, S", duration="Instantaneous", description="2d10 Fire damage."),
        Spell(name="Detect Magic", level=1, school=School.DIVINATION, casting_time="1 Action", range_area="Self", components="V, S", duration="Concentration, 10 Min", description="Sense magic.", ritual=True),
        Spell(name="Guiding Bolt", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="120 ft", components="V, S", duration="1 Round", description="4d6 Radiant + Advantage."),
        Spell(name="Sleep", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="60 ft", components="V, S, M", duration="1 Minute", description="Put creatures to sleep (5d8 HP)."),
        Spell(name="Tasha's Hideous Laughter", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="30 ft", components="V, S, M", duration="Concentration, 1 Min", description="Creature falls prone laughing."),
        Spell(name="Grease", level=1, school=School.CONJURATION, casting_time="1 Action", range_area="60 ft", components="V, S, M", duration="1 Minute", description="Slick area, prone save."),
        Spell(name="Bane", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="30 ft", components="V, S, M", duration="Concentration, 1 Min", description="Subtract 1d4 from saves/attacks."),
        Spell(name="Command", level=1, school=School.ENCHANTMENT, casting_time="1 Action", range_area="60 ft", components="V", duration="1 Round", description="Creature obeys command."),
        Spell(name="Faerie Fire", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="60 ft", components="V", duration="Concentration, 1 Min", description="Advantage on attacks vs targets."),
        Spell(name="Shield of Faith", level=1, school=School.ABJURATION, casting_time="Bonus Action", range_area="60 ft", components="V, S, M", duration="Concentration, 10 Min", description="+2 AC."),
        Spell(name="Witch Bolt", level=1, school=School.EVOCATION, casting_time="1 Action", range_area="30 ft", components="V, S, M", duration="Concentration, 1 Min", description="1d12 Lightning, sustain for auto damage."),
    ]
    
    # Simplified Class Lists (In real app, filter by tag)
    _class_lists = {
        ClassName.WIZARD: ["Fire Bolt", "Light", "Mage Hand", "Prestidigitation", "Magic Missile", "Shield", "Mage Armor", "Burning Hands", "Thunderwave", "Detect Magic", "Charm Person", "Sleep", "Tasha's Hideous Laughter", "Grease", "Witch Bolt"],
        ClassName.CLERIC: ["Sacred Flame", "Thaumaturgy", "Guidance", "Resistance", "Light", "Cure Wounds", "Healing Word", "Bless", "Shield", "Guiding Bolt", "Detect Magic", "Bane", "Command", "Shield of Faith"],
        ClassName.DRUID: ["Shillelagh", "Starry Wisp", "Guidance", "Resistance", "Cure Wounds", "Healing Word", "Thunderwave", "Charm Person", "Detect Magic", "Faerie Fire"],
        ClassName.BARD: ["Vicious Mockery", "Prestidigitation", "Cure Wounds", "Healing Word", "Thunderwave", "Charm Person", "Bane", "Faerie Fire"],
        ClassName.SORCERER: ["Fire Bolt", "Light", "Magic Missile", "Shield", "Burning Hands", "Witch Bolt"],
        ClassName.WARLOCK: ["Eldritch Blast", "Prestidigitation", "Hex", "Hellish Rebuke", "Witch Bolt"], 
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
