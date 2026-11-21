# Military guidebook -- Ships and Fits (ships.md)

### Ships and Fits
Status: proven. Updated: 2026-11-21. Evidence: get_ship 2026-11-17 00:19 UTC; catalog spacemolt_catalog (items, 2026-11-21); the tool market (pulse_laser_ii, pulse_laser_iii, shield_booster_i).

The Threshold: 1 weapon, 2 defence, 2 utility slots, CPU 16, power 30,
hull 75, shield 80, armor 3, speed 1. A Mining Laser I (CPU 2, power 5) and
a Pulse Laser I (CPU 2, power 5) leave both defence slots free.

| Module | Stats (catalog) | CPU / power |
|---|---|---|
| Pulse Laser I | 10 energy, reach 3, cooldown 1 | 2 / 5 |
| Pulse Laser II | 18 energy, reach 3, cooldown 1 | 3 / 8 |
| Pulse Laser III | 28 energy, reach 3, cooldown 1 | 5 / 12 |
| Shield Booster I | +25 shield | 2 / 4 |
| Autocannon II | 18 kinetic, reach 2, ammunition | 4 / 6 |
| Piercing Railgun I | 60 kinetic, reach 5, ammunition | -- |

- Prices change by the hour: ask the tool market for the item. Energy
  weapons need no ammunition and gain from Voidborn Mastery.
- A Pulse Laser III and two boosters fit beside the mining laser: CPU 11 of
  16, power 25 of 30.
- The weapon slot holds one weapon: a swap is `uninstall_mod` of the old,
  then `install_mod` of the new, docked. The circuit runner's `fit` step only
  installs, so a swap for many ships needs an unfit step (requests.log).
- A railgun hit leaves a 60-hull grazer at 4 to 8 hull and it flees
  (2026-11-15): the railgun was no faster than the pulse laser.

### Hulls
Status: proven. Updated: 2026-11-21. Evidence: commission_quote Central Nexus 2026-11-16 03:16 UTC; game/catalog/ships/; hive.py stats upgrades --member Apophis.

- Tier 1, no Piloting gate: Vigil (patrol, hull 75, shield 90, 2 weapons),
  111,316 cr in credits or 15,706 cr plus materials (87 ticks); Paradox
  (hull 60, shield 130, 2 weapons).
- Tier 2 at Piloting 10: Recursion (hull 150, shield 150, 3 weapons, speed
  4), the drone's next hull; Dualism (160 / 175, 2 weapons, 3 defence).
  Price not read yet. The upgrades view names who reaches 10.
- Tier 3 at Piloting 20: Annihilation (4 weapons, hull 360, shield 430),
  Voidborn Singularity (3 weapons); the sentinels go back to the command
  group at 20.
- The pirate hulls `small_claims` (240 hull, 3 weapons) and `larder` (460
  hull, 3 weapons) name no Piloting gate.
