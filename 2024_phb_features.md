# D&D 2024 PHB Character Sheet Emulator - Feature Specification

This document outlines the complete feature set required to emulate a "D&D Beyond-like" experience for the 2024 Player's Handbook (PHB) ruleset.

## 1. Character Creation (The "Builder")

The builder must guide the user step-by-step through the process, adhering to the 2024 rules changes (e.g., Backgrounds granting Ability Scores/Feats).

### 1.1 Core Selection
- **Species Selection**
    - Apply Species Traits (Darkvision, Speed, Special speeds like Fly/Swim).
    - Apply Species-specific features (e.g., Orc Adrenaline Rush, Elf Trance).
    - *Note:* Ability Score Increases are NO LONGER tied to Species in 2024 rules; they are now in Backgrounds.
- **Class Selection**
    - Select Class (Barbarian, Bard, etc.).
    - Apply Hit Die.
    - Select Primary Ability (visual guidance).
    - **Class Features (Level 1):** Automate immediate grants (e.g., Weapon Masteries for martial classes, Spellcasting for casters).
    - **Multiclassing Support:** logic for prerequisites and proficiency handling.
- **Background Selection** (Crucial 2024 Update)
    - **Ability Score Adjustments:** User chooses +2/+1 or +1/+1/+1 to specific stats defined by the Background.
    - **Origin Feat:** Automatically grant the specified Level 1 Feat.
    - **Proficiencies:** Grant 2 Skills and Tool proficiencies.
    - **Equipment:** Grant starting package + Gold.
- **Ability Scores**
    - Calculation Methods: Standard Array, Point Buy (27 points), Manual/Rolled Entry.
    - Validation against min/max limits (usually 20 cap for mortals).

### 1.2 Progression Choices
- **Subclass Selection:** (Usually Level 3, but check specific 2024 class progression).
- **Feats vs. ASI:** At levels 4, 8, etc., choose between distinct Feats or Ability Score Increases.
    - **Feat Filtering:** Filter by prerequisites (Level 4+, Stat requirements).
- **Spells:**
    - Source selection (Class list, Subclass specific spells).
    - Preparation Helper: warnings for "Known" vs "Prepared" limits.
- **Proficiencies:**
    - Skill selection (Class list).
    - Tool selection.
    - Language selection.

### 1.3 Equipment
- **Starting Gear:** Choose Class/Background packages or Gold buy.
- **Shop/Add Item:** Searchable database of PHB 2024 items.
- **Weapon Mastery:** For eligible classes, select which specific weapons have their Mastery properties active.

---

## 2. The Living Character Sheet

The sheet must be dynamic, calculating values in real-time based on state (Conditions, Equipped items, etc.).

### 2.1 Core Statistics (The Header)
- **Ability Scores & Modifiers:** Auto-calculated.
- **Proficiency Bonus:** Scaled by Total Character Level.
- **Inspiration:** Toggle (Heroic Inspiration - affects rerolls).
- **Initiative:** Dex mod + bonuses (e.g., Alert feat).
- **Speed:** Base + Species + Class bonuses (Unarmored Movement) + Item bonuses.
- **Armor Class (AC):**
    - Logic for Unarmored vs. Light/Medium/Heavy.
    - Shield calculation.
    - Application of magic items (+1 armor).
    - Conflict resolution (e.g., Monk Unarmored Defense vs. Barbarian Unarmored Defense - cannot stack).
- **Passive Perception/Investigation/Insight:** 10 + Mod + Proficiency.

### 2.2 Health & Status
- **Hit Points:**
    - Current / Max / Temporary.
    - Auto-calc Max HP based on Con mod + Level + Class average/rolled.
    - "Heal" and "Damage" input fields.
- **Hit Dice:** Track available/total (e.g., 3/5 d8). Feature to "Short Rest" and roll them.
- **Death Saves:** Success/Fail checkboxes. Auto-reset on stabilization/healing.
- **Exhaustion:** 2024 Rules (10 levels, subtracting from d20 rolls).
- **Conditions:**
    - List of standard conditions (Blinded, Charmed, etc.).
    - **Effect Automation:** Toggling "Prone" should imply Disadvantage on attacks (visual indicator) or movement cost.

### 2.3 Actions & Combat
- **Attacks:**
    - Pre-calculated "To Hit" (+Prof +Str/Dex +Magic).
    - Pre-calculated "Damage" (Dice +Mod +Magic).
    - **Weapon Mastery Integration:** Display functionality like "Push", "Sap", "Slow" on the attack entry if the character has Mastery in that weapon.
    - **Dual Wielding:** Logic for "Light" weapon off-hand attacks (Nick mastery property handling).
- **Actions Browser:**
    - Action / Bonus Action / Reaction / Free Object Interaction filters.
    - Special Actions: Dash, Disengage, Dodge, Help, Hide, Ready, Search, Study, Influence.
    - Class Actions: Rage, Bardic Inspiration, Second Wind.

### 2.4 Spellcasting
- **Slots:** Grid of Used/Total slots per level.
- **Casting Modifiers:** Spell Save DC, Spell Attack Bonus.
- **Spell List:**
    - Categorized by Level.
    - Indicators for Ritual, Concentration, Components (V,S,M).
    - **Upcasting:** Quick view of damage at higher tiers.
- **Resource Tracking:** Sorcery Points, Channel Divinity, Lay on Hands pool.

### 2.5 Inventory & encumbrance
- **Weight Calculation:** Current vs. Capacity (Str * 15).
- **Encumbrance Rules:** Visual warning (Speed drop) if variant rules active.
- **Attunement:** Max 3 slots. Prevent benefits if slot not allocated.
- **Containers:** Bags, Haversacks (weight reduction logic).
- **Currency:** CP, SP, EP, GP, PP handling.

### 2.6 Description & Notes
- **Traits/Ideals/Bonds/Flaws.**
- **Notes Section:** Free text.
- **Allies/Organizations.**

---

## 3. Complex Sub-Systems (The "Edge Cases")

These are the features that separate a basic calculator from a full emulator.

### 3.1 Shapeshifting & Transformations
- **Wild Shape (Druid):**
    - Browser for Beast stat blocks eligible by level (CR limits, Fly/Swim speed limits).
    - **Stat Merging:** Replace STR/DEX/CON, keep INT/WIS/CHA. Adopt Beast HP/Hit Dice logic.
    - **Feature Retention:** Logic to keep Class Features/Feats if the beast form allows it.
- **Polymorph/Shapechange:** Similar logic but fully replacing mental stats where applicable.
- **Hypothetical Forms:** Support for "Starry Form" (Druid) or "Form of Dread" (Warlock) which are overlays rather than replacements.

### 3.2 Minions & Companions
- **Pet Management:** Separate mini-sheet for Ranger Companion, Find Steed, or Homunculus.
- **Scaling:** Auto-scale pet stats based on Player Level or PB (Proficiency Bonus).
- **Summon Spells:** "Summon Undead", "Summon Beast" Tasha-style stat blocks that scale with Spell Level.

### 3.3 Multiclassing Complexities
- **Prerequisite Checking:** Enforce STR/DEX/etc. requirements before allowing the class add.
- **Proficiency Rules:** Logic to grant *only* specific proficiencies (e.g., Multiclassing into Fighter doesn't give Heavy Armor automatically).
- **Spell Slot Calculator:**
    - Combined Caster Level (Bard + Cleric).
    - Half-Caster math (Paladin/Ranger).
    - Third-Caster math (Arcane Trickster).
    - **Pact Magic:** Keep Warlock slots separate from Spellcasting slots but allow cross-usage.

---

## 4. Application Logic & Utilities

This is the backend logic required to support the UI.

- **Stacking Rules:** Prevent double proficiency (e.g., Skills) unless Expert. Correctly handle AC calculation preferences.
- **Modifier System:** A robust system where an object (Feat, Item, Spell Effect) can inject a modifier into a statistic.
    - *Example:* "Gauntlets of Ogre Power" sets STR score to 19.
    - *Example:* "Bless" adds 1d4 to Saving Throws and Attacks.
- **Rest System:**
    - **Short Rest:** Reset Warlock slots, Monk Ki, Fighter Action Surge. Roll Hit Dice.
    - **Long Rest:** Reset HP, Hit Dice (half max), Spell Slots, Long Rest cooldowns. Reduce Exhaustion.


---

## 5. Meta-Features (App Level)

### 5.1 Persistence
- **Local Storage:** JSON save files.

### 5.2 Customization
- **Portrait:** Image upload/crop.
- **Theme:** Dark/Light mode.

---

## 6. 2024 PHB Specific Nuances TO-DO List

- [ ] **Weapon Mastery System:** Needs a dedicated database linking Weapons <-> Properties, and a "Known Masteries" tracker for characters.
- [ ] **New Exhaustion Rules:** The -1 per stack linear penalty.
- [ ] **Origin Feats:** Ensure 1st level progression forces a Background selection that grants a Feat.
- [ ] **Spell Changes:** Update spell database with 2024 versions (e.g., *Guidance* reaction changes, *Barkskin* Bonus Action).
- [ ] **Stealth/Hiding:** New Condition "Invisible" logic when successfully creating the Hide action.
- [ ] **Inspiration:** Rename to "Heroic Inspiration" - distinct from Bardic Inspiration. Logic: Can be used to reroll *any* die, not just d20s? (Check specific 2024 final text, primarily d20 rerolls).

## 5. Metadata & Database Needs

- **Database of Spells:** Name, Level, School, Casting Time, Range, Components, Duration, Description, Scaling.
- **Database of Items:** Weapons (Damage, Props, Mastery), Armor (AC, Dex Cap, Str Min, Stealth Disadv), Gear.
- **Database of Features:** Class/Subclass features with "Level Unlocked" triggers.
- **Database of Monsters:** (For Druid Wildshape or Ranger Companion stats).
