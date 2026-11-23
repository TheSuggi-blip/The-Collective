# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-23. Evidence: hive.py route hunt-test-siphon-pilot-whale-sb2; table runs (*-pl3, *-pilot-whale-sb2); data/fleet/funds.json; observations kinds group_hunt, fit_test.

- Shield Booster II: proven (F37), see Weapon fits. Whale hunts for the
  booster ships at four herds 4 to 5 jumps out (`*-pilot-whale-sb2`).
- The Recursion (tier 2, 3 weapons, hull 150, shield 150; table hulls):
  one commissioned for credits at Node Beta on 2026-11-23 (commission_hull.py,
  observations kind fit_test), 702 ticks by its quote; the switch once
  commission_status says ready, then its three results (F37).
- Pulse Laser III hunts: tortoises at six belts, deuteron slugs at three
  ice fields; reserve goods (ferrous nodule, carapace).
- Cloudwhales (20 jumps out): a group sets out only on a census under
  120 minutes (`--census-minutes`).
- Shields and Armor: no ship holds either skill. Open.
- Answered: one Pulse Laser I kills no slag tortoise; the laser III kills
  85 to 95 hull alone, a pilot whale in a side of three, or alone with a
  Shield Booster II.

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