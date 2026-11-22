# Military guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-22. Evidence: get_ship 2026-11-17 00:19 UTC; game/catalog/tables/modules.tsv (0.732.0); the tool market (pulse_laser_ii, pulse_laser_iii, shield_booster_i).

The Threshold: 1 weapon, 2 defence, 2 utility slots, CPU 16, power 30,
hull 75, shield 80, armor 3, speed 1. A Mining Laser I (CPU 2, power 5) and
a Pulse Laser I (CPU 2, power 5) leave both defence slots free.

| Module | Stats (catalog) | CPU / power |
|---|---|---|
| Pulse Laser I | 10 energy, reach 3, cooldown 1 | 2 / 5 |
| Pulse Laser II | 18 energy, reach 3, cooldown 1 | 3 / 8 |
| Pulse Laser III | 28 energy, reach 3, cooldown 1 | 5 / 12 |
| Plasma Cannon II | 38 thermal, cooldown 2, +50% to hull | 6 / 14 |
| Shield Booster I | +25 shield | 2 / 4 |

- Prices change by the hour: ask the tool market for the item. Energy
  and plasma weapons need no ammunition; energy gains from Voidborn
  Mastery, thermal cuts the armor of creatures (tests.md, Weapon fits).
- A Pulse Laser III or a Plasma Cannon II and two boosters fit beside
  the mining laser: CPU 11 or 12 of 16, power 25 or 27 of 30.
- The weapon slot holds one weapon: a route's `fit` with `replace` swaps
  it in one docked stop (BLUEPRINT.md).
- A railgun was no faster than the pulse laser on 60-hull grazers
  (2026-11-15).

### Hulls
Status: proven. Updated: 2026-11-22. Evidence: commission_quote Central Nexus 2026-11-16 03:16 UTC and Node Beta 2026-11-22 08:11 UTC; game/catalog/ships/; hive.py stats upgrades --member Apophis.

- Tier 1, no Piloting gate: Vigil (patrol, hull 75, shield 90, 2 weapons),
  111,316 cr in credits or 15,706 cr plus materials (87 ticks); Paradox
  (hull 60, shield 130, 2 weapons).
- Tier 2 at Piloting 10: Recursion (hull 150, shield 150, 3 weapons, speed
  4), the drone's next hull; Dualism (160 / 175, 2 weapons, 3 defence).
  Node Beta commissions it for 315,699 cr, or 45,247 cr plus materials
  (commission_quote 2026-11-22 08:11 UTC, default fit two Pulse Laser II);
  asked of the purse (requests ENT-345). The upgrades view names who is 10.
- Tier 3 at Piloting 20: Annihilation (4 weapons, hull 360, shield 430),
  Voidborn Singularity (3 weapons); the sentinels go back to the command
  group at 20.
- The pirate hulls `small_claims` (240 hull, 3 weapons) and `larder` (460
  hull, 3 weapons) name no Piloting gate.
