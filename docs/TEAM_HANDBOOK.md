# TibiaCore Team Handbook

> All team members must read this document before contributing. It defines roles, workflows, standards, and references.

---

## Table of Contents

1. [Team Roster](#team-roster)
2. [Workflows](#workflows)
   - [Adding a New Spell](#adding-a-new-spell)
   - [Adding a New Vocation](#adding-a-new-vocation)
3. [Visual Effect Guidelines](#visual-effect-guidelines)
4. [Vocation Balance Standards](#vocation-balance-standards)
5. [Code Standards](#code-standards)
6. [Documentation Standards](#documentation-standards)
7. [Key Reference Files](#key-reference-files)

---

## Team Roster

### Design & Architecture

| Role | Responsibilities |
|------|-----------------|
| **Lead Designer** | Overall vision, feature approval, vocation balance sign-off |
| **System Architect** | C++ engine changes, protocol design, performance |
| **Spell Specialist A** — Fire/Ice Magic | Designs all Mage, Archmage, BloodMage spells |
| **Spell Specialist B** — Holy/Nature | Designs Cleric, Templar, Archer, Marksman spells |
| **Spell Specialist C** — Dark/Death | Designs Occultist, Necromancer, Heretic, DeathKnight spells |
| **Vocation Balance Expert** | Ensures DPS, survivability, and utility are balanced across all 12 vocations; runs DPS tracker benchmarks |
| **OTClient Module Expert** | Expert on all 19+ client modules, shader system, and UI development |

### Development

| Role | Responsibilities |
|------|-----------------|
| **Backend Dev A** | Server-side Lua, talkactions, creature scripts |
| **Backend Dev B** | Monster AI, loot tables, item system |
| **Frontend Dev A** | OTClient UI modules, widgets, client Lua |
| **Frontend Dev B** | Shader effects, rendering, visual polish |
| **C++ Engineer** | Engine modifications, protocol extensions, performance |

### QA & Testing

| Role | Responsibilities |
|------|-----------------|
| **QA Lead** | Test planning, regression tracking, sign-off gating |
| **QA Tester A** | Functional testing — spells, vocations, systems |
| **QA Tester B** | Content testing — items, monsters, loot |
| **Performance Tester** | Server load testing, client FPS profiling, memory analysis |
| **Balance Tester** | Per-vocation DPS benchmarking on training dummy, spell comparison |

---

## Workflows

### Adding a New Spell

```
1. Spell Specialist drafts design
      └─ Damage type, effect ID, level requirement, mana cost, AoE shape

2. Vocation Balance Expert reviews
      └─ Compare vs tier benchmark (see Vocation Balance Standards)

3. Backend Dev implements
      └─ server/data/spells/spells.xml  (registration)
      └─ server/data/spells/scripts/    (Lua logic)

4. If the spell uses a LARGE effect:
      └─ Frontend Dev tunes offset via g_game.setEffectOffset()
      └─ Document offset in docs/EFFECTS_MAPPING.md

5. QA Tester A verifies:
      └─ Spell appears in !spells output
      └─ Correct level gate enforced
      └─ Damage range within design spec

6. Balance Tester runs DPS benchmark on training dummy

7. QA Lead signs off → merge
```

### Adding a New Vocation

```
1. Lead Designer defines
      └─ Role (tank / DPS / support / hybrid)
      └─ Base stats (HP, MP, speed, carry weight)
      └─ Gear restrictions

2. Spell Specialists draft spell lists
      └─ 5 tiers × 5 spells minimum = 25 spells total
      └─ Each tier must satisfy minimum spell requirements (see Balance Standards)

3. Backend Dev implements
      └─ server/data/XML/vocations.xml     — add vocation entry
      └─ server/data/talkactions/scripts/setvocation.lua  — add to switch logic
      └─ vocation_modal.lua               — add to selection UI data

4. QA verifies
      └─ !vocation command shows correct modal entry
      └─ Gear swap works (correct restrictions applied)
      └─ !spells output lists all spells for the new vocation

5. Balance Tester runs full DPS comparison
      └─ Benchmark against all existing vocations at same level tiers
      └─ Confirm results are within allowed variance (see Balance Standards)

6. QA Lead signs off → merge
```

---

## Visual Effect Guidelines

### Effect categories

| Category | Effect IDs | Notes |
|----------|-----------|-------|
| Standard single-tile | 1–76, 151–230 | Use freely; no offset tuning needed |
| LARGE multi-tile / AoE | 34, 43, 50, 51, 53, 72, 172, 202, 239, 241, 313–315, 318, 320, 321 | **Must have offset tuning documented** |

### Ultimate spell effects (preferred)

| Effect ID | Visual | Intended use |
|-----------|--------|-------------|
| 321 | Ice Sword | Ultimate ice / cold abilities |
| 241 | Purple Mandala | Ultimate arcane / void abilities |
| 320 | Fire Bomb | Ultimate fire / explosion abilities |

### Rules

- All new effect IDs must be **verified** against `docs/EFFECTS_MAPPING.md` before use.
- LARGE effects **must** have their `g_game.setEffectOffset()` call documented in `docs/EFFECTS_MAPPING.md`.
- Multi-tile AoE spells that use standard effects must confirm tile coverage in QA.
- Do not reuse an effect for a new spell if it would create visual ambiguity in combat.

---

## Vocation Balance Standards

### DPS targets (measured on training dummy, same level)

| Archetype | Allowed DPS variance |
|-----------|---------------------|
| Pure DPS (Mage, Archmage, BloodMage, Archer, Marksman, Occultist, Necromancer) | Within **±10%** of tier-equivalent vocations |
| Tanks (Knight, Templar, DeathKnight) | Up to **−20%** DPS for higher survivability offset |
| Supports (Templar, Heretic) | Up to **−30%** DPS for healing/utility offset |

### Minimum spell requirements per vocation

Each vocation **must** have, per tier (5 tiers total):

- **1 instant single-target spell** (direct damage or effect)
- **1 AoE spell** (damages/affects multiple tiles)
- **1 utility spell** (heal, buff, debuff, summon, trap, or crowd control)
- **1 ultimate ability** at Level 200+ using a LARGE effect

### Benchmark procedure

1. Create test character at target level with standard gear for vocation.
2. Run 60-second continuous DPS test on training dummy.
3. Record average DPS output.
4. Compare against the reference sheet maintained by the Vocation Balance Expert.
5. Results must be within allowed variance before QA Lead sign-off.

---

## Code Standards

### File locations

| Content | Path |
|---------|------|
| Spell scripts | `server/data/spells/scripts/` |
| Spell registrations | `server/data/spells/spells.xml` |
| Talkaction scripts | `server/data/talkactions/scripts/` |
| Talkaction registrations | `server/data/talkactions/talkactions.xml` |
| Vocation definitions | `server/data/XML/vocations.xml` |

### Lua script rules

- **No magic numbers** — define named constants at the top of each script.
- **Comment non-obvious logic** — a single line explaining *why*, not *what*.
- After any XML change, **restart the server and check the console** for warnings or errors before committing.
- Scripts must not `print()` to console in production paths (use `Game.broadcastMessage` or logging utilities instead).

### Example constant block

```lua
-- spell: Inferno Wave
local DAMAGE_MIN    = 800
local DAMAGE_MAX    = 1200
local MANA_COST     = 340
local COOLDOWN_MS   = 4000
local EFFECT_ID     = 172   -- see docs/EFFECTS_MAPPING.md
local AREA_RADIUS   = 3
```

---

## Documentation Standards

| Trigger | Required update |
|---------|----------------|
| New gameplay system added | `docs/SYSTEMS_OVERVIEW.md` |
| New effect ID used in a spell | `docs/EFFECTS_MAPPING.md` (include offset if LARGE) |
| New OTClient module created | `docs/OTCLIENT_MODULES_GUIDE.md` |
| New spell authoring pattern | `docs/SPELL_AUTHORING_GUIDE.md` |
| New opcode registered | `docs/LUA_OPCODE_SYSTEM_GUIDE.md` |

Documentation must be updated **in the same commit** as the code change. PRs with undocumented systems will not be approved by QA Lead.

---

## Key Reference Files

| File | Purpose |
|------|---------|
| `server/data/XML/vocations.xml` | Vocation IDs and names — **source of truth** |
| `server/data/spells/spells.xml` | All spell registrations |
| `server/data/talkactions/talkactions.xml` | All command registrations |
| `server/data/items/items.xml` | Item definitions |
| `docs/EFFECTS_MAPPING.md` | Visual catalogue of all 321 effects with offset data |
| `docs/SPELL_AUTHORING_GUIDE.md` | Step-by-step guide to creating spells |
| `docs/SYSTEMS_OVERVIEW.md` | All implemented server and client systems |
| `docs/LUA_OPCODE_SYSTEM_GUIDE.md` | Client↔Server extended opcode reference |
| `docs/OTCLIENT_MODULES_GUIDE.md` | All 19+ OTClient modules — usage and API reference |
