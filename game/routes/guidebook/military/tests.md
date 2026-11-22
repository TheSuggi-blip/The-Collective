# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the tool fill (status); observations kind group_hunt and fit_test; table runs.

- Weapon fits (entry below): Pulse Laser III against Plasma Cannon II on
  the bulwarks of Acubens, one ship each.
- Group hunts (entry below): a pilot whale at the Stellar Siphon with the
  wait for every member at the place.
- Patina grazers beyond the border (seven herds, one ship each, standing
  work since 2026-11-22): the work for drones the home herds leave idle.
- The tests the filler adds each turn (`fill.py fill drone --write`): far
  hollow-pilgrim, cinder-sylph and veil-ray herds, one ship each until the
  first RESULT line. A test of another class (a visit mission, a craft
  another division claims) is dropped from the drone plan.
- Not tested: which hit trains Shields and Armor; a tier-1 or tier-2 hull
  with two or three weapons; Cloudwhale Oil Wanted (lumen oil from
  cloudwhales of 508 to 3,304 hull, beyond any side of ours).
- Answered and off (2026-11-17): the cauldronback at Node Beta (0 kills in
  4 runs, hull to 45 percent) and the slag-tortoises at Garnet (0 in 2) with
  one Pulse Laser I: a better weapon or a group first.

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
Status: test. Updated: 2026-11-22. Evidence: game/catalog/tables/modules.tsv; spacemolt.com/docs/wildlife and /docs/combat (read 2026-11-22); hive.py route hunt-test-acubens-bulwark-pl3; routes fit-pulse-laser-iii-lhs-1140, fit-plasma-cannon-ii-krynn.

- Creatures have hull and armor and no shields (the game's docs):
  thermal bypasses 75 percent of armor, energy 25, so a thermal weapon
  gains on every prey; `hull_damage_bonus_50` adds half against hull.
- A starter's laser takes about 0.7 hull a tick from a bulwark (group
  flight, 2026-11-21): the armor takes most of each hit.
- Pulse Laser III (28 energy, cooldown 1): one drone killed two bulwarks
  (hull 95) in 13 minutes at 100 percent hull in its first run; its second
  run killed nothing in 26 minutes. Two runs are no record yet.
- Plasma Cannon II (38 thermal, cooldown 2, hull bonus; CPU 6, power 14)
  hunts the same prey: `hunt-test-acubens-bulwark-pc2`.
- The swap is a route step now: `fit` with `replace` (BLUEPRINT.md), one
  pilot first. The cheap asks move by the hour: read the tool market for
  the item before a fit route is lifted.
- The division's fit goes to the Fleet Admiral when both tests have read
  kills an hour and lowest hull.
