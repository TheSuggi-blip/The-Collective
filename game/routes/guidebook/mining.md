---
name: guidebook-mining
id: 20261115T205803Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# mining.md -- Guidebook of the Mining Division

Kept by Zero; read by every member. What the Mining division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Zero writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`. Every earning is in credits per ship-hour
  (orders F19).
- The plan in force is `game/routes/plans/miner.json`; every route
  with its figure is in `game/routes/index.md`; the fleet as it flies is
  `python3 -I -B game/fleet/hive.py standing` (the tool hive, verb
  standing).

## Standing Plan

What the miners fly between two turns, in the order of the plan
(2026-11-16 03:22 UTC, orders.log ENT-011). A free miner takes the
first route open to it. Credits per ship-hour are `routes.py measure`
of 2026-11-16 03:22 UTC; the scale is the best route, 8,270.

| # | Route | Ships | Expected per ship-hour | What it is for |
|---|---|---|---|---|
| 1 | The missions that pay once (`voidborn-*`) | as their rewards stand | judged with the reward | Every new pilot flies them first |
| 2 | `mine-gsc-0050-gas-plume` | 1 | -220, one run | The gas test; only the one gas miner can fly it; it stands before the fits so that this miner, whose two utility slots are full, buys no ice harvester |
| 3 | `fit-ice-harvester` (Node Alpha) | 1 at a time | money spent once | No ask at Node Alpha now; opens again when one stands |
| 4 | `fit-ice-harvester-node-beta`, `-node-gamma`, `-synchrony`, `-experiment` | 1 at a time each; 2, 2, 4 and 2 pilots | money spent once, 1,449 to 1,460 cr a fit with fuel | One fit route per station, each sized by the asks at 1,413 cr there |
| 5 | `fit-ice-harvester-lhs-1140` | 1 pilot | money spent once | Test: 20 asks at 638 cr at Ironlight Crossroads, beyond the border |
| 6 | `mine-wolf-1061-vent` | 1 | 7,390 (3 runs) | The miner with the Nitrogen Vent |
| 7 | `mine-ruchbah-ice-belt` | 3 | 8,270 (10 runs) | Sold at The Experiment |
| 8 | `mine-achernar-frost-ring` | 3 | 6,850 (8 runs) | Sold at The Experiment |
| 9 | `mine-cryogenic-reserve` | 1, closed | -350 (3 runs) | Closed by the loss stop: all three runs failed to dock for the sale (section 2) |
| 10 | `mine-keid-ice-shelf` | 2 | 2,990 (2 runs) | Sold at Node Alpha; field 2,712 water ice |
| 11 | `mine-intercrus-ice-fields` | 2 | 2,460 (2 runs) | Sold at The Experiment; field 27,238 |
| 12 | `mine-wolf-1061-frozen-drift` | 2 | 4,430 (2 runs) | Sold at Node Alpha |
| 13 | `mine-alnair-ice-fields` | 2 | 4,430 (1 run) | Sold at Node Alpha; field 47,732, richness 67 |
| 14 | `mine-node-beta-frozen-drift` | 1 | 2,460 (5 runs) | Field down to 377 water ice (02:51 UTC): stays at 1 |
| 15 | `mine-gsc-0041-frost-ring` | 1 | 4,560 (1 run) | Field 2,851 |
| 16 | `mine-antares-ice-fields` | 1 | 2,700 (1 run) | Field 1,733, 300 an hour grows back |
| 17 | `mine-wolf-1061-frozen-drift-nexus`, `mine-achernar-frost-ring-nexus` | 1 each | not measured | Tests: sold at Central Nexus, the deepest water-ice ladder |
| 18 | `mine-gsc-0033-cryobelt`, `mine-homam-cryobelt`, `mine-tanglewood-frost-ring`, `mine-gsc-0021-ice-fields` | 1 each | not measured | Tests the route maker wrote, added by the fill gate (03:25 UTC) for the miners fitted this turn |
| 19 | `mission-cracking-the-shell-central` | 1 | judged with its 1,500 cr reward (7 runs, +340 cr a run) | A mission that pays once, added by the fill gate (03:30 UTC) |
| 20 | `census-frontier` | up to 12 | -600 | Reading, when a miner has nothing else |
| 21 | `park` | the rest | 0 | Dock at home and wait |

Why this plan: the limit of the ice work is the tool. 40 miners, 19
with an Ice Harvester I at 03:25 UTC (their ship files) and the rest of
the asks on the fit routes. The ice routes hold 24 places, tests included, shared with the
command group's pathfinders. The next limit is the bid: The Experiment's water-ice
share carries about 2 ships for each of Ruchbah and Achernar at its
best price (fill status, 03:16 UTC), so new places go to Central
Nexus, not to more ships at The Experiment. By 03:32 UTC The Experiment
held 604 units at 38 cr and Synchrony 10 at 40, Central Nexus 47,098 at
24 (fill status).

What would change it: the RESULT line of the Ironlight fit (cheaper
harvesters for the waiting miners); the dock fix asked in requests.log
ENT-084 (it would reopen Cryogenic Reserve and end the stored loads);
the first RESULT lines of the Central Nexus tests (more places); a
field that empties (Node Beta Frozen Drift); a bid that moves.

## 1. Routes That Pay

Measured by `routes.py measure`, 2026-11-16 03:22 UTC, after fuel.

| Route | Credits per ship-hour | Runs | Minutes a run | Note |
|---|---|---|---|---|
| `mine-ruchbah-ice-belt` | 8,270 | 10 | 42 | The scale of the fleet; sold at The Experiment |
| `mine-wolf-1061-vent` | 7,390 | 3 | 55 | Ice Harvester I with a Nitrogen Vent; 83% water in its first load against 59% without |
| `mine-achernar-frost-ring` | 6,850 | 8 | 48 | Sold at The Experiment |
| `mine-gsc-0041-frost-ring` | 4,560 | 1 | 62 | One run |
| `mine-wolf-1061-frozen-drift` | 4,430 | 2 | 67 | Sold at Node Alpha |
| `mine-alnair-ice-fields` | 4,430 | 1 | 69 | One run; the richest water-ice field we read |
| `mine-keid-ice-shelf` | 2,990 | 2 | 73 | |
| `mine-antares-ice-fields` | 2,700 | 1 | 69 | |
| `mine-intercrus-ice-fields` | 2,460 | 2 | 64 | |
| `mine-node-beta-frozen-drift` | 2,460 | 5 | 42 | Field nearly empty |

Mining as a whole in the four hours to 03:22 UTC: 36 mine runs, 27.6
ship-hours flown, 4,673 credits per ship-hour flown (`hive.py tasks`);
the division over all 40 ships, the waiting ones included, 674 credits
per ship-hour. Steady money of the division in the last hour, read at
about 03:19 UTC: +69,530 cr (the tool fleet, view money).

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` | -170 cr per ship-hour each | 2026-11-15 | Iron and copper ore sell for 1 to 4 cr and nobody needs them. Out of every plan (orders F8) |
| `mine-cryogenic-reserve` | 3 runs, -350 cr per ship-hour | 2026-11-16 | Every run ended "not docked for the sale": the ice stayed in storage. Not the field and not the bid: the runner's dock step fails on 14 of 39 mine runs since 2026-11-15 23:00 UTC (errors.log ENT-032). Closed until the fix of requests.log ENT-084 |
| `mine-gsc-0050-gas-plume` | 1 run, -220 cr per ship-hour | 2026-11-16 | The first load was 43 of 65 units neon, which no station buys; that run did not dock for its sale either. One more run is the test |
| `voidborn-first-steps` (15 carbon ore) | Two runs, -109 and -153 cr | 2026-11-15 | Acubens Belt read 0 carbon; carbon regrows slowly (41 at 22:17 UTC) |
| Focused crystal as a chain | One station bid of 1,466 cr for 1 unit, then 40 cr | 2026-11-15 | One craft per refill of that bid (errors.log ENT-015) |
| Honeyglobe | Bids of 154 and 147 cr for 1 unit each | 2026-11-15 | No depth: not tested |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | 39 miner runs, +115,037 cr, of it 117,000 once | 2026-11-15 | Its two neural soma come with the accept |
| `voidborn-mining-missions` (Iron Supply Run, Copper Requisition) | 1,500 + 1,800 cr | 3 runs by 22:24 UTC, +6,430 cr | 2026-11-15 | Booked for every miner now |
| `voidborn-precedence` | 4,000 cr | 146 runs of the fleet, 580,000 cr once | 2026-11-16 | Booked for every miner now |
| `voidborn-first-hunt-*` (three herds) | 930 to 970 cr | one ship each at a time | 2026-11-16 | The home herds read 0 to 3 grazers (queue.log ENT-063): slow |

## 4. Levelling

- Mining XP is one point per unit mined. Level 5 needs 900 XP, level 6
  1,285 (the pilots' files). Median of the 40 miners on 2026-11-16 (read about 03:19 UTC):
  Mining 2, Piloting 3, Deep Core Mining 3 (`hive.py levels`).
- Every ice route trains Mining (ice fields train it like belts) and
  Piloting (the jumps); the miners on ice since 2026-11-15 stand at
  Mining 4 and 5, the waiting ones at 2.
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5. At the division's
  average rate (107 XP an hour of Piloting) the median miner needs
  about 119 hours to Piloting 10 (the tool fleet, view levels).
- Mining skill raises the share of the rarer deposit in a pull (the
  game's `mine` help). At Mining 4 a nebula gave 14.5% energy crystal
  where its richness alone gives 8.3% (section 6).

## 5. Ships and Fits

- The hull: Threshold (tier 0): 2 utility slots, 16 cpu, 30 power, hold
  65. The ice miner flies the Mining Laser I and an Ice Harvester I in
  the two utility slots and the Pulse Laser I in its weapon slot: cpu 8
  of 16, power 17 of 30 (`install_mod`, 2026-11-15).
- Ice Harvester I: 1,413 cr at our stations plus 1% tax; a fit by route
  costs 1,449 to 1,460 cr with the fuel (four fit routes, started
  2026-11-16 03:15 UTC, 3.6 to 4.2 minutes each). 20 stand at 638 cr at Ironlight Crossroads
  (LHS 1140; book of 01:39 UTC): the test route
  `fit-ice-harvester-lhs-1140` says whether the trip pays.
- Size a route that buys a module by the asks at its one station, one
  ship at a time where they are few (errors.log ENT-026). One route per
  station, each with its own `max_pilots`.
- Nitrogen Vent (cpu 4, power 9): with the harvester in place of the
  laser it lifted the water share of a load from 59% to 83% (one run
  each); none on offer in our books since 2026-11-15 23:30 UTC.
- A gas miner (Gas Harvester I beside the laser) has no slot left for an
  ice harvester; `requires.without_module` takes one module only, so the
  gas route stands before the ice fits in the plan.
- The next step of the fit: Ice Harvester II, made by hand from 1 Ice
  Harvester I, 2 ceramite plating, 3 liquid nitrogen and 1 power cell
  (catalog `build_ice_harvester_ii`; cpu 6, power 12, base value 1,800),
  on offer at 2,130 cr at Ironlight Crossroads (queue.log ENT-046). Its
  gain in units a minute is not in the catalog and not measured: one
  miner tests it once the waiting miners carry the Mark I.
- The next hull: tier 2 opens at Piloting 10, about 119 hours away for
  the median miner. Until then the money goes into harvesters (orders
  F17, strategy principle 1).
- Extraction filters take one ore out of a pull's draw (Magnetic Ore
  Separator, Flotation Cell, Electromagnetic Refinery, Isotope
  Separator); not bought: no rare ore of our fields has a buyer with
  depth.

## 6. Tests Flown

### Energy crystal at the nebula of `hunt-gsc-veil-ray`, 2026-11-15

One miner (Mining 4), 21:22 to 22:22 UTC, by hand: 166 units in three
loads (24 energy crystal, 94 iron ore, 48 copper ore), one palladium
ore bought at 436 cr, one focused crystal crafted in a station
workshop (24 ticks, no credit cost) and sold at The Experiment for
1,466 cr (a station bid of one unit), four raw crystals sold at 40 cr.
Result: +1,022 cr in 59.9 minutes after fuel and the palladium, about
1,020 credits per ship-hour; the bid was 40 cr after the sale.

### Ice at Wolf 1061 (frontier), 2026-11-15

One miner (Mining 4), by hand, 22:25 to 23:01 UTC, with one Ice
Harvester I bought at Synchrony: 126 units in two loads (water ice 77,
nitrogen 40, methane 5, deuterium 4); sold at Synchrony, water ice at
34 to 36 cr, methane at 47. Result: +2,688 cr in 30.1 minutes after
fuel, about 5,360 credits per ship-hour, one run. It opened the ice
routes of section 1.

### Fit routes per station, 2026-11-16

Four fit routes, one per station with asks, each `max_pilots` the asks
there and one ship at a time: the first runs at Node Beta, Node Gamma,
Synchrony and The Experiment fitted at 1,449 to 1,460 cr with fuel in
3.6 to 4.2 minutes each (`data/routes/runs.jsonl`, started 03:15 UTC); no buy above
the limit and no run without an ask, against six of ten runs that
found no ask when one route served ten fields (2026-11-15).

### Loops without a runner, 2026-11-16

Not a test: after the engine's restart of 02:00 UTC five miners flew
mining loops with no runner for about 65 minutes; the loops stored
their ice and sold none. Stopped by hand at 03:07 UTC; three sold what
the loops had stored, 1,111 water ice and 23 methane, +42,928 cr in
their wallets (errors.log ENT-032). A ship shown "busy by hand (loop)"
with no hand hold in `data/fleet/orders/` is such a loop.

## 7. Open Tests

- `fit-ice-harvester-lhs-1140`: price, fuel and minutes of the trip
  against 1,450 cr at home; then `max_pilots` up to the asks there.
- `mine-wolf-1061-frozen-drift-nexus`, `mine-achernar-frost-ring-nexus`:
  Central Nexus bids 23 cr for 2,543 water ice at its best price, 54,436
  in all its levels, and regains at least 1,513 units an hour
  (`hive.py refill`, 03:10 UTC).
- `mine-gsc-0050-gas-plume`: one more run; off when its two runs lose
  in sum.
- The vent: a second vent route only when a Nitrogen Vent is on offer.
- Deuterium ice: station bids of 188 to 260 cr for 5 or 6 units at Node
  Alpha and Node Beta; the routes sell it from 166 or 180 cr only and
  store the rest.
- Uranium, thorium and tritium have bids with depth at all six stations;
  no field read in our space or on the frontier holds them.
