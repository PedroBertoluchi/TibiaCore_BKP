# Lua Extended Opcode System - Complete Implementation Guide

This guide provides a practical, step-by-step approach to implementing custom features using Lua extended opcodes for communication between The Forgotten Server (TFS) and OTClient - Redemption.

## Table of Contents
1. [Understanding the System](#understanding-the-system)
2. [Setting Up the Foundation](#setting-up-the-foundation)
3. [Complete Skill Tree Implementation](#complete-skill-tree-implementation)
4. [Advanced Patterns](#advanced-patterns)
5. [Debugging and Testing](#debugging-and-testing)
6. [Common Pitfalls](#common-pitfalls)

## Understanding the System

### What are Extended Opcodes?

Extended opcodes are **custom communication channels** that allow Lua scripts on the server to send data directly to Lua scripts on the client, and vice versa. This bypasses the need to modify C++ protocol code.

### Communication Flow
```
Server Lua Script → sendExtendedOpcode() → Network → Client Lua onExtendedOpcode()
Client Lua Script → sendExtendedOpcode() → Network → Server Lua onExtendedOpcode()
```

### Key Benefits
- ✅ **Pure Lua implementation** - No C++ modifications needed
- ✅ **Real-time communication** - Instant data synchronization
- ✅ **Bidirectional** - Server ↔ Client communication
- ✅ **Flexible data formats** - JSON, strings, numbers
- ✅ **Multiple channels** - Different opcodes for different features

## Setting Up the Foundation

### Step 1: Choose Your Opcode Range
First, decide on opcode numbers for your feature. Use a consistent system:

```lua
-- In both server and client scripts
local OPCODE_SKILLTREE = {
    -- Client → Server requests
    REQUEST_DATA = 0x01,
    UNLOCK_SKILL = 0x02,
    RESET_SKILLS = 0x03,

    -- Server → Client responses
    SEND_DATA = 0x10,
    UNLOCK_SUCCESS = 0x11,
    UNLOCK_FAILED = 0x12,
    SKILL_POINTS_UPDATED = 0x13
}
```

### Step 2: Basic Server Setup
Create a basic handler in your server scripts:

```lua
-- creaturescripts/skilltree_system.lua
local SkillTree = {}

-- Register creature event
function SkillTree.onLogin(player)
    -- Send initial skill tree data when player logs in
    SkillTree.sendSkillTreeData(player)
    return true
end

function SkillTree.sendSkillTreeData(player)
    -- This will be implemented in Step 3
end

-- Make sure to register this in login.lua or creaturescripts.xml
```

### Step 3: Basic Client Setup
Create the client module structure:

```lua
-- modules/game_skilltree/skilltree.lua
local SkillTree = {}

function SkillTree.init()
    -- Register opcode handlers
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA, SkillTree.onSkillTreeData)
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SUCCESS, SkillTree.onUnlockSuccess)
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_FAILED, SkillTree.onUnlockFailed)
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.SKILL_POINTS_UPDATED, SkillTree.onPointsUpdated)

    -- Request skill tree data after login
    connect(g_game, {
        onGameStart = SkillTree.onGameStart
    })
end

function SkillTree.onGameStart()
    SkillTree.requestSkillTreeData()
end

function SkillTree.requestSkillTreeData()
    g_game.sendExtendedOpcode(OPCODE_SKILLTREE.REQUEST_DATA, "")
end

function SkillTree.onSkillTreeData(opcode, buffer)
    -- Parse and display skill tree
end

-- Add to modules/game_skilltree/skilltree.otml to load the module
```

## Complete Skill Tree Implementation

### Part 1: Server-Side Implementation

#### Step 1: Database Schema
Add necessary storage for skill tree data:

```sql
-- Add to players table or create separate table
ALTER TABLE players ADD COLUMN skill_points INT DEFAULT 0;

-- Create skills table
CREATE TABLE player_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    skill_id INT NOT NULL,
    unlocked BOOLEAN DEFAULT FALSE,
    unlock_time INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE KEY (player_id, skill_id)
);
```

#### Step 2: Skill Tree Configuration
Create a skills configuration file:

```lua
-- data/lib/skilltree_config.lua
SkillTreeConfig = {
    -- Skill definitions
    skills = {
        [1] = {
            id = 1,
            name = "Fire Mastery",
            description = "Increases fire damage by 10%",
            icon = 101, -- Item ID for icon
            maxLevel = 5,
            pointsPerLevel = 3,
            prerequisites = {},
            vocation = {"Sorcerer", "Master Sorcerer"}
        },
        [2] = {
            id = 2,
            name = "Ice Shield",
            description = "Reduces ice damage by 15%",
            icon = 102,
            maxLevel = 3,
            pointsPerLevel = 5,
            prerequisites = {1},
            vocation = {"Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"}
        },
        [3] = {
            id = 3,
            name = "Sword Mastery",
            description = "Increases sword damage by 8%",
            icon = 103,
            maxLevel = 5,
            pointsPerLevel = 2,
            prerequisites = {},
            vocation = {"Knight", "Elite Knight"}
        }
    },

    -- Starting skill points
    startingPoints = 10,

    -- Points gained per level
    pointsPerLevel = 1
}
```

#### Step 3: Server Core Functions

```lua
-- data/lib/skilltree_functions.lua
local SkillTree = {}

function SkillTree.getSkillTreeData(player)
    local playerSkills = {}
    local totalPoints = SkillTreeConfig.startingPoints + (player:getLevel() - 1) * SkillTreeConfig.pointsPerLevel
    local usedPoints = 0

    -- Get player's unlocked skills
    local resultId = db.storeQuery("SELECT skill_id FROM player_skills WHERE player_id = " .. player:getGuid())
    if resultId then
        repeat
            local skillId = result.getNumber(resultId, "skill_id")
            playerSkills[skillId] = {
                unlocked = true,
                level = SkillTree.getSkillLevel(player, skillId)
            }
            usedPoints = usedPoints + SkillTree.getUsedPointsForSkill(skillId, playerSkills[skillId].level)
        until not result.next(resultId)
        result.free(resultId)
    end

    -- Build complete skill tree
    local skillTreeData = {
        skills = {},
        availablePoints = totalPoints - usedPoints,
        totalPoints = totalPoints,
        playerLevel = player:getLevel(),
        vocation = player:getVocation():getName()
    }

    -- Add all skills with player data
    for skillId, skillConfig in pairs(SkillTreeConfig.skills) do
        local playerSkill = playerSkills[skillId] or {unlocked = false, level = 0}

        skillTreeData.skills[skillId] = {
            id = skillConfig.id,
            name = skillConfig.name,
            description = skillConfig.description,
            icon = skillConfig.icon,
            maxLevel = skillConfig.maxLevel,
            pointsPerLevel = skillConfig.pointsPerLevel,
            prerequisites = skillConfig.prerequisites,
            unlocked = playerSkill.unlocked,
            currentLevel = playerSkill.level,
            canUnlock = SkillTree.canUnlockSkill(player, skillId, playerSkill.level),
            vocation = skillConfig.vocation
        }
    end

    return skillTreeData
end

function SkillTree.sendSkillTreeData(player)
    local data = SkillTree.getSkillTreeData(player)
    local jsonData = json.encode(data)
    player:sendExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA, jsonData)
end

function SkillTree.canUnlockSkill(player, skillId, currentLevel)
    local skill = SkillTreeConfig.skills[skillId]
    if not skill then return false end

    -- Check vocation
    if skill.vocation and #skill.vocation > 0 then
        local playerVoc = player:getVocation():getName()
        local hasVocation = false
        for _, vocation in ipairs(skill.vocation) do
            if vocation == playerVoc then
                hasVocation = true
                break
            end
        end
        if not hasVocation then return false end
    end

    -- Check prerequisites
    for _, prereqId in ipairs(skill.prerequisites) do
        local hasPrereq = db.storeQuery("SELECT skill_id FROM player_skills WHERE player_id = " ..
                          player:getGuid() .. " AND skill_id = " .. prereqId)
        if not hasPrereq then
            result.free(hasPrereq)
            return false
        end
        result.free(hasPrereq)
    end

    -- Check max level
    if currentLevel >= skill.maxLevel then return false end

    -- Check skill points
    local data = SkillTree.getSkillTreeData(player)
    return data.availablePoints >= skill.pointsPerLevel
end

function SkillTree.unlockSkill(player, skillId)
    if not SkillTree.canUnlockSkill(player, skillId, 0) then
        player:sendExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_FAILED, "Cannot unlock this skill")
        return false
    end

    local skill = SkillTreeConfig.skills[skillId]

    -- Add to database
    db.query("INSERT INTO player_skills (player_id, skill_id, unlocked, unlock_time) VALUES (" ..
             player:getGuid() .. ", " .. skillId .. ", 1, " .. os.time() ..
             ") ON DUPLICATE KEY UPDATE unlocked = 1, unlock_time = " .. os.time())

    -- Send success response
    player:sendExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SUCCESS, tostring(skillId))

    -- Send updated skill tree data
    SkillTree.sendSkillTreeData(player)

    return true
end

function SkillTree.onExtendedOpcode(player, opcode, buffer)
    if opcode == OPCODE_SKILLTREE.REQUEST_DATA then
        SkillTree.sendSkillTreeData(player)
    elseif opcode == OPCODE_SKILLTREE.UNLOCK_SKILL then
        local skillId = tonumber(buffer)
        if skillId then
            SkillTree.unlockSkill(player, skillId)
        end
    elseif opcode == OPCODE_SKILLTREE.RESET_SKILLS then
        SkillTree.resetSkills(player)
    end
end

-- Register the opcode handler
function SkillTree.registerEvents()
    -- This would be called from a global event or similar
end

return SkillTree
```

#### Step 4: Register Server Events

```lua
-- creaturescripts/skilltree_login.lua
local SkillTree = require("data.lib.skilltree_functions")

function onLogin(player)
    SkillTree.sendSkillTreeData(player)

    -- Register opcode handler for this player
    player:registerEvent("SkillTreeOpcode")
    return true
end
```

```lua
-- creaturescripts/skilltree_opcode.lua
local SkillTree = require("data.lib.skilltree_functions")

function onExtendedOpcode(player, opcode, buffer)
    SkillTree.onExtendedOpcode(player, opcode, buffer)
end
```

### Part 2: Client-Side Implementation

#### Step 1: Module Structure
Create the complete client module:

```lua
-- modules/game_skilltree/skilltree.lua
local SkillTree = {}

-- UI elements
local skillTreeWindow
local skillsContainer
local pointsLabel
local skillButtons = {}

function SkillTree.init()
    -- Create UI
    SkillTree.setupUI()

    -- Register opcode handlers
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA, SkillTree.onSkillTreeData)
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SUCCESS, SkillTree.onUnlockSuccess)
    g_game.registerExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_FAILED, SkillTree.onUnlockFailed)

    -- Connect events
    connect(g_game, {
        onGameStart = SkillTree.onGameStart,
        onGameEnd = SkillTree.onGameEnd
    })

    -- Load UI if already in game
    if g_game.isOnline() then
        SkillTree.onGameStart()
    end
end

function SkillTree.terminate()
    -- Cleanup
    disconnect(g_game, {
        onGameStart = SkillTree.onGameStart,
        onGameEnd = SkillTree.onGameEnd
    })

    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA)
    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SUCCESS)
    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_FAILED)

    if skillTreeWindow then
        skillTreeWindow:destroy()
    end

    SkillTree = nil
end

function SkillTree.setupUI()
    skillTreeWindow = g_ui.createWidget('SkillTreeWindow', rootWidget)
    skillTreeWindow:hide()

    skillsContainer = skillTreeWindow:recursiveGetChildById('skillsContainer')
    pointsLabel = skillTreeWindow:recursiveGetChildById('pointsLabel')

    -- Create skill tree button
    local skillTreeButton = modules.game_interface.getRootPanel():recursiveGetChildById('skillTreeButton')
    if not skillTreeButton then
        skillTreeButton = g_ui.createWidget('SkillTreeButton', modules.game_interface.getRootPanel())
        skillTreeButton:setIcon('/images/game/skilltree/button')
        skillTreeButton:setTooltip('Open Skill Tree')
    end

    skillTreeButton.onClick = SkillTree.toggle
end

function SkillTree.onGameStart()
    -- Request skill tree data when entering game
    addEvent(function()
        g_game.sendExtendedOpcode(OPCODE_SKILLTREE.REQUEST_DATA, "")
    end, 1000)
end

function SkillTree.onGameEnd()
    if skillTreeWindow then
        skillTreeWindow:hide()
    end
end

function SkillTree.toggle()
    if skillTreeWindow:isVisible() then
        skillTreeWindow:hide()
    else
        skillTreeWindow:show()
        skillTreeWindow:raise()
        skillTreeWindow:focus()
    end
end

function SkillTree.onSkillTreeData(opcode, buffer)
    local success, data = pcall(json.decode, buffer)
    if not success then
        g_logger.error("Failed to parse skill tree data: " .. buffer)
        return
    end

    SkillTree.currentData = data
    SkillTree.updateUI()
end

function SkillTree.updateUI()
    if not SkillTree.currentData then return end

    local data = SkillTree.currentData

    -- Update points display
    pointsLabel:setText("Skill Points: " .. data.availablePoints .. "/" .. data.totalPoints)

    -- Clear existing skills
    skillsContainer:destroyChildren()
    skillButtons = {}

    -- Create skill nodes
    for _, skill in pairs(data.skills) do
        SkillTree.createSkillNode(skill)
    end
end

function SkillTree.createSkillNode(skill)
    local skillWidget = g_ui.createWidget('SkillNode', skillsContainer)

    -- Set skill icon
    local icon = skillWidget:getChildById('icon')
    icon:setItemId(skill.icon)

    -- Set skill name
    local nameLabel = skillWidget:getChildById('nameLabel')
    nameLabel:setText(skill.name)

    -- Set skill description
    local descLabel = skillWidget:getChildById('descriptionLabel')
    descLabel:setText(skill.description)

    -- Set level display
    local levelLabel = skillWidget:getChildById('levelLabel')
    levelLabel:setText("Level " .. skill.currentLevel .. "/" .. skill.maxLevel)

    -- Set unlock button
    local unlockButton = skillWidget:getChildById('unlockButton')

    if skill.unlocked then
        unlockButton:setText("Upgrade")
        unlockButton:setEnabled(true)
    else
        unlockButton:setText("Unlock")
        unlockButton:setEnabled(skill.canUnlock)
    end

    if skill.currentLevel >= skill.maxLevel then
        unlockButton:setText("Max Level")
        unlockButton:setEnabled(false)
    end

    -- Store skill data
    skillButtons[skill.id] = {
        widget = skillWidget,
        button = unlockButton,
        skill = skill
    }

    -- Set button click handler
    unlockButton.onClick = function()
        SkillTree.attemptUnlockSkill(skill.id)
    end

    -- Style based on unlock status
    if skill.unlocked then
        skillWidget:setStyle('UnlockedSkillNode')
    else
        skillWidget:setStyle('LockedSkillNode')
    end
end

function SkillTree.attemptUnlockSkill(skillId)
    local skill = skillButtons[skillId]
    if not skill then return end

    -- Send unlock request to server
    g_game.sendExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SKILL, tostring(skillId))

    -- Disable button temporarily to prevent spam
    skill.button:setEnabled(false)
    addEvent(function()
        if skill and skill.button then
            skill.button:setEnabled(true)
        end
    end, 2000)
end

function SkillTree.onUnlockSuccess(opcode, buffer)
    local skillId = tonumber(buffer)
    if not skillId then return end

    -- Show success message
    modules.game_textmessage.displaySuccessMessage("Skill unlocked successfully!")

    -- Play sound effect
    g_sounds.playSound('skill_unlock.ogg')
end

function SkillTree.onUnlockFailed(opcode, buffer)
    -- Show error message
    modules.game_textmessage.displayFailureMessage("Cannot unlock skill: " .. buffer)

    -- Update UI to refresh skill states
    if SkillTree.currentData then
        SkillTree.updateUI()
    end
end

return SkillTree
```

#### Step 2: UI Definition

```xml
<!-- modules/game_skilltree/skilltree.otml -->
SkillTreeWindow < UIWindow
  size: 600 400
  @onEscape: SkillTree.hide()
  title: Skill Tree

  @onEnter: SkillTree.hide()

  VBox
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    margin-top: 10

    Label
      id: pointsLabel
      text: "Skill Points: 0/0"
      anchors.horizontalcenter: parent.horizontalcenter
      font: verdana-12px-bold

    VerticalSpacer
      size: 10

    ScrollArea
      id: skillsContainer
      layout: vertical
      height: 300
      padding: 5

SkillNode < UIWidget
  layout: horizontal
  height: 80
  margin: 5
  padding: 10
  background-color: #2a2a2a
  border: 1 #555555
  border-radius: 5

  Item
    id: icon
    width: 64
    height: 64
    margin-right: 10

  VBox
    anchors.verticalcenter: parent.verticalcenter
    width: 300

    Label
      id: nameLabel
      font: verdana-12px-bold
      color: #ffffff

    Label
      id: descriptionLabel
      font: verdana-10px
      color: #cccccc
      wrap: true

    Label
      id: levelLabel
      font: verdana-10px
      color: #ffcc00

  Widget
    anchors.verticalcenter: parent.verticalcenter
    width: 20

  Button
    id: unlockButton
    width: 100
    height: 30
    anchors.verticalcenter: parent.verticalcenter

UnlockedSkillNode < SkillNode
  background-color: #2a4a2a
  border: 1 #4a7a4a

LockedSkillNode < SkillNode
  background-color: #4a2a2a
  border: 1 #7a4a4a
  opacity: 0.8

SkillTreeButton < UIButton
  size: 34 34
  anchors.top: parent.top
  anchors.right: parent.right
  margin-top: 45
  margin-right: 85
  image-source: /images/game/skilltree/button
  image-clip: 0 0 34 34
```

#### Step 3: Module Registration

```xml
<!-- modules/game_skilltree/mod.otml -->
Module
  name: game_skilltree
  description: Skill tree system
  author: Your Name
  website: https://github.com/yourname
  version: 1.0
  sandboxed: false
  scripts: [ skilltree ]
  @onLoad: SkillTree.init()
  @onUnload: SkillTree.terminate()
```

## Advanced Patterns

### Pattern 1: Real-time Updates
Send updates when player gains levels or points:

```lua
-- Server: On level up
function onAdvance(player, skill, oldLevel, newLevel)
    if skill == SKILL_LEVEL then
        -- Check if gained new skill points
        local newPoints = SkillTreeConfig.pointsPerLevel
        if newPoints > 0 then
            player:sendTextMessage(MESSAGE_EVENT_ADVANCE, "You gained " .. newPoints .. " skill points!")
            SkillTree.sendSkillTreeData(player)
        end
    end
end
```

### Pattern 2: Skill Effects
Apply skill effects when unlocked:

```lua
-- Server: Apply skill effects
function SkillTree.applySkillEffect(player, skillId, level)
    local skill = SkillTreeConfig.skills[skillId]

    if skill.id == 1 then -- Fire Mastery
        -- Add fire damage bonus
        player:setStorageValue(20001, level * 10) -- 10% per level
    elseif skill.id == 2 then -- Ice Shield
        -- Add ice resistance
        player:setStorageValue(20002, level * 15) -- 15% per level
    end
end
```

### Pattern 3: Visual Effects
Send visual effect data to client:

```lua
-- Server: Send effect with unlock
function SkillTree.unlockSkill(player, skillId)
    -- ... unlock logic ...

    -- Send effect to client
    local effectData = {
        type = "skill_unlock",
        skillId = skillId,
        effect = "fire_explosion",
        color = "#ff6600"
    }
    player:sendExtendedOpcode(OPCODE_SKILLTREE.VISUAL_EFFECT, json.encode(effectData))
end

-- Client: Handle visual effects
function SkillTree.onVisualEffect(opcode, buffer)
    local data = json.decode(buffer)
    if data.type == "skill_unlock" then
        -- Play particle effect
        SkillTree.playUnlockEffect(data.effect, data.color)
    end
end
```

## Debugging and Testing

### Server Debugging
```lua
-- Add logging to server functions
function SkillTree.sendSkillTreeData(player)
    local data = SkillTree.getSkillTreeData(player)
    local jsonData = json.encode(data)

    if g_config.getBoolean(ConfigManager::DEBUG_PROTOCOL) then
        print("Sending skill tree data to player " .. player:getName() .. ": " .. jsonData)
    end

    player:sendExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA, jsonData)
end
```

### Client Debugging
```lua
-- Add logging to client functions
function SkillTree.onSkillTreeData(opcode, buffer)
    g_logger.debug("Received skill tree data: " .. buffer)

    local success, data = pcall(json.decode, buffer)
    if not success then
        g_logger.error("Failed to parse skill tree data: " .. buffer)
        return
    end

    g_logger.debug("Parsed skill tree: " .. table.tostring(data))
    SkillTree.updateUI()
end
```

### Testing Tools
```lua
-- Test module for offline development
-- modules/game_skilltree/test_skills.lua
local TestSkills = {}

function TestSkills.generateMockData()
    return {
        skills = {
            {
                id = 1,
                name = "Fire Mastery",
                description = "Increases fire damage by 10%",
                icon = 101,
                maxLevel = 5,
                pointsPerLevel = 3,
                prerequisites = {},
                unlocked = true,
                currentLevel = 2,
                canUnlock = true
            }
        },
        availablePoints = 5,
        totalPoints = 15,
        playerLevel = 20,
        vocation = "Sorcerer"
    }
end

function TestSkills.testSkillTree()
    local mockData = TestSkills.generateMockData()
    SkillTree.onSkillTreeData(OPCODE_SKILLTREE.SEND_DATA, json.encode(mockData))
end

-- Call this for testing
TestSkills.testSkillTree()
```

## Common Pitfalls and Solutions

### Pitfall 1: JSON Encoding Issues
**Problem**: Complex tables with circular references or unsupported types
**Solution**: Ensure data is JSON-serializable:

```lua
-- Bad: Contains functions or circular references
local badData = {
    player = player, -- Complex object
    calculate = function() end -- Function
}

-- Good: Simple data types only
local goodData = {
    playerId = player:getId(),
    playerName = player:getName(),
    skills = {} -- Simple array
}
```

### Pitfall 2: Opcode Conflicts
**Problem**: Using opcode numbers that conflict with other modules
**Solution**: Use a structured numbering system:

```lua
-- Good: Organized by feature
local OPCODES = {
    SKILLTREE_BASE = 0x10,
    SKILLTREE_REQUEST = 0x11,
    SKILLTREE_DATA = 0x12,

    MARKET_BASE = 0x20,
    MARKET_REQUEST = 0x21,
    MARKET_DATA = 0x22
}
```

### Pitfall 3: Memory Leaks
**Problem**: Not cleaning up opcode handlers
**Solution**: Always unregister handlers:

```lua
function SkillTree.terminate()
    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.SEND_DATA)
    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_SUCCESS)
    g_game.unregisterExtendedOpcode(OPCODE_SKILLTREE.UNLOCK_FAILED)
    -- ... other cleanup
end
```

### Pitfall 4: Network Overload
**Problem**: Sending too much data too frequently
**Solution**: Implement rate limiting and data caching:

```lua
-- Server: Rate limiting
local lastUpdateTime = {}
function SkillTree.sendSkillTreeData(player)
    local now = os.time()
    local playerId = player:getId()

    if lastUpdateTime[playerId] and now - lastUpdateTime[playerId] < 1 then
        return -- Limit to once per second
    end

    lastUpdateTime[playerId] = now
    -- ... send data
end
```

This complete guide provides everything needed to implement a robust skill tree system using Lua extended opcodes. The same patterns can be adapted for any custom feature requiring real-time server-client communication.

---

## Opcode Registry

All opcodes currently in use. **Never reuse a number.**

| Opcode | Constant | Direction | Purpose |
|--------|----------|-----------|---------|
| 1 | `OPCODE_LANGUAGE` | C→S | Language preference (`"en"` / `"pt"`) |
| 112 | — | S→C | Boss kill counts |
| 113 | — | S→C | Elemental damage display |
| 202 | — | S→C | Loyalty system data |
| 203 | — | S→C | Daily reward state |
| 214 | — | S→C | Player titles |
| 216 | — | S→C | Boss progress bar |
| 218 | — | S→C | Talent system data |
| 219 | — | S→C | Map system |
| 220 | — | S→C | Missions list |
| 225 | `VOCATION_OPCODE` | C↔S | Vocation modal (open/choose/request) |
| 226 | `BLESS_OPCODE` | C↔S | Blessing golden frame (request/blessed) |

---

## Real-World Example: Blessing Golden Frame (Opcode 226)

This is the cleanest real-time pull+push pattern in the codebase — use it as a template for any boolean state that must stay in sync.

### Architecture

```
onGameStart (client)
  → sendExtendedOpcode(226, {action="request"})
    → extendedopcode.lua checks hasBlessing(1..6)
      → sendExtendedOpcode(226, {blessed=true/false})
        → inventory.lua onBlessOpcode → show/hide golden frame

Player:addBlessing() / Player:removeBlessing()  (anywhere on server)
  → wrapper in player.lua auto-pushes opcode 226
    → client updates frame instantly
```

### Why "pull on connect" beats the `addEvent` delay
TFS fires `onLogin` **before** sending the initial map/game packets to the client.
A client-side pull from `onGameStart` happens **after** the client is fully ready, eliminating the need for the historical `addEvent(..., 1500)` workaround.

### Server — `extendedopcode.lua`
```lua
local BLESS_OPCODE = 226

-- Inside onExtendedOpcode:
elseif opcode == BLESS_OPCODE then
    local ok, data = pcall(function() return json.decode(buffer) end)
    if ok and type(data) == "table" and data.action == "request" then
        local blessed = false
        for i = 1, 6 do
            if player:hasBlessing(i) then blessed = true; break end
        end
        player:sendExtendedOpcode(BLESS_OPCODE, json.encode({ blessed = blessed }))
    end
```

### Server — `lib/core/player.lua` (auto-push wrapper)
```lua
-- Wrap addBlessing / removeBlessing so ANY source triggers a client update
local _addBlessing = Player.addBlessing
function Player.addBlessing(self, blessing)
    _addBlessing(self, blessing)
    pcall(function() self:sendExtendedOpcode(226, json.encode({ blessed = true })) end)
end

local _removeBlessing = Player.removeBlessing
function Player.removeBlessing(self, blessing)
    _removeBlessing(self, blessing)
    pcall(function()
        local blessed = false
        for i = 1, 6 do if self:hasBlessing(i) then blessed = true; break end end
        self:sendExtendedOpcode(226, json.encode({ blessed = blessed }))
    end)
end
```
`pcall` is required because `onLogin` / DB loading can call these before a player has an active network connection.

### Client — `game_inventory/inventory.lua`
```lua
local BLESS_OPCODE = 226

local function onBlessOpcode(protocol, opcode, buffer)
    local ok, data = pcall(json.decode, buffer)
    if not ok or type(data) ~= "table" then return end
    setBlessFrame(data.blessed == true)
end

-- In onGameStart:
ProtocolGame.registerExtendedOpcode(BLESS_OPCODE, onBlessOpcode)
inventoryController:sendExtendedOpcode(BLESS_OPCODE, json.encode({ action = "request" }))

-- In onGameEnd:
ProtocolGame.unregisterExtendedOpcode(BLESS_OPCODE, onBlessOpcode)
setBlessFrame(false)
```

### Reusing this pattern for other boolean states
1. Pick the next free opcode number (check the registry above)
2. Add the opcode constant to `extendedopcode.lua`
3. Handle `{action="request"}` → read server state → `sendExtendedOpcode(n, {value=...})`
4. Wrap the relevant `Player.*` setter in `player.lua` with `pcall(sendExtendedOpcode, ...)`
5. In the client module: register handler + send request in `onGameStart`, unregister in `onGameEnd`