# OTClient Modules Guide

> **Reference only** — all modules listed here are **already implemented** in TibiaCore. Do not rebuild them; only use and extend them.

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [Module Reference](#module-reference)
3. [OTClient Module Structure](#otclient-module-structure)
4. [Creating a New Module](#creating-a-new-module)
5. [Extended Opcode System](#extended-opcode-system)
6. [Custom Widgets](#custom-widgets)
7. [Effect Offsets](#effect-offsets)

---

## Module Overview

TibiaCore ships with **19 custom OTClient modules** that extend the base client with gameplay systems, UI panels, and visual effects. Each module lives under `client/modules/` and follows the standard OTClient module convention.

---

## Module Reference

### 1. `game_talents`
**Purpose:** Talent tree and passive skill progression system. Allows players to spend talent points across branching upgrade trees.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode (see `LUA_OPCODE_SYSTEM_GUIDE.md`) — server sends talent data on login and on point spend |
| Key Lua events | `Talents.onReceiveData(data)`, `Talents.onPointSpent(talentId)` |
| Config location | `client/modules/game_talents/game_talents.otmod` |

---

### 2. `game_randomstats`
**Purpose:** Displays random affix/stat rolls on items (similar to Diablo-style modifiers). Hooks into item inspection to show rolled bonus stats.

| Item | Detail |
|------|--------|
| Server trigger | Item extended attribute packet; server embeds random stat data in item description or via opcode |
| Key Lua events | `RandomStats.parseItemStats(item)`, `RandomStats.formatTooltip(stats)` |
| Config location | `client/modules/game_randomstats/game_randomstats.otmod` |

---

### 3. `game_shaders`
**Purpose:** Applies custom GLSL shader effects to the game renderer (map, creatures, UI layers). Enables visual effects such as bloom, outlines, water distortion, and night vision.

| Item | Detail |
|------|--------|
| Server trigger | Automatic / client-side toggle; some shaders activated by server opcode |
| Key Lua events | `Shaders.setMapShader(name)`, `Shaders.resetShader()` |
| Config location | `client/modules/game_shaders/` — GLSL files in `shaders/` subdirectory |

---

### 4. `game_attachedeffects`
**Purpose:** Attaches looping particle effects to creatures or players — auras, trails, wing effects, glow halos. Effects persist while the attachment condition is active.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode; server sends attach/detach commands with creature ID and effect descriptor |
| Key Lua events | `AttachedEffects.attach(creature, effectId)`, `AttachedEffects.detach(creature, effectId)` |
| Config location | `client/modules/game_attachedeffects/game_attachedeffects.otmod` |

---

### 5. `game_cooldown`
**Purpose:** Renders cooldown bars beneath the hotbar and/or in a dedicated panel, showing remaining cooldown time per spell/skill.

| Item | Detail |
|------|--------|
| Server trigger | Standard cooldown packet (opcode 0xA4 / `GameFeature`); also responds to spell cast events |
| Key Lua events | `Cooldown.onSpellCooldown(spellId, duration)`, `Cooldown.onGroupCooldown(groupId, duration)` |
| Config location | `client/modules/game_cooldown/game_cooldown.otmod` |

---

### 6. `game_actionbar`
**Purpose:** Hotbar with configurable action slots for spells, items, macros, and equipment toggles. Supports multiple bars and drag-and-drop assignment.

| Item | Detail |
|------|--------|
| Server trigger | Client-side only; slot assignments persisted in local config |
| Key Lua events | `ActionBar.useSlot(slot)`, `ActionBar.assignSlot(slot, type, id)` |
| Config location | `client/modules/game_actionbar/game_actionbar.otmod` |

---

### 7. `game_quickloot`
**Purpose:** Autoloot container management UI. Players configure which containers receive which item types; loot is routed automatically on kill.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode for container mapping sync; server applies routing on loot drop |
| Key Lua events | `QuickLoot.setContainerForCategory(category, containerId)`, `QuickLoot.onLootReceived(item)` |
| Config location | `client/modules/game_quickloot/game_quickloot.otmod` |

---

### 8. `game_market`
**Purpose:** In-game market and auction house UI. Players can browse listings, post offers, and manage transactions without visiting an NPC.

| Item | Detail |
|------|--------|
| Server trigger | Dedicated market opcodes (browse, offer, cancel, history) |
| Key Lua events | `Market.onBrowse(category)`, `Market.onOfferCreate(itemId, amount, price)` |
| Config location | `client/modules/game_market/game_market.otmod` |

---

### 9. `game_questlog`
**Purpose:** Quest tracking log UI. Displays active, completed, and failed quests with objectives, progress, and reward previews.

| Item | Detail |
|------|--------|
| Server trigger | Quest state packet sent on login and on quest state change |
| Key Lua events | `QuestLog.onQuestUpdate(questId, state)`, `QuestLog.onOpen()` |
| Config location | `client/modules/game_questlog/game_questlog.otmod` |

---

### 10. `game_tasks`
**Purpose:** Daily and weekly task system UI. Shows available tasks, current progress counters, and reward claim buttons.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode; server pushes task list and progress updates |
| Key Lua events | `Tasks.onTaskUpdate(taskId, progress, goal)`, `Tasks.onTaskComplete(taskId)` |
| Config location | `client/modules/game_tasks/game_tasks.otmod` |

---

### 11. `game_dailyreward`
**Purpose:** Daily login reward chest UI. Presents reward options for the current streak day and confirms claim.

| Item | Detail |
|------|--------|
| Server trigger | Server opens reward window via opcode on login when reward is available |
| Key Lua events | `DailyReward.onOpen(streakDay, rewards)`, `DailyReward.onClaim(choiceIndex)` |
| Config location | `client/modules/game_dailyreward/game_dailyreward.otmod` |

---

### 12. `game_bossbar`
**Purpose:** Displays a dedicated health bar for boss creatures at the top of the screen, styled differently from standard creature health bars.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode; server designates a creature as a boss and sends HP% updates |
| Key Lua events | `BossBar.setTarget(creatureId, name, hpPercent)`, `BossBar.clear()` |
| Config location | `client/modules/game_bossbar/game_bossbar.otmod` |

---

### 13. `game_bosskills`
**Purpose:** Boss kill counter and tracking panel. Records kills per boss, personal bests, and server records.

| Item | Detail |
|------|--------|
| Server trigger | Extended opcode after boss death; server sends updated kill counts |
| Key Lua events | `BossKills.onKill(bossName, count)`, `BossKills.onOpen()` |
| Config location | `client/modules/game_bosskills/game_bosskills.otmod` |

---

### 14. `game_cyclopedia`
**Purpose:** Bestiary / monster encyclopedia. Displays creature stats, loot tables, kill counts, and unlocked bestiary entries.

| Item | Detail |
|------|--------|
| Server trigger | Cyclopedia opcodes for entry request/response; kill counts synced on login |
| Key Lua events | `Cyclopedia.onEntryReceived(monsterId, data)`, `Cyclopedia.openEntry(monsterId)` |
| Config location | `client/modules/game_cyclopedia/game_cyclopedia.otmod` |

---

### 15. `game_imbuing`
**Purpose:** Item imbuing / enchanting UI. Lets players apply imbuments to equipment slots using the imbuement station.

| Item | Detail |
|------|--------|
| Server trigger | Imbuing opcodes triggered when player interacts with imbuement shrine/NPC |
| Key Lua events | `Imbuing.onOpen(item, slots)`, `Imbuing.onApply(slotIndex, imbumentId)` |
| Config location | `client/modules/game_imbuing/game_imbuing.otmod` |

---

### 16. `game_imbuementtracker`
**Purpose:** Tracks active imbuments on equipped items and shows remaining time / charges before expiry.

| Item | Detail |
|------|--------|
| Server trigger | Automatic on login and on imbument apply; server sends imbument state with timer |
| Key Lua events | `ImbuementTracker.onUpdate(item, slot, timeRemaining)`, `ImbuementTracker.onExpire(item, slot)` |
| Config location | `client/modules/game_imbuementtracker/game_imbuementtracker.otmod` |

---

### 17. `game_store`
**Purpose:** In-game cash shop UI. Displays purchasable offers by category, handles coin balance display, and confirms purchases.

| Item | Detail |
|------|--------|
| Server trigger | Store opcodes for catalog fetch, balance update, and purchase result |
| Key Lua events | `Store.onOpen()`, `Store.onPurchase(offerId, quantity)`, `Store.onBalanceUpdate(coins)` |
| Config location | `client/modules/game_store/game_store.otmod` |

---

### 18. `game_prey`
**Purpose:** Prey / hunting system UI. Players select prey targets for combat bonuses; displays active prey, time remaining, and reroll options.

| Item | Detail |
|------|--------|
| Server trigger | Prey opcodes on login and on prey selection/reroll |
| Key Lua events | `Prey.onPreyUpdate(slot, monsterName, bonusType, bonusValue, timeRemaining)` |
| Config location | `client/modules/game_prey/game_prey.otmod` |

---

### 19. `game_mapsystem`
**Purpose:** Minimap and world map UI with zoom, waypoint markers, and floor switching. Replaces the default minimap module.

| Item | Detail |
|------|--------|
| Server trigger | Standard map packets + extended opcode for custom markers/labels |
| Key Lua events | `MapSystem.addMarker(pos, iconId, label)`, `MapSystem.onFloorChange(floor)` |
| Config location | `client/modules/game_mapsystem/game_mapsystem.otmod` |

---

## OTClient Module Structure

Every OTClient module follows this layout:

```
client/modules/game_example/
├── game_example.otmod      # Module manifest (id, name, author, dependencies, scripts, widgets)
├── init.lua                # Entry point — loaded first; registers events and initializes state
├── game_example.lua        # Core logic
├── game_example.otui       # Main widget layout (UIWidget tree)
└── images/                 # Textures/icons used by the module (optional)
    └── icon.png
```

### `game_example.otmod` format

```lua
Module {
  name: "game_example",
  description: "Example module",
  author: "TibiaCore",
  version: 1,
  sandboxed: true,
  scripts: [ "game_example.lua" ],
  @onLoad: init,
  @onUnload: terminate
}
```

### `init.lua` conventions

```lua
function init()
  -- Connect to game events
  connect(g_game, {
    onGameStart = onGameStart,
    onGameEnd   = onGameEnd,
  })
  -- Register your UI panel
  ExamplePanel = g_ui.loadUI("game_example.otui", modules.game_interface.getRightPanel())
end

function terminate()
  disconnect(g_game, {
    onGameStart = onGameStart,
    onGameEnd   = onGameEnd,
  })
  ExamplePanel:destroy()
end
```

---

## Creating a New Module

1. **Create the directory** under `client/modules/game_yourmodule/`.
2. **Write `game_yourmodule.otmod`** — set `name`, `scripts`, `@onLoad`, `@onUnload`.
3. **Write `init.lua`** — call `connect()` for relevant game events; load your `.otui`.
4. **Write your `.otui`** — define the widget hierarchy.
5. **Register** the module in `client/modules/init.lua` (or the modules loader list) so it loads at startup.
6. **Document** the new module in this file.

### Minimal checklist
- [ ] `.otmod` manifest present
- [ ] `init()` and `terminate()` defined and connected
- [ ] Widget anchored or hidden on game end
- [ ] Added to `docs/OTCLIENT_MODULES_GUIDE.md`

---

## Extended Opcode System

TibiaCore uses a custom **extended opcode** channel to send arbitrary JSON payloads between server Lua and client Lua without modifying the C++ protocol.

Full reference: [`docs/LUA_OPCODE_SYSTEM_GUIDE.md`](LUA_OPCODE_SYSTEM_GUIDE.md)

### Quick reference

**Server → Client** (server Lua):
```lua
-- Send opcode 100 with a JSON payload to a specific player
player:sendExtendedOpcode(100, json.encode({ key = "value" }))
```

**Client receives** (client Lua, in your module's `init()`):
```lua
ProtocolGame.registerExtendedOpcode(100, function(protocol, opcode, buffer)
  local data = json.decode(buffer)
  -- handle data
end)
```

**Client → Server** (client Lua):
```lua
local protocol = g_game.getProtocolGame()
if protocol then
  protocol:sendExtendedOpcode(101, json.encode({ action = "claim" }))
end
```

**Server receives** (server Lua, in `creaturescripts` or global event):
```lua
-- In data/creaturescripts/scripts/extended_opcode.lua
function onExtendedOpcode(player, opcode, buffer)
  if opcode == 101 then
    local data = json.decode(buffer)
    -- handle action
  end
end
```

### Opcode allocation (reserved ranges)

| Range | Owner |
|-------|-------|
| 1–49 | Core engine / base systems |
| 50–99 | UI modules (talents, store, prey, etc.) |
| 100–149 | Combat systems (boss bar, cooldowns) |
| 150–199 | Economy systems (market, imbuing) |
| 200–255 | Free for new features |

---

## Custom Widgets

Widgets are defined in `.otui` files using a declarative syntax and instantiated in Lua.

### Defining a widget

```lua
-- game_example.otui
ExampleWindow < MainWindow {
  !text: tr("Example")
  size: 300 200

  Label {
    id: titleLabel
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    margin-top: 10
    !text: tr("Hello World")
  }

  Button {
    id: closeButton
    anchors.bottom: parent.bottom
    anchors.right: parent.right
    margin: 5
    !text: tr("Close")
    @onClick: modules.game_example.hide()
  }
}
```

### Loading and using a widget in Lua

```lua
local window

function init()
  window = g_ui.loadUI("game_example.otui", modules.game_interface.getRightPanel())
  window:hide()
end

function show()
  window:show()
  window:raise()
  window:focus()
end

function hide()
  window:hide()
end
```

### Useful widget API calls

| Call | Purpose |
|------|---------|
| `widget:show()` / `:hide()` | Visibility toggle |
| `widget:setText(str)` | Set label/button text |
| `widget:getChildById(id)` | Get child widget by id |
| `widget:addChild(widget)` | Dynamically add child |
| `widget:destroyChildren()` | Clear all children |
| `widget:setImageSource(path)` | Change image |
| `widget:setEnabled(bool)` | Enable/disable interaction |

---

## Effect Offsets

Some large visual effects render off-center and must be adjusted with `g_game.setEffectOffset()`.

Full documentation is in [`docs/SYSTEMS_OVERVIEW.md`](SYSTEMS_OVERVIEW.md) — search for **"setEffectOffset"**.

Quick usage:
```lua
-- Shift effect rendering by x, y pixels (called once during module init or spell registration)
g_game.setEffectOffset(effectId, x, y)
```

See also `docs/EFFECTS_MAPPING.md` for the complete list of effect IDs and their known offset requirements.
