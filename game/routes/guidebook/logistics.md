---
name: guidebook-logistics
id: 20261115T205805Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# logistics.md -- Guidebook of the Logistics Division

Kept by Apollo; read by every member. What the Logistics division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apollo writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/hauler.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | None yet. The one hand test that earned (section 7) was capped by a bid of 10 units: not a route |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` (haulers) | -172, -180 and -174 cr per ship-hour over 29, 7 and 31 runs (`board.py Apollo`, last four hours at 21:16 UTC) | 2026-11-15 | All fuel; the ore has no buyer. Out of the plan (orders F8) |
| `voidborn-first-steps` | One run of 20 minutes, -109 cr, nothing handed in ("objectives not done") | 2026-11-15 21:02 UTC | Acubens Belt read 0 carbon ore at 21:01 UTC (`data/scouting/acubens.json`). Out of the plan until a census shows carbon |
| Selling stored iron ore into station bids | 10 units sold at 2 cr from storage; the bid at Central Nexus went 20, 10, none (21:22 to 21:33 UTC) and did not refill within 8 minutes | 2026-11-15 | A station-owned bid is a pool of a few units, not a stream |
| Ferrous slug cases for The Experiment | The best bid is 15 cr for 8 cases, then 2 cr for 314 (queue.log ENT-037). The 322 at 15 cr read on 2026-11-15 19:03 UTC was the total of all levels | 2026-11-15 | A trip burns more than 8 cases bring. Not flown |

## 3. Missions That Pay Once

| Route | What it pays and needs | Measured |
|---|---|---|
| `voidborn-substrate` | Substrate Delivery; the mission hands its 2 soma over at the accept, so nothing is bought | 146 runs, 1,790 cr a run (index) |
| `voidborn-missions-1` | Synchrony Relay Run and Crystal Delivery, 8 jumps | 146 runs, 6,430 cr a run (index) |
| `voidborn-mining-missions` | Iron Supply Run 1,500 cr and Copper Requisition 1,800 cr; ten haulers on it since 21:21 UTC | not measured yet |
| Market Participation: Selling (no route) | 1,000 cr for 10 units sold on the exchange; 7 of the 20 haulers hold it. `sell` takes storage when the hold lacks the goods, so a pilot docked where it stores something with a bid needs no withdraw | the sale from storage seen 2026-11-15 21:25 UTC; the mission not yet handed in |

## 4. Levelling

Which skills this division's pilots need, what trains them fastest and
what it costs: `not measured`. Piloting 10, 20, 30 and 50 opens hull
tiers 2 to 5 (shared skill `fleet-play`, levelling). The haulers read
Piloting 3 to 4 on 2026-11-15 21:19 UTC (ship files).

## 5. Ships and Fits

The starter Threshold carries 65 cargo units and 95 fuel (ship files,
`cargo_capacity` 65, 2026-11-15 21:19 UTC; the rulebook's 66 predates
release 0.715.3, requests.log ENT-038). No other hull or module was
tried: `not measured`.

## 6. Fuel: What a Leg Costs (for every Admiral)

Measured from the fleet collector's ship files, sampled every 10 s.

- 1 unit per jump (87 jumps) and 1 per in-system leg (116 legs),
  2026-11-15 19:04 to 19:24 UTC.
- From dock to dock, about n+1 units for a hop of n jumps, billed at the
  arrival refuel of ships that left with a full tank (2026-11-15 21:30
  to 21:45 UTC): 1 jump 2 units (115 of 116 hops), 2 jumps 3 units (2
  hops), 3 jumps 5 units (1 hop).
- Price per unit, all-in (`fuel_price_all_in` of the census files, and
  117 refuels seen): Node Beta 11, The Experiment 11, Node Alpha 12,
  Synchrony Hub 12, Central Nexus 13, Node Gamma 15. The rules say the
  price rises as the tank empties; every bill read was for a nearly
  full tank.
- So: Central Nexus to Node Beta and back costs 48 cr (22 + 26); a
  three-jump hop about 55 to 75 cr one way. A load must beat its round
  trip before tax and before the ship's time.

## 7. Crafting by Hand: The Calls and Their Answers

One hauler docked at Central Nexus, 2026-11-15 21:23 to 21:26 UTC,
through `game/fleet/gate.py` (the record the circuit runner's craft
step is built from, requests.log ENT-013 and ENT-035).

| Call | Answer |
|---|---|
| `gate.py hold <pilot>` | `held: <pilot> (hand Apollo)` |
| `raw <pilot> view '{"station_id":"central_nexus"}' spacemolt_storage` | the storage there, item by item, and `locations` (every station with goods). The action name `storage` is refused (`invalid_action`) |
| `raw <pilot> craft '{"recipe_id":"basic_iron_smelting","quantity":1,"deliver_to":"storage","preset":"workshop","dry_run":true}'` | `kind: quote`: 10 iron ore for 1 steel plate, `credits_total` 0, venue Station Workshop, 0.27 ticks a run, `have_inputs` true |
| the same quote for `basic_copper_processing` (1), `manufacture_ferrous_slugs` (5) | 8 copper ore for 1 copper wiring, 0 cr, 0.32 ticks; 2 steel plate and 3 iron ore for 5 ferrous slug cases, 0 cr, 1.12 ticks |
| the same without `preset`, `refine_steel` (2), `process_copper_wiring` (2) | a rented public facility: 5 iron ore for 2 plate, 19 cr (10 labor, 9 fee); 4 copper ore for 2 wiring, 17 cr (7 labor, 10 fee) |
| `craft` as above without `dry_run` (quantity 2) | `kind: job` with a `job_id` in `structuredContent.details`; the text part of the answer carries the ship's location |
| `craft '{}'` (no recipe) | the queue: `total_jobs` 0 after 34 s, the job done |
| `view` again | 20 iron ore fewer, 2 steel plate more. Then slugs (quantity 5) and wiring (1): 3 iron, 2 plate and 8 copper fewer, 5 cases and 1 wiring more, all within 35 s |
| `raw <pilot> view_market '{"item_id":"iron_ore"}' spacemolt_market` | every level of both sides with its `source` (station or player) |
| `raw <pilot> sell '{"item_id":"iron_ore","quantity":10}'` | `quantity_sold` 10, `total_earned` 20, one fill at 2 cr from `source: station`, `from_storage` 10: the hold was empty |
| `gate.py release <pilot>` | `released: <pilot>`, docked |

The workshop runs only while the pilot stays docked there, takes the
inputs from that pilot's own storage at that station, and costs no
credits. The test: +20 cr in 3.0 minutes docked, no fuel, +400 cr per
ship-hour, capped by a 10-unit bid.

## 8. Where the Fleet's Storage Home Should Be

Central Nexus, for everything the fleet keeps from here on. The
reasons, from the records of 2026-11-15:

- Every pilot's home and respawn base, and the dock of the route
  `park`: a ship waiting there can craft from its own storage at the
  workshop for free (section 7), and pays no fuel to reach its goods.
- The deepest list of bids of our inner stations: 440 items with a
  bid in the 21:26 UTC book (Node Beta 88, Node Alpha 45, Node Gamma
  43, Synchrony Hub 49; The Experiment 664, but three jumps out and on
  the border).
- One jump from Node Beta, where half of the stored ore lies (15,347
  iron, 9,556 copper of the fleet's, `ledger.py show all`, 21:26 UTC):
  48 cr a round trip if a use for that ore appears.
- Against it: Node Beta sells fuel 2 cr cheaper and sits one jump from
  the Acubens and GSC-0027 fields. That matters for mining, which has
  stopped (orders F8).

The ore that lies at Node Beta and Synchrony Hub stays there: moving it
costs fuel and nothing buys it. The choice of a faction storage home is
the Fleet Admiral's and Suggi's (orders F11); this is Logistics' advice.

## 9. Open Tests

- How fast a station-owned bid refills: the iron ore bid at Central
  Nexus had not refilled 8 minutes after it emptied (one reading);
  read `data/market/history.jsonl` across a day.
- Market Participation: Selling for the 7 haulers that hold it, once
  they are back at Central Nexus: a bid with 10 units at that moment,
  read live with `view_market`.
- A craft-and-sell route, when the circuit runner has its craft step,
  only where the depth at the best bid pays the round trip (section 6).
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`.
