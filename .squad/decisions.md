# Squad Decisions

## Active Decisions

### 1. Vocation Selection & DPS Trainer System (2026-04-16)
**Author:** Ciri  
**Status:** Deployed

- **ModalWindow for vocation UI:** Provides clean structured UI with choices, avoiding typo ambiguity vs chat dialog. Modal ID 10001 chosen to avoid collision. Restricted to Rookies only (one-time use).
- **DPS tracker uses per-player storage:** Idiomatic TFS pattern for persistent per-player state (storage keys 90001–90003: start, cumulative damage, last-hit). Uses `os.time()` for timestamps.
- **Idle reset at 30s:** If player stops hitting dummy for 30 seconds, session auto-resets on next hit to prevent AFK gaps inflating DPS numbers.
- **Training Dummy: 1M HP, non-hostile:** Never dies under normal testing, never aggros, never rewards XP/loot. Sufficient for extended sessions.
- **Oracle vocation fix:** Corrected broken vocation mapping (cleric→archer, fighter→occultist) and renamed choices to match actual vocations (Mage, Archer, Knight, Occultist).

### 2. !spells Talkaction UI Overhaul (2026-04-16)
**Author:** Triss  
**Status:** Deployed

- **Single message output:** Consolidated all spell output into one `sendTextMessage` call with `\n` separators, eliminating message flood.
- **Category grouping order:** Attack → Healing → Support (fixed order, not level-sorted).
- **Dynamic headers:** Category headers only appear when category has at least one unlocked spell (suppresses empty sections).
- **Global "next unlock":** Scans all spells for nearest locked level, providing single actionable goal rather than per-category context.
- **Summary always visible:** Total/unlocked count (e.g., "3/7 unlocked") shown even in `!spells available` mode for context preservation.

### 3. Spell Scripts & Vocation Fix (2026-04-16)
**Author:** Ciri, Triss  
**Status:** Historical (Previous Session)

- Created 38 new Lua spell scripts for all 12 vocations + !spells talkaction
- Fixed spell vocation name mappings: Wizard→Archmage, Cleric→Occultist, Priest→Blood Mage, Sniper→Marksman, Fighter→Knight, Berserker→Death Knight

### 4. Vocation Balance Framework (2026-04-16)
**Author:** Lambert  
**Status:** Ready for Implementation

- Comprehensive vocation balance analysis identifies 10 critical/high/medium priority issues
- Phase 1 focus: Add Occultist spell progression, fix Knight mana cost, add tank healing, fill spell gaps
- Phase 2: Create promotion identities (Archmage AoE vs Necromancer summons, etc.)
- Phase 3: Polish progression milestones and soul mechanics
- See `.squad/skills/vocation-balance/SKILL.md` for full analysis

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
