# Gameplay Rules Overrides

This document records intentional deviations from default TFS/OTClient behavior. Any future developer who encounters a "missing" restriction should check here before restoring it.

---

## Mount in Protection Zone — ALLOWED

**Decision:** Players may mount and remain mounted inside Protection Zones (PZ).

**Default TFS behavior (REMOVED):**
TFS enforces two PZ mount restrictions — both have been stripped:

### 1. `Player::toggleMount()` — `server/src/player.cpp`
The original code blocked mounting inside PZ:
```cpp
// REMOVED — do not restore
if (!group->access && tile->hasFlag(TILESTATE_PROTECTIONZONE)) {
    sendCancelMessage(RETURNVALUE_ACTIONNOTPERMITTEDINPROTECTIONZONE);
    return false;
}
```

### 2. `Player::onChangeZone()` — `server/src/player.cpp`
The original code auto-dismounted on PZ entry and auto-remounted on PZ exit:
```cpp
// REMOVED — do not restore
if (!group->access && isMounted()) {
    dismount();
    g_game.internalCreatureChangeOutfit(this, defaultOutfit);
    wasMounted = true;
}
// ...
} else {
    if (wasMounted) {
        toggleMount(true);
        wasMounted = false;
    }
}
```

**Where to look if mounts break again:**
- `Player::toggleMount()` — any early-return before outfit change
- `Player::onChangeZone()` — any `dismount()` call gated on `ZONE_PROTECTION`
- `game.cpp` — search `isMounted()` for any dismount triggered by tile/zone transitions
- `spells.cpp` — mount checks during spell casting (not changed, intentional)

**`wasMounted` flag:** Still declared in `player.h`. It is no longer set by PZ zone entry. The only remaining use is the `toggleMount()` cooldown bypass (`!wasMounted` at the exhaust check) — safe to leave in place.

---

## Lua `g_settings` — Default Values Pattern

**Problem:** `g_settings.getNumber(key)` returns `0` when a key has **never been saved** — it does NOT return `nil`. This means `if value ~= nil` is always true and the data_options default is never used on a fresh install.

**Fix applied in:** `client/modules/client_options/options.lua`

**Rule:** Always use `g_settings.exists(key)` before reading a setting:
```lua
-- CORRECT
if g_settings.exists(k) then
    setOption(k, g_settings.getNumber(k), true)
else
    setOption(k, defaultValue, true)  -- from data_options
end

-- WRONG — getNumber returns 0, not nil, for unset keys
local value = g_settings.getNumber(k)
if value ~= nil then ...  -- always true, default never applies
```

**Return values by type when key is not saved:**
| Function | Returns when unset |
|---|---|
| `g_settings.getNumber(k)` | `0` |
| `g_settings.getBoolean(k)` | `false` |
| `g_settings.getString(k)` | `""` |
| `g_settings.exists(k)` | `false` ← use this to detect unset |

---

## Mouse Control — Default: Classic Controls

**Decision:** Default mouse mode is **Classic Controls** (value `1`), not Regular Controls (value `0`).

**Where the default is set:** `client/modules/client_options/data_options.lua`
```lua
mouseControlMode = {
    value = 1, -- Classic Controls (0=Regular, 1=Classic, 2=Left Smart-Click)
```

---

## New C++ Bindings — Guard Against Old Binaries

When adding new `g_client` (or any singleton) Lua bindings in C++, the Lua modules will crash with `attempt to call field 'X' (a nil value)` if run against an older binary that doesn't have the binding compiled in.

**Pattern — always guard new bindings in Lua:**
```lua
if g_client.myNewFunction then
    g_client.myNewFunction(value)
end
```
This makes all Lua modules forward-compatible with older binaries during the window between code change and rebuild.
