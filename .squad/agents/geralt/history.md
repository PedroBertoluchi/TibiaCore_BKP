# Geralt — History

## Project: TibiaCore
Custom Tibia MMORPG server (C++/TFS) + client (OTClient). Alt0b11 is the lead dev.

## Vocations (12 total)
- Base: Rookie(0), Mage(1), Archer(2), Knight(3), Occultist(4)
- Mage promos: Archmage(5), Necromancer(6)
- Archer promos: Marksman(7), Beastmaster(8)
- Knight promos: Templar(9), Death Knight(10)
- Occultist promos: Blood Mage(11), Heretic(12)

## Critical Issue (Session 1)
spells.xml uses wrong vocation names causing server warnings:
- Wizard → Archmage, Cleric → Occultist, Priest → Blood Mage
- Sniper → Marksman, Fighter → Knight, Berserker → Death Knight

## Learnings
