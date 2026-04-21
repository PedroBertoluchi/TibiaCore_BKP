# Copilot Instructions — TibiaCore

## MANDATORY — Read All Docs First

Before any code change, read:
- `P:\Tibia\TibiaCore\docs\` — project-wide architecture and rule overrides
- `P:\Tibia\TibiaCore\client\docs\` — client implementation notes

## OTUI Interface Design (client/)

Every game UI module must follow `client/otui-interface-design-skill.md`:
- Add a mainpanel toggle button via `addToggleButton` in `onGameStart`
- `open()` → `m_Button:setOn(true)`, `close()` → `m_Button:setOn(false)`
- Destroy button in both `onGameEnd()` and `terminate()`
- Use `g_game.getProtocolGame():sendExtendedOpcode()` (not `g_game.sendExtendedOpcode()`)
- All `.otmod` files need `autoload: true` + `autoload-priority`
- All UI text wrapped in `tr()`

## Server Guardrails (server/)

- Combat hooks: skip `ORIGIN_NONE` and `COMBAT_HEALING` in damage modifiers
- Map buffs: only via `MapSystem.Config.buffPool` in `map_system.lua`
- Tooltips: server opcode 105 is authoritative
- Talent keys: character 50001–50011, account 60001–60099 (opcode 218)
- Doc sync: update `SERVER_MECHANICS_OVERVIEW.md` + instruction files after system changes

## Git Structure

- `client/` → `https://github.com/ThanksUniverse/otclient-main.git`
- `server/` → `https://github.com/ThanksUniverse/forgottenserver-1.4.git`
