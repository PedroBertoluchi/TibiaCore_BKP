# AGENTS.md — TibiaCore Umbrella Monorepo

AI agent guidance for the TibiaCore project. This is a monorepo containing two git submodules:
- `client/` — OTClient-Redemption (C++20 + Lua, OpenGL)
- `server/` — ForgottenServer fork (C++17 + Lua)

---

## ⚠️ STEP 0 — Route to the Right Subagent

Before doing any work, select the appropriate specialist:

| Task area | Use agent |
|-----------|-----------|
| Client UI / Lua modules / OTUI / C++ rendering | **`client`** agent (`.github/agents/client.md`) |
| Server Lua / C++ game logic / opcodes / data scripts | **`server`** agent (`.github/agents/server.md`) |
| Cross-cutting feature (both sides involved) or architecture | **`general`** agent (`.github/agents/general.md`) |

---

## ⚠️ STEP 1 — Mandatory Doc Reading

**Always read before touching code.** Skipping these causes re-introducing known bugs and undoing intentional decisions.

### Shared docs (always read)
- `docs/SYSTEMS_OVERVIEW.md` — all implemented systems at a glance
- `docs/LUA_OPCODE_SYSTEM_GUIDE.md` — opcode allocation, how server↔client talk
- `docs/ELEMENTAL_DAMAGE_IMPLEMENTATION_GUIDE.md` — elemental system architecture
- `docs/ITEM_RARITY_IMPLEMENTATION_GUIDE.md` — random attributes, rarity tiers
- `docs/SPELL_AUTHORING_GUIDE.md` — how spells are written and balanced
- `docs/GAMEPLAY_RULES_OVERRIDES.md` — intentional departures from standard OT behavior
- `docs/TEAM_HANDBOOK.md` — team conventions, workflow, commit style

### Client docs (read when touching `client/`)
- `client/otui-interface-design-skill.md` — **THE** UI design standard (mandatory)
- `client/otui-dark-fantasy-modal-skill.md` — modal / dialog design standard
- `client/OTCLIENT_MODULE_DEVELOPMENT_MASTER_GUIDE.md` — full module lifecycle
- `client/MODULE_DEVELOPMENT_GUIDE.md` — quick module reference
- `client/documentation/ULTIMATE_OTCLIENT_KNOWLEDGE_COMPENDIUM.md` — deep internals
- `client/documentation/OTUI_MODULE_ICONS_GUIDE.md` — icon / image conventions
- `client/documentation/NIL_CHECKING_MASTERY.md` — common nil-crash patterns
- `client/documentation/tooltip_client_server_checklist.md` — tooltip integration checklist
- `client/docs/tooltip_client_server_checklist.md` — tooltip checklist (client/docs mirror)

### Server docs (read when touching `server/`)
- `server/SERVER_MECHANICS_OVERVIEW.md` — canonical server system reference
- `server/DAMAGE_ATTRIBUTES_CHANGES.md` — how damage attributes were modified
- `server/SHADERS_AND_EXTENDED_OUTFITS.md` — shader/outfit opcode protocol

---

## ⚠️ STEP 2 — Cross-Cutting Change Checklist

**Any change in one submodule may require a matching change in the other.** Run through this checklist whenever you touch server OR client code:

### Server → Client impact
| You changed on server | Check on client |
|-----------------------|-----------------|
| Added / renamed extended opcode | `client/modules/` — register handler via `ProtocolGame.registerExtendedOpcode` |
| Changed `AddPlayer*` packet fields | `client/src/` C++ protocol parsing (`protocolgame.cpp`) |
| Added new item attribute / stat | `client/modules/game_skills/skills.lua` — add to statsCache + display |
| Added new item attribute / stat | `client/modules/game_skills/skills.otui` — add widget |
| Changed vocation list / IDs | `client/modules/game_vocationmodal/` + any vocation-keyed UI |
| Added / changed spell | Spell description, icon, and progression docs if player-visible |
| Changed opcode JSON keys | All client handlers parsing that opcode |
| Changed storage key ranges | `server/AGENTS.md` + `client/` if client mirrors them |

### Client → Server impact
| You changed on client | Check on server |
|-----------------------|-----------------|
| New `sendExtendedOpcode(N, ...)` call | `server/data/scripts/creaturescripts/extendedopcode.lua` — register handler |
| Changed expected opcode JSON structure | Server script building that JSON |
| New vocation modal action | Server handler for the corresponding opcode |
| Changed skill IDs referenced | Server `Skill.*` constants must match |

---

## ⚠️ STEP 3 — Code Standards

### Client UI rules (every game module)
1. Add a mainpanel toggle button via `modules.game_mainpanel.addToggleButton` in `onGameStart()`
2. `open()` → `m_Button:setOn(true)` · `close()` → `m_Button:setOn(false)`
3. Destroy button in both `onGameEnd()` AND `terminate()`
4. Use `g_game.getProtocolGame():sendExtendedOpcode()` — **never** `g_game.sendExtendedOpcode()`
5. All `.otmod` files: `autoload: true` + `autoload-priority`
6. All user-facing text: `tr("...")`
7. OTUI files used with `g_ui.displayUI()` must have **exactly one** root widget
8. Style definitions go in `data/styles/NN-name.otui` — never mixed into module `.otui`
9. **Never use `--` comments in `.otui` files** — use `//` only
10. Font name is `verdana-11px-antialised` (typo is intentional — it is the actual asset name)

### Server combat rules
- Combat hooks use `data/lib/core/combat_hook_utils.lua` guards
- Skip processing when `origin == ORIGIN_NONE` (recursion guard)
- Skip healing events (`COMBAT_HEALING` in primary or secondary type) in offensive modifiers
- Keep `onHealthChange` and `onManaChange` aligned in logic

### Server map & tooltip rules
- Map buff source of truth: `data/scripts/systems/map_system.lua` → `MapSystem.Config.buffPool`
- Item tooltip authority: `data/scripts/item_tooltips.lua` opcode `105`

### Opcode registry — do not reuse
| Range | Owner |
|-------|-------|
| 80 (0x50) | Elemental damage + item bonuses |
| 105 | Item tooltips |
| 202 | Loyalty |
| 203 | Daily reward |
| 218 | Talents (character + account) |
| 225 | Vocation modal |
| 226 | Bless golden frame |

---

## ⚠️ STEP 4 — Documentation & Changelog

### CHANGELOG.md — mandatory for every user-facing change
- File: `server/CHANGELOG.md`
- Sections: `### Added`, `### Changed`, `### Fixed`, `### Removed` under `## [Unreleased]`
- Plain language — no internal details — readable by any player
- Both client and server changes go in the **same** file

### Doc sync — when you change a core system update all four:
1. `server/SERVER_MECHANICS_OVERVIEW.md`
2. `server/AGENTS.md`
3. `server/.github/copilot-instructions.md`
4. `AGENTS.md` (this file) if it's cross-cutting

---

## Project Structure

```
TibiaCore/                    ← this repo (monorepo root)
├── client/                   ← git submodule → otclient-main
├── server/                   ← git submodule → forgottenserver-1.4
├── docs/                     ← shared architecture docs (read first)
├── .github/agents/           ← specialist subagent definitions
├── .squad/                   ← squad orchestration config
└── AGENTS.md                 ← this file
```

### Git workflow
- `client/` and `server/` are independent git repos — `cd` into them before committing
- Root repo tracks which commit of each submodule is "current"
- After pushing client or server, also commit + push root to update submodule pointer
