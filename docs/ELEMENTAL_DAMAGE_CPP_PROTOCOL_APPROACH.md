# Elemental Damage Display - C++ Protocol Approach (Future Implementation)

**Date Created:** October 7, 2025  
**Status:** Documentation Only - Not Implemented  
**Purpose:** Reference guide for implementing elemental damage via core protocol modification

---

## Overview

This document describes how to implement elemental damage display by modifying the core C++ protocol between the server and client. This is **Approach 1** - the more robust but complex method that requires C++ compilation.

**Current Implementation:** We are using Approach 2 (Extended Opcodes/Lua). This document is kept for future migration if needed.

---

## Why Use This Approach?

### Advantages
- ✅ **Native Integration** - Part of core stats/skills system
- ✅ **Automatic Updates** - Sent whenever skills are updated
- ✅ **Type Safety** - C++ compile-time checking
- ✅ **Better Performance** - No JSON encoding/decoding overhead
- ✅ **Consistent with Core** - Follows same pattern as existing stats

### Disadvantages
- ❌ **Requires C++ Compilation** - Both server and client need rebuilding
- ❌ **More Complex** - Changes across multiple C++ files
- ❌ **Harder to Debug** - Requires debugging C++ code
- ❌ **Version Compatibility** - Need to ensure server/client versions match

---

## Implementation Guide

### Phase 1: Server-Side Changes

#### File 1: `Server/forgottenserver-1.4/src/protocolgame.cpp`

**Location:** `AddPlayerSkills()` function (around line 3045)

**Current Code:**
```cpp
void ProtocolGame::AddPlayerSkills(NetworkMessage& msg)
{
	msg.addByte(0xA1);

	for (uint8_t i = SKILL_FIRST; i <= SKILL_LAST; ++i) {
		msg.add<uint16_t>(std::min<int32_t>(player->getSkillLevel(i), std::numeric_limits<uint16_t>::max()));
		msg.add<uint16_t>(player->getBaseSkill(i));
		msg.addByte(player->getSkillPercent(i));
	}

	for (uint8_t i = SPECIALSKILL_FIRST; i <= SPECIALSKILL_LAST; ++i) {
		msg.add<uint16_t>(std::min<int32_t>(100, player->varSpecialSkills[i]));
		msg.add<uint16_t>(0);
	}
}
```

**Modified Code:**
```cpp
void ProtocolGame::AddPlayerSkills(NetworkMessage& msg)
{
	msg.addByte(0xA1);

	for (uint8_t i = SKILL_FIRST; i <= SKILL_LAST; ++i) {
		msg.add<uint16_t>(std::min<int32_t>(player->getSkillLevel(i), std::numeric_limits<uint16_t>::max()));
		msg.add<uint16_t>(player->getBaseSkill(i));
		msg.addByte(player->getSkillPercent(i));
	}

	for (uint8_t i = SPECIALSKILL_FIRST; i <= SPECIALSKILL_LAST; ++i) {
		msg.add<uint16_t>(std::min<int32_t>(100, player->varSpecialSkills[i]));
		msg.add<uint16_t>(0);
	}

	// ADD: Elemental Damage Values
	// Send all 7 elemental damage types
	msg.add<uint16_t>(std::min<int32_t>(player->getPhysicalDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getFireDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getIceDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getEarthDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getEnergyDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getHolyDamage(), std::numeric_limits<uint16_t>::max()));
	msg.add<uint16_t>(std::min<int32_t>(player->getDeathDamage(), std::numeric_limits<uint16_t>::max()));
}
```

**Note:** The server already has these methods in `player.cpp` (lines 292-395):
- `int32_t Player::getPhysicalDamage()`
- `int32_t Player::getFireDamage()`
- `int32_t Player::getIceDamage()`
- `int32_t Player::getEarthDamage()`
- `int32_t Player::getEnergyDamage()`
- `int32_t Player::getHolyDamage()`
- `int32_t Player::getDeathDamage()`

---

### Phase 2: Client-Side Changes

#### File 2: `Client/otclient-main/src/client/game.h`

**Add Feature Flag:**
```cpp
// Around line 100+ where other features are defined
enum GameFeature : uint8_t {
    // ... existing features ...
    GameElementalDamage = 100,  // Choose appropriate number
    // ... more features ...
};
```

#### File 3: `Client/otclient-main/src/client/protocolgameparse.cpp`

**Location:** `parsePlayerSkills()` function (around line 2369)

**Current Code End:**
```cpp
void ProtocolGame::parsePlayerSkills(const InputMessagePtr& msg) const
{
    // ... existing skill parsing code ...
    
    if (g_game.getFeature(Otc::GameForgeSkillStats)) {
        const uint8_t lastSkill = g_game.getClientVersion() >= 1332 ? Otc::LastSkill : Otc::Momentum + 1;
        for (int_fast32_t skill = Otc::Fatal; skill < lastSkill; ++skill) {
            const uint16_t level = msg->getU16();
            const uint16_t baseLevel = msg->getU16();
            m_localPlayer->setSkill(static_cast<Otc::Skill>(skill), level, 0);
            m_localPlayer->setBaseSkill(static_cast<Otc::Skill>(skill), baseLevel);
        }
    }
}
```

**Modified Code:**
```cpp
void ProtocolGame::parsePlayerSkills(const InputMessagePtr& msg) const
{
    // ... existing skill parsing code ...
    
    if (g_game.getFeature(Otc::GameForgeSkillStats)) {
        const uint8_t lastSkill = g_game.getClientVersion() >= 1332 ? Otc::LastSkill : Otc::Momentum + 1;
        for (int_fast32_t skill = Otc::Fatal; skill < lastSkill; ++skill) {
            const uint16_t level = msg->getU16();
            const uint16_t baseLevel = msg->getU16();
            m_localPlayer->setSkill(static_cast<Otc::Skill>(skill), level, 0);
            m_localPlayer->setBaseSkill(static_cast<Otc::Skill>(skill), baseLevel);
        }
    }

    // ADD: Parse Elemental Damage Values
    if (g_game.getFeature(Otc::GameElementalDamage)) {
        const uint16_t physicalDamage = msg->getU16();
        const uint16_t fireDamage = msg->getU16();
        const uint16_t iceDamage = msg->getU16();
        const uint16_t earthDamage = msg->getU16();
        const uint16_t energyDamage = msg->getU16();
        const uint16_t holyDamage = msg->getU16();
        const uint16_t deathDamage = msg->getU16();

        m_localPlayer->setElementalDamage(physicalDamage, fireDamage, iceDamage, 
                                          earthDamage, energyDamage, holyDamage, deathDamage);
    }
}
```

#### File 4: `Client/otclient-main/src/client/localplayer.h`

**Add Member Variables (around line 150+ in private section):**
```cpp
private:
    // ... existing variables ...
    
    // Elemental Damage Values
    uint16_t m_physicalDamage{ 0 };
    uint16_t m_fireDamage{ 0 };
    uint16_t m_iceDamage{ 0 };
    uint16_t m_earthDamage{ 0 };
    uint16_t m_energyDamage{ 0 };
    uint16_t m_holyDamage{ 0 };
    uint16_t m_deathDamage{ 0 };
```

**Add Setter Method (around line 60+ in public section):**
```cpp
public:
    // ... existing methods ...
    
    void setElementalDamage(uint16_t physical, uint16_t fire, uint16_t ice, 
                           uint16_t earth, uint16_t energy, uint16_t holy, uint16_t death);
    
    // Getters for Lua access
    uint16_t getPhysicalDamage() { return m_physicalDamage; }
    uint16_t getFireDamage() { return m_fireDamage; }
    uint16_t getIceDamage() { return m_iceDamage; }
    uint16_t getEarthDamage() { return m_earthDamage; }
    uint16_t getEnergyDamage() { return m_energyDamage; }
    uint16_t getHolyDamage() { return m_holyDamage; }
    uint16_t getDeathDamage() { return m_deathDamage; }
```

#### File 5: `Client/otclient-main/src/client/localplayer.cpp`

**Add Implementation:**
```cpp
void LocalPlayer::setElementalDamage(uint16_t physical, uint16_t fire, uint16_t ice, 
                                     uint16_t earth, uint16_t energy, uint16_t holy, uint16_t death)
{
    // Check if values actually changed
    if (m_physicalDamage == physical && m_fireDamage == fire && m_iceDamage == ice &&
        m_earthDamage == earth && m_energyDamage == energy && m_holyDamage == holy &&
        m_deathDamage == death) {
        return;
    }

    m_physicalDamage = physical;
    m_fireDamage = fire;
    m_iceDamage = ice;
    m_earthDamage = earth;
    m_energyDamage = energy;
    m_holyDamage = holy;
    m_deathDamage = death;

    // Trigger Lua callback
    callLuaField("onElementalDamageChange", physical, fire, ice, earth, energy, holy, death);
}
```

#### File 6: `Client/otclient-main/src/client/luafunctions.cpp`

**Register Lua Functions (find the registerClass section for LocalPlayer):**
```cpp
// Around where other LocalPlayer methods are registered
g_lua.registerMember<LocalPlayer>("getPhysicalDamage", &LocalPlayer::getPhysicalDamage);
g_lua.registerMember<LocalPlayer>("getFireDamage", &LocalPlayer::getFireDamage);
g_lua.registerMember<LocalPlayer>("getIceDamage", &LocalPlayer::getIceDamage);
g_lua.registerMember<LocalPlayer>("getEarthDamage", &LocalPlayer::getEarthDamage);
g_lua.registerMember<LocalPlayer>("getEnergyDamage", &LocalPlayer::getEnergyDamage);
g_lua.registerMember<LocalPlayer>("getHolyDamage", &LocalPlayer::getHolyDamage);
g_lua.registerMember<LocalPlayer>("getDeathDamage", &LocalPlayer::getDeathDamage);
```

---

### Phase 3: Lua Module Changes

#### File 7: `Client/otclient-main/modules/game_skills/skills.lua`

**Add Event Handler:**
```lua
function init()
    connect(LocalPlayer, {
        onExperienceChange = onExperienceChange,
        onLevelChange = onLevelChange,
        -- ... existing connections ...
        onElementalDamageChange = onElementalDamageChange  -- ADD THIS
    })
    -- ... rest of init ...
end

function terminate()
    disconnect(LocalPlayer, {
        onExperienceChange = onExperienceChange,
        onLevelChange = onLevelChange,
        -- ... existing disconnections ...
        onElementalDamageChange = onElementalDamageChange  -- ADD THIS
    })
    -- ... rest of terminate ...
end

-- ADD THIS FUNCTION
function onElementalDamageChange(player, physical, fire, ice, earth, energy, holy, death)
    setSkillValue('physicalDamage', physical)
    setSkillValue('fireDamage', fire)
    setSkillValue('iceDamage', ice)
    setSkillValue('earthDamage', earth)
    setSkillValue('energyDamage', energy)
    setSkillValue('holyDamage', holy)
    setSkillValue('deathDamage', death)
end
```

#### File 8: `Client/otclient-main/modules/game_skills/skills.otui`

**Add UI Widgets (after existing skill buttons):**
```lua
HorizontalSeparator
  margin-top: 5

Label
  !text: tr('Elemental Damage:')
  font: verdana-11px-monochrome
  color: #C0C0C0
  height: 15
  margin-top: 3

SkillButton
  id: physicalDamage
  height: 15
  SkillNameLabel
    !text: tr('Physical')
  SkillValueLabel

SkillButton
  id: fireDamage
  height: 15
  SkillNameLabel
    !text: tr('Fire')
  SkillValueLabel

SkillButton
  id: iceDamage
  height: 15
  SkillNameLabel
    !text: tr('Ice')
  SkillValueLabel

SkillButton
  id: earthDamage
  height: 15
  SkillNameLabel
    !text: tr('Earth')
  SkillValueLabel

SkillButton
  id: energyDamage
  height: 15
  SkillNameLabel
    !text: tr('Energy')
  SkillValueLabel

SkillButton
  id: holyDamage
  height: 15
  SkillNameLabel
    !text: tr('Holy')
  SkillValueLabel

SkillButton
  id: deathDamage
  height: 15
  SkillNameLabel
    !text: tr('Death')
  SkillValueLabel
```

---

## Compilation Steps

### Server Compilation

```bash
cd Server/forgottenserver-1.4
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### Client Compilation

```bash
cd Client/otclient-main
mkdir build && cd build
cmake ..
make -j$(nproc)
```

**Windows:** Use Visual Studio to rebuild both projects.

---

## Testing Procedure

1. **Start server** with modified binary
2. **Start client** with modified binary
3. **Login** and open Skills window (Alt+S)
4. **Equip items** with elemental damage
5. **Verify** values update in real-time
6. **Check** that values persist on relog

---

## Advantages Over Extended Opcode Approach

1. **Automatic Synchronization** - Updates sent with every skill update
2. **No Extra Network Traffic** - Piggybacks on existing skill packet
3. **Type Safety** - Compiler catches errors
4. **Native Performance** - No JSON encoding overhead
5. **Consistent** - Follows same pattern as Critical, Life Leech, etc.

---

## Migration Path

If currently using Extended Opcode approach (Approach 2), migration steps:

1. **Remove** extended opcode handlers from Lua
2. **Implement** C++ changes above
3. **Recompile** both server and client
4. **Keep** UI code from Approach 2 (mostly compatible)
5. **Test** thoroughly with various equipment

---

## Version Compatibility

**Important:** After implementing this approach, server and client versions MUST match. Mismatched versions will cause:
- Protocol errors
- Disconnections
- Incorrect data display

**Solution:** Implement version checking or feature flags to ensure compatibility.

---

## Notes

- Values are sent as `uint16_t` (0-65535 range)
- Values are clamped to prevent overflow
- Feature flag `GameElementalDamage` allows backward compatibility
- This approach follows the exact same pattern as existing special skills

---

## Related Files Reference

**Server:**
- `src/protocolgame.cpp` - Protocol implementation
- `src/protocolgame.h` - Protocol headers
- `src/player.cpp` - Player damage calculation methods
- `src/player.h` - Player class definition

**Client:**
- `src/client/protocolgameparse.cpp` - Protocol parsing
- `src/client/localplayer.h` - LocalPlayer class
- `src/client/localplayer.cpp` - LocalPlayer implementation
- `src/client/game.h` - Game features
- `modules/game_skills/skills.lua` - Skills module
- `modules/game_skills/skills.otui` - Skills UI

---

**End of Document**
