# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the tool fill (status); observations kind group_hunt and fit_test; table runs.

- Plasma Cannon II against the bulwarks of Acubens, now with ammunition
  (Weapon fits).
- Group hunts (entry below): a pilot whale with three ships that carry
  the Pulse Laser III, once three stand fitted.
- Caustic sac for the reserve: chlorophage herds at Alathfar, Fulu and
  Chara, one ship each, stored at Node Beta for the recruitment center
  (the tool needs); standing work.
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
Status: proven. Updated: 2026-11-22. Evidence: table runs, routes hunt-test-keid-ice-shelf-deuteron-slug-pl3, hunt-test-gsc-0035-belt-b-slag-tortoise-pl3, hunt-test-acubens-bulwark-pl3, hunt-test-acubens-bulwark-pc2; catalog 0.732.0 (plasma_cannon_ii); spacemolt.com/docs/wildlife.

- Creatures have hull and armor and no shields (the game's docs):
  thermal bypasses 75 percent of armor, energy 25.
- Pulse Laser III (28 energy, cooldown 1, no ammunition) is the
  division's weapon (rule F37 held): two drones killed deuteron slugs (85
  hull) 3 a run, slag tortoises (90) 3 a run and bulwarks (95) 2 a run,
  the lowest hull 100 percent in every run; the Pulse Laser I had killed
  no slag tortoise. Fitted by `fit-pulse-laser-iii-lhs-1140` (fit with
  replace, 3 at a time, 20 pilots, `requires.ask`), each from its own
  wallet; the bigger prey hunts need the module (`requires.module`).
- Plasma Cannon II (38 thermal, cooldown 2, hull bonus) takes plasma
  ammunition (magazine 80): its fit bought none, so three test runs never
  fought (0 kills, hull 100). `buy-plasma-ammo-central-nexus` brings packs;
  a weapon that takes ammunition is fitted with its ammunition.
- The swap is a route step: `fit` with `replace` (BLUEPRINT.md). The cheap
  asks move by the hour: read the tool market before a fit is lifted.