# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-21. Evidence: the tool fill (status); observations kind group_hunt and fit_test; table runs.

- Weapon fits (entry below): one drone fits a Pulse Laser III since
  2026-11-21 20:51 UTC; `hunt-test-acubens-bulwark-pl3` is its test.
- Group hunts (entry below): the next flight waits for the members to
  stand at the place before the leader attacks.
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
Status: test. Updated: 2026-11-21. Evidence: observations kind group_hunt (2026-11-17 20:39, 2026-11-18 00:34 and 00:54 UTC); skill military-turn group_hunt.py; the retired entry of routes.md (hive.py guide military --retired).

`group_hunt.py` (skill script, background) takes free drones within
`--max-jumps` of home, docks them, makes a game fleet, flies to the place,
sets targets, advances each ship to its own `dist` 2, flees all at hull
under 85 percent or shield 0, docks for repair, releases all.

- The leader counts in the capacity of 3; a member at the place when the
  fight opens joins it at tick 0, and so does a ship outside the fleet that
  hunts the same creature.
- `dist` is a ship's own distance from the fight's centre, not from the
  prey: an advance rule that compares with the prey's dist never fires.
- Three starters on a pilot whale (220 hull): about 3 hull a tick for the
  side, while the whale broke the leader (shield 111 to 0, hull to 9
  percent) in about 20 ticks. No starter group on pilot whales.
- 2026-11-21, a bulwark (95 hull) at Acubens: the members did not follow
  the flight, reached the place a tick after the leader attacked and were
  not pulled in; their own `hunt` was refused (`in_fleet`). The leader
  alone took it from 100 to 65 percent in 45 ticks, its shield 111 to 7.
  Next flight: the leader attacks only when every member stands at the
  place; a member outside the battle joins it (`spacemolt_battle
  engage`), never hunts. Far drones stalled two tries: `--max-jumps`.

### Weapon fits
Status: test. Updated: 2026-11-21. Evidence: catalog spacemolt_catalog (pulse_laser_i/ii/iii); the tool market; observations kind fit_test.

- Pulse Laser II deals 18, III 28 against 10 for the starter (cooldown 1
  each). The whale fights read about 1 hull a tick per Pulse Laser I
  against nominal 10: the prey's armour takes a share of each hit, so a
  bigger hit may gain more than its catalog ratio. Not measured.
- A starter's laser takes about 0.7 hull a tick from a bulwark (the
  group flight of 2026-11-21): the prey's armour takes most of each hit.
- The test: one drone fits a Pulse Laser III (`fit_test.py`, skill
  military-turn; bought at Node Alpha, fitted 2026-11-21 20:51 UTC after a
  rescue: the swap lost its dock to a runner, errors.log ENT-114) and
  hunts bulwarks at Acubens (`hunt-test-acubens-bulwark-pl3`). Its kills
  an hour and lowest hull decide the fit.
- For the division: about 70 weapons; a swap step in the circuit runner
  (unfit, then fit) is asked of the Fleet Admiral.
