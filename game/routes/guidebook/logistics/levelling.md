# Logistics guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 4.

Which skills a ship of this division levels and on which work (rule F23): the work of
its own role first, gathering ore only when none is open. Every hauler is a Threshold.

| Kind of ship | Fit | Skills its work trains | Template | Next step |
|---|---|---|---|---|
| Hauler | mining laser, pulse laser | navigation (about 3 XP a jump, 1 a dock), trading (each sale), piloting | `stored-goods`, once missions | navigation 3 opens Signal Fragments (7,000 cr once) |
| Crafter (any hauler docked at a workshop) | none | crafting and refining (0 to 1 each on 145 smelting runs) | `craft-reserve`, hand chains | which crafting level a recipe asks for is not read: no quote asked for one |
| Gas hauler (4) | Gas Harvester I beside the laser | mining | `gas-harvest` | -- |
| Every hauler, fallback | mining laser | mining, deep core mining | `gather-reserve` | -- |

Levels on 2026-11-17 00:09 UTC (table ship_skills, 40 haulers): piloting 3 to 7 (average
4.5), deep core mining 1 to 7, mining 1 to 6, navigation 2 to 4, exploration 2, trading 0
to 2; crafting and refining 0 to 3 on the 9 haulers that carry them. The tool fleet
(view=levels, 00:01 UTC): Piloting median 6, 153 Piloting XP an hour since birth, 75 hours
to Piloting 10 and the tier-2 hulls at that rate (141 hours on 2026-11-16 09:00 UTC, 20
haulers).

Levels on 2026-11-17 04:05 UTC (table ship_skills; the tool fleet, view=levels): Piloting 4 /
6 / 7 (lowest, median, highest), 168 Piloting XP an hour since birth, 63 hours to Piloting 10;
navigation 3 or 4 on every hauler; crafting and refining 1 to 3 on haulers 1 to 20, none on the
20 born on 2026-11-16, which the any-role steel routes now train.

Levels on 2026-11-17 08:00 UTC (table ship_skills, 40 haulers; the tool fleet, view=levels): Piloting 5
/ 7 / 7, 171 Piloting XP an hour since birth, 57 hours to Piloting 10; navigation 3 to 5 (3.6 on
average); crafting and refining 2 to 4 on 36 haulers (2.6), none on 4; engineering 2 on one hauler;
Corporation Management 0 on all.

Navigation is bought with jumps: ten haulers went from navigation 2 to 3 in 3 to 6 loops
of six jumps and three docks between our own stations (49 loops, -5,341 cr, 2026-11-16
13:05 to 14:27 UTC; `train.py` of the skill logistics-stock), 534 cr a pilot against
7,000 cr once. First Hunt pays 50 Weapons XP, 15 Xenobiology XP and 20 Piloting XP.

A hull needs no Piloting level at tier 1: the freighters of section 5 are open to our
pilots today (`browse_ships` with can_fly, 2026-11-17 00:23 UTC). Piloting 10, 20, 30 and
50 open tiers 2 to 5.
