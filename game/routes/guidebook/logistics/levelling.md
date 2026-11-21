# Logistics guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-21. Evidence: table ship_skills and the tool fleet view=levels, 2026-11-16 to 18; train.py runs 2026-11-16 13:05 to 14:27 UTC; browse_ships 2026-11-17 00:23 UTC; rule F23.

A hauler levels on the work of its own role; gathering is Mining's alone (rule F23). Levels now: the tool fleet, view=levels, member Apollo; XP per ship-hour by skill and route: hive.py stats xp.

| Kind of ship | Fit | Skills its work trains | Template | Next step |
|---|---|---|---|---|
| Hauler | mining laser, pulse laser | navigation (about 3 XP a jump, 1 a dock), trading (each sale), piloting | `stored-goods`, once missions | navigation 3 opens Signal Fragments (7,000 cr once) |
| Crafter (any hauler docked at a workshop) | none | crafting and refining (0 to 1 each on 145 smelting runs) | `craft-reserve`, hand chains | the level a recipe asks is not read |

- Navigation is bought with jumps: ten haulers went from 2 to 3 in 3 to 6 loops of six jumps and three docks between our own stations (49 loops, -5,341 cr, `train.py` of the skill logistics-stock): 534 cr a pilot against 7,000 cr once.
- First Hunt pays 50 Weapons XP, 15 Xenobiology XP and 20 Piloting XP.
- Tier 1 hulls ask no Piloting; Piloting 10, 20, 30 and 50 open tiers 2 to 5.
- The newest snapshot on record (2026-11-18 00:16 UTC, the tool fleet view=levels): Piloting 6 / 8 / 8 (lowest, median, highest), 177 Piloting XP an hour, 35 hours to Piloting 10.
