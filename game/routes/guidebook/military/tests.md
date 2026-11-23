# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-23. Evidence: table runs (lowest_hull_pct); list_ships and switch_ship (switch_hull.py RESULT); gauges.py ship; table herds; admirals.log ENT-111; routes fit-armor-plate-ii-*-test, recursion-parts-*, hunt-kit-*.

- Whale hunts alone with a Shield Booster II: the siphon and Antares herds
  hold (lowest hull 52 to 100 percent); two other herds took ships to 4 and
  14 percent and are off for danger (F9). The proven way stays a group of
  three Laser III ships.
- The Recursion: commissioned for credits at Node Beta; the yard's own
  bids filled by our once routes took it from SOURCING to BUILDING. It
  came with two Pulse Laser II, a Focused Beam I, a Shield Booster II and
  a Shield Recharger II (hull 150, shield 200, speed 4; list_ships).
  switch_hull.py moved its pilot in (the Threshold stays stored there):
  firepower 52 and toughness 350 by the gauges, so prey of up to 175
  weight passes alone. Its first runs: a kit hunt (cauldronback, magnet-
  barnacle), then the whale hunts; three results decide the batch.
- The Atria kit's creature parts (orders P3): hunts of silica-borer,
  cauldronback and magnet-barnacle (hunt-kit-*, gift to a hauler at Node
  Beta). The wild herds are small (one to four a place) and F38 keeps
  two, so a place gives one kill a run at most; mirror-skate and inkwyrm
  herds are never huntable (two animals a place). The parts a kill drops
  are not measured yet.
- Armor Plate II (armor +10, speed penalty 1): fitted on a Crimson Shard
  (armor 8 -> 18) and a Solarian Theoria (5 -> 15); speed stays 1 (ship
  files). Lifted for the role (F17); its hunts' lowest hull is read next.
- Pulse Laser III hunts: tortoises, deuteron slugs, bulwarks; reserve
  goods (ferrous nodule, carapace).
- Cloudwhales (20 jumps out): a group sets out only on a census under
  120 minutes (`--census-minutes`).
- Pirate formations (F27): the next build is a group form of
  pirate_test.py (three Laser III ships on one lone weak pirate).
### Group hunts
Status: proven. Updated: 2026-11-23. Evidence: observations kind group_hunt (2026-11-17 to 2026-11-23 04:46 UTC); errors.log ENT-129, ENT-130; spacemolt.com/docs/combat; skill military-turn group_hunt.py.

`group_hunt.py` (skill script, background) takes free drones within
`--max-jumps` of home, docks them, makes a game fleet, waits until every
pilot stands at the place (`--arrive-ticks`), sets targets, advances each
ship to its own `dist` 2, flees all at hull under 85 percent or shield 0,
docks for repair, releases all.

- The leader counts in the capacity of 3. Members join the leader's hunt
  only when they are in the system as it engages (the docs; the bulwark
  flight of 2026-11-21 lost both members to a late arrival); a member
  left out joins with `spacemolt_battle engage`, never `hunt` (`in_fleet`).
- `dist` is a ship's own distance from the fight's centre, not from the
  prey: an advance rule that compares with the prey's dist never fires.
- Pilot whale (220 hull), Stellar Siphon: three starters took it to 89
  percent in 9 ticks and fled; three Pulse Laser III ships killed it
  three times (08:40, 12:30, 12:39 UTC on 2026-11-22), 6 ticks each, every
  hull at 100 (F37 met). Weapon first, then the group.
- A pair of starter Shards (Pulse Laser I) killed a magnet barnacle (100
  hull) at The Anvil in 12 ticks, both at 100 percent hull (2026-11-23, 1
  of 3, F37): `--size 2 --from-place` takes the newborns near the prey.
- Take only a ship with no engine goal (`--module`, goal check); stop a
  running group with `stop_script.sh`, never a kill of the shell's PID.

### Weapon fits
Status: proven. Updated: 2026-11-22. Evidence: table runs, routes hunt-test-keid-ice-shelf-deuteron-slug-pl3, hunt-test-gsc-0035-belt-b-slag-tortoise-pl3, hunt-test-acubens-bulwark-pl3, hunt-test-acubens-bulwark-pc2, fit-pulse-laser-iii-lhs-1140; tool stock (dispersal_plasma_cell_pack); the live catalog (plasma_cannon_ii); spacemolt.com/docs/wildlife.

- Creatures have hull and armor, no shields (the game's docs): thermal
  bypasses 75% of armor, energy 25%.
- Pulse Laser III (28 energy, cooldown 1, no ammunition) is the
  division's weapon (rule F37 held): two drones killed deuteron slugs (85
  hull) 3 a run, slag tortoises (90) 3 a run and bulwarks (95) 2 a run,
  the lowest hull 100% in every run (the Pulse Laser I killed no
  slag tortoise). `fit-pulse-laser-iii-lhs-1140` fitted its cap of 20
  pilots by 2026-11-22 05:25 UTC, each from its own wallet; the bigger
  prey hunts (`*-pl3`) need the module (`requires.module`).
- Plasma Cannon II (38 thermal, ammunition): no better than the laser
  against hull (bulwarks 2 a run, about 76 cr of packs a kill); it stays
  on one ship for armoured prey, packs reloaded by `load-plasma-ammo-*`.
- Shield Booster II (cpu 3, power 6): shield 80 to 130; one Pulse Laser
  III ship with it killed a pilot whale (220 hull) alone in 8 of 9 runs
  by two ships, the lowest hull 97 percent (F37 held, 2026-11-22). Lifted
  for the role in First (`fit-shield-booster-ii-lhs-1140`).
- The swap: `fit` with `replace` (BLUEPRINT.md).