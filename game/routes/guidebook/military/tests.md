# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the tool fill (status); observations kinds group_hunt and fit_test; table runs; tables ship_skills and stats_pilot_hour.

- Pulse Laser III hunts on four herds of slag tortoises and deuteron
  slugs (`*-pl3`): the tortoises kill 2 to 3 a run (ferrous nodule and
  carapace, both short); the deuteron slugs at Node Beta and Aldhibah
  read zero kills in four of six runs. Three results each before a lift.
- Plasma ammunition: a circuit stop `store: all` stores the packs too;
  `load-plasma-ammo-*` take them back aboard (requests.log ENT-352).
- Shields and Armor: the catalog trains them by shield or hull damage
  taken in combat, yet no ship of the fleet holds either skill after
  eight days of hunts. Open: what does train them.
- Not tested: a Shield Booster II; a tier-1 or tier-2 hull with two or
  three weapons; cloudwhales (508 to 3,304 hull).
- Answered: one Pulse Laser I kills no cauldronback or slag tortoise; the
  Pulse Laser III kills prey of 85 to 95 hull alone and a pilot whale in
  a side of three (Group hunts).

### Group hunts
Status: proven. Updated: 2026-11-22. Evidence: observations kind group_hunt (2026-11-17 to 2026-11-22 12:41 UTC); errors.log ENT-129, ENT-130; spacemolt.com/docs/combat; skill military-turn group_hunt.py.

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
- Take only a ship with no engine goal (`--module`, goal check); stop a
  running group with `stop_script.sh`, never a kill of the shell's PID.

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