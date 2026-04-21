# TibiaCore — Spell System QA Report
**QA Lead:** Vesemir  
**Date:** 2025-07-15  
**Scope:** Spell system overhaul — spells.xml, 38 new Lua scripts, `!spells` talkaction

---

## Overall Verdict: ❌ NEEDS FIXES

**3 critical issues must be resolved before this can go to test.**

---

## Check 1 — Vocation Names

> Valid names: Rookie, Mage, Archer, Knight, Occultist, Archmage, Necromancer, Marksman, Beastmaster, Templar, Death Knight, Blood Mage, Heretic

**Result: ✅ PASS**

All `<vocation name="...">` tags in spells.xml match exactly one of the 13 valid vocation names. No typos, no obsolete names found.

---

## Check 2 — Script Files Exist

**Result: ✅ PASS**

All 38 script files referenced by player spells in spells.xml exist on disk.

| Directory | Files Found | Referenced |
|---|---|---|
| `scripts/attack/` | 38 | All 35 unique attack scripts ✅ |
| `scripts/healing/` | 7 | All 7 healing scripts ✅ |
| `scripts/support/` | 9 | All 9 support scripts ✅ |

Note: `attack/divine_caldera.lua` is shared between two spells (see Warn #3 below).

---

## Check 3 — Duplicate spellid Values

**Result: ✅ PASS**

No duplicate `spellid` values found across all 55 player spell entries.

---

## Check 4 — Duplicate Spell Names

**Result: ✅ PASS**

No duplicate `name` values found. All 55 player spells have unique names.

---

## Check 5 — Duplicate `words` Values

**Result: ❌ FAIL — 4 collisions**

TFS performs word-to-spell lookup globally. Duplicate words on different spells **will** cause one spell to shadow the other depending on load order.

| # | Shared Words | Spell A | Vocation(s) | Spell B | Vocation(s) | Lines |
|---|---|---|---|---|---|---|
| 1 | `exori mort` | Soul Drain (spellid=207) | Necromancer | Shadow Bolt (spellid=229) | Occultist, Blood Mage, Heretic | 33 vs 199 |
| 2 | `utevo res` | Raise Dead (spellid=209) | Necromancer | Call Beast (spellid=217) | Beastmaster | 69 vs 128 |
| 3 | `exevo mas san` | Consecrate (spellid=225) | Templar | Sacred Nova (spellid=124) | Occultist, Blood Mage, Heretic | 166 vs 209 |
| 4 | `exevo gran mort` | Death Storm (spellid=210) | Necromancer | Hemorrhage (spellid=233) | Blood Mage | 48 vs 229 |

**Fix required:** Each spell must have unique `words`. Suggested replacements:

| Spell | Current Words | Suggested Replacement |
|---|---|---|
| Shadow Bolt | `exori mort` | `exori vis mort` |
| Call Beast | `utevo res` | `utevo ven` |
| Sacred Nova | `exevo mas san` | `exevo mas san ico` |
| Hemorrhage | `exevo gran mort` | `exevo gran mas mort` |

---

## Check 6 — XML Structure

**Result: ❌ FAIL — CRITICAL: Malformed XML**

The `</spells>` root closing tag appears at **line 312**, but the file continues with a verbatim duplicate of all House Spells and all 51 Monster Spells through **line 371**, which ends with a second `</spells>` tag.

```
line 311:  <instant name="dipthrah skill reducer" ... />
line 312:  </spells>            ← ROOT CLOSED HERE
line 313:  <!-- House Spells -->  ← CONTENT OUTSIDE ROOT
line 314:  <instant name="Edit Door" ... />
  ...
line 371:  </spells>            ← SECOND CLOSING TAG (invalid)
```

Any strict XML parser will reject the file. On lenient parsers (like the one TFS uses), only the first 312 lines are parsed — meaning **all monster spells are silently dropped** from the server's spell registry.

**Fix required:** Delete lines 313–371 entirely. The content is an exact duplicate of what already appears at lines 254–311 inside the valid root element.

---

## Check 7 — talkactions.xml & spells_list.lua

**Result: ✅ PASS**

- `!spells` entry confirmed at `talkactions.xml` line 52:
  ```xml
  <talkaction words="!spells" separator=" " script="spells_list.lua" />
  ```
- `server/data/talkactions/scripts/spells_list.lua` exists ✅
- Script logic covers all 12 player vocations (IDs 1–12); Rookie (id=0) correctly returns a "no spells yet" message.

---

## Check 8 — Lua Syntax

**Result: ✅ PASS (with warnings)**

All 54 Lua scripts reviewed. No blocking syntax errors:

| Rule | Status |
|---|---|
| `Combat()` created at module level (not inside onCastSpell) | ✅ All scripts compliant |
| `onCastSpell` uses `return combat:execute(...)` | ✅ All scripts compliant |
| No missing `end` for function blocks | ✅ All scripts compliant |
| No bare `combat:execute(...)` without `return` | ✅ All scripts compliant |

### Lua Warnings (non-blocking)

**⚠️ WARN-1:** `attack/energy_strike.lua` line 9
```lua
return -min, -min   -- max is computed on line 8 but silently discarded
```
The local `max` variable is calculated but never returned. The spell deals min=max damage. May be intentional for a lock-on bolt, but worth confirming.

**⚠️ WARN-2:** `attack/corruption.lua` and `attack/crimson_wave.lua` — identical content
Both files use `COMBAT_DEATHDAMAGE`, `CONST_ME_MORTAREA`, and the exact same formula (`magicLevel * 3.2 + 35` / `magicLevel * 5.0 + 60`). These are distinct spells (Heretic Lv.70 vs Blood Mage Lv.75) — likely a copy-paste error where `crimson_wave.lua` was never properly differentiated.

**⚠️ WARN-3:** `attack/divine_caldera.lua` shared between two vocations
- Arrow Volley (spellid=1003, Archer/Marksman/Beastmaster, Lv.50) — physical/ranged
- Sacred Nova (spellid=124, Occultist/Blood Mage/Heretic, Lv.50) — holy/nova
Both use `COMBAT_HOLYDAMAGE` + `CONST_ME_HOLYAREA` + `AREA_CIRCLE3X3`. An archer "Arrow Volley" dealing holy AoE damage seems unintentional.

**⚠️ WARN-4:** `support/call_beast.lua` and `support/raise_dead.lua` — unused Combat object
Both scripts create a `Combat()` at module level but `onCastSpell` never calls `combat:execute()`. The combat object is dead code. These are marked TODO placeholders — acceptable for now, but flag for pre-release cleanup.

---

## Issues Summary

| # | Severity | File | Issue |
|---|---|---|---|
| 1 | ❌ CRITICAL | `spells.xml` lines 313–371 | Duplicate content after `</spells>` — invalid XML, monster spells may be dropped |
| 2 | ❌ FAIL | `spells.xml` lines 33 & 199 | Duplicate words `"exori mort"` (Soul Drain vs Shadow Bolt) |
| 3 | ❌ FAIL | `spells.xml` lines 69 & 128 | Duplicate words `"utevo res"` (Raise Dead vs Call Beast) |
| 4 | ❌ FAIL | `spells.xml` lines 166 & 209 | Duplicate words `"exevo mas san"` (Consecrate vs Sacred Nova) |
| 5 | ❌ FAIL | `spells.xml` lines 48 & 229 | Duplicate words `"exevo gran mort"` (Death Storm vs Hemorrhage) |
| 6 | ⚠️ WARN | `attack/energy_strike.lua` line 9 | `return -min, -min` — max value discarded |
| 7 | ⚠️ WARN | `attack/corruption.lua` & `crimson_wave.lua` | Identical file content — copy-paste error suspected |
| 8 | ⚠️ WARN | `attack/divine_caldera.lua` (shared) | Archer "Arrow Volley" uses holy AoE damage script |
| 9 | ⚠️ WARN | `support/call_beast.lua`, `raise_dead.lua` | Combat() created but never executed (TODO stubs) |

---

## Fix Checklist

- [ ] **spells.xml** — Delete lines 313–371 (duplicate block after `</spells>`)
- [ ] **spells.xml** — Rename `words` for Shadow Bolt: `exori mort` → `exori vis mort`
- [ ] **spells.xml** — Rename `words` for Call Beast: `utevo res` → `utevo ven`
- [ ] **spells.xml** — Rename `words` for Sacred Nova: `exevo mas san` → `exevo mas san ico`
- [ ] **spells.xml** — Rename `words` for Hemorrhage: `exevo gran mort` → `exevo gran mas mort`
- [ ] **spells_list.lua** — Update matching `words` strings in vocationSpells table after above renames
- [ ] *(Low priority)* `attack/crimson_wave.lua` — Differentiate from `corruption.lua`
- [ ] *(Low priority)* `attack/divine_caldera.lua` — Consider separate script for Arrow Volley (physical/ranged damage)
