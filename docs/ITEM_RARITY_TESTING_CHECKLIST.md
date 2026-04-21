# Item Rarity System - Testing Checklist

## Pre-Deployment Checklist

### Server Compilation
- [ ] Compile server successfully
- [ ] No new compilation errors
- [ ] Server starts without crashes
- [ ] Check console for any warnings about new attributes

### Client Compilation
- [ ] Compile client successfully
- [ ] No new compilation errors
- [ ] Client starts without crashes
- [ ] Shaders load correctly (check console output)

### Server Testing

#### 1. Basic Functionality
- [ ] Create item with `Game.createItem(2400, 1)` works
- [ ] `item:setRarity(0)` works (Common)
- [ ] `item:setRarity(1)` works (Uncommon)
- [ ] `item:setRarity(2)` works (Rare)
- [ ] `item:setRarity(3)` works (Legendary)
- [ ] `item:setRarity(4)` works (Unique)
- [ ] `item:getRarity()` returns correct value

#### 2. Persistence Testing
- [ ] Set item rarity
- [ ] Save server
- [ ] Restart server
- [ ] Item still has correct rarity
- [ ] Check database - item attributes saved

#### 3. Network Testing
- [ ] Give player item with rarity
- [ ] Player receives item
- [ ] No disconnect/crashes
- [ ] Item appears in inventory

#### 4. Lua API Testing
```lua
-- Run this test script
function testRarity()
    local item = Game.createItem(2400, 1)
    
    -- Test setter
    item:setRarity(3)
    
    -- Test getter
    local rarity = item:getRarity()
    print("Rarity set: " .. rarity)
    
    -- Test persistence
    item:setAttribute(ITEM_ATTRIBUTE_RARITY, 2)
    local attr = item:getAttribute(ITEM_ATTRIBUTE_RARITY)
    print("Attribute: " .. attr)
    
    return rarity == 3 and attr == 2
end

print(testRarity() and "PASS" or "FAIL")
```
- [ ] Test script passes

### Client Testing

#### 1. Shader Loading
- [ ] Check console: "Loading shader: Rarity - Uncommon"
- [ ] Check console: "Loading shader: Rarity - Rare"
- [ ] Check console: "Loading shader: Rarity - Legendary"
- [ ] Check console: "Loading shader: Rarity - Unique"
- [ ] No shader compilation errors

#### 2. Visual Effects
- [ ] Common items (rarity 0) have NO glow
- [ ] Uncommon items (rarity 1) have GREEN glow
- [ ] Rare items (rarity 2) have BLUE/PURPLE glow
- [ ] Legendary items (rarity 3) have GOLDEN glow
- [ ] Unique items (rarity 4) have RAINBOW effect

#### 3. Inventory Display
- [ ] Items in backpack show shader
- [ ] Items on ground show shader
- [ ] Items in equipment slots show shader
- [ ] Items in trade window show shader
- [ ] Items in depot show shader

#### 4. Lua API Testing
```lua
-- Client-side test
function testClientRarity()
    local player = g_game.getLocalPlayer()
    local item = player:getInventoryItem(SlotRight)
    
    if item then
        local rarity = item:getRarity()
        print("Client rarity: " .. rarity)
        return true
    end
    return false
end
```
- [ ] Test script works
- [ ] Rarity matches server value

### Integration Testing

#### 1. Item Creation Flow
- [ ] Server creates item with rarity
- [ ] Server sends to client
- [ ] Client receives correct rarity
- [ ] Client applies correct shader
- [ ] Visual effect visible

#### 2. Item Movement
- [ ] Drop item on ground - shader persists
- [ ] Pick up item - shader persists
- [ ] Trade item - shader persists
- [ ] Store in depot - shader persists
- [ ] Retrieve from depot - shader persists

#### 3. Multiple Items
- [ ] Create 5 items with different rarities
- [ ] All show correct shaders simultaneously
- [ ] No performance issues
- [ ] No visual glitches

### Performance Testing

- [ ] Server FPS stable with rarity items
- [ ] Client FPS stable with rarity items
- [ ] 100+ items with shaders on screen - no lag
- [ ] Network bandwidth acceptable (only 1 byte per item)
- [ ] Memory usage acceptable

### Edge Cases

#### 1. Invalid Rarity Values
```lua
item:setRarity(255) -- Should work but show as common
item:setRarity(-1) -- Should handle gracefully
item:setRarity(nil) -- Should handle gracefully
```
- [ ] No crashes with invalid values

#### 2. Missing Shaders
- [ ] Rename shader file
- [ ] Client should not crash
- [ ] Item should render without shader
- [ ] Console shows error message

#### 3. Backward Compatibility
- [ ] Old items (no rarity set) default to Common
- [ ] Old saves load correctly
- [ ] No migration issues

### Database Verification

```sql
-- Check items with rarity in database
SELECT * FROM player_items WHERE attributes LIKE '%rarity%';

-- Verify item attributes
SELECT id, player_id, attributes 
FROM player_items 
WHERE attributes IS NOT NULL 
LIMIT 10;
```
- [ ] Rarity saved in attributes field
- [ ] Values are correct (0-4)

## Sample Test Script (Complete)

### Server Test Script
```lua
-- Save as: data/scripts/test_rarity.lua
local testRarity = CreatureEvent("TestRarity")

function testRarity.onLogin(player)
    -- Test all rarities
    local testItems = {
        {id = 2400, rarity = 0, name = "Common Sword"},
        {id = 2401, rarity = 1, name = "Uncommon Staff"},
        {id = 2402, rarity = 2, name = "Rare Axe"},
        {id = 2403, rarity = 3, name = "Legendary Club"},
        {id = 2404, rarity = 4, name = "Unique Spear"}
    }
    
    for _, data in ipairs(testItems) do
        local item = Game.createItem(data.id, 1)
        if item then
            item:setRarity(data.rarity)
            player:addItem(item)
            
            -- Verify
            local check = item:getRarity()
            if check == data.rarity then
                player:sendTextMessage(MESSAGE_INFO_DESCR, 
                    "✓ " .. data.name .. " created successfully")
            else
                player:sendTextMessage(MESSAGE_INFO_DESCR, 
                    "✗ " .. data.name .. " FAILED (expected " .. 
                    data.rarity .. ", got " .. check .. ")")
            end
        end
    end
    
    return true
end

testRarity:register()
```
- [ ] Test script runs successfully
- [ ] All items created with correct rarity

### Client Test Module
```lua
-- Save as: modules/test_rarity/rarity_test.lua
rarityTest = {}

function rarityTest.test()
    local player = g_game.getLocalPlayer()
    if not player then 
        print("Player not found")
        return 
    end
    
    -- Test all inventory slots
    local slots = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    for _, slot in ipairs(slots) do
        local item = player:getInventoryItem(slot)
        if item then
            local rarity = item:getRarity()
            print(string.format("Slot %d: Item %d has rarity %d", 
                slot, item:getId(), rarity))
        end
    end
    
    print("Rarity test complete")
end

-- Bind test command
g_keyboard.bindKeyPress('F12', rarityTest.test)
```
- [ ] Test module works
- [ ] F12 shows item rarities

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] No critical bugs
- [ ] Performance acceptable
- [ ] Shaders working correctly

### Deployment
- [ ] Backup database
- [ ] Backup server files
- [ ] Backup client files
- [ ] Deploy server updates
- [ ] Deploy client updates
- [ ] Deploy shader files

### Post-Deployment
- [ ] Monitor server logs
- [ ] Monitor client crashes
- [ ] Check player feedback
- [ ] Monitor performance metrics

## Known Limitations

1. **Shader Performance**: Many items with shaders may reduce FPS on low-end systems
2. **Network Overhead**: +1 byte per item in protocol
3. **Database Size**: Rarity stored in attributes increases row size slightly

## Success Criteria

✅ **SYSTEM IS READY** when:
- All compilation succeeds
- All tests pass
- Shaders display correctly
- No crashes or errors
- Performance is acceptable
- Players can see and use rarity system

---

**Last Updated**: Implementation Complete  
**Status**: Ready for Testing
