# Item Rarity Quick Reference

## Rarity Values
```cpp
0 = Common      (no visual effect)
1 = Uncommon    (green/blue shader)
2 = Rare        (blue/purple shader)
3 = Legendary   (gold/orange shader)
4 = Unique      (custom shader)
```

## Server-Side (Lua)

### Set Item Rarity
```lua
-- Method 1: Direct setter (recommended)
item:setRarity(3) -- Sets to Legendary

-- Method 2: Using setAttribute with string
item:setAttribute("rarity", 3)

-- Method 3: Using setAttribute with constant
item:setAttribute(ITEM_ATTRIBUTE_RARITY, 3)
```

### Get Item Rarity
```lua
-- Method 1: Direct getter (recommended)
local rarity = item:getRarity() -- Returns 0-4

-- Method 2: Using getAttribute with string
local rarity = item:getAttribute("rarity")

-- Method 3: Using getAttribute with constant
local rarity = item:getAttribute(ITEM_ATTRIBUTE_RARITY)
```

### Example: Random Rarity on Loot
```lua
function onDeath(creature, corpse, killer, mostDamageKiller, lastHitUnjustified, mostDamageUnjustified)
    local items = corpse:getItems()
    for _, item in ipairs(items) do
        local chance = math.random(100)
        if chance > 95 then
            item:setRarity(4) -- Unique (5%)
        elseif chance > 85 then
            item:setRarity(3) -- Legendary (10%)
        elseif chance > 70 then
            item:setRarity(2) -- Rare (15%)
        elseif chance > 50 then
            item:setRarity(1) -- Uncommon (20%)
        else
            item:setRarity(0) -- Common (50%)
        end
    end
    return true
end
```

## Client-Side (Lua)

### Get Item Rarity
```lua
local item = player:getInventoryItem(SlotRight)
local rarity = item:getRarity()
```

### Manual Shader Override
```lua
item:setShader("Rarity - Legendary")
```

## Required Shaders

Create these shader files in `Client/otclient-main/data/shaders/`:

1. `Rarity - Uncommon.frag` - Green/blue glow
2. `Rarity - Rare.frag` - Blue/purple glow
3. `Rarity - Legendary.frag` - Gold/orange glow
4. `Rarity - Unique.frag` - Rainbow/custom effect

## Shader Template

```glsl
// Save as: data/shaders/Rarity - Uncommon.frag
uniform float u_Time;
uniform sampler2D u_Tex0;
varying vec2 v_TexCoord;

void main()
{
    vec4 color = texture2D(u_Tex0, v_TexCoord);
    if(color.a > 0.1) {
        float pulse = (sin(u_Time * 2.0) + 1.0) * 0.5;
        // Uncommon = Green glow
        color.rgb += vec3(0.0, 0.3 * pulse, 0.1 * pulse);
    }
    gl_FragColor = color;
}
```

## Color Recommendations

- **Uncommon**: Green (#00FF00, rgb(0, 1, 0))
- **Rare**: Blue (#0080FF, rgb(0, 0.5, 1))
- **Legendary**: Gold (#FFD700, rgb(1, 0.84, 0))
- **Unique**: Rainbow (cycle through hues)

## Testing Commands

### Server Console
```lua
/lua local player = Player("YourName"); local item = player:getSlotItem(CONST_SLOT_RIGHT); if item then item:setRarity(3); player:sendTextMessage(MESSAGE_INFO_DESCR, "Rarity set!") end
```

### Check Item Rarity
```lua
/lua local player = Player("YourName"); local item = player:getSlotItem(CONST_SLOT_RIGHT); if item then print("Rarity: " .. item:getRarity()) end
```
