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
- The plan in force is the division's plan file (the tool plan); every
  route with its figure is in `game/routes/master-index.md` and its
  sub-indexes.

## Standing Plan

What the drones fly between two turns. The plan in force is the division's plan file
(`/srv/collective/data/plans/plan-military.md`, applied 2026-11-16 18:38 UTC; the tool plan),
written out without names as `game/routes/plans/drone.json` and `game/routes/plan-drone.md`.
Every ship has routes of its own since this turn (orders ENT-017, T1). Each herd holds one
hunter (rule F9); every route beyond the border carries `alone` and an empty hold (F13).
Figures: drone runs from 2026-11-16 13:35 to 18:35 UTC (`data/routes/runs.jsonl`), credits per
ship-hour after fuel, steady money (paid once apart).

| Order | Routes | Ships (own route first in the list) | Carries, expected | Why |
|---|---|---|---|---|
| First | The once line: `voidborn-signal-fragments`, the Central Nexus board line, `voidborn-precedence`, `-conductive-lattice`, First Hunt (nexus, gsc, achernar), Cracking the Shell (`-achernar`, `-central`), `voidborn-selling`, `-concurrent`, `-substrate`, `-missions-1`, `-mining-missions` | every drone; each route's own limit | 7,000, 1,500 and 1,000 cr once | At 18:27 UTC (`data/fleet/onetime.json`) 5 drones lacked Signal Fragments, 22 Cracking the Shell, 10 Market Participation: Selling; every other title of the line is booked by all 30. `voidborn-collective-provides` left the list: `status off` |
| Own, every drone | `sell-curd-central-nexus`, `-node-beta`, `-experiment` | 1 each | 330 cr a curd while the bid stands | 37 curd lie in drone storage at three stations (the tool stock, 18:29 UTC). Closed by `requires.bid` now: no curd bid since 13:24 to 13:38 UTC |
| Own, 3 ships | `guard-marfik-emission-nebula` | 1 at a time | -108 per ship-hour, one run (section 6) | Orders ENT-017: fly the guard route once with one drone (requests.log ENT-165). It guards `mine-marfik-emission-nebula` (a trader's gas run of about 77 minutes, lawless, six jumps) |
| Own, 12 hunters | `hunt-test-achernar-cinder-sylph`, the seven veil-ray hunts (`hunt-gsc-`, `-hamal-`, `-ruchbah-`, `-keid-fractured-prism-`, `-faintlight-drift-`, `-cedarhold-dim-lattice-`, `-low-charge-glint-veil-ray`), `hunt-test-lesath-cinder-sylph`, `hunt-home-drift-ray`, `hunt-keid-belt-carapace`, `hunt-felis-frost-ring-hollow-pilgrim` (test, first in the list) | the 12 drones with the most gunnery and xenobiology; each hunt takes 1 | carries 1 each. Achernar cinder-sylphs 6,098 per ship-hour (2 runs); the rest standing work, a cost | Orders ENT-017: hunt as far as each herd regains; goods without a bid go into storage. A station takes 34,832 verdigris curd (we hold 37), 35,640 creature carapace (904) and 4,420 crystallized biogas (116) (base_plan, 18:30 UTC). The veil-ray hunts and the drift-ray hunt carry `standing: true` and no `requires.bid` since 18:33 UTC; the Keid carapace hunt and the hollow-pilgrim hunt (crystal melt, behind a bid of 1,000 cr) are one-ship tests; the Achernar carapace test is off (a foreign ship at the belt in both runs) |
| Own, 2 ships | `census-guard-ice` | 2 | -602 per ship-hour (32 runs) | The guard until the guard route is proven (requests.log ENT-165) |
| Own, 1 ship | `mine-gliese-876-belt` | 1 (test) | 804 per ship-hour estimated by the route maker, not measured | Put in by the hourly job (testing is allowed); nickel ore sold at a Solarian station (requests.log ENT-160) |
| Own, standing | `gather-gsc-0027-prism-scatter` (6 ships first), `gather-hamal-crystal-bloom` (4), `mine-acubens` (2), `mine-pherkad-rift` (2); every hunter and guard falls back on the first two | shared fleet limits 56, 56, 18, 18 | -128 and -188 per ship-hour (66 and 33 runs) | Iron and copper ore into storage for the station list (P4); the fields' floors (`min_left`) close them |
| Then | `gather-gsc-0027-prism-scatter`, `gather-hamal-crystal-bloom`, `census-frontier`, `park` | -- | -- | A ship should never reach `park` |

The forecast of the division (the tool hive, verb=forecast): before the plan, 18:28 UTC,
-4,402 credits an hour, -147 a ship, 26,120 paid once on the way. After the plan: see the
newest report of the division.

Beside the plan: `game/fleet/plate.py` is not run while carapace and armor plate stand on the
station list (base_plan: 5,940 armor plate by `carapace_plating`); the plates and the carapace stay
in storage. `sell_stored.py` (skill military-turn) sells stored curd where a drone is docked when
the bid is back.

What would change the plan: the curd bid back (the sell-curd routes open by themselves and the
hunters sell); the guard route's first RESULT line (a guard beside each mine run beyond the border,
and `census-guard-ice` out); the carapace tests' RESULT lines (kills, carapace a run, strangers at the
place); a herd under its floor (the hunt closes by itself).

## 1. Route Guides

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

Measured by `routes.py measure`, 2026-11-16 05:21 UTC, all runs of each route,
credits per ship-hour after fuel. The wallet change of a run (the `delta` of
`data/routes/runs.jsonl`) also holds what the hunter sold of goods it carried in
(a neural soma from a mission sells for 500 to 650 cr), so a run without a kill
can read above zero there; `routes.py measure` reads lower where that happened
(Lesath: 840 cr against a delta of 1,456).

| Route | Credits per ship-hour | Runs, minutes a run, credits a run | Note |
|---|---|---|---|
| `hunt-test-achernar-cinder-sylph` | 5,380 (`measured`, 09:15 UTC); 6,423 over the four hours to 09:10 UTC (the tool fleet, view tasks), the best repeating route of the fleet | 6, 10 min, 830 cr | 3 drone runs from 05:30 UTC: 4 kills, 6 ember glands, +2,726 cr in 26 hunter-minutes. The herd read 4 at 08:49 UTC (data/wildlife/achernar.json), beside 4 pilot-whales and 12 drift-rays |
| `hunt-test-lesath-cinder-sylph` | 1,490 | 2, 15 min, 360 cr | 1 drone run from 05:30 UTC: 2 kills, 1 gland, +348 cr; the herd read 2 at 07:58 UTC |
| Carapace into armor plate (`game/fleet/plate.py`, not a route) | no fuel: +746 cr for 12 carapace in about two minutes, one test | 1 | 2026-11-16 09:06 UTC at Central Nexus: 2 plates crafted free in one tick, sold into a bid of 373 cr x 4. The drones hold about 617 carapace in storage (about 100 plates); the plate bids are the limit: pools of 3 to 6 at 221 to 486 cr at six stations, most of them 0 at 09:02 UTC after Logistics sold into them |
| Stored curd sold where it lies (`sell_stored.py` by hand, then `sell-curd-*` routes) | no fuel for a pilot docked there: +9,570 cr by hand for 29 curd at Central Nexus and Node Beta (13:13 to 13:17 UTC), +3,630 cr for 11 by the first `sell-curd-central-nexus` run (13:22 UTC, 0.7 min) | 6 | 2026-11-16: 114 curd lay in drone storage at three stations (the tool stock, 13:10 UTC), looted while the bid was gone; the bid stood at 330 cr x 50 again from 12:07 UTC |
| Plate by `plate.py` over all drones, second pass | +4,665 cr, no fuel: 23 plates made, 15 sold at 287 to 361 cr, 8 stay in storage | 11 | 2026-11-16 13:23 to 13:33 UTC; the plate bids of 1 to 5 units at each station took 15 of 23; the drones held about 720 carapace before it (the tool stock, 13:10 UTC) |

Drone hunts from 2026-11-16 09:30 to 13:00 UTC (`hunt_figures.py --since 09:30 --role drone`):
4 runs, 52.7 hunter-minutes, +1,535 cr, 1,748 cr per hunter-hour; Achernar cinder-sylphs
2 runs, 4 kills, 4 ember glands, 4,085 per hunter-hour; Lesath 2 runs, 0 kills (herd 0),
-546. Every other hunt stood closed: the curd bid gone until 12:07 UTC.

Drone hunts from 2026-11-16 13:35 to 18:35 UTC (`hunt_figures.py --since 13:35 --role drone`):
4 runs, 44.3 hunter-minutes, +1,557 cr, 2,109 cr per hunter-hour; Achernar cinder-sylphs
2 runs, 2 kills, 4 ember glands, +1,799 cr in 17.7 minutes, 6,098 per hunter-hour (ember gland
bid 480 cr x 21 at The Experiment, 18:26 UTC); Lesath 2 runs, 0 kills, -242 cr. The seven
veil-ray hunts flew no run: the loss stop held them until the curd bid had left again.

Ember glands are bid 480 cr, 30 to 50 deep, at all eight stations of our books
(09:02 UTC). Drone hunts from 2026-11-16 05:30 to 09:10 UTC, all routes:
1,052 hunter-minutes, +20,307 cr, 1,158 cr per hunter-hour (`hunt_figures.py`);
the veil-ray part of it stopped paying at 07:05 UTC (the list in this file's history). No hull lost.

## 2. Route Templates

A kind of work is a named list of routes: a template. The templates of
this division are kept in `game/routes/templates/military.json` and listed
in `game/routes/templates-military.md`, a page a script writes once the
division has its first template. A ship's row in the plan file names a
template as `@<name>`, alone or beside routes of its own, and a ship is
switched to other work with one word.

| Task | How |
|---|---|
| See the templates and how many ships use each | the tool `plan` with `action=templates` (`plan.py templates`) |
| Make or change one | `plan.py template <name> <routes with commas> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>` (the tool `plan` with `action=use`) |
| Take one away | `plan.py template <name> none`, once no ship names it |

A template is a guide for one kind of ship: its routes in the order a
ship tries them, the skills it trains (`--trains`) and, in its note,
the fit it needs. Keep one for each kind of work of the division, so
that a ship born tomorrow gets its work with one word.

This guidebook keeps no list of routes that did not pay (Suggi,
2026-11-16; rule F22). The game changes by the hour: a route that lost
yesterday may pay today. What a route earns now, with the age of the
figure, is asked each turn: the tool `routes`, or `SELECT * FROM
route_earnings` through the tool `hive` with `verb=sql`. How a step of
the game works is a mechanic, not a verdict on a route: it belongs in
the sections below. The list this section held until 2026-11-16 is in
the file's history (`git log -- game/routes/guidebook/military.md`).

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. Measured by `routes.py measure`, 2026-11-15 23:58 UTC, all runs of
the fleet:

| Route | Pays once | Measured | Note |
|---|---|---|---|
| `voidborn-precedence` | 4,000 cr | 41 runs, 15 min, 3,890 cr a run | Accept at Node Beta, two docks, nothing bought. Drones from 23:40 UTC |
| `voidborn-first-hunt-nexus`, `-gsc`, `-acubens` | 1,000 cr, 50 Weapons XP, 15 Xenobiology XP, 20 Piloting XP | 2026-11-16 03:19 UTC, all runs of the fleet: nexus 10 runs, 21 min, 570 cr a run; gsc 7, 27 min, 790 cr; acubens 12, 14 min, 370 cr | The circuit runner's `hunt` step: accept, three belt-grazer kills, hand in. One hunter per herd, so the fleet's pilots queue for three herds |
| `voidborn-first-hunt-schedar` | the same | 10 runs, 11 min, 40 cr a run (2026-11-16 03:19 UTC); see the list in this file's history | A fourth herd one jump beyond GSC-0027 (20 belt-grazers, no pilot, 21:14 UTC), `alone` and an empty hold; a test from 2026-11-15 23:58 UTC |
| `voidborn-selling` | 1,000 cr for the pilots that hold Market Participation: Selling | 40 runs, 5 min, 870 cr a run | 20 drones held the mission (`data/fleet/ships/`, 23:46 UTC) |
| `voidborn-concurrent` | 3,000 cr | every drone has it booked | Flown by all 30 drones on 2026-11-15 |
| `voidborn-first-hunt-ironhollow-echo`, `-ironhollow-fading`, `-achernar` | 1,000 cr, accepted and handed in at The Experiment | Achernar: 1 run, 19 min, +960 cr (03:00 UTC); Ironhollow: see the list in this file's history | Three herds one jump beyond The Experiment, written 2026-11-16 03:00 UTC: 26, 19 and 12 belt-grazers at their reads of 01:19 to 01:20 UTC |
| `mission-cracking-the-shell-achernar`, `-central` | 1,500 cr, 55 Weapons XP | achernar 2 runs, refused at the accept; central 24 runs of the fleet, 730 cr per ship-hour (`routes.py measure`, 05:21 UTC) | Back in the plan since 2026-11-16 05:16 UTC with `requires.booked` First Hunt (requests.log ENT-102): in 19 runs of the fleet (2026-11-16 01:16 to 03:22 UTC) the pilots with First Hunt booked were offered it (7 of 7) and the others not (12 of 12). `-central` hunts at Alnair Ice Fields since 05:17 UTC (8 pressblisters at 01:55 UTC, no predator); Node Gamma Ice Belt read no pressblister from 01:50 UTC on. "Hunt 3 Pressblisters at an ice field": any ice field. Achernar Frost Ring read 8 pressblisters at 01:21 UTC |

| `voidborn-signal-fragments` (Trade's) | 7,000 cr | 36 runs of the fleet, 14 min, 5,730 cr a run (`measured`, 09:15 UTC) | Only from navigation 3 (`requires.skills`); 11 drones have it. In the drone plan since 09:02 UTC, at its head |
| `voidborn-network-expansion` (Trade's) | 1,500 cr | 9 runs of the fleet, 8 min, 1,440 cr a run; 7 drone hand-ins from 09:02 to 09:15 UTC, +10,150 cr | Only after First Steps in the Void (`requires.booked`); 14 drones hold it |
| `voidborn-conductive-lattice` (Trade's) | 10,893 cr in a chain of three | 29 drone runs from 05:30 UTC, 29 hand-ins, +315,369 cr in all, about 10,875 a run after the silver and crystal it buys | 29 of 30 drones have flown it |
| Drone once runs, 2026-11-16 09:30 to 13:24 UTC (`data/routes/runs.jsonl`, the 12:27 UTC tax taken out) | -- | Signal Fragments 4 runs, 4 hand-ins, +27,630 cr in 57 min; First Hunt gsc 7 runs, 7 hand-ins, +6,498 cr in 196 min (1,985 per ship-hour with the reward); First Hunt nexus 10 runs, 3 hand-ins, +2,418 cr in 196 min (741); Cracking the Shell achernar 10 runs, 5 hand-ins, +6,122 cr in 191 min (1,926) | Paid once to drones in four hours to 13:18 UTC: 59,000 cr (the tool fleet, view tasks). The herds, not the board, bound First Hunt and Cracking the Shell: both now carry `min_creatures` 3 |
| Drone once runs, 2026-11-16 13:35 to 18:35 UTC (`data/routes/runs.jsonl`) | -- | Signal Fragments 17 runs, +119,000 cr once; Network Expansion 15 runs, +22,500; First Steps 12 runs, +12,000; Ghosts in the Cloud 23 runs, 5 hand-ins, +10,000; First Hunt gsc 3 runs, +2,000, nexus 1, +1,000; Cracking the Shell achernar 3 runs, +1,500: 168,000 cr paid once in 229 drone runs | At 18:27 UTC every title of the once line but Signal Fragments (5 drones lack it), Cracking the Shell (22), Market Participation: Selling (10) and Ghosts in the Cloud (25) is booked by all 30 drones (`data/fleet/onetime.json`). Ghosts in the Cloud left the drone plan: refused "not offered" in most runs of the fleet (queue.log ENT-105) |

Belt-grazer goods are creature carapace and raw xeno meat; no station of
ours bids above 1 cr for either. The mission is the pay. Carapace becomes armor
plate at a workshop (section 1).

## 4. Levelling Guide

Which skills a ship of this division levels and on which work (rule
F23): the work of its own role first, gathering ore only when none is
open. Per kind of ship: the skill, what raises it, what the next level
opens, and the template that trains it (section 2).

- Piloting opens the hulls: tier 2 needs Piloting 10. The drones stand
  at Piloting 3 (20 drones), 4 (8) and 5 (2) (`data/fleet/ships/`,
  2026-11-15 23:35 UTC). The catalog's XP per level: 900 for level 4 to 5,
  then 1,285, 1,740, 2,265, 2,860 and 3,525 for level 9 to 10. What a hunt
  gives in Piloting is not measured; First Hunt gives 20.
- 2026-11-16 03:18 UTC (`hive.py levels`): Piloting 3, 3 and 5 (lowest, median,
  highest) over 30 drones, 114 XP an hour on average since birth, so about 112
  hours to Piloting 10 at that rate. A hunt trains Gunnery, Weapons, Tactics and
  Xenobiology; First Hunt and Cracking the Shell add 20 Piloting XP each.
- 2026-11-16 05:20 UTC (`hive.py levels`): Piloting 3, 3 and 5 again, 98 XP an
  hour on average since birth (10 hours played, median): 130 hours to Piloting 10.
  The average falls while 22 of 30 drones wait docked.
- 2026-11-16 09:10 UTC (`hive.py levels`): Piloting 3, 4 and 6, 89 XP an hour on
  average since birth (14 hours played, median): 141 hours to Piloting 10. Medians
  of the other skills: deep core mining 3, xenobiology 2, trading 2, tactics 2,
  navigation 2; 11 drones stand at navigation 3 (data/fleet/ships/), which opens
  Signal Fragments.
- 2026-11-16 13:18 UTC (`hive.py levels`): Piloting 3, 4 and 6, 73 XP an hour on
  average since birth (18 hours played, median): 170 hours to Piloting 10. Navigation
  2 median (26 XP an hour): 12 drones at navigation 3, 18 at 2 with 173 to 334 of the
  340 XP the level asks (data/fleet/ships/, 13:05 UTC).
- Navigation by jumps (test `train-navigation-home`, one drone, RESULT of 2026-11-16
  13:17 UTC): five jumps through our own stations (Node Alpha, Synchrony, Node Gamma,
  Node Beta, Central Nexus) and their docks in 15.0 minutes, -117 cr, took the pilot
  from 334 XP at level 2 to 13 XP into level 3: 19 XP, about 4 XP and 23 cr a jump
  (runs.jsonl; ship file 13:33 UTC). At that rate the drone furthest from level 3 (173
  XP) needs about 44 jumps, nine runs, about 1,050 cr of fuel and two and a half hours,
  for a mission that pays 7,000 cr once (requests.log ENT-150).
- 2026-11-16 18:40 UTC (`hive.py levels`): Piloting 4, 5 and 7, 96 XP an hour on average since
  birth (24 hours played, median): 119 hours to Piloting 10. Every drone stands at navigation 3
  or above (data/fleet/ships/, 18:27 UTC), reached by the work itself; 25 have handed in Signal
  Fragments. `train-navigation-home` left the plan: no drone is below the gate.
- Weapons stand at 0 to 2, Gunnery at 0 to 3, Tactics at 0 to 3 and
  Xenobiology at 0 to 3 on the eight drones that have hunted; the other
  drones carry none of these skills (same read). First Hunt gives 50
  Weapons XP; what a kill gives is not measured.
- The tier-1 hulls name no Piloting gate: the game's quote for a Vigil
  said "shipyard tier 0 required" (section 5).

## 5. Ships and Fits

The starter Threshold: 1 weapon, 2 defence and 2 utility slots, CPU 16,
power 30 (`get_ship`, 2026-11-15 21:27 UTC). Every drone fits a Mining
Laser I and a Pulse Laser I but one, which fits a Piercing Railgun I; no
drone fits a defence module (`data/fleet/ships/`, 23:35 UTC).

| Module or item | What it does | Price in our books |
|---|---|---|
| Piercing Railgun I | 60 kinetic damage, magazine 7, cooldown 3 ticks, 70% armour bypass | 5,000 cr (Central Nexus, 3) |
| Ferrous Slug Case | Railgun ammunition; one case loads a whole magazine. Recipe: 2 steel plate and 3 iron ore make 5 cases | 52 cr (Central Nexus, 744) |
| Tungsten Slug Case | Railgun ammunition, +40% armour bypass | 40 cr (Central Nexus, 3) |
| Shield Booster I | +25 shield, 2 CPU, 4 power | 2,483 cr (Central Nexus, 26) |
| Pulse Laser I | The starter weapon | 1,385 cr (Central Nexus, 5) |

Catalog and books read 2026-11-15 23:24 to 23:32 UTC.

- A railgun hit does not kill a 60-hull grazer: the first hit leaves it
  at 4 to 8 hull and it flees (hunt logs of 21:30 and 22:52 UTC). On
  veil-rays it was no faster than the pulse laser (the list in this file's history).
- Hulls, priced by the game (`commission_quote` at Central Nexus, read
  only, 2026-11-15 23:30 to 23:32 UTC):

| Hull | Tier | Credits only | Credits plus materials | Materials |
|---|---|---|---|---|
| Vigil | 1 | 106,208 cr | 15,040 cr | 8 steel plate, 15 copper wiring, 14 silicate composite, 5 shield emitter, 3 thruster nozzle, 2 sensor array, 2 Pulse Laser I, 2 Shield Booster I |
| Paradox | 1 | 82,690 cr | 12,368 cr | 15 silicate composite, 10 copper wiring, 1 processing core, 2 shield emitter, 4 void nanite suspension, 5 shield matrix, 1 phase matrix, 2 Pulse Laser I, 1 Shield Booster I, 1 Shield Recharger I |

- Re-quoted 2026-11-16 between 03:16 and 03:18 UTC at Central Nexus: the Vigil costs 111,316 cr
  with credits only (materials 47,805, labor 1,050, yard fee 14,656), or
  15,706 cr plus the same materials; build time 87 ticks.
- The railgun ship flies the Pulse Laser I again since 2026-11-16 03:10 UTC; its
  Piercing Railgun I lies in its storage at Central Nexus. A storage withdraw to
  the own hold is `withdraw` with item and quantity only; with `target: cargo`
  the gate's wall refuses it as a give-away.
- The exchange lists ships too: `browse_ships` showed 259 listings at the
  stations our pilots have charted, tier-1 hulls from 1,000 cr, all at
  stations of other empires (2026-11-15 23:31 UTC).
- The division flies the Threshold with the Pulse Laser I this week. A
  hunt is bounded by the herd and by other hunters, not by the weapon
  (sections 1 and 2): a hull that kills faster earns more only where a
  herd grows under our ranch. What a Vigil would earn is not measured.

## 6. Open Tests

The yield tests of 2026-11-16 03:00 to 03:16 UTC are read (the list in this file's history): of eight,
the Lesath cinder-sylph herd paid and stays; the rest left the plan at 05:16 UTC.
Open now, one ship each:

- `guard-marfik-emission-nebula`, the first guard route (requests.log ENT-165), flown once:
  one drone from 18:38 UTC, at the place from 18:43 to 19:43 UTC, 61 looks, left after its 60
  minutes, docked at Node Beta, hull 100 percent all along, -132 cr in 73.4 minutes (about -108 per
  ship-hour; `census-guard-ice` costs -602). The guarded gas miner stood at the field in 11 of the
  61 looks: its mining loop hauls each load to Node Beta, six jumps away, so the guard watched an
  empty field most of the hour. A Combat Drone of the faction BUSY stood at the field in 12 looks
  (19:10 to 19:21 UTC), 4 of them beside our miner; nobody fired (the run's row and the guard's log,
  data/routes/). Next: a guard that keeps beside the guarded pilot, not at the field, before a
  second guard flies; `census-guard-ice` stays behind it meanwhile.
- `hunt-felis-frost-ring-hollow-pilgrim` (since 19:30 UTC): the route maker's candidate, one hunter,
  open only while The Experiment bids 1,000 cr or more for 4 crystal melt (the bid moves between
  54 cr x 50 and about 1,394 cr x 10, data/market/history.jsonl). Not flown yet.
- `hunt-keid-belt-carapace` (since 2026-11-16 18:33 UTC): belt-grazers and patina-grazers for creature
  carapace into storage, standing work, `alone` and an empty hold; one ship. First run (18:58 UTC):
  left without a fight, a ship not of ours at the belt, -110 cr. Its twin `hunt-achernar-belt-carapace`
  met a foreign ship in both its runs (1 kill, 2 carapace, -99 and -44 cr) and is off since 19:23 UTC.
- The seven veil-ray hunts and `hunt-home-drift-ray` as standing work (since 18:33 UTC). First rows
  to 19:23 UTC: three veil-ray runs (GSC-0027, Keid, Achird) made 4 kills each and looted 4 to 6
  curd and 5 carapace each, -65 to -121 cr in about 30 minutes; Ruchbah and Cedarhold left without
  a fight, a ship not of ours at the place, -88 and -121 cr; three drift-ray runs made 3 kills each
  and stored 7 crystallized biogas in all, -26 to -65 cr in 10 to 13 minutes (data/routes/runs.jsonl).
  The veil-ray hunts gather carapace too: about one carapace a kill beside the curd.
- `mine-gliese-876-belt` (put in by the hourly job, 18:13 UTC): nickel ore sold at a Solarian
  station, 804 cr per ship-hour estimated by the route maker; one ship.

- `mission-cracking-the-shell-central` (Unity's) hunts at GSC-0041 Frost Ring since
  10:38 UTC with a herd floor of three (requests.log ENT-135); the ring read 0
  pressblisters, 4 deuteron-slugs, 2 rime-grazers and a frost-lurker of 400 hull at
  12:09 UTC (data/wildlife/gsc_0041.json): closed by its floor. Back in the drone plan.
- `train-navigation-home`: closed. One run measured about 4 XP a jump (section 4); every drone
  passed navigation 3 by its own work by 18:27 UTC, and the route left the plan.
- `sell-curd-central-nexus`, `-node-beta`, `-experiment`: one ship each; the first run
  sold 11 curd for +3,630 cr in 0.7 min (13:22 UTC). Two runs went to pilots whose curd
  had been sold by hand minutes before (0.0 min, 0 cr): `requires.stored` reads the
  ledger, which reads each pilot about every 40 minutes.
- `census-guard-ice`: 32 drone runs from 13:35 to 18:35 UTC, -4,483 cr, -602 per ship-hour;
  before that 25 runs from 09:30 to 13:24 UTC, -3,567 cr without the tax,
  -611 cr per ship-hour, two ships: about 1,220 cr an hour, the price of the guard
  (orders F16). What its reads renewed is not measured.
- `game/fleet/plate.py`: off since 2026-11-16 18:33 UTC while carapace and armor plate stand
  on the station list (base_plan). Before that, over all drones each turn: how many plates the bids take in
  four hours is not measured; the pools refill within the hour (logistics.md).
- Pirate Bounty (2,000 cr once, kill one pirate; on the boards of Central Nexus, Node
  Gamma and Synchrony Hub, data/missions/ at 09:20 UTC): not
  flown. Orders F2 forbid firing first at an NPC ship; pirates stood at Gliese 876
  and Felis at 04:40 UTC (queue.log ENT-090). Suggi's word, put in my report.
- No new species test: at 05:10 UTC and again at 13:20 UTC no untested grazer of
  100 hull or less stood in a herd of four or more in our readings (data/wildlife/: bulwark 3, coronid
  2; carrion-moths and ash-scarabs are scavengers, outside orders F9).
- Which prey drops caustic sac (bid 420 cr, 50 at seven stations): not measured.
  The catalog names no source ("mined, dropped or bought only"), and no run of
  the fleet has looted one (`data/routes/runs.jsonl`, 05:10 UTC).
- A tier-1 hull with two weapons: only after a test shows prey worth a tougher
  hull (section 5); prey over 100 hull needs an order beyond F9.
