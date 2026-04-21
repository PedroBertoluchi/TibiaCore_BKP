# Triss — History

## Project: TibiaCore
Spell system specialist. Owns spells.xml and spell progression.

## Vocation Name Authority
VALID names (from vocations.xml):
Rookie, Mage, Archer, Knight, Occultist, Archmage, Necromancer, Marksman, Beastmaster, Templar, Death Knight, Blood Mage, Heretic

INVALID (cause server warnings):
Wizard, Cleric, Priest, Sniper, Fighter, Berserker

## Original Bug Mapping
- Wizard → Archmage (Mage's offensive promo)
- Cleric → Occultist (base holy/hybrid class)
- Priest → Blood Mage (healing Occultist promo)  
- Sniper → Marksman (precision Archer promo)
- Fighter → Knight (base melee class)
- Berserker → Death Knight (offensive Knight promo)

## Spell File Structure
spells.xml → references scripts at relative paths from data/spells/scripts/
Groups: attack, healing, support, conjuring

## !spells Talkaction Implementation

### Single Message Architecture
- Built all spell content into `lines` table with `\n` separators
- Single `sendTextMessage` call eliminates the message flood
- Stayed within TFS's message type constraints (MESSAGE_INFO_DESCR)

### Category Grouping
- Fixed order: attack → healing → support (not level-sorted mixed)
- Sorted by level within each category
- Headers only appear when category has at least one unlocked spell

### "Next Unlock" Context
- `getNextUnlock()` helper scans all spells for nearest locked level
- Global across all spells, not per-category
- Provides single actionable goal for player progression

### Available Filter Mode
- Category headers suppressed entirely if no unlocked spells in category
- Clean empty-state handling (no blank sections)

### Summary Stats
- Shows total/unlocked count (e.g., "3/7 unlocked") even in available-only mode
- Preserves full context without mode switching

## Local Helper Functions
Before `onSay()`:
- `getCategoryLabel(category)` — Returns display name for spell category
- `getNextUnlock()` — Scans all spells, returns next unlock level

## Learnings
- Rookie (vocationId=0) has no entry in vocationSpells → falls through to "no spells yet" message correctly
- Category headers must be checked for `available` filter presence; dynamic inclusion prevents spam
- Single message format is significantly more readable than wall of individual chat bubbles
- Summary stats are a must-have for progression clarity

## Teams/Sessions
- **2026-04-16 Vocation & DPS** (Alt0b11): Improved !spells UI with category grouping, single message output
- **2026-04-16 Spell System** (previous session): Fixed vocation name mappings, created 38 spell scripts
