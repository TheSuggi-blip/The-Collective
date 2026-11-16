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
last committed 2026-11-16 09:19 UTC; `hive.py standing` prints it ship by ship). Every
place holds one hunter (orders F9); every route beyond the border carries `alone`
and an empty hold (F13). Figures: `routes.py measure` as written in the route files
at 09:15 UTC, all runs of each route, after fuel. The scale of the hour: the best
repeating route of the fleet is our own `hunt-test-achernar-cinder-sylph`, 6,423
credits per ship-hour over four hours (the tool fleet, view tasks, 09:10 UTC), and 0
for a ship that waits.

| Order | Routes | Ships | Expected | Why |
|---|---|---|---|---|
| 1 | `voidborn-network-expansion` (Trade's route) | up to 10 for the fleet | 1,440 cr once in about 8 min (9 runs) | `requires.booked` First Steps: 14 drones hold it; 7 drones handed in from 09:02 to 09:15 UTC |
| 2 | `voidborn-signal-fragments` (Trade's route) | up to 10 for the fleet | 5,730 cr once a run in about 14 min (36 runs of the fleet) | `requires.skills` navigation 3: 11 drones have it |
| 3 | `voidborn-precedence`, `voidborn-conductive-lattice` | as booked | once | Every drone has Precedence; 29 of 30 flew the Node Beta chain (+10,875 cr a run, 29 drone runs from 05:30 UTC) |
| 4 | First Hunt: `voidborn-first-hunt-nexus`, `-gsc` (home) | 1 each | 1,000 cr once; 3 hand-ins each in 5 drone runs from 05:30 UTC | 19 drones have not booked it; one hunter per herd |
| 5 | Cracking the Shell: `mission-cracking-the-shell-achernar` (Achernar Frost Ring, 3 pressblisters and 6 pilots not ours at 08:44 UTC) | 1 | 1,500 cr once | `requires.booked` First Hunt; 11 drones hold it. `-central` is out: Alnair Ice Fields holds no pressblister (section 6) |
| 6 | `voidborn-first-steps`, `voidborn-selling`, `voidborn-concurrent` and the other once routes | as booked | once | Pass by themselves once booked |
| 7 | Cinder-sylphs: `hunt-test-achernar-cinder-sylph` 5,380 (6 runs), `hunt-test-lesath-cinder-sylph` 1,490 (2) | 1 each | about 1,500 to 5,400 | Ember glands at 480 cr, 30 to 50 deep at all eight stations (09:02 UTC); the only drop of our prey with a bid |
| 8 | `census-guard-ice` | 2 | a cost: -610 cr per ship-hour (28 runs) | The guard of orders ENT-013 block APOPHIS (2) until the guard runner exists: reads the eight lawless systems of our mine routes every hour and records who stands beside our miners |
| 9 | `census-frontier`, then `park` | up to 12, then the rest | reads; 0 | Docked costs nothing |

Beside the plan, every turn: `game/fleet/plate.py` over all drones (orders ENT-013,
APOPHIS (6)): the carapace in each drone's storage becomes armor plate where the drone
is docked, and plates are sold no deeper than the bid there. Not a route yet: the
circuit runner has no craft step.

At 09:34 UTC the fill gate read PASS with 20 drones waiting. What closes the work to
them: navigation 3 for Signal Fragments (12), First Steps not booked for Network
Expansion (13), one hunter per First Hunt herd (12 for 2 places), cinder-sylph herds
under four or resting, every census system read. The veil-ray hunts are `off` since
09:12 UTC: the verdigris curd bid left every station of our books between 07:08 and
07:51 UTC (section 2). Hunting carries one or two hunters today; the waiting drones
earn when a once mission opens to them.

What would change the plan: a verdigris curd bid of 100 cr or more read again (the
seven veil-ray hunts go back on; `requires.bid` on hunt routes is asked of Unity,
requests.log ENT-125); a census that reads Achernar or Schedar Belt without a ship
not ours twice in a row (First Hunt there goes back on); a cinder-sylph herd of four
or more at a new place; the guard route kind (owed by Unity, requests.log ENT-070),
which replaces `census-guard-ice` with a drone beside each mine route beyond the
border.

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

- `mission-cracking-the-shell-central` at Alnair Ice Fields: from 05:43 UTC 5 runs
  of the fleet (3 drones), 0 hand-ins, -871 cr; Alnair Ice Fields read no pressblister
  at 09:07 UTC (data/wildlife/alnair.json). Out of the drone plan at 09:19 UTC (commit 57ec2f2); the
  move of its hunt to an ice field with pressblisters is asked of Unity, since five
  plans fly the route (requests.log, this turn).
- `census-guard-ice`: 28 runs, -610 cr per ship-hour (`measured`, 09:15 UTC), two
  ships: about 1,220 cr an hour, the price of the guard (orders F16). What its reads
  renewed is not measured.
- `game/fleet/plate.py` over all drones each turn: how many plates the bids take in
  four hours is not measured; the pools refill within the hour (logistics.md).
- Pirate Bounty (2,000 cr once, kill one pirate; on the boards of Central Nexus, Node
  Gamma and Synchrony Hub, data/missions/ at 09:20 UTC): not
  flown. Orders F2 forbid firing first at an NPC ship; pirates stood at Gliese 876
  and Felis at 04:40 UTC (queue.log ENT-090). Suggi's word, put in my report.
- No new species test: at 05:10 UTC no untested grazer of 100 hull or less stood
  in a herd of four or more in our readings (data/wildlife/: bulwark 3, coronid
  2; carrion-moths and ash-scarabs are scavengers, outside orders F9).
- Which prey drops caustic sac (bid 420 cr, 50 at seven stations): not measured.
  The catalog names no source ("mined, dropped or bought only"), and no run of
  the fleet has looted one (`data/routes/runs.jsonl`, 05:10 UTC).
- A tier-1 hull with two weapons: only after a test shows prey worth a tougher
  hull (section 5); prey over 100 hull needs an order beyond F9.
