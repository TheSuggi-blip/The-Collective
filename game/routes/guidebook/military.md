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

## Standing Plan

What the drones fly between two turns, in this order (`game/routes/plans/drone.json`,
last committed 2026-11-16 13:21 UTC; `hive.py standing` prints it ship by ship). Every
place holds one hunter (orders F9); every route beyond the border carries `alone`
and an empty hold (F13). Figures: drone runs from 09:30 to 13:24 UTC
(`data/routes/runs.jsonl`), after fuel, the weekly tax of 12:27 UTC taken out of the
seven runs it fell into, and the route files' `measured` (all runs) where named. The
scale of the hour: the best repeating route of the fleet, `hunt-test-homam-frost-moth`,
4,142 credits per ship-hour over four hours (the tool fleet, view tasks, 13:18 UTC),
and 0 for a ship that waits.

| Order | Routes | Ships | Expected | Why |
|---|---|---|---|---|
| 1 | `voidborn-signal-fragments` (Trade's) | up to 10 for the fleet | 7,000 cr once; 4 drone runs from 09:30 UTC, +27,630 cr in 57 min | `requires.skills` navigation 3: 12 drones have it, 18 stand at navigation 2 |
| 2 | The once line of the Central Nexus board (Trade's): `voidborn-first-steps-board`, `-network-expansion`, `-collective-provides`, `-signal-protocol` | Trade's limits (3, 20, 2, 20) | 1,000, 1,500, 2,500 and 3,500 cr once | Orders ENT-014 (c). 16 drones lack First Steps and Network Expansion; Collective Provides is `off` (its reef read 0 nickel) and Signal Protocol waits on it |
| 3 | `voidborn-precedence`, `voidborn-conductive-lattice` | as booked | once | Every drone has Precedence; 29 of 30 the Node Beta chain |
| 4 | First Hunt: `voidborn-first-hunt-nexus`, `-gsc`, `-achernar` (herd floor 3) | 1 each | 1,000 cr once; gsc 7 runs, 7 hand-ins, 1,985 per ship-hour with the reward; nexus 10 runs, 3 hand-ins, 741 | 5 drones have not booked it. Achernar Belt read 10 belt-grazers and no pilot at 12:15 UTC |
| 5 | Cracking the Shell: `mission-cracking-the-shell-achernar` (herd floor 3), `-central` (Unity's, GSC-0041, floor 3) | 1 each | 1,500 cr once; achernar 10 runs, 5 hand-ins, 1,926 per ship-hour with the reward | 18 drones hold First Hunt without it. Achernar Frost Ring read 1 pressblister at 12:40 UTC, GSC-0041 0 at 12:09 UTC: both closed by their floor until a census reads three |
| 6 | `voidborn-selling`, `-concurrent`, `-substrate`, `-missions-1`, `-mining-missions` | as booked | once | Pass by themselves once booked |
| 7 | `sell-curd-central-nexus`, `sell-curd-node-beta`, `sell-curd-experiment` | 1 each (tests) | about 330 cr a curd, no jump for the pilot docked there | The curd the veil-ray hunts stored while its bid was gone; closed by `requires.stored` and `requires.bid` |
| 8 | Hunts, best first: `hunt-test-achernar-cinder-sylph` (4,230 measured), `hunt-gsc-veil-ray` (3,020), `-hamal-` (2,310), `-ruchbah-` (2,100), `-keid-fractured-prism-` (1,420), `-faintlight-drift-` (1,300), `hunt-test-lesath-cinder-sylph` (970), `hunt-cedarhold-dim-lattice-veil-ray` (840), `hunt-low-charge-glint-veil-ray` (800) | 1 each | 800 to 4,200 per ship-hour where the herd stands at four or more | Each names its loot's bid at its sell station (`requires.bid`, 100 cr); the veil-ray hunts open as the loss stop's window passes their losing runs of 07:05 to 09:20 UTC |
| 9 | `train-navigation-home` | 1 (test) | a cost; opens Signal Fragments | Five jumps through our own stations for a drone without Signal Fragments: what navigation XP a jump gives (section 4) |
| 10 | `census-guard-ice` | 2 | a cost: -611 cr per ship-hour (25 runs from 09:30 UTC) | The guard of orders F16 until the guard runner exists (Unity, her turn of 18:30 UTC) |
| 11 | `census-frontier`, then `park` | up to 12, then the rest | reads; 0 | Docked costs nothing |

Beside the plan, every turn: `game/fleet/stash.py` empties the holds that close the
hunts and the census (`hold not empty` in `fill` status), then `game/fleet/plate.py`
over all drones: carapace becomes armor plate where it lies and plates are sold no
deeper than the bid; `sell_stored.py` (skill military-turn) sells a stored good into
the bid of the station where a drone is docked.

At 13:16 UTC the fill gate read PASS with 23 drones waiting. What closes the work to
them: navigation 3 for Signal Fragments (16), the three places of First Steps on the
board (14), the loss stop's six-hour window on the veil-ray hunts, First Hunt nexus and
achernar and Cracking the Shell achernar, the herd floor (cinder-sylphs under four,
pressblisters under three), every census system read. Hunting carries one to seven
hunters as the window passes (veil-ray herds 4 to 8 at five places, 09:46 to 13:03 UTC).

What would change the plan: the curd or ember-gland bid gone again (the routes close
by themselves); a navigation figure from `train-navigation-home` that shows the fuel to
level 3 well under 7,000 cr (then more drones on it); a pressblister herd of three or
more (Cracking the Shell reopens by itself); the guard route kind, which replaces
`census-guard-ice` with a drone beside each mine route beyond the border.

## 1. Routes That Pay

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
| Plate by `plate.py` over all drones, second pass | +2,943 cr at three stations by 13:25 UTC (made 12, sold 9 at 287 to 361 cr) | 3 | 2026-11-16 13:23 UTC; plate bids of 4 to 5 at each station took 9 of 12; the drones still hold about 720 carapace (the tool stock, 13:10 UTC) |

Drone hunts from 2026-11-16 09:30 to 13:00 UTC (`hunt_figures.py --since 09:30 --role drone`):
4 runs, 52.7 hunter-minutes, +1,535 cr, 1,748 cr per hunter-hour; Achernar cinder-sylphs
2 runs, 4 kills, 4 ember glands, 4,085 per hunter-hour; Lesath 2 runs, 0 kills (herd 0),
-546. Every other hunt stood closed: the curd bid gone until 12:07 UTC.

Ember glands are bid 480 cr, 30 to 50 deep, at all eight stations of our books
(09:02 UTC). Drone hunts from 2026-11-16 05:30 to 09:10 UTC, all routes:
1,052 hunter-minutes, +20,307 cr, 1,158 cr per hunter-hour (`hunt_figures.py`);
the veil-ray part of it stopped paying at 07:05 UTC (section 2). No hull lost.

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `hunt-acubens-urchin` | 3 runs, 6 kills, -240 cr per ship-hour | 2026-11-15 | No radiant bile dropped, carapace only. Off |
| `hunt-home-drift-ray` | 11 runs, -260 cr per ship-hour | 2026-11-15 | Crystallized biogas bid 1 to 2 cr. Out of the plan (orders F8) |
| A pilot-whale (220 hull) | Took a starter with a railgun from 73 to 15 hull in one fight | 2026-11-15 | Not for a starter hull with no defence module (orders F9) |
| Piercing Railgun I on veil-rays (`hunt-gsc-veil-ray`, 21:55 to 22:54 UTC) | 3 runs: 4, 4 and 0 kills; the two trips with 4 kills took 21.4 and 24.0 min, the eight pulse-laser trips with 4 kills at the same place 21.7 to 26.8 min (18:20 to 21:28 UTC); +1,915, +1,915 and -65 cr | 2026-11-15 | No gain measured, and the weapon needs ammunition: 8 slug cases bought for 320 cr ran out in the third run, which fled at once. The hunters keep the Pulse Laser I. No hunt route takes a ship with a railgun (`requires.without_module`) until it carries ammunition |
| Yield test: bell-jellies at Nexus Prime Stellar Siphon | 1 run, 2 kills in 6 min at the place, -26 cr | 2026-11-15 23:29 UTC | Drop: 3 crystallized biogas, 1 levity bladder; both bid 1 to 2 cr. Off |
| Yield test: rime-grazers and pressblisters at Node Gamma Ice Belt | 1 run, 3 kills in 16.8 min, -60 cr a run (`routes.py measure`) | 2026-11-15 23:29 UTC | Drop: 3 creature carapace, 2 nitrogen bladder; both bid 1 to 2 cr. Off |
| Yield test: deuteron-slugs at Node Beta Frozen Drift | 1 run, 2 kills in 23.3 min, no goods recorded, -33 cr | 2026-11-15 23:29 UTC | Off |
| Yield test: kiln-snails (100 hull) at Eltanin Prime Belt, Node Beta | 1 run of 32.8 min: 0 kills, hull 75 -> 46 (lowest 68% in the battle table), -167 cr | 2026-11-15 23:29 UTC | The one fight of the turn that cost hull: prey of 100 hull hits a starter hard. Off (orders F9) |
| `hunt-ruchbah-veil-ray` by hand, hold empty | 1 run: 0 kills, -77 cr, two ships of a faction of 1,249 members joined the fight within three minutes | 2026-11-15 21:26 UTC | The first run of the route (below, section 6) found nobody there |
| `hunt-garnet-dim-lattice-veil-ray` | 6 runs, 0 kills, -610 cr per ship-hour | 2026-11-16 03:19 UTC | A ship not of ours at the place in every run; the herd read 23 at 01:30 UTC. Out of the plan (orders F8) |
| `hunt-test-acubens-patina-grazer` | 5 runs, 0 kills, -500 cr per ship-hour | 2026-11-16 03:19 UTC | A pilot not of ours at the place in every run; out. Patina-grazers are tested at Atlas instead |
| `voidborn-first-hunt-schedar` | 10 runs, 190 cr per ship-hour with the reward; 1 of 9 counted runs handed in | 2026-11-16 03:19 UTC | A foreign pilot at the place in 8 of 9 runs (route logs). Kept last among the once routes because the fill gate counts it paying |
| `voidborn-first-hunt-ironhollow-echo`, `-fading` | 2 runs each, no hand-in (`first_hunt_belt_grazers not offered` in 3 of 4), closed by the loss stop | 2026-11-16 05:16 UTC | Out of the plan |
| `voidborn-first-hunt-acubens` | 21 runs since 01:00 UTC, 2 hand-ins | 2026-11-16 05:20 UTC | Acubens Shadow Pocket held no belt-grazer at any read from 03:33 to 04:48 UTC (data/wildlife/history.jsonl); out until the herd is back |
| `hunt-test-gsc-0050-cinder-sylph` | 2 runs, 0 kills, -540 cr per ship-hour | 2026-11-16 05:16 UTC | The herd read 0 at 01:52 UTC. Out |
| `hunt-test-atlas-patina-grazer` | 5 runs, 4 kills, -360 cr per ship-hour | 2026-11-16 05:16 UTC | Drop: creature carapace and raw xeno meat, no bid above 2 cr; a ship not ours at the place in 3 of 5 runs. Out |
| `hunt-test-garnet-slag-tortoise` | 2 runs, 0 kills, -630 cr per ship-hour | 2026-11-16 05:16 UTC | Out; the drop of a slag-tortoise is still not seen |
| `hunt-test-goldcrest-glitterback-crab` | 2 runs, 0 kills, -600 cr per ship-hour | 2026-11-16 05:16 UTC | A ship not ours at the place; out |
| `hunt-test-tanglewood-hollow-pilgrim` | 1 run, 2 kills, -50 cr per ship-hour | 2026-11-16 05:16 UTC | Drop: 2 crystal melt (bid 54 cr) and creature carapace. Out |
| `hunt-dimming-pocket-veil-ray`, `hunt-denebola-fractured-prism-veil-ray` | 3 runs each: 610 and -10 cr per ship-hour, 1 and 2 kills | 2026-11-16 05:16 UTC | A ship not ours at the place in every Dimming Pocket run and in 2 of 3 at Denebola. Out |
| The seven veil-ray hunts: `hunt-gsc-veil-ray` (3,020 by all its runs), `-hamal-` (2,310), `-ruchbah-` (2,100), `-keid-fractured-prism-` (1,850), `-faintlight-drift-` (1,300), `-low-charge-glint-` (1,060), `-cedarhold-dim-lattice-` (900) | 21 drone runs from 07:05 UTC, read at 09:05 UTC: -1,851 cr in about 474 hunter-minutes, about -234 cr per ship-hour; at 09:20 UTC 23 runs, -2,056 cr, none sold anything, 18 looted curd | 2026-11-16 09:12 UTC | The verdigris curd bid (330 cr x 50) left all seven stations of our books between 07:08 and 07:51 UTC (data/market/history.jsonl) and none stood at 09:02 UTC; The Experiment bids 2 cr. Our runs sold 128 curd from 03:00 to 08:00 UTC against about 350 bid at seven stations: whether others sold the rest, or the bids were withdrawn, is not in our record. `status: off` and out of the plan; back when a curd bid of 100 cr or more reads again |
| `hunt-dimming-pocket-veil-ray` (no plan holds it) | 7 runs of the fleet, 80 cr per ship-hour by all runs | 2026-11-16 09:32 UTC | Sells curd like the seven: `status: off` when the fill gate asked for it; back with a curd bid |
| `voidborn-first-hunt-achernar` | 19 drone runs from 05:30 UTC, 0 hand-ins, -1,474 cr | 2026-11-16 09:12 UTC | A ship not ours at the place in every run from 06:49 UTC (the hunt step's last word in each row). Out of the plan; `store: all` at its last stop |
| `voidborn-first-hunt-schedar` | 17 runs of the fleet from 03:13 UTC, 1 hand-in, -12 cr in sum | 2026-11-16 09:16 UTC | A ship not ours at the place in every run from 04:58 UTC. `status: off`; back when a census reads the belt free twice in a row |

| The weekly tax inside runs | 7 drone runs in flight at the assessment of 12:27 UTC carried 29,346 cr of their pilots' tax (census-guard-ice 2, First Hunt 3, Cracking the Shell 2); the division paid 125,248 cr in all, 2,868 to 5,315 a drone (`get_tax_estimate`, 13:05 UTC) | 2026-11-16 12:27 UTC | Not a loss of the routes: the money was owed. Read without it, the drones' steady money over four hours to 13:18 UTC was -5,077 cr (-42 per ship-hour over 30 ships) against -34,423 with it (the tool fleet, view tasks). Next assessment in about six days; Trade asked Unity to keep it out of the run rows (requests.log ENT-147) |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. Measured by `routes.py measure`, 2026-11-15 23:58 UTC, all runs of
the fleet:

| Route | Pays once | Measured | Note |
|---|---|---|---|
| `voidborn-precedence` | 4,000 cr | 41 runs, 15 min, 3,890 cr a run | Accept at Node Beta, two docks, nothing bought. Drones from 23:40 UTC |
| `voidborn-first-hunt-nexus`, `-gsc`, `-acubens` | 1,000 cr, 50 Weapons XP, 15 Xenobiology XP, 20 Piloting XP | 2026-11-16 03:19 UTC, all runs of the fleet: nexus 10 runs, 21 min, 570 cr a run; gsc 7, 27 min, 790 cr; acubens 12, 14 min, 370 cr | The circuit runner's `hunt` step: accept, three belt-grazer kills, hand in. One hunter per herd, so the fleet's pilots queue for three herds |
| `voidborn-first-hunt-schedar` | the same | 10 runs, 11 min, 40 cr a run (2026-11-16 03:19 UTC); see section 2 | A fourth herd one jump beyond GSC-0027 (20 belt-grazers, no pilot, 21:14 UTC), `alone` and an empty hold; a test from 2026-11-15 23:58 UTC |
| `voidborn-selling` | 1,000 cr for the pilots that hold Market Participation: Selling | 40 runs, 5 min, 870 cr a run | 20 drones held the mission (`data/fleet/ships/`, 23:46 UTC) |
| `voidborn-concurrent` | 3,000 cr | every drone has it booked | Flown by all 30 drones on 2026-11-15 |
| `voidborn-first-hunt-ironhollow-echo`, `-ironhollow-fading`, `-achernar` | 1,000 cr, accepted and handed in at The Experiment | Achernar: 1 run, 19 min, +960 cr (03:00 UTC); Ironhollow: see section 2 | Three herds one jump beyond The Experiment, written 2026-11-16 03:00 UTC: 26, 19 and 12 belt-grazers at their reads of 01:19 to 01:20 UTC |
| `mission-cracking-the-shell-achernar`, `-central` | 1,500 cr, 55 Weapons XP | achernar 2 runs, refused at the accept; central 24 runs of the fleet, 730 cr per ship-hour (`routes.py measure`, 05:21 UTC) | Back in the plan since 2026-11-16 05:16 UTC with `requires.booked` First Hunt (requests.log ENT-102): in 19 runs of the fleet (2026-11-16 01:16 to 03:22 UTC) the pilots with First Hunt booked were offered it (7 of 7) and the others not (12 of 12). `-central` hunts at Alnair Ice Fields since 05:17 UTC (8 pressblisters at 01:55 UTC, no predator); Node Gamma Ice Belt read no pressblister from 01:50 UTC on. "Hunt 3 Pressblisters at an ice field": any ice field. Achernar Frost Ring read 8 pressblisters at 01:21 UTC |

| `voidborn-signal-fragments` (Trade's) | 7,000 cr | 36 runs of the fleet, 14 min, 5,730 cr a run (`measured`, 09:15 UTC) | Only from navigation 3 (`requires.skills`); 11 drones have it. In the drone plan since 09:02 UTC, at its head |
| `voidborn-network-expansion` (Trade's) | 1,500 cr | 9 runs of the fleet, 8 min, 1,440 cr a run; 7 drone hand-ins from 09:02 to 09:15 UTC, +10,150 cr | Only after First Steps in the Void (`requires.booked`); 14 drones hold it |
| `voidborn-conductive-lattice` (Trade's) | 10,893 cr in a chain of three | 29 drone runs from 05:30 UTC, 29 hand-ins, +315,369 cr in all, about 10,875 a run after the silver and crystal it buys | 29 of 30 drones have flown it |
| Drone once runs, 2026-11-16 09:30 to 13:24 UTC (`data/routes/runs.jsonl`, the 12:27 UTC tax taken out) | -- | Signal Fragments 4 runs, 4 hand-ins, +27,630 cr in 57 min; First Hunt gsc 7 runs, 7 hand-ins, +6,498 cr in 196 min (1,985 per ship-hour with the reward); First Hunt nexus 10 runs, 3 hand-ins, +2,418 cr in 196 min (741); Cracking the Shell achernar 10 runs, 5 hand-ins, +6,122 cr in 191 min (1,926) | Paid once to drones in four hours to 13:18 UTC: 59,000 cr (the tool fleet, view tasks). The herds, not the board, bound First Hunt and Cracking the Shell: both now carry `min_creatures` 3 |

Belt-grazer goods are creature carapace and raw xeno meat; no station of
ours bids above 1 cr for either. The mission is the pay. Carapace becomes armor
plate at a workshop (section 1).

## 4. Levelling

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
- Navigation by jumps (test `train-navigation-home`, one drone, 2026-11-16 13:17 UTC):
  three jumps through our own stations (Central Nexus, Node Alpha, Synchrony, Node
  Gamma) and their docks took the pilot from 334 XP at level 2 to 6 XP into level 3,
  12 XP, about 4 XP a jump, for 80 cr of fuel (ship file 13:27 UTC). At that rate the
  drone furthest from level 3 (173 XP) needs about 42 jumps and about 1,100 cr of fuel
  for a mission that pays 7,000 cr once. The whole run's RESULT line is read next turn.
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
  veil-rays it was no faster than the pulse laser (section 2).
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

The yield tests of 2026-11-16 03:00 to 03:16 UTC are read (section 2): of eight,
the Lesath cinder-sylph herd paid and stays; the rest left the plan at 05:16 UTC.
Open now, one ship each:

- `mission-cracking-the-shell-central` (Unity's) hunts at GSC-0041 Frost Ring since
  10:38 UTC with a herd floor of three (requests.log ENT-135); the ring read 0
  pressblisters, 4 deuteron-slugs, 2 rime-grazers and a frost-lurker of 400 hull at
  12:09 UTC (data/wildlife/gsc_0041.json): closed by its floor. Back in the drone plan.
- `train-navigation-home`: one drone, five jumps through our own stations; what a jump
  gives in navigation XP (section 4). Every run loses its fuel, so the loss stop closes
  it after three runs; to fly it for every drone short of navigation 3 it needs a field
  the dispatcher reads (asked of Unity in requests.log this turn).
- `sell-curd-central-nexus`, `-node-beta`, `-experiment`: one ship each; the first run
  sold 11 curd for +3,630 cr in 0.7 min (13:22 UTC). Two runs went to pilots whose curd
  had been sold by hand minutes before (0.0 min, 0 cr): `requires.stored` reads the
  ledger, which reads each pilot about every 40 minutes.
- `census-guard-ice`: 25 runs from 09:30 to 13:24 UTC, -3,567 cr without the tax,
  -611 cr per ship-hour, two ships: about 1,220 cr an hour, the price of the guard
  (orders F16). What its reads renewed is not measured.
- `game/fleet/plate.py` over all drones each turn: how many plates the bids take in
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
