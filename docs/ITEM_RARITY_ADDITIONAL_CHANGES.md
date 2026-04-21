# Additional Changes - String Attribute Support

## Summary

Good catch! Two additional changes were needed to fully integrate the rarity attribute with the existing attribute system.

## Changes Made

### 1. Added to `intAttributeTypes` bitmask (item.h)

**File**: `Server/forgottenserver-1.4/src/item.h`

**What**: Added `ITEM_ATTRIBUTE_RARITY` to the `intAttributeTypes` static constant

**Why**: This tells the attribute system that rarity is an **integer attribute** (not a string). This is crucial for:
- Type checking in `isIntAttrType()`
- Proper handling in `setAttribute()` and `getAttribute()`
- Serialization/deserialization logic

**Code**:
```cpp
const static uint64_t intAttributeTypes = ITEM_ATTRIBUTE_ACTIONID | ITEM_ATTRIBUTE_UNIQUEID | ITEM_ATTRIBUTE_DATE
    | ITEM_ATTRIBUTE_WEIGHT | ITEM_ATTRIBUTE_ATTACK | ITEM_ATTRIBUTE_DEFENSE | ITEM_ATTRIBUTE_EXTRADEFENSE
    | ITEM_ATTRIBUTE_ARMOR | ITEM_ATTRIBUTE_HITCHANCE | ITEM_ATTRIBUTE_SHOOTRANGE | ITEM_ATTRIBUTE_OWNER
    | ITEM_ATTRIBUTE_DURATION | ITEM_ATTRIBUTE_DECAYSTATE | ITEM_ATTRIBUTE_CORPSEOWNER | ITEM_ATTRIBUTE_CHARGES
    | ITEM_ATTRIBUTE_FLUIDTYPE | ITEM_ATTRIBUTE_DOORID | ITEM_ATTRIBUTE_DECAYTO | ITEM_ATTRIBUTE_WRAPID | ITEM_ATTRIBUTE_STOREITEM
    | ITEM_ATTRIBUTE_ATTACK_SPEED | ITEM_ATTRIBUTE_ENERGY_DAMAGE | ITEM_ATTRIBUTE_ICE_DAMAGE | ITEM_ATTRIBUTE_FIRE_DAMAGE
    | ITEM_ATTRIBUTE_DEATH_DAMAGE | ITEM_ATTRIBUTE_EARTH_DAMAGE | ITEM_ATTRIBUTE_HOLY_DAMAGE | ITEM_ATTRIBUTE_PHYSICAL_DAMAGE
    | ITEM_ATTRIBUTE_RARITY;  // <-- ADDED THIS
```

### 2. Added to `stringToItemAttribute()` function (tools.cpp)

**File**: `Server/forgottenserver-1.4/src/tools.cpp`

**What**: Added "rarity" string mapping to `ITEM_ATTRIBUTE_RARITY`

**Why**: This allows Lua scripts to use **string-based attribute access**:
```lua
-- Now you can use:
item:setAttribute("rarity", 3)
local rarity = item:getAttribute("rarity")
```

**Code**:
```cpp
itemAttrTypes stringToItemAttribute(const std::string& str)
{
    // ... existing mappings ...
    } else if (str == "physicaldamage") {
        return ITEM_ATTRIBUTE_PHYSICAL_DAMAGE;
    } else if (str == "rarity") {           // <-- ADDED THIS
        return ITEM_ATTRIBUTE_RARITY;
    }
    return ITEM_ATTRIBUTE_NONE;
}
```

## Why These Were Needed

Without these changes:

❌ **Without `intAttributeTypes`**:
- `item:setAttribute()` wouldn't know how to handle rarity
- Type checking would fail
- Serialization might be incorrect

❌ **Without `stringToItemAttribute`**:
- Could only use numeric constant: `item:setAttribute(ITEM_ATTRIBUTE_RARITY, 3)`
- Could NOT use string: `item:setAttribute("rarity", 3)` ❌

With these changes:

✅ **Complete Integration**:
- All three access methods work:
  1. `item:setRarity(3)` ← Direct (best)
  2. `item:setAttribute("rarity", 3)` ← String-based
  3. `item:setAttribute(ITEM_ATTRIBUTE_RARITY, 3)` ← Constant-based

## Updated File Count

**Total Modified Files: 17** (was 15, now 17)

### Server Files: 7 (was 6, now 7)
1. ✅ `src/enums.h`
2. ✅ `src/item.h` ← **Modified again (intAttributeTypes)**
3. ✅ `src/item.cpp`
4. ✅ `src/networkmessage.cpp`
5. ✅ `src/tools.cpp` ← **NEW FILE MODIFIED**
6. ✅ `src/luascript.h`
7. ✅ `src/luascript.cpp`

### Client Files: 5 (unchanged)
8. ✅ `src/client/const.h`
9. ✅ `src/client/item.h`
10. ✅ `src/client/item.cpp`
11. ✅ `src/client/protocolgameparse.cpp`
12. ✅ `src/client/luafunctions.cpp`

### Shader Files: 4 (unchanged)
13-16. ✅ Shader files

### Documentation: 5+ (unchanged)
17+. ✅ Documentation files

## Testing These Changes

### Test String-Based Access
```lua
-- Test in server console
/lua local item = Game.createItem(2400, 1); item:setAttribute("rarity", 3); print("Rarity: " .. item:getAttribute("rarity"))
-- Should output: Rarity: 3

-- Verify type checking works
/lua local item = Game.createItem(2400, 1); item:setRarity(2); local r = item:getAttribute("rarity"); print(r)
-- Should output: 2
```

### Verify Compatibility
All three methods should work identically:
```lua
local item = Game.createItem(2400, 1)

-- Method 1: Direct setter
item:setRarity(3)
print(item:getRarity()) -- 3

-- Method 2: String-based setAttribute
item:setAttribute("rarity", 2)
print(item:getAttribute("rarity")) -- 2

-- Method 3: Constant-based setAttribute
item:setAttribute(ITEM_ATTRIBUTE_RARITY, 1)
print(item:getAttribute(ITEM_ATTRIBUTE_RARITY)) -- 1
```

## Conclusion

These two additions ensure the rarity system is **fully integrated** with the existing attribute infrastructure, providing maximum flexibility for scripters.

Thank you for catching this! The implementation is now complete and robust. 🎉
