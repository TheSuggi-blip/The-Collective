---
name: guidebook-military
id: 20261115T205807Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# military.md -- Guidebook of the Military Division

Kept by Apophis; read by every member. What the Military division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apophis writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/drone.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| `hunt-gsc-veil-ray` | 3,500 over 11 runs, 24 min a run, 1,720 cr a run (`routes.py measure`) | 2026-11-15 21:42 UTC | 53 kills, none of the 11 runs without a kill. One hunter, ranched: no hunt below four animals, four kills a run. The herd read 6 to 7 from 17:58 to 20:02 UTC and 13 at 21:24 UTC while it was hunted (`data/wildlife/history.jsonl`): the ranch takes less than the herd regrows. From 21:40 UTC only the railgun ship is sent here (the test of section 6) |
| `hunt-hamal-veil-ray` | 3,120 over 5 runs, 23 min a run, 1,070 cr a run (`routes.py measure`) | 2026-11-15 21:42 UTC | 2 of 5 runs without a kill. The herd read 0 at 18:48, 19:31 and 20:04, 2 at 20:48 and 8 at 21:25 UTC: it comes back from nothing in under an hour |

Both sell verdigris curd (330 cr) at Central Nexus since 2026-11-15 21:40
UTC: Node Beta's bid had fallen to 15 units (20:45 UTC); Central Nexus,
Node Alpha, Synchrony and The Experiment bid 330 for 50 to 526 units
(`data/market/`, 20:29 to 20:55 UTC).

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `hunt-acubens-urchin` | 3 runs, 6 kills, -240 cr per ship-hour | 2026-11-15 | No radiant bile dropped, carapace only. Off |
| `hunt-home-drift-ray` | 11 runs, -260 cr per ship-hour | 2026-11-15 | Crystallized biogas bid 1 to 2 cr. Out of the plan (orders F8) |
| A pilot-whale (220 hull) | Took a starter with a railgun from 73 to 15 hull in one fight | 2026-11-15 | Not for a starter hull with no defence module (orders F9) |
| `hunt-ruchbah-veil-ray` (lawless, by hand, hold empty) | 1 run: 0 kills, -77 cr of fuel, 11 min door to door, no damage | 2026-11-15 21:26 UTC | Seven veil-rays at 21:14 UTC. Two ships of the faction BUSY (Dialectic and Opus Magna class, named "Combat Drone") joined the fight within three minutes, the runner fled as built, and at 21:35 UTC the place listed no creature. Off: a herd beyond our border is shared with a faction of 1,249 members (`game/factions/n-busy.md`) |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time.

**Concurrent Approval** (`voidborn-concurrent`): 3,000 cr once per
pilot, buys nothing; tested by the Trade division (its route note and
queue.log ENT-038). At the head of the drone plan since 2026-11-15
22:02 UTC; no drone had it booked then.

**First Hunt: Belt-Grazers** (template `first_hunt_belt_grazers`, giver
the Station Hunters' Registry). On the boards of all six Voidborn
stations (`data/missions/`, 2026-11-15). Reward 1,000 cr, 50 Weapons XP,
15 Xenobiology XP, 20 Piloting XP. Objective: kill 3 belt-grazers at an
asteroid belt. Flown by hand twice on 2026-11-15:

- A Pulse Laser I drone accepted it at Central Nexus (21:23 UTC), made
  its 3 kills at GSC-0027 Spacetime Seep in 15.0 minutes at the place
  (5.7, 4.2 and 5.1 minutes per kill; each grazer fled twice, at 15 and
  at 5 hull, before it died), no damage, and handed it in at Central
  Nexus: wallet 30,866 -> 31,788 cr, +922 after 78 cr of fuel, 25
  minutes door to door.
- The railgun drone held it at 2 of 3 when the turn began; its third
  kill at Nexus Prime Material Harvesters took 2.9 minutes, and the
  hand-in at Central Nexus paid +1,000 cr (21:36 UTC).
- Belt-grazer goods: creature carapace and raw xeno meat; no station
  of ours bids for either above 1 cr. The mission is the pay.
- No pilot of the fleet had it booked (`data/fleet/onetime.json`,
  21:20 UTC). Belt-grazers in our space: GSC-0027 Spacetime Seep 7,
  Nexus Prime 3 (`data/wildlife/`, 20:56 to 21:24 UTC).
- No route can fly it yet: the circuit runner accepts and hands in but
  cannot hunt, and the hunt runner hunts but neither accepts nor hands
  in. Asked of the Fleet Admiral (requests.log ENT-047).

## 4. Levelling

- Piloting opens the hulls: tier 2 needs Piloting 10. The catalog's
  XP per level (`catalog skills piloting`, 2026-11-15): 900 for level
  4 to 5, then 1,285, 1,740, 2,265, 2,860 and 3,525 for level 9 to 10.
  The drones stand at Piloting 3 and 4 (`data/fleet/ships/`, 21:17
  UTC); a drone at level 4 with 519 XP needs 12,056 XP more for tier 2.
  The exploration missions on our boards give 320 to 520 Piloting XP
  each (`data/missions/`, 2026-11-15); what a hunt gives is not measured.
- Weapons: First Hunt gives 50 XP; the drones stand at Weapons 0 to 2.
- Xenobiology rises per kill and raises the value of the goods
  (shared skill `fleet-play`, hunting).

## 5. Ships and Fits

The starter Threshold: 1 weapon, 2 defence and 2 utility slots, CPU 16,
power 30; the railgun drone's Mining Laser I and Piercing Railgun I use
7 CPU and 17 power (`get_ship`, 2026-11-15 21:27 UTC). No drone fits a
defence module: both defence slots stand empty (`data/fleet/ships/`). From the catalog and our books (2026-11-15):

| Module | What it does | CPU / power | Ask in our books |
|---|---|---|---|
| Piercing Railgun I | 60 kinetic damage, reach 5, cooldown 3 ticks, magazine 7, 70% armour bypass | 5 / 12 | 5,000 cr (Central Nexus 3, The Experiment 2) |
| Tungsten Slug Case | Its ammunition; the hunt runner reloads from the hold | -- | 40 cr (Central Nexus), 27 cr (Node Alpha) |
| Shield Booster I | +25 shield | 2 / 4 | 2,483 cr (Central Nexus, 26) to 4,256 |
| Armor Plate I | +5 armour, speed penalty 1 | 1 / 0 | 646 cr (Central Nexus, 2) |
| Emergency Warp Stabilizer | Jumps the ship home when a hit would take it under 20% hull | 6 / 8 | No seller; base value 19,000 cr |

- A railgun hit does not kill a 60-hull grazer: the first hit left a
  belt-grazer at 4 hull and it fled; the kill took three fights (2026-11-15
  21:30 to 21:33 UTC). Damage on the target is less than the catalog
  figure.
- The fit to test next, not flown yet: Threshold, Piercing Railgun I,
  two Shield Booster I (11 CPU, 25 power; about 9,970 cr at Central
  Nexus asks): 50 shield more against bigger prey.

## 6. Open Tests

- Railgun on a veil-ray herd: from 2026-11-15 21:40 UTC
  `hunt-gsc-veil-ray` takes only the railgun ship, for turn T5. Measure
  against the pulse figure of section 1: kills and credits per
  hunter-hour, damage, slugs used.
- First Hunt: Belt-Grazers for every drone, as a route, when the
  runner can hunt for a mission.
- Herds beyond Voidborn space (orders F13): veil-rays at Garnet Dim
  Lattice (8 at 2026-11-15 21:24 UTC); cinder-sylphs (40 hull) at
  Achernar Gas Pocket, whose ember gland The Experiment bids 480 cr for
  550 (`data/market/`, 20:36 UTC). One ship each, hold empty, by hand.
- Bigger prey: the fit of section 5 against a pilot-whale, one ship,
  the flee rule kept.
