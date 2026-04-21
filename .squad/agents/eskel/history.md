# Eskel — History

## Project: TibiaCore
Performance tester. Checks Lua scripts for efficiency, AoE lag, memory use.

## Performance Rules Learned
- Combat() objects must be module-level (not inside onCastSpell)
- AoE with AREA_CROSS or AREA_FULLBEAM: watch for radius > 5 on busy servers
- setCallback is cheaper than inline formula evaluation

## Learnings
