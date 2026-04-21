# Compilation Error Fixes

## Errors Found
During compilation, errors were discovered related to missing `getRarity()` and `setRarity()` methods in the `Item` class.

### Error 1: `getRarity` is not a member of `Item`
**File**: `networkmessage.cpp` line 122  
**Issue**: Called `item->getRarity()` but method doesn't exist in Item class

### Error 2: `getRarity` is not a member of `Item`  
**File**: `luascript.cpp` line 6846  
**Issue**: Called `item->getRarity()` but method doesn't exist in Item class

### Error 3: `setRarity` is not a member of `Item`
**File**: `luascript.cpp` line 6863  
**Issue**: Called `item->setRarity()` but method doesn't exist in Item class

### Error 4: `lua_pushnumber` function does not take 1 argument
**File**: `luascript.cpp` line 6846  
**Issue**: Missing the second parameter (the number value) - this was already fixed

## Root Cause
The `setRarity()` and `getRarity()` methods were only added to the `ItemAttributes` class, but NOT to the `Item` class itself. 

The `Item` class needs its own wrapper methods (just like `setActionId()`, `setOwner()`, etc.) that call the underlying `setIntAttr()` and `getIntAttr()` methods.

## Fix Applied

### Added to Item class (item.h)
Added these methods to the `Item` class after `getCorpseOwner()`:

```cpp
void setRarity(uint8_t rarity) {
    setIntAttr(ITEM_ATTRIBUTE_RARITY, rarity);
}
uint8_t getRarity() const {
    if (!attributes) {
        return 0;
    }
    return static_cast<uint8_t>(getIntAttr(ITEM_ATTRIBUTE_RARITY));
}
```

This follows the same pattern as other Item attribute methods like:
- `setActionId()` / `getActionId()`
- `setOwner()` / `getOwner()`
- `setCorpseOwner()` / `getCorpseOwner()`

## Why This Pattern

The Item class has TWO levels of attribute access:

1. **ItemAttributes class** (line ~195 in item.h)
   - Internal attribute storage
   - Has `setRarity()` and `getRarity()` methods
   - Not directly accessible from Item instances

2. **Item class** (line ~521 in item.h)
   - Public interface for items
   - Needs wrapper methods that call `setIntAttr()` / `getIntAttr()`
   - **This is what we were missing!**

## Compilation Status
✅ **FIXED** - Added getRarity() and setRarity() to Item class  
✅ **CONSISTENT** - Follows same pattern as other attributes  
✅ **NULL-SAFE** - Checks if attributes exist before accessing  

## Files Modified (to fix errors)
1. ✅ `Server/forgottenserver-1.4/src/item.h` - Added getRarity() and setRarity() to Item class
2. ✅ `Server/forgottenserver-1.4/src/networkmessage.cpp` - Already uses item->getRarity()
3. ✅ `Server/forgottenserver-1.4/src/luascript.cpp` - Already uses item->getRarity() and item->setRarity()

The server should now compile successfully! 🎉

