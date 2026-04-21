# TibiaCore Spell Authoring Guide

A comprehensive reference for creating spells in TibiaCore — covering XML registration, Lua scripting, large effect centering, vocation design, and testing.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Spell XML Registration (spells.xml)](#2-spell-xml-registration-spellsxml)
3. [Lua Script Structure](#3-lua-script-structure)
4. [The Big Effect / Centered Spell System](#4-the-big-effect--centered-spell-system)
5. [Designing Spell Progression (Level Tiers)](#5-designing-spell-progression-level-tiers)
6. [AoE Area Examples](#6-aoe-area-examples)
7. [Vocation-Specific Design Guidelines](#7-vocation-specific-design-guidelines)
8. [Quick Reference: Effect IDs by Element](#8-quick-reference-effect-ids-by-element)
9. [Full Spell Script Template (Production Quality)](#9-full-spell-script-template-production-quality)
10. [Testing Checklist](#10-testing-checklist)

---

## 1. Overview

TibiaCore spells are defined in two parts:

- **XML definition** — registered in `server/data/spells/spells.xml`. Declares the spell's metadata: name, cast words, vocation restrictions, level/mana requirements, and which Lua script to load.
- **Lua script** — lives in `server/data/spells/scripts/`. Contains the actual combat logic: damage type, formula, AoE area, and conditions.

TibiaCore also supports a **pixel offset centering system** for large multi-tile effects. Standard Tibia effects are anchored to a single tile; oversized effects (e.g. a 5×5 ice explosion sprite) would render off-center without correction. The offset system lets you shift the rendered effect by a configurable number of pixels so it lines up exactly with the target tile.

---

## 2. Spell XML Registration (spells.xml)

All spells must have an entry in `server/data/spells/spells.xml` before they will function in-game.

### 2.1 Instant Spell (cast from memory / hotkey)

```xml
<instant
    name="Arcane Nova"
    words="exevo arcana hur"
    group="attack"
    type="instant"
    level="50"
    mana="180"
    range="0"
    effect="75"
    needlearn="0"
    script="mage/arcane_nova.lua"
>
    <vocation name="Mage" lastlevel="200" />
    <vocation name="Archmage" />
    <vocation name="Blood Mage" />
</instant>
```

### 2.2 Rune Spell

```xml
<rune
    name="Ice Strike Rune"
    runeId="2304"
    group="attack"
    type="rune"
    level="25"
    magicLevel="4"
    range="6"
    effect="53"
    script="runes/ice_strike_rune.lua"
>
    <vocation name="Mage" />
    <vocation name="Archmage" />
</rune>
```

### 2.3 Conjure Spell

```xml
<instant
    name="Conjure Ice Rune"
    words="adori gran frigo"
    group="support"
    type="instant"
    level="25"
    mana="120"
    soul="2"
    needlearn="0"
    script="conjure/conjure_ice_rune.lua"
>
    <vocation name="Mage" />
</instant>
```

### 2.4 Field Reference — All XML Attributes

| Attribute      | Description |
|----------------|-------------|
| `name`         | Display name shown in-game spell list |
| `words`        | Cast incantation (must be globally unique) |
| `group`        | `attack`, `healing`, `support`, or `special` |
| `type`         | `instant` or `rune` |
| `level`        | Minimum character level to cast |
| `mana`         | Mana cost per cast |
| `soul`         | Soul point cost (conjure spells) |
| `range`        | Maximum target range in tiles (0 = self/AoE) |
| `effect`       | Visual effect ID played on cast (optional hint; logic is in Lua) |
| `needlearn`    | `1` = must be learned from NPC; `0` = available automatically |
| `script`       | Path relative to `server/data/spells/scripts/` |
| `<vocation>`   | One entry per allowed vocation; `lastlevel` caps the vocation to a level range |

### 2.5 Available Vocations

| ID | Name |
|----|------|
| 0  | Rookie |
| 1  | Mage |
| 2  | Archer |
| 3  | Knight |
| 4  | Occultist |
| 5  | Archmage |
| 6  | Necromancer |
| 7  | Marksman |
| 8  | Beastmaster |
| 9  | Templar |
| 10 | Death Knight |
| 11 | Blood Mage |
| 12 | Heretic |

> **Note:** Vocation names in XML must match exactly (including capitalisation and spaces). A mismatch produces a `Wrong vocation name` warning in the server log on startup.

---

## 3. Lua Script Structure

### 3.1 Minimal Template

```lua
local combat = Combat()
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_ENERGYDAMAGE)
combat:setParameter(COMBAT_PARAM_EFFECT, 12) -- effect ID played on target tile
combat:setFormula(COMBAT_FORMULA_LEVELMAGIC, -1, 0, -1, 0)

function onCastSpell(creature, variant)
    return combat:execute(creature, variant)
end
```

### 3.2 Damage Types

Pass one of the following constants to `COMBAT_PARAM_TYPE`:

| Constant | Element |
|----------|---------|
| `COMBAT_PHYSICALDAMAGE` | Physical |
| `COMBAT_FIREDAMAGE` | Fire |
| `COMBAT_ICEDAMAGE` | Ice / Cold |
| `COMBAT_ENERGYDAMAGE` | Lightning / Energy |
| `COMBAT_EARTHDAMAGE` | Nature / Poison (instant) |
| `COMBAT_HOLYDAMAGE` | Holy / Light |
| `COMBAT_DEATHDAMAGE` | Death / Dark |
| `COMBAT_HEALINGDAMAGE` | Healing (positive value) |
| `COMBAT_MAGICDAMAGE` | Arcane / Magic |

### 3.3 Setting an AoE Area

Use `createCombatArea()` with a 2-D table (see [Section 6](#6-aoe-area-examples) for full shape library):

```lua
local AREA_3x3 = {
    {1, 1, 1},
    {1, 3, 1},  -- 3 marks the caster's/origin tile
    {1, 1, 1}
}

local combat = Combat()
combat:setArea(createCombatArea(AREA_3x3))
```

### 3.4 Multiple Combat Objects in One Cast

Useful for spells that deal two damage types simultaneously (e.g. fire + physical):

```lua
local combat1 = Combat()
combat1:setParameter(COMBAT_PARAM_TYPE, COMBAT_FIREDAMAGE)
combat1:setParameter(COMBAT_PARAM_EFFECT, 1)
combat1:setFormula(COMBAT_FORMULA_LEVELMAGIC, -1.5, 0, -1.0, 0)

local combat2 = Combat()
combat2:setParameter(COMBAT_PARAM_TYPE, COMBAT_PHYSICALDAMAGE)
combat2:setParameter(COMBAT_PARAM_EFFECT, 6)
combat2:setFormula(COMBAT_FORMULA_LEVELMAGIC, -0.5, 0, -0.3, 0)

function onCastSpell(creature, variant)
    combat1:execute(creature, variant)
    return combat2:execute(creature, variant)
end
```

### 3.5 Applying Conditions

```lua
local condition = Condition(CONDITION_FIRE)   -- or CONDITION_POISON, CONDITION_FREEZE, etc.
condition:setParameter(CONDITION_PARAM_DELAYED, true)
condition:setParameter(CONDITION_PARAM_TICKS, 10000)     -- duration in ms
condition:setParameter(CONDITION_PARAM_TICKINTERVAL, 2000)
condition:setParameter(CONDITION_PARAM_DAMAGE, -30)      -- damage per tick (negative = damage)

local combat = Combat()
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_FIREDAMAGE)
combat:setParameter(COMBAT_PARAM_EFFECT, 1)
combat:addCondition(condition)
combat:setFormula(COMBAT_FORMULA_LEVELMAGIC, -1.5, 0, -1.0, 0)

function onCastSpell(creature, variant)
    return combat:execute(creature, variant)
end
```

Common condition types: `CONDITION_FIRE`, `CONDITION_POISON`, `CONDITION_FREEZE`, `CONDITION_ENERGY`, `CONDITION_DROWN`, `CONDITION_CURSED`, `CONDITION_BLEEDING`.

---

## 4. The Big Effect / Centered Spell System

### 4.1 The Problem

Tibia's rendering engine anchors every effect sprite to the top-left of a single tile. Large multi-tile sprites (e.g. a 5×5 ice explosion painted as a single image) therefore appear shifted up and to the left of their intended target when played at the target's tile position.

### 4.2 How the Offset System Works

TibiaCore's OTClient exposes a global pixel offset that is applied to **all effects rendered during the next frame**:

```lua
g_game.setEffectOffset(x, y, z)
```

- **x / y** — pixel shift relative to the target tile's screen position.
- **z** — reserved (set to `0`).
- The offset is consumed (reset to zero) after one frame, so it only affects the effect you trigger immediately after setting it.
- **Default global offset** set in `client/init.lua`: `(321, 60, 0)`.

The offset is communicated from server to client via the **extended opcode system** — the spell's server-side Lua script sends an opcode payload containing the desired offset values, and a registered client-side handler calls `g_game.setEffectOffset()` before the effect packet is processed.

### 4.3 Workflow for a Large Effect

1. Trigger the effect on the server at the target position as normal.
2. Before or alongside the effect, send an extended opcode with the desired pixel offset.
3. The client module receives the opcode, calls `g_game.setEffectOffset(x, y, z)`, and the engine applies the correction when painting the effect sprite.

### 4.4 Offset Tuning Workflow

1. Start with the **default global offset** `(321, 60, 0)` — correct for effect ID 53 (ice5x5).
2. Use the `!setoffset <x> <y>` talkaction in-game (if available) to live-tune values.
3. Cast the spell repeatedly, adjusting x/y until the large sprite is visually centered on the target tile.
4. Record the final offset values as constants at the top of the spell's Lua script.

### 4.5 Recommended Large Effects and Their Offsets

| Effect ID | Name | X Offset | Y Offset |
|-----------|------|----------|----------|
| 53 | Ice Glacier (ice5x5) | 321 | 60 |
| 202 | Massive Ice Ball | 240 | 80 |
| 239 | Ice Crown Explosion | 280 | 70 |
| 241 | Purple Mandala | 260 | 65 |
| 320 | Fire Bomb Large | 200 | 80 |
| 321 | Ice Sword Pillar *(EPIC)* | 300 | 100 |
| 34 | Blue Dragon | 200 | 120 |
| 50 | Golden Fire Dragon | 200 | 80 |
| 72 | Undead Knight Scene | 250 | 90 |
| 172 | Dark Demonic Beast | 270 | 85 |
| 318 | Spider Web Large | 240 | 60 |

> Offsets are starting points. Always verify visually in-game before shipping.

---

## 5. Designing Spell Progression (Level Tiers)

### 5.1 Tier Definitions

| Tier | Level Range | Design Goals |
|------|------------|--------------|
| **1 — Basic** | 1–20 | Small effects, single target, moderate mana. Establishes the vocation's identity. |
| **2 — Advanced** | 20–50 | Medium effects, small AoE (3×3 or cross), meaningfully higher mana. |
| **3 — Expert** | 50–100 | Visually impressive effects, medium AoE (3×3 to 5×5), significant mana investment. |
| **4 — Master** | 100–200 | Large effects (consider offset system), wide AoE, defining vocation moments. |
| **5 — Ultimate** | 200+ | LARGE/EPIC effects with full offset tuning, widest AoE, signature moves that feel earned. |

### 5.2 Per-Vocation Progression Example — Mage

| Level | Spell | Effect ID | Notes |
|-------|-------|-----------|-------|
| 1 | Magic Arrow | 2 | Basic ranged arcane bolt |
| 8 | Fire Bomb | 1 | First AoE; 3×3 fire |
| 20 | Ice Wave | 11 | Frontal cone, 5-tile range |
| 50 | Arcane Nova | 75 | Medium 3×3 AoE, arcane burst |
| 100 | Blizzard | 202 | LARGE ice explosion, offset required |
| 200 | Glacier Strike | 321 | EPIC ice sword pillar, ultimate |

Apply this pattern to every vocation — each tier should feel like a meaningful power jump, and Ultimate spells should use the largest, most visually striking effects available.

---

## 6. AoE Area Examples

Area tables are passed to `createCombatArea()`. Cell values:

- `0` — not affected
- `1` — affected tile
- `3` — origin tile (caster position or targeted center)

```lua
-- Single target (no AoE table needed; pass no area to Combat)

-- Cross / plus shape (3×3)
local AREA_CROSS = {
    {0, 1, 0},
    {1, 3, 1},
    {0, 1, 0}
}

-- 3×3 square
local AREA_3x3 = {
    {1, 1, 1},
    {1, 3, 1},
    {1, 1, 1}
}

-- Diamond (5×5)
local AREA_DIAMOND = {
    {0, 0, 1, 0, 0},
    {0, 1, 1, 1, 0},
    {1, 1, 3, 1, 1},
    {0, 1, 1, 1, 0},
    {0, 0, 1, 0, 0}
}

-- 5×5 full square
local AREA_5x5 = {
    {1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1},
    {1, 1, 3, 1, 1},
    {1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1}
}

-- Frontal cone (3 tiles wide, 3 tiles deep — facing south as example)
local AREA_CONE_S = {
    {0, 0, 0},
    {0, 3, 0},
    {1, 1, 1},
    {1, 1, 1},
    {0, 1, 0}
}
```

> For directional areas (cone, line), supply a second table variant per direction to `createCombatArea()` and use `DIRECTION_` constants.

---

## 7. Vocation-Specific Design Guidelines

### 7.1 Mage / Archmage / Blood Mage

- **Primary damage**: Arcane, Fire, Ice
- **Playstyle**: High burst, glass cannon, large AoE specialist
- **Best effects**: 1, 2, 53, 75, 202, 239, 241, 321
- **Signature ultimate**: Ice Sword Pillar (321) or Purple Mandala (241)
- **Design note**: Mages should have the widest AoE at high tiers but comparatively low survivability. Ultimate spells should feel cinematic.

### 7.2 Cleric / Templar

- **Primary damage**: Holy; secondary: Healing
- **Playstyle**: Support/hybrid, moderate tank capability
- **Best effects**: 3, 8, 19, 56, 270, 313
- **Signature ultimate**: Golden Sunburst (270), Green Crystal (313)
- **Design note**: Balance offensive and healing spells roughly 50/50. Healing spells use `COMBAT_HEALINGDAMAGE` with a positive formula multiplier.

### 7.3 Archer / Marksman

- **Primary damage**: Physical, Earth; secondary: Fire
- **Playstyle**: Ranged DPS, precision strikes, traps
- **Best effects**: 6, 13, 22, 235, 248, 260, 304
- **Signature ultimate**: Sniper Lock (235) + meteor (248) combo
- **Design note**: Favour linear / directional AoE shapes over squares to reflect precision archery.

### 7.4 Knight / Death Knight

- **Primary damage**: Physical; secondary: Death
- **Playstyle**: Melee sustain, charge abilities, gap-closers
- **Best effects**: 22, 52, 60, 264, 275, 311, 306
- **Signature ultimate**: Cross Slash (306), Claw Strike (311)
- **Design note**: Keep AoE shapes tight (cross, small square). High damage, low range. Death Knight variants can use Death damage and darker visuals.

### 7.5 Occultist / Necromancer / Heretic

- **Primary damage**: Death, Poison; secondary: Dark AoE
- **Playstyle**: DoT application, summons, debuffs, AoE corruption
- **Best effects**: 5, 26, 38, 65, 172, 267, 275, 292, 294, 312, 314
- **Signature ultimate**: Dark Demonic Beast (172), Shadow Orb (294)
- **Design note**: Lean into conditions (bleed, poison, curse). Large AoE corruption spells work well at master/ultimate tiers. Effect 172 is a big-effect candidate requiring offset tuning.

---

## 8. Quick Reference: Effect IDs by Element

Use these lists to pick a visually appropriate effect for any spell.

| Element | Effect IDs |
|---------|-----------|
| **Fire** | 1, 7, 27, 41, 66, 184, 204, 229, 234, 261, 271, 276, 277, 278, 279, 319, 320 |
| **Ice** | 11, 23, 40, 53, 63, 185, 205, 225, 239, 247, 250, 254, 280, 281, 282, 283, 284, 321 |
| **Lightning** | 12, 230, 246 |
| **Nature / Poison** | 4, 10, 18, 25, 30, 37, 45, 64, 73, 169, 177, 186, 190, 191, 197, 233, 236, 286, 304, 310 |
| **Dark / Death** | 5, 26, 38, 52, 65, 69, 196, 203, 209, 267, 273, 285, 286, 294 |
| **Holy / Light** | 3, 8, 19, 29, 42, 48, 56, 68, 175, 179, 207, 217, 219, 257, 270, 280, 313, 315, 316 |
| **Arcane / Magic** | 2, 9, 15, 28, 44, 47, 54, 75, 152, 155, 200, 201, 228, 233, 241, 245, 255, 288, 289, 292, 314 |
| **Physical** | 6, 13, 22, 60, 198, 260, 290, 311 |
| **Wind / Feather** | 199, 231, 232, 236, 252, 253, 258, 307, 317 |

> IDs marked in the [Recommended Large Effects](#45-recommended-large-effects-and-their-offsets) table require offset tuning before shipping.

---

## 9. Full Spell Script Template (Production Quality)

Save as `server/data/spells/scripts/<vocation>/<spell_name>.lua`.

```lua
-- arcane_nova.lua
-- Vocation: Mage / Archmage / Blood Mage
-- Level Required: 50
-- Effect: Arcane Nova (effect ID 75)
-- Type: AoE, Arcane damage, 3×3 square

-- ──────────────────────────────────────────────
-- Area Definition
-- ──────────────────────────────────────────────
local AREA_3x3 = {
    {1, 1, 1},
    {1, 3, 1},
    {1, 1, 1}
}

-- ──────────────────────────────────────────────
-- Combat Setup
-- ──────────────────────────────────────────────
local combat = Combat()
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_MAGICDAMAGE)
combat:setParameter(COMBAT_PARAM_EFFECT, 75)
combat:setArea(createCombatArea(AREA_3x3))

-- Formula: (level * multiplierMin + flatMin) to (level * multiplierMax + flatMax)
-- At level 50 with magic level ~40 this yields roughly 300–500 damage.
combat:setFormula(COMBAT_FORMULA_LEVELMAGIC, -2.0, 0, -1.5, 0)

-- ──────────────────────────────────────────────
-- Cast Handler
-- ──────────────────────────────────────────────
function onCastSpell(creature, variant)
    return combat:execute(creature, variant)
end
```

### Large Effect Variant (with offset)

```lua
-- glacier_strike.lua
-- Vocation: Archmage
-- Level Required: 200
-- Effect: Ice Sword Pillar (effect ID 321) — LARGE, requires offset
-- Type: AoE, Ice damage, 5×5 square

local EFFECT_ID     = 321
local EFFECT_OFFSET_X = 300
local EFFECT_OFFSET_Y = 100

local AREA_5x5 = {
    {1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1},
    {1, 1, 3, 1, 1},
    {1, 1, 1, 1, 1},
    {1, 1, 1, 1, 1}
}

local combat = Combat()
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_ICEDAMAGE)
combat:setParameter(COMBAT_PARAM_EFFECT, EFFECT_ID)
combat:setArea(createCombatArea(AREA_5x5))
combat:setFormula(COMBAT_FORMULA_LEVELMAGIC, -5.0, 0, -3.5, 0)

function onCastSpell(creature, variant)
    -- Send offset opcode to client so the large sprite centres on the target.
    -- Replace OPCODE_EFFECT_OFFSET with the registered opcode number used in your server build.
    local targetPos = variant:getPosition()
    if targetPos then
        Game.broadcastMessage(
            string.format("effectoffset %d %d %d", EFFECT_OFFSET_X, EFFECT_OFFSET_Y, 0),
            MESSAGE_STATUS_DEFAULT
        )
        -- In production: use sendExtendedOpcode() or the equivalent server API
        -- to transmit EFFECT_OFFSET_X / EFFECT_OFFSET_Y to the affected clients.
    end
    return combat:execute(creature, variant)
end
```

---

## 10. Testing Checklist

Work through each item before considering a spell ready to ship.

- [ ] Spell appears in the `!spells` output for every intended vocation
- [ ] Spell is **not** available to vocations that should be excluded
- [ ] Spell activates at the correct minimum level (and not below)
- [ ] Mana cost is appropriate — neither trivially cheap nor prohibitive for the tier
- [ ] Casting words are unique (no conflict with any existing spell in `spells.xml`)
- [ ] Visual effect fires correctly on the target tile
- [ ] **If using a LARGE effect**: effect is visually centered on the target after offset tuning
- [ ] **If using a LARGE effect**: offset constants are documented in the script header
- [ ] Damage range is balanced against other spells of the same tier and vocation
- [ ] AoE area matches the intended shape (test on a flat floor with multiple targets)
- [ ] Conditions (if any) apply, tick correctly, and expire on time
- [ ] Server log shows **no** `Wrong vocation name` warnings after restart
- [ ] Spell behaves consistently when cast by players at the minimum level vs. high-level players
- [ ] No Lua errors in the server log when the spell is cast
