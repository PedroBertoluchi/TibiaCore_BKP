# TibiaCore — Systems Overview

Complete reference for all custom systems implemented in TibiaCore.

TibiaCore is a custom MMORPG based on The Forgotten Server engine with a custom OTClient. All systems below are fully implemented and working.

---

## 1. Effect Offset / Big Spell Centering System

### Purpose
Allows LARGE multi-tile effects (like ice5x5, fire bomb, dragon sprites) to be pixel-perfectly centered on a target tile rather than rendering from the top-left corner of the tile.

### C++ Implementation
- `g_game.setEffectOffset(x, y, z)` — registered in the Lua bindings
- Applied at render time: the effect sprite is drawn at `targetScreen + offset` instead of `targetScreen`
- The offset is relative to the TARGET tile's screen position (NOT the caster)

### Default Offset
Set in client `init.lua` or equivalent:
```lua
g_game.setEffectOffset(321, 60, 0)
```

### Lua Usage
```lua
-- Per-spell override (via extended opcode or direct call):
g_game.setEffectOffset(280, 70, 0)  -- custom centering
-- Cast the effect
-- Reset if needed
g_game.setEffectOffset(321, 60, 0)  -- back to default
```

### Key LARGE Effects and Tuned Offsets
| Effect | Name | X | Y |
|--------|------|---|---|
| 53 | Ice Glacier (ice5x5) | 321 | 60 |
| 202 | Massive Ice Ball | 240 | 80 |
| 239 | Ice Crown | 280 | 70 |
| 241 | Purple Mandala | 260 | 65 |
| 320 | Large Fire Bomb | 200 | 80 |
| 321 | Epic Ice Sword | 300 | 100 |

---

## 2. Vocation System

### Vocations
| ID | Name | Promoted Forms |
|----|------|----------------|
| 0 | Rookie | (starter) |
| 1 | Mage | Archmage(5), Blood Mage(11) |
| 2 | Archer | Marksman(7), Beastmaster(8) |
| 3 | Knight | Templar(9), Death Knight(10) |
| 4 | Occultist | Necromancer(6), Heretic(12) |

### Vocation Exchange (`!vocation` command)
- **Command**: `!vocation`
- **Opens**: In-game modal listing all 4 base vocations (+ Rookie)
- **Behavior**:
  - If player already has the selected vocation (or its promotion), shows error
  - Otherwise, sets vocation, clears inventory, gives full starter gear set
  - Uses `getBaseVocId()` to map promoted → base for comparison
- **Starter gear**: Defined per vocation in `vocation_modal.lua` — full set of weapons, armor, accessories

### File Locations
- `server/data/talkactions/scripts/setvocation.lua` — opens the modal
- `server/data/creaturescripts/scripts/vocation_modal.lua` — handles selection, gear assignment

---

## 3. Spell System

### Registration
All spells registered in `server/data/spells/spells.xml`. Lua scripts in `server/data/spells/scripts/`.

### Tier Progression
| Tier | Level Range | Description |
|------|-------------|-------------|
| 1 | 1-20 | Basic spells, single target, small effects |
| 2 | 20-50 | AoE available, medium effects |
| 3 | 50-100 | Wide AoE, notable effects |
| 4 | 100-200 | Large effects, high damage |
| 5 | 200+ | EPIC effects, ultimate abilities |

### `!spells` Command
- Lists all spells available to the player's current vocation
- Groups by tier/level
- Shows: spell name, level requirement, mana cost, words
- File: `server/data/talkactions/scripts/spells_list.lua`

### `!skills` Command
- Shows all player skills formatted for easy reading
- Shows: level, mana, magic level, combat skills, defensive skills
- File: `server/data/talkactions/scripts/skills.lua`

---

## 4. DPS Tracker System

### Training Dummy
- Monster: `training_dummy` in `server/data/monster/monsters/training_dummy.xml`
- Has `DummyThink` event registered in `creaturescripts.xml`
- Infinite health (heals fully), immortal

### How It Works
1. **Player targets the dummy** → `dps_tracker.lua` `healthChange` event fires → `_G.DPS_TRACKER[playerId]` initialized with `startTime`, `totalDamage = 0`
2. **Each hit** → `healthChange` adds damage to `totalDamage`
3. **Player untargets** → `training_dummy_think.lua` `onThink` detects `player:getAttackTarget() == nil` or target changed → DPS report fires

### DPS Report
- **Monster say bubble**: Dummy says `"[PlayerName] DPS: X | Time: Ys"` in `TALKTYPE_MONSTER_SAY`
- **Blue console message**: Player receives blue text in their chat console

### File Locations
- `server/data/creaturescripts/scripts/dps_tracker.lua`
- `server/data/creaturescripts/scripts/training_dummy_think.lua`
- `server/data/creaturescripts/creaturescripts.xml`
- `server/data/monster/monsters/training_dummy.xml`

---

## 5. Extended Opcode System (Client ↔ Server)

See `docs/LUA_OPCODE_SYSTEM_GUIDE.md` for full reference including the complete opcode registry and the blessing frame as a worked real-time example.

### Quick Summary
- Server → Client: `player:sendExtendedOpcode(opcode, data)`
- Client → Server: `inventoryController:sendExtendedOpcode(opcode, data)` (or any Controller)
- All server-side receives go through one global handler: `extendedopcode.lua`
- Prefer the **pull-on-connect + auto-push-on-change** pattern over `addEvent` delays

---

## 6. Blessing Golden Frame System

### Purpose
Shows a golden decorative frame on equipped item slots in the inventory when the player has at least one blessing active.

### Commands
- `!bless` — grants all 6 blessings (talkaction)

### How it Works (Real-Time, No Delay)
1. Client `onGameStart` → sends opcode 226 `{action="request"}` to server
2. Server reads `player:hasBlessing(1..6)` → responds with `{blessed=true/false}`
3. Client `inventory.lua` shows/hides `.golden` child on each equipment slot widget
4. Any server-side `player:addBlessing()` or `player:removeBlessing()` call automatically pushes a new opcode 226 update via wrapper in `player.lua`

### Files
| File | Role |
|------|------|
| `server/data/creaturescripts/scripts/extendedopcode.lua` | Handles `{action="request"}` → reads blessing state → responds |
| `server/data/lib/core/player.lua` | Wraps `addBlessing`/`removeBlessing` to auto-push opcode 226 |
| `server/data/talkactions/scripts/bless.lua` | `!bless` command — grants blessings (wrapper handles the push) |
| `client/modules/game_inventory/inventory.lua` | Registers opcode 226 handler, requests on connect, updates UI |

### Key Design Decisions
- **No `addEvent` delay** — client initiates after it's ready, no timing race
- **`pcall` in wrappers** — `addBlessing` is called during DB load before player has a connection; must not throw
- **Auto-push covers all sources** — any script calling `player:addBlessing()` (quests, GM commands, etc.) automatically syncs the client

---

## 6. Item Rarity System

See `docs/ITEM_RARITY_README.md` for full documentation.

### Quick Summary
- Items drop with rarity: Common, Uncommon, Rare, Epic, Legendary
- Visual indicators and loot announcements per rarity tier
- Configurable drop rates per monster type

---

## 7. Elemental Damage System

See `docs/ELEMENTAL_DAMAGE_IMPLEMENTATION_GUIDE.md` for full documentation.

### Quick Summary
- Extended damage types beyond TFS defaults
- Per-vocation elemental affinity
- Resistances and weaknesses on monsters

---

## 8. Color Messages / Loot Display

See `docs/COLOR_MESSAGES_AND_LOOT_GUIDE.md`.

---

## 9. Recommended Testing Workflow

1. Start server: compile + run TibiaCore server
2. Connect client, login as GM/admin
3. Use `!vocation` to select a test vocation
4. Use `!spells` to verify spells are registered correctly
5. Test each spell on training dummy
6. Check DPS output after untargeting dummy
7. Test LARGE effects with offset tuning if needed
8. Check server console for any "Wrong vocation name" warnings

---

## 11. System Interaction Map

```
Player
  ├── !vocation → VocationModal → setVocation + giveGear
  ├── !spells   → SpellsList → filtered by vocId
  ├── !skills   → SkillsDisplay
  ├── !bless    → bless.lua → addBlessing(1..6)
  │                              └── player.lua wrapper
  │                                    └── sendExtendedOpcode(226, {blessed=true})
  │                                          └── inventory.lua → show golden frame
  ├── onGameStart (client)
  │     └── sendExtendedOpcode(226, {action="request"})
  │           └── extendedopcode.lua → hasBlessing check → respond
  │                 └── inventory.lua → show/hide golden frame
  └── Targets TrainingDummy
        ├── healthChange → DPS_TRACKER[id].totalDamage++
        └── onThink (untarget) → DPS Report
              ├── dummy:say(MONSTER_SAY)
              └── player:sendTextMessage(BLUE)
```
