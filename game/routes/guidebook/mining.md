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
(2026-11-16 12:25 UTC, orders.log ENT-014). A free miner takes the
first route open to it. Credits per ship-hour flown are the runs of
2026-11-16 08:00 to 12:20 UTC (`data/routes/runs.jsonl`); the scale is
the best repeating route of the last four hours, mine-wolf-1061-vent
at 6,578 (`hive.py tasks`, 12:15 UTC); a ship without work earns 0.

| # | Route | Ships | Expected per ship-hour | What it is for |
|---|---|---|---|---|
| 1 | `voidborn-signal-fragments` | Trade's limit, 10 | 7,000 cr once in about 14 minutes | Pilots with navigation 3 |
| 2 | `voidborn-first-steps-board`, `-network-expansion`, `-collective-provides`, `-signal-protocol` | Trade's limits: 3, 20, 2, 20 | 922, 1,450, 2,188, 3,409 cr once (Trade's tests) | The once line of the Central Nexus board, in this order (orders ENT-014 (c)) |
| 3 | The other missions that pay once (`voidborn-concurrent` to `-precedence`), `voidborn-conductive-lattice`, the First Hunts | as their files stand | judged with the reward | Every pilot flies them first |
| 4 | the six `fit-ice-harvester*` routes | closed | money spent once | Their asks are used up; 39 of 40 miners carry a harvester |
| 5 | `carry-ice-node-alpha-nexus` | 3 | not measured: 65 water ice a run, 1 jump, about 2,080 cr of sales | Stored ice of Node Alpha into the Central Nexus bid |
| 6 | `drain-ice-node-alpha` | 2 | not measured | Stored ice sold at Node Alpha when its bid regains |
| 7 | `carry-ice-synchrony-nexus`, `carry-ice-experiment-nexus` | 2, 3 | not measured: 2 and 3 jumps | Stored ice of Synchrony and The Experiment into the Central Nexus bid |
| 8 | `mine-wolf-1061-vent` | 1 | 6,578 (3 runs) | Only a pilot with a Nitrogen Vent: none fitted now |
| 9 | `mine-achernar-frost-ring-nexus` | 3 (15 before) | 3,047 (45 runs, 8 of them at a loss) | Central Nexus, four jumps |
| 10 | `mine-ruchbah-ice-belt-nexus`, `-alnair-ice-fields-nexus`, `-wolf-1061-frozen-drift-nexus`, `mine-cryogenic-reserve` | 1 each | 3,549 (3), 3,182 (14), 2,043 (12), 9,225 (1 run, sold storage) | Central Nexus, four, five, four and zero jumps |
| 11 | `census-frontier` | up to 12 | -592 (`hive.py tasks`) | Reading, when a miner has nothing else |
| 12 | `park` | the rest | 0 | Dock at home and wait |

Every route of rows 5 to 10 names its water-ice bid (`requires.bid`):
the drains and carries at 25 cr for 30 or 65 units, the mine routes
for 300. A route closes while a book read within the hour shows less,
and opens by itself when one shows it back. The drains and carries go
only to a pilot whose own storage holds the load (`requires.stored`);
their first stop stores what is aboard, then withdraws (the circuit
runner's `withdraw` step, built this turn).

Why this plan: the buyers, not the tool, bound Mining. At 12:01 UTC the
whole water-ice ladder of Central Nexus read 32 cr x 563 (42,635 at
09:17 UTC; 8,500 at 10:37 UTC; `data/market/central_nexus.json`); it
regains about 1,197 units an hour at its best price (`hive.py refill`),
about ten ships' ice. The bids of Node Alpha (regains about 351 an
hour), The Experiment (about 7) and Synchrony (about 15) read 0. Miners
hold 16,224 water ice in storage (the tool stock, 12:04 UTC: The
Experiment 6,980, Node Alpha 5,500, Central Nexus 2,043, Synchrony
1,791): selling it costs only the fuel of one to three jumps, so it
goes first; the Central Nexus mine runs sell their pilots' storage
there themselves. The mine routes to The Experiment and Node Alpha
are out of the plan while their stations hold our stock.

What would change it: the stored ice outside Central Nexus under about
2,000 units (then the Central Nexus mine routes back toward ten ships);
a water-ice bid with depth near the fields (requires.bid opens its
routes by itself); a buyer for another good of the ice fields. Each
turn starts with the skill script `stalled.py` of the mining-chains
skill.

## 1. Routes That Pay

Runs of 2026-11-16 08:00 to 12:20 UTC (`data/routes/runs.jsonl`), after
fuel, per ship-hour flown:

| Route | Credits per ship-hour | Runs | Note |
|---|---|---|---|
| `mine-wolf-1061-vent` | 6,578 | 3 | Sold at Synchrony while its bid stood |
| `mine-ruchbah-ice-belt-nexus` | 3,549 | 3 | Central Nexus, four jumps: the one-ship test of 08:12 UTC holds |
| `mine-alnair-ice-fields-nexus` | 3,182 | 14 | Central Nexus, five jumps |
| `mine-achernar-frost-ring-nexus` | 3,047 | 45 | Central Nexus, four jumps; 8 runs at -138 to -318 cr ended 11:00 to 11:10 UTC while the bid read 0 |
| `mine-wolf-1061-frozen-drift-nexus` | 2,043 | 12 | Central Nexus, four jumps |

Mining over all 40 ships in the four hours to 12:15 UTC: 1,446 credits
per ship-hour, 2,246 per ship-hour flown, 453,122 cr paid once beside
it (`hive.py tasks`); steady net of the division in the hour to 12:15
UTC +39,778 cr (`hive.py fleet`).

The figures below were measured by `routes.py measure` at 08:20 UTC:

Measured by `routes.py measure`, 2026-11-16 08:20 UTC, after fuel, over
every run of a route. The figures of the routes that sold at The
Experiment and Node Alpha were earned while their bids stood; since
07:07 and 07:25 UTC those bids read 0 (section 2).

| Route | Credits per ship-hour | Runs | Minutes a run | Note |
|---|---|---|---|---|
| `mine-ruchbah-ice-belt` | 7,430 | 46 | 43 | The Experiment, one jump; 8,950 over 16 runs at 04:23 UTC; its last ten runs sold no water ice |
| `mine-achernar-frost-ring` | 5,460 | 35 | 48 | The Experiment, one jump; its last nine runs sold no water ice |
| `mine-wolf-1061-vent` | 5,360 | 5 | 56 | Ice Harvester I with a Nitrogen Vent |
| `mine-achernar-frost-ring-nexus` | 2,650 | 5 | 51 | Central Nexus, four jumps; +2,755, +3,012, +2,916 cr on its paying runs |
| `mine-homam-cryobelt` | 2,660 | 4 | 73 | The Experiment; +5,041 and +8,318 cr while the bid stood; out of the plan |
| `mine-gsc-0041-frost-ring` | 2,080 | 5 | 62 | Node Alpha; out of the plan |
| `mine-wolf-1061-frozen-drift` | 2,070 | 10 | 67 | Node Alpha; sells methane while the water bid regains |
| `mine-alnair-ice-fields-nexus` | 1,820 | 3 | 77 | Central Nexus, five jumps; +3,670 cr on its paying run |
| `mine-wolf-1061-frozen-drift-nexus` | 1,640 | 4 | 66 | Central Nexus, four jumps; +3,496 and +4,333 cr on its paying runs |
| `mine-node-beta-frozen-drift` | 1,340 | 12 | 44 | Field 225 water ice (07:53 UTC); out of the plan |
| `mine-keid-ice-shelf` | 1,120 | 8 | 96 | Node Alpha, five jumps; out of the plan |
| `mine-intercrus-ice-fields` | 880 | 8 | 76 | The Experiment; out of the plan |
| `mine-alnair-ice-fields` | 840 | 9 | 67 | Node Alpha |

Mining as a whole in the four hours to 08:18 UTC: 98 mine runs, 93.9
ship-hours flown, 2,302 credits per ship-hour flown (`hive.py tasks`);
the division over all 40 ships, 1,183 credits per ship-hour (scale
7,910). Steady money of the division in the last hour, read at 08:17
UTC: +14,370 cr (`hive.py fleet`), against +70,528 at 04:16 UTC: the
near bids emptied in between.

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` | -170 cr per ship-hour each | 2026-11-15 | Iron and copper ore sell for 1 to 4 cr and nobody needs them. Out of every plan (orders F8) |
| `mine-cryogenic-reserve` | 3 runs, -350 cr per ship-hour | 2026-11-16 | Every run ended "not docked for the sale": the ice stayed in storage. Not the field and not the bid: the runner's dock step fails on 14 of 39 mine runs since 2026-11-15 23:00 UTC (errors.log ENT-032). Closed until the fix of requests.log ENT-084 |
| `mine-gsc-0050-gas-plume` | 2 runs, -230 cr per ship-hour (-407 cr in sum) | 2026-11-16 | Both runs ended "not docked for the sale"; the first load was 43 of 65 units neon, which no station buys, and the plasma bid at Node Beta holds 4 to 12 units. Closed by the loss stop, out of the plan with its fit route; the harvester lies in storage at Central Nexus |
| `voidborn-first-steps` (15 carbon ore) | Two runs, -109 and -153 cr | 2026-11-15 | Acubens Belt read 0 carbon; carbon regrows slowly (41 at 22:17 UTC) |
| Focused crystal as a chain | One station bid of 1,466 cr for 1 unit, then 40 cr | 2026-11-15 | One craft per refill of that bid (errors.log ENT-015) |
| `mission-cracking-the-shell-central` | 8 miner runs, all "not offered", -286 cr | 2026-11-16 | The board offers it only to a pilot with First Hunt booked (errors.log ENT-033); fill.py had added it on the figure of another role. Out of the plan |
| Honeyglobe | Bids of 154 and 147 cr for 1 unit each | 2026-11-15 | No depth: not tested |
| Selling at The Experiment, Node Alpha and Synchrony after their bids emptied | 36 runs started 05:20 to 07:20 UTC sold no water ice, -12,384 cr of fuel in sum; about 11,100 water ice stored there | 2026-11-16 | The Experiment's 15,832 at 36 cr was one order: used up in three hours, it regains about 10 units an hour. Routes cut to one ship each, the rest to Central Nexus (commit 9585697); the stored ice waits for a carry (requests.log ENT-117) |
| `mine-keid-ice-shelf`, `-intercrus-ice-fields`, `-gsc-0033-cryobelt`, `-gsc-0021-ice-fields`, `-tanglewood-frost-ring`, `-antares-ice-fields` | -400 to -490 cr per ship-hour on their last runs, or runs of 76 to 96 minutes | 2026-11-16 | Their stations' bids are 0 and they lie five to seven jumps from Central Nexus. Out of the plan |
| `voidborn-first-hunt-acubens` | 25 runs, -1,375 cr in six hours | 2026-11-16 | The belt's herd read 0; closed by the loss stop and out of the plan |
| Titanium Extraction Contract (3,500 cr once) | not flown | 2026-11-16 | 20 titanium ore to be mined at HD 147513 Belt, 7 jumps, lawless: it held 127 titanium beside 866 iron, 680 copper and 1,047 gold, each over 97% mined out (census 08:50 UTC); a hold of that mix brings a few titanium, so one mission is two or more trips of 14 jumps. No route file |
| The Central Nexus depth | 42,635 water ice at 30 cr at 09:17 UTC, 8,500 at 10:37, 563 in all levels at 12:01 | 2026-11-16 | The second deep water-ice order in a day gone within three hours; our ships sold a part of it, the rest went to others or was withdrawn (not measured which). 29 miners were sized on it. Cut to 7 mine places and the stored ice first |
| `carry-ice-node-alpha-nexus`, first three runs | -50 cr each, nothing sold | 2026-11-16 | The withdraw step counted the free hold in item units; the game counts space (tungsten and lead ore take two) and refused it. Fixed (commit 180d58b); the loss stop holds the route until about 18:15 UTC |
| `drain-ice-nexus` | two runs, 0 and -39 cr, nothing to take | 2026-11-16 | The ledger reads storage every 40 minutes, and the Central Nexus mine runs already sell their pilots' storage there: out of the plan |
| `mission-ghosts-in-the-cloud-node` | one miner run, -24 cr | 2026-11-16 | "not offered" four times in a row since 11:31 UTC after two hand-ins of 2,000 cr: out of the plan |
| `mine-ruchbah-ice-belt`, `-achernar-frost-ring`, `-wolf-1061-frozen-drift`, `-alnair-ice-fields` | their stations' water bids 0 | 2026-11-16 | The Experiment and Node Alpha hold 6,980 and 5,500 of our stored water ice: out of the plan until their bids regain with depth |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | 39 miner runs, +115,037 cr, of it 117,000 once | 2026-11-15 | Its two neural soma come with the accept |
| `voidborn-mining-missions` (Iron Supply Run, Copper Requisition) | 1,500 + 1,800 cr | 3 runs by 22:24 UTC, +6,430 cr | 2026-11-15 | Booked for every miner now |
| `voidborn-precedence` | 4,000 cr | 146 runs of the fleet, 580,000 cr once | 2026-11-16 | Booked for every miner now |
| `voidborn-first-hunt-*` (three herds) | 930 to 970 cr | one ship each at a time | 2026-11-16 | The home herds read 0 to 3 grazers (queue.log ENT-063): slow |
| `voidborn-signal-fragments` | 7,000 cr | 40 miner runs, +275,879 cr | 2026-11-16 08:00 to 12:20 UTC | Pilots with navigation 3 |
| `voidborn-conductive-lattice` | about 10,900 cr | 32 miner runs, +273,451 cr | 2026-11-16 08:00 to 12:20 UTC | The Node Beta chain |
| `voidborn-network-expansion` | 1,500 cr | 12 miner runs, +17,374 cr | 2026-11-16 08:00 to 12:20 UTC | After First Steps |

## 4. Levelling

- At 12:15 UTC (`hive.py levels`): median Mining 5 (115 XP an hour),
  Piloting 5 (132 XP an hour), Navigation 3, Deep Core Mining 3; 86 hours
  to Piloting 10 at that rate.
- Mining XP is one point per unit mined. Level 5 needs 900 XP, level 6
  1,285 (the pilots' files). Median of the 40 miners on 2026-11-16 at
  08:20 UTC: Mining 4, Piloting 4, Navigation 3, Deep Core Mining 3
  (`hive.py levels`); at 03:19 UTC it was Mining 2, Piloting 3.
- Every ice route trains Mining (ice fields train it like belts) and
  Piloting (the jumps); the miners on ice since 2026-11-15 stand at
  Mining 4 and 5, the waiting ones at 2.
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5. At the division's
  average rate (118 XP an hour of Piloting) the median miner needs
  about 103 hours to Piloting 10 (the tool fleet, view levels, 08:20
  UTC). A route that sells at Central Nexus flies four to five jumps
  each way: more Piloting per run than a one-jump route.
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
  2026-11-16 03:15 UTC, 3.6 to 4.2 minutes each). At Ironlight Crossroads (LHS 1140,
  beyond the border) the fit costs 687 or 709 cr with fuel and tax,
  8.7 to 12.4 minutes from Node Beta (9 runs to 04:22 UTC,
  `data/routes/runs.jsonl`): about 760 cr less a ship than at home. 18 asks at 638 cr stood
  at 04:24 UTC; 20 asks at 518 cr at 07:42 UTC. 39 of the 40 miners
  carry one (2026-11-16 08:01 UTC, `hive.py standing`).
- A hold is counted in space, not in units: each row of the pilot's
  `state/cargo` carries a `size` (tungsten and lead ore 2, ice and the
  other ores 1). The game refused a withdraw of 23 units into a hold
  with 9 free (2026-11-16 12:15 UTC).
- Goods move between two of our own pilots docked at one station:
  `deposit` (spacemolt_storage) with `source` storage and `target` the
  other pilot's name gives them from the one storage into the other
  (2026-11-16 08:11 UTC, silicon ore and energy crystal to Logistics,
  read back from both storages).
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

- The drain and carry routes of stored water ice (Standing Plan, rows 5
  to 7): their first RESULT lines on the fixed runner. One carry
  withdrew 65 water ice at The Experiment or Synchrony at 12:19 UTC.
- The vent: a second vent route only when a Nitrogen Vent is on offer.
- Deuterium ice: station bids of 2 cr at The Experiment now (492 units);
  the routes sell it from 166 cr only and store the rest.
- Methane ice: 36 cr bids at eight stations in pools of 500 to 1,000,
  regaining about 65 an hour where read twice (Synchrony, The
  Experiment); the fields hold it beside water ice, so it comes with
  the water, not alone.
- Palladium ore: bids of 358 cr at four stations, 43,460 units in all
  (the tool fleet, view capacity, 12:03 UTC); no field we read holds it.
  Uranium and thorium the same, and they need a tool we lack.
