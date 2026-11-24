# Military guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-24. Evidence: table runs (kills, lowest_hull_pct); data/fleet/hunt_packs.json; game/hunt-policy-packs.json and route hunt-network-packs; route strip-missile-launcher-central-nexus; requests.log ENT-523.

- Whale hunts alone with a Shield Booster II hold at the siphon and Antares
  herds; two other herds took ships to 4 and 14 percent and are off (F9).
  The proven way stays three Laser III in one fleet (`group_hunt.py`).
- Pack lane (route `hunt-network-packs`, policy
  `game/hunt-policy-packs.json`): no pack launched in its first five hours.
  `pack_try_join_or_create` caps pack pilots at max(3, active x
  `target_share`) and a joiner must stand within `rally_max_jumps` of the
  target: at 0.02 three singletons filled the quota at three far places.
  Retuned: share 0.07, pack and escort reach 6 jumps. Read three
  `hunt_net pack` RESULT lines before any lift.
- Cleavers and Broadaxes: strip the empty launcher or railgun, then three
  hunts read kills (`strip-missile-launcher-central-nexus`).
- Atria kit parts: the kit is assembled only in a facility we do not own
  (requests.log ENT-523); the kit hunts stay off the tier-2 rows until
  the Fleet Admiral decides how the kit is got.
- Armor Plate II on a Shard or Theoria: armor +10, speed stays 1; lifted.
- Pirate formations (F27): `group_hunt.py --pirate` after three wildlife
  packs hold; lone scouts only, never at a pack's POI.

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