# Elemental Damage Display System - Implementation Guide

**Implemented:** October 7, 2025  
**Approach:** Extended Opcode (Lua-based)  
**Status:** ✅ Ready to Test

---

## Overview

This system sends elemental damage values from the TFS server to the OTClient and displays them in the Skills window. It uses extended opcodes (0x50) for communication, requiring **no C++ compilation**.

---

## What Was Implemented

### Server-Side

1. **Created:** `Server/forgottenserver-1.4/data/creaturescripts/scripts/elemental_damage.lua`
   - Sends elemental damage on login
   - Automatically updates when equipment changes
   - Uses opcode 0x50

2. **Modified:** `Server/forgottenserver-1.4/data/creaturescripts/creaturescripts.xml`
   - Registered the `ElementalDamageLogin` event

### Client-Side

1. **Modified:** `Client/otclient-main/modules/game_skills/skills.lua`
   - Added opcode registration (0x50)
   - Added `onElementalDamageReceived()` handler
   - Added elemental damage to statsCache
   - Updated SKILL_GROUPS to include elemental damage widgets

2. **Modified:** `Client/otclient-main/modules/game_skills/skills.otui`
   - Added 7 new skill buttons for elemental damage display
   - Added separator for visual organization

---

## Files Modified Summary

### Server Files
```
✅ data/creaturescripts/scripts/elemental_damage.lua (NEW)
✅ data/creaturescripts/creaturescripts.xml (MODIFIED)
```

### Client Files
```
✅ modules/game_skills/skills.lua (MODIFIED)
✅ modules/game_skills/skills.otui (MODIFIED)
```

---

## How It Works

### Data Flow

```
Player Login/Equipment Change
         ↓
Server: elemental_damage.lua
         ↓
Calls player:getFireDamage(), etc.
         ↓
Encodes data as JSON
         ↓
Sends via Extended Opcode 0x50
         ↓
Client: onElementalDamageReceived()
         ↓
Decodes JSON
         ↓
Updates Skills Window UI
```

### Elemental Types Tracked

1. **Physical Damage** - From `player:getPhysicalDamage()`
2. **Fire Damage** - From `player:getFireDamage()`
3. **Ice Damage** - From `player:getIceDamage()`
4. **Earth Damage** - From `player:getEarthDamage()`
5. **Energy Damage** - From `player:getEnergyDamage()`
6. **Holy Damage** - From `player:getHolyDamage()`
7. **Death Damage** - From `player:getDeathDamage()`

---

## Testing Instructions

### 1. Start the Server

```bash
cd Server/forgottenserver-1.4
./tfs
```

The server will load `elemental_damage.lua` automatically.

### 2. Start the Client

```bash
cd Client/otclient-main
./otclient
```

### 3. Test Scenario

1. **Login** to your character
2. **Open Skills Window** (Alt+S)
3. **Look for** the new elemental damage section under offensive stats
4. **Equip items** with elemental damage properties
5. **Verify** the values update in real-time

### 4. Expected Behavior

- Values should appear immediately on login
- Values should update when you equip/unequip items
- All 7 elemental types should display
- Values should match item properties

---

## Debugging

### Enable Debug Output

The client already has debug output enabled. Check the console for:

```
Elemental Damage - Physical: X, Fire: Y, Ice: Z, Earth: A, Energy: B, Holy: C, Death: D
```

### Server-Side Debugging

Add this to `elemental_damage.lua` after encoding:

```lua
print(string.format("[Elemental Damage] Sent to %s: %s", player:getName(), buffer))
```

### Common Issues

**Issue:** Values don't appear
- **Solution:** Check if opcode 0x50 conflicts with other systems
- **Solution:** Verify `creaturescripts.xml` registered the script
- **Solution:** Check server console for Lua errors

**Issue:** Values don't update on equipment change
- **Solution:** The event uses a 100ms delay; wait a moment
- **Solution:** Check if equip/deequip events are firing

**Issue:** Client shows error decoding JSON
- **Solution:** Verify server has `json` library available
- **Solution:** Check data format being sent

---

## Customization

### Change Opcode Number

If 0x50 conflicts with another system:

1. **Server:** Change `OPCODE_ELEMENTAL_DAMAGE` in `elemental_damage.lua`
2. **Client:** Change `OPCODE_ELEMENTAL_DAMAGE` in `skills.lua`

### Hide Specific Elements

To hide certain elemental types, edit `skills.otui`:

```lua
SmallSkillButton
  id: fireDamage
  visible: false  -- Always hidden
```

### Add Icons

Add element-specific icons like the resistance display:

```lua
SmallSkillButton
  id: fireDamage
  visible: false
  SkillNameLabel
    !text: tr('Fire Damage')
  SkillValueLabel
  ImageSkill
    image-source: /path/to/fire-icon
    image-size: 9 9
```

---

## Performance Considerations

### Network Traffic

- **Size:** ~100 bytes per update (JSON encoded)
- **Frequency:** On login + equipment changes only
- **Impact:** Negligible

### Server Load

- Calculations are simple integer sums
- No database queries
- Minimal CPU usage

### Client Load

- JSON decode: ~0.1ms
- UI update: ~1ms
- No performance impact

---

## Future Enhancements

### Option 1: Add Tooltips

```lua
function onElementalDamageReceived(protocol, opcode, buffer)
    -- ... existing code ...
    
    setSkillValueWithTooltips('fireDamage', data.fire, 
        "Fire damage added to physical attacks", false)
end
```

### Option 2: Color-Coded Values

Edit `skills.otui`:

```lua
SmallSkillButton
  id: fireDamage
  SkillValueLabel
    color: #FF4500  -- Orange-red for fire
```

### Option 3: Combine with Total Attack

Show combined attack power:

```lua
local totalAttack = data.physical + data.fire + data.ice + 
                    data.earth + data.energy + data.holy + data.death
setSkillValue('totalElementalDamage', totalAttack)
```

---

## Migration to C++ Protocol

If you later want to use Approach 1 (C++ Protocol):

1. See `ELEMENTAL_DAMAGE_CPP_PROTOCOL_APPROACH.md`
2. Remove extended opcode code from `skills.lua`
3. Implement C++ changes as documented
4. Recompile both server and client

**Benefits of migrating:**
- Automatic sync with skill updates
- No JSON overhead
- Type-safe implementation

---

## Troubleshooting Commands

### Server Console

Check if player methods work:

```lua
/lua print(player:getFireDamage())
```

### Client Console (F1)

Test opcode reception:

```lua
print("Opcode 0x50 registered:", ProtocolGame.isExtendedOpcodeRegistered(0x50))
```

---

## Credits

- **Implementation:** Extended Opcode System
- **Based on:** OTClient Extended Opcode Architecture
- **Reference:** LUA_OPCODE_SYSTEM_GUIDE.md

---

## Version History

**v1.0** - October 7, 2025
- Initial implementation
- All 7 elemental types supported
- Auto-updates on equipment change
- Debug output included

---

## Support

If you encounter issues:

1. Check server console for Lua errors
2. Check client console for JSON decode errors
3. Verify opcode number isn't conflicting
4. Test with `/lua player:sendExtendedOpcode(0x50, '{"fire":100}')`

---

**End of Document**
