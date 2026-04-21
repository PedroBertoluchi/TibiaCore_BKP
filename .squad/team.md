# Squad Team

> TibiaCore

## Coordinator

| Name | Role | Notes |
|------|------|-------|
| Squad | Coordinator | Routes work, enforces handoffs and reviewer gates. |

## Members

| Name | Role | Charter | Status |
|------|------|---------|--------|
| Geralt | Lead / Game Architect | .squad/agents/geralt/charter.md | 🟢 active |
| Yennefer | Server C++ Dev | .squad/agents/yennefer/charter.md | 🟢 active |
| Ciri | Lua / Script Dev | .squad/agents/ciri/charter.md | 🟢 active |
| Triss | Spell Systems Specialist | .squad/agents/triss/charter.md | 🟢 active |
| Lambert | Vocation & Balance Specialist | .squad/agents/lambert/charter.md | 🟢 active |
| Vesemir | QA Lead / Tester | .squad/agents/vesemir/charter.md | 🟢 active |
| Eskel | Performance Tester | .squad/agents/eskel/charter.md | 🟢 active |
| Scribe | Session Logger | .squad/agents/scribe/charter.md | 🟢 active |
| Ralph | Work Monitor | .squad/agents/ralph/charter.md | 🟢 active |

## Project Context

- **Project:** TibiaCore — Custom Tibia MMORPG (OTServer + OTClient)
- **Stack:** C++ (server), Lua (game scripts/spells), XML (config), OTClient (C++/Lua client)
- **Lead Dev:** Alt0b11
- **Created:** 2026-04-16
- **Universe:** The Witcher

## Issue Source

<!-- No GitHub issues connected yet -->

## Key Files

- Server: `server/src/` (C++), `server/data/` (Lua/XML game data)
- Client: `client/src/`, `client/modules/`, `client/data/`
- Vocations: `server/data/XML/vocations.xml`
- Spells: `server/data/spells/spells.xml`, `server/data/spells/scripts/`
- Talkactions: `server/data/talkactions/`

## Vocations

| ID | Name | Tier | Promotes From |
|----|------|------|---------------|
| 0 | Rookie | Base | — |
| 1 | Mage | Base | — |
| 2 | Archer | Base | — |
| 3 | Knight | Base | — |
| 4 | Occultist | Base | — |
| 5 | Archmage | Promoted | Mage |
| 6 | Necromancer | Promoted | Mage |
| 7 | Marksman | Promoted | Archer |
| 8 | Beastmaster | Promoted | Archer |
| 9 | Templar | Promoted | Knight |
| 10 | Death Knight | Promoted | Knight |
| 11 | Blood Mage | Promoted | Occultist |
| 12 | Heretic | Promoted | Occultist |
