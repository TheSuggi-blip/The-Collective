# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-21. Evidence: the tool fill (status); observations kind group_hunt and fit_test; table runs.

- Weapon fits (entry below): Pulse Laser III on one drone from 2026-11-21
  20:06 UTC; its first hunts of prey above 78 hull decide the fit for the
  division.
- Group hunts (entry below): three drones on a bulwark (95 hull) at
  Acubens, 2026-11-21 from 20:06 UTC.
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
`--max-jumps` of home, docks them, makes a game fleet, flies the leader
to the place, sets each member's target, advances each ship until its own
`dist` is 2 or less, flees all at hull under 85 percent or shield 0, loots
only new wrecks, docks for repair, releases all.

- The leader counts in the capacity of 3; members follow its flight and
  join its hunt at tick 0; a ship outside the fleet that hunts the same
  creature joins the same side.
- `dist` is a ship's own distance from the fight's centre, not from the
  prey: an advance rule that compares with the prey's dist never fires.
- Three starters on a pilot whale (220 hull): about 3 hull a tick for the
  side, while the whale broke the leader (shield 111 to 0, hull to 9
  percent) in about 20 ticks. No starter group on pilot whales.
- 2026-11-21: a first try took free drones at Edasich and Arneb and
  stalled; `--max-jumps` (default 3) keeps far drones out.
- Next: prey of 80 to 140 hull (bulwark, slag-tortoise, cauldronback).

### Weapon fits
Status: test. Updated: 2026-11-21. Evidence: catalog spacemolt_catalog (pulse_laser_i/ii/iii); the tool market; observations kind fit_test.

- Pulse Laser II deals 18, III 28 against 10 for the starter (cooldown 1
  each). The whale fights read about 1 hull a tick per Pulse Laser I
  against nominal 10: the prey's armour takes a share of each hit, so a
  bigger hit may gain more than its catalog ratio. Not measured.
- The test: one drone swaps its Pulse Laser I for a Pulse Laser III at
  Node Alpha (`fit_test.py` by hand, skill scratch), then hunts prey a
  starter cannot kill. Its kills an hour and its lowest hull decide.
- For the division: about 70 weapons; a swap step in the circuit runner
  (unfit, then fit) is asked of the Fleet Admiral.
