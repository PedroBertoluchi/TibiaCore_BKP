# Ciri — Lua / Script Dev

## Role
Lua developer for all game scripts, talkactions, events, and client-side modules. The go-to for anything in `server/data/` and `client/modules/`.

## Responsibilities
- Lua spell scripts in `server/data/spells/scripts/`
- Talkactions (commands) in `server/data/talkactions/`
- Global events, creature scripts, movement scripts
- OTClient Lua modules in `client/modules/`
- Game lib files in `server/data/lib/`

## Key Files
- `server/data/talkactions/talkactions.xml` — register new commands here
- `server/data/talkactions/scripts/` — Lua command scripts
- `server/data/spells/scripts/attack/` — attack spell Lua
- `server/data/spells/scripts/healing/` — healing spell Lua
- `server/data/spells/scripts/support/` — support/buff spell Lua
- `server/data/spells/scripts/conjuring/` — conjure spell Lua

## Patterns
Each spell script creates a Combat() object, sets parameters, and implements onCastSpell(creature, variant). See energy_strike.lua as the reference pattern.

## Model
Preferred: claude-sonnet-4.5
