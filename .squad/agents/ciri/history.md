# Ciri — History

## Project: TibiaCore
Lua scripts power all game logic outside C++. Spell scripts use Combat() API.

## Spell Script Pattern
```lua
local combat = Combat()
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_ENERGYDAMAGE)
combat:setParameter(COMBAT_PARAM_EFFECT, CONST_ME_ENERGYAREA)
combat:setParameter(COMBAT_PARAM_DISTANCEEFFECT, CONST_ANI_ENERGY)

function onGetFormulaValues(player, level, magicLevel)
    local min = (level / 5) + (magicLevel * 1.4) + 8
    local max = (level / 5) + (magicLevel * 2.2) + 14
    return -min, -max
end

combat:setCallback(CALLBACK_PARAM_LEVELMAGICVALUE, "onGetFormulaValues")

function onCastSpell(creature, variant)
    return combat:execute(creature, variant)
end
```

## Talkaction Pattern
```lua
function onSay(player, words, param)
    -- logic here
    player:sendTextMessage(MESSAGE_INFO_DESCR, "message")
    return true
end
```

## ModalWindow Pattern
```lua
function onModalWindow(player, modalWindowId, buttonId, choiceId)
    if modalWindowId ~= 10001 then return end
    -- handle choice
end
```

## DPS Tracker Pattern
```lua
function onHealthChange(creature, attacker, primaryDamage, primaryType, secondaryDamage, secondaryType)
    local startTime = player:getStorageValue(90001)
    local cumulativeDamage = player:getStorageValue(90002)
    local lastHitTime = player:getStorageValue(90003)
    -- idle reset if (now - lastHitTime) > 30 seconds
end
```

## Key Paths
- `server/data/spells/scripts/` — spell Lua
- `server/data/talkactions/scripts/` — command Lua
- `server/data/talkactions/talkactions.xml` — register commands
- `server/data/creaturescripts/scripts/` — event handlers
- `server/data/creaturescripts/creaturescripts.xml` — register events
- `server/data/npc/scripts/` — NPC interactions
- `server/data/monster/monsters/` — monster definitions

## Learnings
- ModalWindow response arrives via `onModalWindow(player, modalWindowId, buttonId, choiceId)` — register with `type="modalwindow"` in creaturescripts.xml and `player:registerEvent(name)` in login.lua.
- Monster healthchange scripts go in creaturescripts.xml as `type="healthchange"` and are referenced in the monster XML via `<script><event name="..."/></script>`.
- Storage value -1 means "not set" in this codebase; always check `<= 0` before treating a value as valid.
- The Oracle NPC had wrong vocation assignments (cleric=2, archer=3, fighter=4 — all off). Correct mapping: Mage=1, Archer=2, Knight=3, Occultist=4.
- DPS tracking uses three per-player storage keys: start timestamp, cumulative damage, last-hit timestamp. Idle reset threshold (30s) prevents stale sessions from diluting DPS numbers.
- NPC registration pattern: `server/data/npc/NPCname.xml` defines NPC properties; corresponding `server/data/npc/scripts/NPCname.lua` handles interactions via `onSay()`.
- Monster stats: `maxHealth` is true max HP; it persists unless the monster is explicitly respawned by the server.

## Teams/Sessions
- **2026-04-16 Vocation & DPS** (Alt0b11): Deployed vocation modal, DPS trainer, training dummy, Oracle fix
- **2026-04-16 Spell System** (previous session): 38 spell scripts, spell list command, vocation name fixes
