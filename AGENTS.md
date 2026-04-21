# AGENTS.md — TibiaCore Umbrella Project

Default AI agent guidance for the TibiaCore project.

## ⚠️ MANDATORY — Read All Docs Before Starting Any Task

**Before touching any code, always read every file in ALL docs folders:**

- `P:\Tibia\TibiaCore\docs\` — project-wide architecture, implemented systems, and intentional rule overrides
- `P:\Tibia\TibiaCore\client\docs\` — client-specific implementation notes
- `P:\Tibia\TibiaCore\server\docs\` — server-specific implementation notes (if present)

These folders contain critical decisions that **cannot be inferred from code alone**. Skipping them leads to undoing intentional changes or re-introducing known bugs.

Read the docs first. Then read the code.

## ⚠️ MANDATORY — OTUI Interface Design Rules

**Every client UI module MUST follow `P:\Tibia\TibiaCore\client\otui-interface-design-skill.md`.**

Key rules:
1. Every game UI module needs a mainpanel toggle button (`modules.game_mainpanel.addToggleButton`)
2. Buttons need full state styles: `$hover`, `$pressed`, `$disabled`
3. Checkable buttons need `checkable: true` in OTUI
4. Always use `g_game.getProtocolGame():sendExtendedOpcode()` — not `g_game.sendExtendedOpcode()`
5. All `.otmod` files need `autoload: true` + `autoload-priority`
6. All user-facing text uses `tr()` for localization
7. Button lifecycle: created in `onGameStart`, destroyed in `onGameEnd` AND `terminate`

## Server Guardrails

### 1) Combat hook consistency
- Reuse shared helpers in `data/lib/core/combat_hook_utils.lua`.
- For generic damage-modifier scripts (not healing systems), skip when:
  - `origin == ORIGIN_NONE`
  - event is healing (`COMBAT_HEALING` in primary or secondary type)
- Use a single positive-damage predicate before applying modifiers.
- Keep `onHealthChange` and `onManaChange` logic aligned.

### 2) Healing behavior
- Do not apply flat/elemental bonus damage while healing.
- If a system explicitly modifies healing, document it and still block `ORIGIN_NONE` recursion.

### 3) Map System source of truth
- Main file: `data/scripts/systems/map_system.lua`.
- New map buffs must be added to `MapSystem.Config.buffPool`.
- Tooltip placement must be config-driven.

### 4) Tooltip authority
- Server tooltip builder (`data/scripts/item_tooltips.lua`, opcode 105) is authoritative.
- Map item tooltip data must come from map custom attributes.

### 5) Documentation sync
- When changing core systems, update `SERVER_MECHANICS_OVERVIEW.md`, `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md`.

### 6) CHANGELOG.md — MANDATORY for every user-facing change
- **Whenever you add a feature, fix a bug, or change gameplay behavior, add an entry to `server/CHANGELOG.md`.**
- Write in plain language that any player can understand (no internal implementation details).
- Sections: `### Added`, `### Changed`, `### Fixed`, `### Removed`. New entries go under `## [Unreleased]`.
- Both client and server changes go in the same file — it is the single player-facing history.

## Project Structure

- **`client/`** — OTClient-Redemption (separate git repo)
- **`server/`** — Forgotten Server fork (separate git repo)
- **`docs/`** — Shared project documentation

Each subdirectory has its own `CLAUDE.md`, `AGENTS.md`, and `.github/copilot-instructions.md` with full detail.
