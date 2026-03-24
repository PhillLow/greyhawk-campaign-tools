"""
Comprehensive Feature Test Suite for greyhawk-campaign-tools.
Tests verify that each major feature works as intended per 2024 PHB rules.
"""
import unittest
from src.models.character import Character
from src.models.species import Species, SpeciesName
from src.models.class_model import CharacterClass, ClassLevel, ClassName
from src.models.background import Background, BackgroundName
from src.models.feat import Feat, FeatDatabase
from src.models.stats import Stats, Ability
from src.models.equipment import Weapon, Armor, ArmorCategory, WeaponProperty
from src.models.spell_database import SpellDatabase
from src.models.transformation import Transformation
from src.models.modifier import Modifier


class TestHPCalculation(unittest.TestCase):
    """Tests for HP calculation logic."""
    
    def test_level1_hp_max_die(self):
        """Level 1 HP should be max die + Con mod."""
        char = Character(name="Test")
        wiz = CharacterClass.get_template(ClassName.WIZARD)
        char.classes = [ClassLevel(character_class=wiz, level=1)]
        char.stats.constitution.score = 14  # +2 mod
        
        # Wizard d6 = 6 + 2 Con = 8
        self.assertEqual(char.max_hp, 8)
    
    def test_level2_hp_average_die(self):
        """Level 2+ HP uses average die + Con mod."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=2)]
        char.stats.constitution.score = 14  # +2 mod
        
        # Fighter d10: Level 1 = 10 + 2 = 12, Level 2 = 6 (avg) + 2 = 8
        # Total: 12 + 8 = 20
        self.assertEqual(char.max_hp, 20)
    
    def test_multiclass_hp(self):
        """Multiclass HP calculates correctly per class."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        wizard = CharacterClass.get_template(ClassName.WIZARD)
        char.classes = [
            ClassLevel(character_class=fighter, level=1),  # Primary: 10 + Con
            ClassLevel(character_class=wizard, level=1)    # Secondary: 4 (avg) + Con
        ]
        char.stats.constitution.score = 10  # +0 mod
        
        # Fighter L1: 10 + 0 = 10
        # Wizard L1 (secondary): 4 + 0 = 4
        # Total: 14
        self.assertEqual(char.max_hp, 14)
    
    def test_tough_feat_bonus(self):
        """Tough feat adds +2 HP per level."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=3)]
        char.stats.constitution.score = 10  # +0 mod
        
        # Base: 10 + 6 + 6 = 22
        base_hp = char.max_hp
        self.assertEqual(base_hp, 22)
        
        # Add Tough
        tough = FeatDatabase.get_feat("Tough")
        char.feats.append(tough)
        
        # With Tough: 22 + 6 (2 * 3) = 28
        self.assertEqual(char.max_hp, 28)


class TestACCalculation(unittest.TestCase):
    """Tests for Armor Class calculation logic."""
    
    def test_unarmored_ac(self):
        """Unarmored AC = 10 + Dex mod."""
        char = Character(name="Test")
        char.stats.dexterity.score = 16  # +3 mod
        
        self.assertEqual(char.armor_class, 13)
    
    def test_light_armor_ac(self):
        """Light armor AC = armor base + Dex mod."""
        char = Character(name="Test")
        char.stats.dexterity.score = 16  # +3 mod
        
        leather = Armor(
            name="Leather Armor",
            ac_base=11,
            category=ArmorCategory.LIGHT,
            weight=10
        )
        char.inventory.append(leather)
        char.equip_item("Leather Armor")
        
        # 11 + 3 Dex = 14
        self.assertEqual(char.armor_class, 14)
    
    def test_medium_armor_dex_cap(self):
        """Medium armor caps Dex bonus at +2."""
        char = Character(name="Test")
        char.stats.dexterity.score = 18  # +4 mod, but capped at +2
        
        scalemail = Armor(
            name="Scale Mail",
            ac_base=14,
            category=ArmorCategory.MEDIUM,
            dex_cap=2,  # Medium armor caps at +2
            weight=45
        )
        char.inventory.append(scalemail)
        char.equip_item("Scale Mail")
        
        # 14 + 2 (capped) = 16
        self.assertEqual(char.armor_class, 16)
    
    def test_heavy_armor_no_dex(self):
        """Heavy armor ignores Dex modifier."""
        char = Character(name="Test")
        char.stats.dexterity.score = 18  # +4 mod, ignored
        
        plate = Armor(
            name="Plate",
            ac_base=18,
            category=ArmorCategory.HEAVY,
            dex_cap=0,  # Heavy armor: no Dex bonus
            weight=65
        )
        char.inventory.append(plate)
        char.equip_item("Plate")
        
        self.assertEqual(char.armor_class, 18)
    
    def test_shield_bonus(self):
        """Shield adds +2 AC."""
        char = Character(name="Test")
        char.stats.dexterity.score = 12  # +1 mod
        
        shield = Armor(
            name="Shield",
            ac_base=2,
            category=ArmorCategory.SHIELD,
            weight=6
        )
        char.inventory.append(shield)
        char.equip_item("Shield")
        
        # 10 + 1 Dex + 2 Shield = 13
        self.assertEqual(char.armor_class, 13)


class TestShortRestMechanics(unittest.TestCase):
    """Tests for Short Rest functionality."""
    
    def test_short_rest_increments_counter(self):
        """perform_short_rest() increments short_rests_taken."""
        char = Character(name="Test")
        self.assertEqual(char.short_rests_taken, 0)
        
        char.perform_short_rest()
        self.assertEqual(char.short_rests_taken, 1)
        
        char.perform_short_rest()
        self.assertEqual(char.short_rests_taken, 2)
    
    def test_short_rest_third_increments_still(self):
        """Third short rest still increments (no hard block)."""
        char = Character(name="Test")
        char.perform_short_rest()
        char.perform_short_rest()
        result = char.perform_short_rest()  # Third
        
        self.assertEqual(char.short_rests_taken, 3)
        self.assertFalse(result)  # Returns False when exceeding limit
    
    def test_short_rest_returns_limit_status(self):
        """perform_short_rest returns True/False based on limit."""
        char = Character(name="Test")
        
        self.assertTrue(char.perform_short_rest())  # 1st: True
        self.assertTrue(char.perform_short_rest())  # 2nd: True
        self.assertFalse(char.perform_short_rest()) # 3rd: False (exceeded)
    
    def test_pact_slots_restore_on_short_rest(self):
        """Warlock pact slots restore on Short Rest."""
        char = Character(name="Test")
        warlock = CharacterClass.get_template(ClassName.WARLOCK)
        char.classes = [ClassLevel(character_class=warlock, level=3)]
        
        # Use pact slot
        char.current_pact_slots = 0
        
        char.perform_short_rest()
        
        # Should have restored (level 3 = 2 slots)
        self.assertEqual(char.current_pact_slots, 2)


class TestLongRestMechanics(unittest.TestCase):
    """Tests for Long Rest functionality."""
    
    def test_long_rest_resets_short_rest_counter(self):
        """perform_long_rest() resets short_rests_taken to 0."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        
        char.short_rests_taken = 3
        char.perform_long_rest()
        
        self.assertEqual(char.short_rests_taken, 0)
    
    def test_long_rest_restores_hp(self):
        """Long Rest restores HP to max."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        char.stats.constitution.score = 10
        
        char.current_hp = 1
        char.perform_long_rest()
        
        self.assertEqual(char.current_hp, char.max_hp)
    
    def test_long_rest_restores_spell_slots(self):
        """Long Rest restores spell slots."""
        char = Character(name="Test")
        wizard = CharacterClass.get_template(ClassName.WIZARD)
        char.classes = [ClassLevel(character_class=wizard, level=3)]
        
        # Use all slots
        char.current_spell_slots = {}
        
        char.perform_long_rest()
        
        # Level 3 Wizard: 4 first level slots, 2 second level
        self.assertGreater(char.current_spell_slots.get(1, 0), 0)
    
    def test_long_rest_reduces_exhaustion(self):
        """Long Rest reduces exhaustion by 1."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        char.exhaustion = 3
        
        char.perform_long_rest()
        
        self.assertEqual(char.exhaustion, 2)
    
    def test_long_rest_resets_free_casts(self):
        """Long Rest resets feat free casts to 1."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        
        # Simulate Magic Initiate granting Shield free cast
        char.free_casts["Shield"] = 0  # Used up
        
        char.perform_long_rest()
        
        self.assertEqual(char.free_casts["Shield"], 1)


class TestTransformationAvailability(unittest.TestCase):
    """Tests for who can access transformation features."""
    
    def test_fighter_cannot_transform(self):
        """Fighter does NOT have can_transform."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=5)]
        
        self.assertFalse(char.can_transform)
    
    def test_wizard_cannot_transform(self):
        """Wizard does NOT have can_transform."""
        char = Character(name="Test")
        wizard = CharacterClass.get_template(ClassName.WIZARD)
        char.classes = [ClassLevel(character_class=wizard, level=5)]
        
        self.assertFalse(char.can_transform)
    
    def test_druid_can_transform(self):
        """Druid DOES have can_transform."""
        char = Character(name="Test")
        druid = CharacterClass.get_template(ClassName.DRUID)
        char.classes = [ClassLevel(character_class=druid, level=2)]
        
        self.assertTrue(char.can_transform)
    
    def test_multiclass_druid_can_transform(self):
        """Fighter/Druid multiclass has can_transform."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        druid = CharacterClass.get_template(ClassName.DRUID)
        char.classes = [
            ClassLevel(character_class=fighter, level=5),
            ClassLevel(character_class=druid, level=2)
        ]
        
        self.assertTrue(char.can_transform)


class TestTransformationMechanics(unittest.TestCase):
    """Tests for transformation stat overrides."""
    
    def test_transformation_ac_override(self):
        """Transformation overrides AC."""
        char = Character(name="Test")
        druid = CharacterClass.get_template(ClassName.DRUID)
        char.classes = [ClassLevel(character_class=druid, level=2)]
        char.stats.dexterity.score = 10  # Base AC 10
        
        wolf = Transformation.get_template("Wolf")
        char.toggle_transformation(wolf)
        
        self.assertEqual(char.armor_class, 13)  # Wolf natural armor
    
    def test_transformation_speed_override(self):
        """Transformation overrides speed."""
        char = Character(name="Test")
        druid = CharacterClass.get_template(ClassName.DRUID)
        char.classes = [ClassLevel(character_class=druid, level=2)]
        
        wolf = Transformation.get_template("Wolf")
        char.toggle_transformation(wolf)
        
        self.assertEqual(char.speed, 40)  # Wolf speed
    
    def test_revert_transformation(self):
        """Reverting transformation restores original stats."""
        char = Character(name="Test")
        druid = CharacterClass.get_template(ClassName.DRUID)
        char.classes = [ClassLevel(character_class=druid, level=2)]
        char.stats.dexterity.score = 14  # +2, base AC 12
        
        original_ac = char.armor_class
        
        wolf = Transformation.get_template("Wolf")
        char.toggle_transformation(wolf)
        self.assertNotEqual(char.armor_class, original_ac)
        
        # Revert
        char.toggle_transformation(wolf)
        self.assertEqual(char.armor_class, original_ac)


class TestSpellSelection(unittest.TestCase):
    """Tests for spell selection and spellbook."""
    
    def test_spell_database_has_cantrips(self):
        """SpellDatabase has required cantrips."""
        self.assertIsNotNone(SpellDatabase.get_spell("Fire Bolt"))
        self.assertIsNotNone(SpellDatabase.get_spell("Ray of Frost"))
        self.assertIsNotNone(SpellDatabase.get_spell("Minor Illusion"))
    
    def test_spell_database_has_level1(self):
        """SpellDatabase has required level 1 spells."""
        self.assertIsNotNone(SpellDatabase.get_spell("Magic Missile"))
        self.assertIsNotNone(SpellDatabase.get_spell("Shield"))
        self.assertIsNotNone(SpellDatabase.get_spell("Ice Knife"))
    
    def test_wizard_spell_list(self):
        """Wizard spell list includes expected spells."""
        spells = SpellDatabase.get_available_spells(ClassName.WIZARD, level=0)
        names = [s.name for s in spells]
        
        self.assertIn("Fire Bolt", names)
        self.assertIn("Ray of Frost", names)
        self.assertIn("Minor Illusion", names)


class TestFeatBehavior(unittest.TestCase):
    """Tests for feat effects."""
    
    def test_tough_modifies_hp(self):
        """Tough feat modifies max_hp."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=5)]
        char.stats.constitution.score = 10
        
        base = char.max_hp
        
        tough = FeatDatabase.get_feat("Tough")
        char.feats.append(tough)
        
        self.assertEqual(char.max_hp, base + 10)  # +2 per level
    
    def test_magic_initiate_exists(self):
        """Magic Initiate feat exists in database."""
        feat = FeatDatabase.get_feat("Magic Initiate")
        self.assertIsNotNone(feat)


class TestCombatCalculations(unittest.TestCase):
    """Tests for attack and damage calculations."""
    
    def test_attack_roll_str_weapon(self):
        """Attack roll uses Str + PB for strength weapons."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        char.stats.strength.score = 16  # +3 mod
        
        longsword = Weapon(
            name="Longsword",
            damage_dice="1d8",
            damage_type="Slashing",
            properties=[WeaponProperty.VERSATILE],
            weight=3
        )
        
        to_hit = char.calculate_attack_roll(longsword)
        # Str (+3) + PB (+2) = +5
        self.assertEqual(to_hit, 5)
    
    def test_attack_roll_finesse_uses_higher(self):
        """Finesse weapons use higher of Str/Dex."""
        char = Character(name="Test")
        rogue = CharacterClass.get_template(ClassName.ROGUE)
        char.classes = [ClassLevel(character_class=rogue, level=1)]
        char.stats.strength.score = 10  # +0
        char.stats.dexterity.score = 18  # +4
        
        rapier = Weapon(
            name="Rapier",
            damage_dice="1d8",
            damage_type="Piercing",
            properties=[WeaponProperty.FINESSE],
            weight=2
        )
        
        to_hit = char.calculate_attack_roll(rapier)
        # Dex (+4) + PB (+2) = +6
        self.assertEqual(to_hit, 6)
    
    def test_exhaustion_penalty_on_attack(self):
        """Exhaustion applies penalty to attack rolls."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        char.stats.strength.score = 10  # +0
        char.exhaustion = 2  # -4 penalty
        
        longsword = Weapon(
            name="Longsword",
            damage_dice="1d8",
            damage_type="Slashing",
            properties=[],
            weight=3
        )
        
        to_hit = char.calculate_attack_roll(longsword)
        # Str (+0) + PB (+2) + Exhaustion (-4) = -2
        self.assertEqual(to_hit, -2)


class TestInventoryEquipment(unittest.TestCase):
    """Tests for inventory and equipment management."""
    
    def test_equip_weapon(self):
        """Equipping weapon updates equipped status."""
        char = Character(name="Test")
        
        sword = Weapon(
            name="Longsword",
            damage_dice="1d8",
            damage_type="Slashing",
            properties=[],
            weight=3,
            equipped=False
        )
        char.inventory.append(sword)
        char.equip_item("Longsword")
        
        self.assertTrue(char.inventory[0].equipped)
    
    def test_equip_armor_changes_ac(self):
        """Equipping armor updates AC."""
        char = Character(name="Test")
        char.stats.dexterity.score = 14  # +2
        
        base_ac = char.armor_class  # 10 + 2 = 12
        
        chainmail = Armor(
            name="Chain Mail",
            ac_base=16,
            category=ArmorCategory.HEAVY,
            dex_cap=0,  # Heavy armor: no Dex bonus
            weight=55,
            equipped=False
        )
        char.inventory.append(chainmail)
        char.equip_item("Chain Mail")
        
        self.assertEqual(char.armor_class, 16)
        self.assertNotEqual(char.armor_class, base_ac)


class TestLevelUp(unittest.TestCase):
    """Tests for leveling up."""
    
    def test_level_increment(self):
        """Level increment increases total level."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        
        self.assertEqual(char.level, 1)
        
        char.classes[0].level = 5
        self.assertEqual(char.level, 5)
    
    def test_multiclass_total_level(self):
        """Multiclass level sums correctly."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        wizard = CharacterClass.get_template(ClassName.WIZARD)
        char.classes = [
            ClassLevel(character_class=fighter, level=3),
            ClassLevel(character_class=wizard, level=2)
        ]
        
        self.assertEqual(char.level, 5)
    
    def test_proficiency_bonus_scales(self):
        """Proficiency bonus scales with level."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=1)]
        
        self.assertEqual(char.proficiency_bonus, 2)  # Level 1-4
        
        char.classes[0].level = 5
        self.assertEqual(char.proficiency_bonus, 3)  # Level 5-8
        
        char.classes[0].level = 9
        self.assertEqual(char.proficiency_bonus, 4)  # Level 9-12


class TestExhaustion(unittest.TestCase):
    """Tests for exhaustion mechanics."""
    
    def test_exhaustion_penalty_to_rolls(self):
        """Exhaustion applies -2 per level to d20 tests."""
        char = Character(name="Test")
        char.exhaustion = 3
        
        self.assertEqual(char.exhaustion_penalty, -6)
    
    def test_exhaustion_speed_reduction(self):
        """Exhaustion reduces speed by -5 ft per level."""
        char = Character(name="Test")
        char.exhaustion = 2
        
        self.assertEqual(char.speed_penalty, -10)
    
    def test_exhaustion_affects_speed(self):
        """Character speed includes exhaustion penalty."""
        char = Character(name="Test")
        # Human base speed is 30
        
        base_speed = char.speed
        char.exhaustion = 2
        
        self.assertEqual(char.speed, base_speed - 10)


class TestHitDice(unittest.TestCase):
    """Tests for hit dice spending and recovery."""
    
    def test_roll_hit_die_heals(self):
        """Rolling hit die heals character."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=3)]
        char.stats.constitution.score = 14  # +2
        char.current_hit_dice = {"Fighter": 3}
        char.current_hp = 1
        
        healed = char.roll_hit_die("Fighter")
        
        self.assertGreater(healed, 0)
        self.assertGreater(char.current_hp, 1)
    
    def test_roll_hit_die_decrements_pool(self):
        """Rolling hit die decrements available dice."""
        char = Character(name="Test")
        fighter = CharacterClass.get_template(ClassName.FIGHTER)
        char.classes = [ClassLevel(character_class=fighter, level=3)]
        char.current_hit_dice = {"Fighter": 3}
        char.current_hp = 1
        
        char.roll_hit_die("Fighter")
        
        self.assertEqual(char.current_hit_dice["Fighter"], 2)


if __name__ == "__main__":
    unittest.main()
