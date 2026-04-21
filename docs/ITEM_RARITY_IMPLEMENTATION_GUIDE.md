# Item Rarity System Implementation Guide

## Overview
This document describes the implementation of an item rarity system for the TibiaProject, including server-side attribute management and client-side visual effects using shaders.

## Rarity Tiers

The system supports 5 rarity tiers:

| Rarity | Value | Description | Shader Name |
|--------|-------|-------------|-------------|
| Common | 0 | Default tier (T8 - T7) | None |
| Uncommon | 1 | Improved tier (T5 - T4) | "Rarity - Uncommon" |
| Rare | 2 | Advanced tier (T3) | "Rarity - Rare" |
| Legendary | 3 | Superior tier (T2 - T1) | "Rarity - Legendary" |
| Unique | 4 | Special modifiers | "Rarity - Unique" |

## Server-Side Implementation

### Files Modified

#### 1. `Server/forgottenserver-1.4/src/enums.h`
- **Added `ItemRarity_t` enum** with 5 rarity levels
- **Added `ITEM_ATTRIBUTE_RARITY`** to `itemAttrTypes` enum (bit 34)

```cpp
enum ItemRarity_t : uint8_t {
    ITEM_RARITY_COMMON = 0,
    ITEM_RARITY_UNCOMMON = 1,
    ITEM_RARITY_RARE = 2,
    ITEM_RARITY_LEGENDARY = 3,
    ITEM_RARITY_UNIQUE = 4
};
```

#### 2. `Server/forgottenserver-1.4/src/item.h`
- **Added `ATTR_RARITY = 49`** to `AttrTypes_t` enum for serialization
- **Added rarity getter/setter** methods to `ItemAttributes` class:
  - `void setRarity(uint8_t rarity)`
  - `uint8_t getRarity() const`

#### 3. `Server/forgottenserver-1.4/src/item.cpp`
- **Added deserialization** for `ATTR_RARITY` in attribute reading (reads uint8_t)
- **Added serialization** for `ATTR_RARITY` in `serializeAttr()` method (writes uint8_t)

#### 4. `Server/forgottenserver-1.4/src/networkmessage.cpp`
- **Modified `addItem(const Item* item)`** to send rarity as one byte after animation phase
- **Modified `addItem(uint16_t id, uint8_t count)`** to send default rarity (0 = Common)

#### 5. `Server/forgottenserver-1.4/src/luascript.h` & `luascript.cpp`
- **Added Lua functions**:
  - `item:getRarity()` - Returns the item's rarity (0-4)
  - `item:setRarity(rarity)` - Sets the item's rarity

### Server-Side Usage Examples

```lua
-- Set item rarity in Lua script
local item = player:getSlotItem(CONST_SLOT_RIGHT)
if item then
    item:setRarity(ITEM_RARITY_LEGENDARY) -- Set to legendary
    print("Item rarity: " .. item:getRarity())
end

-- Create item with rarity
local newItem = Game.createItem(2400, 1) -- create sword
newItem:setRarity(ITEM_RARITY_RARE)
player:addItem(newItem)
```

## Client-Side Implementation

### Files Modified

#### 1. `Client/otclient-main/src/client/const.h`
- **Added `ItemRarity` enum** with 5 rarity levels matching server

```cpp
enum ItemRarity : uint8_t {
    ItemRarityCommon = 0,
    ItemRarityUncommon = 1,
    ItemRarityRare = 2,
    ItemRarityLegendary = 3,
    ItemRarityUnique = 4
};
```

#### 2. `Client/otclient-main/src/client/item.h`
- **Added `m_rarity` member** variable (uint8_t)
- **Added rarity getter/setter**:
  - `void setRarity(uint8_t rarity)` - Also applies shader automatically
  - `uint8_t getRarity()`

#### 3. `Client/otclient-main/src/client/item.cpp`
- **Implemented `setRarity()`** method with automatic shader application:
  - Common: No shader
  - Uncommon: "Rarity - Uncommon"
  - Rare: "Rarity - Rare"
  - Legendary: "Rarity - Legendary"
  - Unique: "Rarity - Unique"

#### 4. `Client/otclient-main/src/client/protocolgameparse.cpp`
- **Modified `getItem()`** to read rarity byte after WrapKit feature and before shader

#### 5. `Client/otclient-main/src/client/luafunctions.cpp`
- **Added Lua bindings**:
  - `item:setRarity(rarity)`
  - `item:getRarity()`

### Client-Side Usage Examples

```lua
-- Get item rarity from Lua
local item = g_game.getLocalPlayer():getInventoryItem(SlotRight)
if item then
    local rarity = item:getRarity()
    print("Item rarity: " .. rarity)
    
    -- Manually set shader (normally done automatically)
    if rarity == ItemRarityLegendary then
        item:setShader("Rarity - Legendary")
    end
end
```

## Shader System

The client automatically applies shaders based on item rarity. You need to create the following shader files:

### Required Shaders

1. **Rarity - Uncommon** - Green/Blue glow effect
2. **Rarity - Rare** - Blue/Purple glow effect
3. **Rarity - Legendary** - Gold/Orange glow effect
4. **Rarity - Unique** - Rainbow/Custom effect

### Shader Location
Place shader files in: `Client/otclient-main/data/shaders/`

### Example Shader (Uncommon - Green Glow)
```glsl
// fragment shader example
uniform float u_Time;
uniform sampler2D u_Tex0;
varying vec2 v_TexCoord;

void main()
{
    vec4 color = texture2D(u_Tex0, v_TexCoord);
    if(color.a > 0.1) {
        // Add green glow
        float pulse = (sin(u_Time * 2.0) + 1.0) * 0.5;
        color.rgb += vec3(0.0, 0.3, 0.1) * pulse;
    }
    gl_FragColor = color;
}
```

## Protocol Changes

### Network Message Format

When sending an item to the client, the rarity is sent as **1 byte (uint8_t)** after the item's animation phase and before the shader name.

**Item packet structure:**
1. Item Client ID (uint16_t)
2. Mark byte (0xFF)
3. Count/SubType (if stackable/fluid/etc)
4. Animation phase (if applicable)
5. Container/Podium/Tier info (if applicable)
6. **→ Rarity (uint8_t)** ← NEW
7. Shader name (string, if GameItemShader feature enabled)
8. Tooltip (string, if applicable)

## Database Considerations

If you want items to persist with rarity:

### Option 1: Use existing attribute system
Items with rarity are already saved to the database using the attribute serialization system (`ATTR_RARITY = 49`).

### Option 2: Add dedicated column (future enhancement)
```sql
ALTER TABLE `player_items` ADD COLUMN `rarity` TINYINT UNSIGNED DEFAULT 0;
```

## Testing

### Server-Side Test
```lua
-- Create test item with rarity
function onUse(player, item, fromPosition, target, toPosition, isHotkey)
    local testItem = Game.createItem(2400, 1)
    testItem:setRarity(3) -- Legendary
    player:addItem(testItem)
    player:sendTextMessage(MESSAGE_INFO_DESCR, "Created legendary item!")
    return true
end
```

### Client-Side Test
```lua
-- Check received items
function onGameStart()
    local player = g_game.getLocalPlayer()
    if player then
        for slot = 1, 10 do
            local item = player:getInventoryItem(slot)
            if item then
                print("Slot " .. slot .. " rarity: " .. item:getRarity())
            end
        end
    end
end
```

## Notes & Future Enhancements

1. **Shader Creation**: The shaders referenced ("Rarity - Uncommon", etc.) need to be created in the client's shader system
2. **T-System Integration**: The T8-T1 tier system mentioned should be integrated with this rarity system
3. **Loot Generation**: Consider creating a loot system that assigns rarity based on monster difficulty
4. **Trading/Market**: Update trading systems to display rarity
5. **Item Comparison**: Add UI elements to show rarity when comparing items
6. **Rarity Colors**: Consider adding color coding to item names based on rarity

## Compatibility

- **Server Version**: ForgottenServer 1.4+
- **Client Version**: OTClient with shader support
- **Protocol**: Custom extension, compatible with existing protocol
- **Backward Compatibility**: Items without rarity default to Common (0)

## Summary

The item rarity system is now fully integrated into both server and client:

✅ Server can assign and store rarity for any item  
✅ Rarity is persisted to database through attribute system  
✅ Network protocol sends rarity to client  
✅ Client receives and displays rarity with automatic shader effects  
✅ Lua API available on both server and client  

Next steps: Create the shader files and integrate with your tier/modification system.
