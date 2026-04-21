# Copilot Instructions — TibiaCore Monorepo

## Step 0 — Choose the Right Agent

| Task | Agent |
|------|-------|
| Client UI, Lua modules, OTUI, C++ rendering | `.github/agents/client.md` |
| Server Lua, C++ game logic, combat, opcodes | `.github/agents/server.md` |
| Cross-cutting feature, architecture, both sides | `.github/agents/general.md` |

## Step 1 — Read Docs First

**Shared (always):**
- `docs/SYSTEMS_OVERVIEW.md`
- `docs/LUA_OPCODE_SYSTEM_GUIDE.md`
- `docs/GAMEPLAY_RULES_OVERRIDES.md`

**Client work:**
- `client/otui-interface-design-skill.md` — mandatory UI standard
- `client/OTCLIENT_MODULE_DEVELOPMENT_MASTER_GUIDE.md`
- `client/documentation/NIL_CHECKING_MASTERY.md`

**Server work:**
- `server/SERVER_MECHANICS_OVERVIEW.md`
- `docs/SPELL_AUTHORING_GUIDE.md`
- `docs/ITEM_RARITY_IMPLEMENTATION_GUIDE.md`

## Step 2 — Cross-Cutting Change Checklist

### Server → Client
| Server change | Check |
|---------------|-------|
| New/changed extended opcode | Register handler in `client/modules/` |
| Changed `AddPlayer*` packet | Update `client/src/client/protocolgame.cpp` |
| New stat/attribute | Add widget + Lua in `client/modules/game_skills/` |
| Changed opcode JSON keys | Update all client parsers |

### Client → Server
| Client change | Check |
|---------------|-------|
| New `sendExtendedOpcode(N)` | Register N in `server/data/scripts/creaturescripts/extendedopcode.lua` |
| Changed JSON expected from server | Update server builder script |

## OTUI Interface Rules (client/)

1. Toggle button in `onGameStart()` via `modules.game_mainpanel.addToggleButton`
2. Destroy in both `onGameEnd()` AND `terminate()`
3. Exactly one root widget per `g_ui.displayUI()` file
4. Style definitions → `data/styles/NN-name.otui` only
5. `//` comments in OTUI — NEVER `--`
6. `g_game.getProtocolGame():sendExtendedOpcode()` — not `g_game.sendExtendedOpcode()`
7. All `.otmod`: `autoload: true` + `autoload-priority`
8. All UI text: `tr("...")`
9. Font: `verdana-11px-antialised` (typo intentional)

## Server Rules

- Combat hooks: skip `ORIGIN_NONE` and `COMBAT_HEALING` in damage modifiers
- Map buffs: only via `MapSystem.Config.buffPool` in `map_system.lua`
- Tooltips: server opcode 105 is authoritative
- Talent keys: character 50001–50011, account 60001–60099 (opcode 218)

## Opcode Registry
| Opcode | System |
|--------|--------|
| 80 (0x50) | Elemental damage + item bonuses |
| 105 | Item tooltips |
| 202 | Loyalty |
| 203 | Daily reward |
| 218 | Talents (character + account) |
| 225 | Vocation modal |
| 226 | Bless golden frame |

## CHANGELOG.md — Mandatory
Every user-facing change → `server/CHANGELOG.md` under `## [Unreleased]`
Plain language, no internals. Sections: `### Added`, `### Changed`, `### Fixed`, `### Removed`

## Git Structure
- `client/` → submodule → `https://github.com/ThanksUniverse/otclient-main.git`
- `server/` → submodule → `https://github.com/ThanksUniverse/forgottenserver-1.4.git`
- After pushing client or server, update root: `git add client server && git commit -m "chore: update submodules" && git push`
