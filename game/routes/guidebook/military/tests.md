# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the tool fill (status); observations kind group_hunt and fit_test; table runs.

- Pulse Laser III hunts on four herds of slag tortoises and deuteron
  slugs (`*-pl3`, 2026-11-22), one ship each until three results; carapace
  for the reserve.
- Group hunts (entry below): a pilot whale with three Pulse Laser III ships.
- Caustic sac: chlorophage herds at Alathfar, Fulu and Chara, stored at
  Node Beta; standing work while the tool needs names it short.
- The tests the filler adds each turn (`fill.py fill drone --write`): far
  herds, one ship each until three results (F37). A test of another class
  is dropped from the drone plan.
- Not tested: which hit trains Shields and Armor; a tier-1 or tier-2 hull
  with two or three weapons; cloudwhales (508 to 3,304 hull).
- Answered: one Pulse Laser I kills no cauldronback or slag tortoise; the
  Pulse Laser III kills prey of 85 to 95 hull (Weapon fits).

### Group hunts
Status: test. Updated: 2026-11-22. Evidence: observations kind group_hunt (2026-11-17 to 2026-11-22 00:45 UTC); spacemolt.com/docs/combat; skill military-turn group_hunt.py.

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
- Three starters on a pilot whale (220 hull), 2026-11-22 at Stellar
  Siphon, all three in the fight from tick 0: the whale 100 to 89 percent
  in 9 ticks, the leader's shield gone and its hull 75 to 36; no kill. A
  starter group loses the race to the stalemate: weapon first.

### Weapon fits
Status: proven. Updated: 2026-11-22. Evidence: table runs, routes hunt-test-keid-ice-shelf-deuteron-slug-pl3, hunt-test-gsc-0035-belt-b-slag-tortoise-pl3, hunt-test-acubens-bulwark-pl3, hunt-test-acubens-bulwark-pc2, fit-pulse-laser-iii-lhs-1140; tool stock (dispersal_plasma_cell_pack); catalog 0.732.0 (plasma_cannon_ii); spacemolt.com/docs/wildlife.

- Creatures have hull and armor, no shields (the game's docs): thermal
  bypasses 75 percent of armor, energy 25.
- Pulse Laser III (28 energy, cooldown 1, no ammunition) is the
  division's weapon (rule F37 held): two drones killed deuteron slugs (85
  hull) 3 a run, slag tortoises (90) 3 a run and bulwarks (95) 2 a run,
  the lowest hull 100 percent in every run (the Pulse Laser I killed no
  slag tortoise). `fit-pulse-laser-iii-lhs-1140` fitted its cap of 20
  pilots by 2026-11-22 05:25 UTC, each from its own wallet; the bigger
  prey hunts (`*-pl3`) need the module (`requires.module`).
- Plasma Cannon II (38 thermal, cooldown 2, hull bonus) takes plasma
  ammunition (magazine 80), fitted with it or it never fires. With four
  packs (686 cr) one ship killed bulwarks 2, 2, 2, 2, 1 in five runs at
  hull 100 (F37 held), about 76 cr of ammunition a kill: no better than
  the laser against hull, so the laser stays the fit; the cannon stays on
  one ship for armoured prey. A hunt's store can take the packs into
  storage: `load-plasma-ammo-nova-terra` puts them back aboard.
- The swap: `fit` with `replace` (BLUEPRINT.md).