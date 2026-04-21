# CLAUDE.md — TibiaCore Umbrella Project

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ MANDATORY — Read All Docs Before Starting Any Task

**Before touching any code, always read every file in ALL docs folders:**

- `P:\Tibia\TibiaCore\docs\` — project-wide architecture, implemented systems, and intentional rule overrides
- `P:\Tibia\TibiaCore\client\docs\` — client-specific implementation notes
- `P:\Tibia\TibiaCore\server\docs\` — server-specific implementation notes (if present)

These folders contain critical decisions (gameplay rule overrides, system guardrails, known pitfalls) that **cannot be inferred from the code alone**. Skipping them leads to undoing intentional changes or re-introducing known bugs.

Read the docs first. Then read the code.

## ⚠️ MANDATORY — OTUI Interface Design Rules

**Every client UI module MUST follow `P:\Tibia\TibiaCore\client\otui-interface-design-skill.md`.**

Key rules that must never be skipped:

1. **Always add a mainpanel toggle button** for every game UI module:
   ```lua
   -- In onGameStart():
   m_Button = modules.game_mainpanel.addToggleButton(
       'myModuleButton', tr('Label'), '/images/options/icon', toggle, false, priority
   )
   -- In open()/show(): m_Button:setOn(true)
   -- In close()/hide(): m_Button:setOn(false)
   -- In onGameEnd() and terminate(): m_Button:destroy(); m_Button = nil
   ```

2. **All buttons must have proper state feedback**: `$hover`, `$pressed`, `$disabled` in OTUI

3. **Checkable buttons require `checkable: true`** in the OTUI widget definition

4. **Use `g_game.getProtocolGame():sendExtendedOpcode()`** — never `g_game.sendExtendedOpcode()`

5. **Use `autoload: true` + `autoload-priority`** in every `.otmod` file

6. **All text must use `tr()`** for translation support

7. **`onGameStart`** creates the button; **`onGameEnd`** destroys it; **`terminate`** destroys both button and window

## ⚠️ MANDATORY — Server Guardrails

See `server/CLAUDE.md`, `server/AGENTS.md`, and `server/.github/copilot-instructions.md` for full detail. Key rules:

### Combat hook consistency
- Use `data/lib/core/combat_hook_utils.lua` for guard logic in `onHealthChange` / `onManaChange`.
- For generic damage modifiers: skip when `origin == ORIGIN_NONE` or event is healing (`COMBAT_HEALING`).
- Keep health and mana handlers aligned in behavior.

### Map system
- Source of truth: `data/scripts/systems/map_system.lua`.
- New buffs must go into `MapSystem.Config.buffPool`.

### Tooltip authority
- Server tooltip payload (`data/scripts/item_tooltips.lua`, opcode `105`) is authoritative.

### Documentation sync
- When adding/changing a main system, update `SERVER_MECHANICS_OVERVIEW.md`, `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md`.

## Project Structure

This is a mono-repo containing two separate git repositories:

- **`client/`** — OTClient-Redemption (C++20 + Lua, OpenGL rendering)
  - See `client/CLAUDE.md` for full client-specific guidance
- **`server/`** — The Forgotten Server fork (C++17 + Lua)
  - See `server/CLAUDE.md` for full server-specific guidance
- **`docs/`** — Shared project documentation (read first!)

## Git Workflow

Each subdirectory is its own git repository with its own remote:
- `client/` → `https://github.com/ThanksUniverse/otclient-main.git`
- `server/` → `https://github.com/ThanksUniverse/forgottenserver-1.4.git`

Always `cd` into the correct subdirectory before running git commands.
