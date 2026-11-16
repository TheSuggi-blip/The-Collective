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
(2026-11-16 08:24 UTC, orders.log ENT-013). A free miner takes the
first route open to it. Credits per ship-hour are `routes.py measure`
of 2026-11-16 08:20 UTC over all runs of a route; "paying runs" leaves
out the runs that ended "not docked for the sale" before the dock fix
of 04:47 UTC. The scale is the best repeating route of the last four
hours, 7,910 (`hive.py tasks`, 08:18 UTC); a ship without work earns 0.

| # | Route | Ships | Expected per ship-hour | What it is for |
|---|---|---|---|---|
| 1 | `voidborn-signal-fragments` | Trade's limit, 3 at a time | 7,000 cr once in about 14 minutes | Pilots with navigation 3 (orders ENT-013) |
| 2 | The other missions that pay once (`voidborn-concurrent` to `-precedence`) | as their rewards stand | judged with the reward | Every new pilot flies them first |
| 3 | `voidborn-conductive-lattice` | Trade's limit, 10 at a time | 19,320 (73 runs of the fleet), about 10,900 cr once | The Node Beta chain, in every plan (orders ENT-012) |
| 4 | `voidborn-first-steps`, `voidborn-first-hunt-nexus`, `-gsc`, `-gsc-0031` | 2, 1, 1, 1 | once, 480 to 970 cr | Pilots that hold or have not flown them |
| 4b | `voidborn-network-expansion` | 20 | 1,500 cr once in about 8 minutes | Pilots with First Steps booked; nothing carried |
| 5 | `fit-ice-harvester` and the four station fits | 1 each, closed | money spent once | Their asks are used up |
| 6 | `fit-ice-harvester-lhs-1140` | 5 at a time, 20 pilots | money spent once, about 570 cr at the 518 cr asks | The one miner still without a harvester |
| 7 | `mine-wolf-1061-vent` | 1 | 5,360 (5 runs) | Only a pilot with a Nitrogen Vent: none fitted now |
| 8 | `mine-achernar-frost-ring-nexus` | 15 (14 miners, 1 hauler of Logistics) | 2,650 (5 runs); about 3,200 on its 4 paying runs | Central Nexus, four jumps: the one deep water-ice bid |
| 9 | `mine-wolf-1061-frozen-drift-nexus` | 5 | 1,640 (4 runs); about 3,400 on its 2 paying runs | Central Nexus, four jumps; field 7,882 water ice |
| 10 | `mine-ruchbah-ice-belt-nexus` | 1, a test | not measured | Central Nexus, four jumps; field 6,832 water ice |
| 11 | `mine-alnair-ice-fields-nexus` | 8 (6 -> 8 at 09:05 UTC) | 1,820 (3 runs); about 2,870 on its paying run | Central Nexus, five jumps; field 47,439 water ice |
| 12 | `mine-ruchbah-ice-belt`, `mine-achernar-frost-ring` | 1 each | their last three runs sold no water ice | The Experiment: they sell methane at 36 and what the water bid regains, from storage too |
| 13 | `mine-cryogenic-reserve` | 1, closed by the loss stop | not measured at Central Nexus | Nexus Prime, 0 jumps; field 727 water ice |
| 14 | `mine-wolf-1061-frozen-drift`, `mine-alnair-ice-fields` | 1 each | 2,070 (10 runs), 840 (9 runs) | Node Alpha: its bid regains about 485 an hour at 31 cr |
| 15 | `census-frontier` | up to 12 | -620 | Reading, when a miner has nothing else |
| 16 | `park` | the rest | 0 | Dock at home and wait |

Why this plan: the bid, not the tool, is the limit now. 39 of 40
miners carry an Ice Harvester I. The water-ice bids near the fields
are gone: The Experiment bid 0 from 07:07 UTC (it held 15,832 at 36 cr
at 04:02 UTC and regains about 10 units an hour: it was an order, not a
pool), Node Alpha 0 at 07:25 UTC (regains about 485 an hour), Synchrony
0 since 04:13 UTC (the tool market; `hive.py refill`). One deep bid
stands: Central Nexus, 28 cr for 732 and 44,128 in all its levels at
07:58 UTC, regaining about 1,250 an hour at its best price. It lies
four to five jumps from Achernar, Wolf 1061, Ruchbah and Alnair; the
plan puts about 29 ships there, about 4,600 units an hour; the
best level read 30 cr for 42,635 at 09:17 UTC, so the depth carries for the four hours to the next turn. The Experiment and
Node Alpha routes keep one ship each to sell what their bids regain.

What would change it: a bid near the fields that regains with depth
(then more ships back there, one jump instead of four); the Central
Nexus depth under about 5,000 units (then fewer ships); `requires.bid`
(owed by the Fleet Admiral) or `requires.stored` (requests.log ENT-117)
for a carry of the 11,123 water ice that lie in miners' storage at The
Experiment, Node Alpha and Synchrony (the tool stock, 08:02 UTC); a
field that empties. Each turn starts with the skill script `stalled.py`
of the mining-chains skill: a mine route whose last three runs sold
nothing.

## 1. Routes That Pay

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
| Titanium Extraction Contract (3,500 cr once) | not flown | 2026-11-16 | 20 titanium ore to be mined at HD 147513 Belt, which held 34 (census 04:40 UTC): one pilot at most; no route file |

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

- `mine-ruchbah-ice-belt-nexus`: Ruchbah sold at Central Nexus, four
  jumps, one ship from 2026-11-16 08:12 UTC.
- A carry of stored water ice to the Central Nexus bid: about 11,100
  units lie in miners' storage where the bids are 0 (The Experiment
  5,103, Node Alpha 4,163, Synchrony 1,857; the tool stock, 08:02 UTC).
  Storage is personal, so a carry route needs a pilot condition on what
  it holds there (requests.log ENT-117) and a withdraw stop in the
  circuit runner (Mining builds it).
- The vent: a second vent route only when a Nitrogen Vent is on offer.
- Deuterium ice: station bids of 188 to 260 cr for 5 or 6 units at Node
  Alpha and Node Beta; the routes sell it from 166 or 180 cr only and
  store the rest.
- Methane ice: 36 cr bids at eight stations, 7,156 units in all (the
  tool fleet, view capacity, 08:18 UTC); the fields hold it at richness
  13 to 16 beside water ice, so it comes with the water, not alone.
- Uranium, thorium and tritium have bids with depth at all six stations;
  no field read in our space or on the frontier holds them.
