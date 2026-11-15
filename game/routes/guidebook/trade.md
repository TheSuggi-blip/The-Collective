---
name: guidebook-trade
id: 20261115T205804Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# trade.md -- Guidebook of the Trade Division

Kept by Mercury; read by every member. What the Trade division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Mercury writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/trader.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | None that repeats yet. The one-time missions of section 3 pay once per pilot |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| Buying at one of our six stations, selling at another | Six distinct read sets of every book, 19:03 to 21:25 UTC; with the depth at the best price (`best_buy_qty`, `best_sell_qty`), the best gap that held in all six is 134 cr per hold before fuel, 1 unit deep | 2026-11-15 | Fuel for a round trip is about 40 to 100 cr. No trade route between our stations. Read again from `data/market/history.jsonl` each turn |
| Control nodes made by hand (`assemble_control_node`: 2 circuit boards, 4 copper wiring, 1 gold wiring, 1 silver wiring make 2 nodes) | One craft by hand: inputs 1,309 cr at Central Nexus, craft 12 ticks at the Station Workshop at no cost, 2 nodes sold into the station bid of 864 cr at Node Gamma (191 units at that price): +371 cr after 48 cr of fuel in 12.6 minutes, about +1,770 cr per ship-hour | 2026-11-15 | Paid once. The silver wiring at 185 cr was the only unit on offer there; the next silver costs 472 cr (Node Alpha), which leaves about +128 cr a craft before fuel, and about 21 gold wiring are on offer at our stations. Not a route until the inputs come cheaper. Ironlight Crossroads (LHS 1140) asked 248 cr for 300 silver wiring (23:21 UTC) |
| `trade-voidborn-neural-soma-central-the` (route maker: soma bought at Central Nexus, sold at The Experiment) | Two runs, 23:27 and 23:35 UTC: 3 soma bought each time (3 x 258 cr paid 781 cr); the first sold 1 into a bid of 657 cr (the book of 22:58 UTC had read 690 cr for 2), the second found no bid: -168 and -851 cr, 5 soma kept in two holds | 2026-11-15 | Out of the plan. The soma bids of 646 to 690 cr at our stations are 1 or 2 units that come and go (ledger history, 21:35 to 23:16 UTC). The second run happened because the dispatcher gave the route to the next free trader the moment the first ended: `max_ships` 1 limits ships at once, not runs. A one-load gap is flown once by hand |
| `trade-ceramite-plating-the-central` (route maker: bought at The Experiment, sold at Central Nexus) | One run, 23:27 to 23:38 UTC: 5 bought at a player's ask of 899 cr (4,539 cr paid), 4 sold into the bid of 1,185 cr (+4,740 cr), the fifth sold by hand into the next level, the station's own unit at 1,129 cr: +1,234 cr cash for the 5 units, fuel included | 2026-11-15 | Out of the plan. The station bids one unit at a time and raises its price while the unit stands (1,067 to 1,185 cr from 21:18 to 23:11 UTC); after the sale one unit at 1,129 cr was left (view_market 23:41 UTC). A trade of a few units when the bid has climbed again: read `ledger.py prices ceramite_plating` first. Ironlight asks 961 cr for 260 |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | RESULT: 3/3 stops in 8 min, +2,952 cr (48 cr fuel) | 2026-11-15 | The accept puts the 2 neural soma into the hold: nothing is bought. Once per pilot: the mission left the board after the hand-in |
| Market Participation: Selling (`voidborn-selling`; the trader pilots have it done) | 1,000 cr | Command group RESULT lines: +865 cr each after the ten units bought and sold | 2026-11-15 | Ten units sold into any bid. The route buys liquid nitrogen at The Experiment |
| `voidborn-precedence` (Precedence) | 4,000 cr and 1 neural soma | 14 traders, 23:35 to 23:58 UTC: +54,483 cr after 1,517 cr of fuel, about 15 minutes each (runs.jsonl) | 2026-11-15 | Three docks at our own stations, nothing bought. In the plan since its first RESULT line (command group, 23:20 UTC) |
| `voidborn-conductive-lattice` (Conductive Lattice, Node Beta) | 5,500 cr and 45 trading XP | One hand run, 23:33 to 23:55 UTC: the accept hands out nothing; 20 silver ore bought at Ironlight Crossroads (LHS 1140) for 3,040 cr; delivered at the Node Beta redock: RESULT 3/3 stops in 21 min, +2,312 cr after the silver and 148 cr of fuel | 2026-11-15 | Six jumps each way through Pherkad, GSC-0041 and Antares, hold empty on the way out (orders F13); hull 75 of 75 throughout. No silver ore is on offer in our six books. `max_pilots` 9: 180 units stood at 152 cr after our buy, more levels not seen. Once per pilot: after the hand-in the board offered the next mission of the same giver instead |
| Resonance Substrate (Node Beta, after Conductive Lattice) | 7,000 cr, 30 trading XP | Hand test under way: the accept hands out nothing; 15 energy crystal asked at Central Nexus by a player at 420 cr (641 units, view_market 23:56 UTC), about 6,363 cr with the tax | 2026-11-15 | About +590 cr after crystals and fuel if bought; Mining's own crystals would make it +7,000 |

## 4. Levelling

Which skills this division's pilots need, what trains them fastest and
what it costs: `not measured`. At 2026-11-15 23:25 UTC every one of the
20 traders stood at trading 1, piloting 3 or 4, mining 2 to 4 and
navigation 2 (data/fleet/ships/). Trading XP comes with the delivery
missions of Node Beta (Conductive Lattice 45, Resonance Substrate 30)
and from market sales; how much a sale gives is not measured. Piloting 10, 20, 30 and 50 opens hull
tiers 2 to 5 (shared skill `fleet-play`, levelling). A hand craft is
labour at the Station Workshop: its speed scales with the crafting
skill, and it runs only while the pilot stays docked there (the game's
`craft` help, 2026-11-15).

## 5. Ships and Fits

The hull and the modules for this division's work beyond the starter,
what they cost and what they changed in a run: `not measured`.

## 6. Crafting by Hand: the Calls

Flown 2026-11-15, 21:21 to 21:34 UTC, through `game/fleet/gate.py`;
each answer read. A route's craft step is built from this
(requests.log ENT-030).

| Step | Call (tool group) | Answer |
|---|---|---|
| Quote the buy | `estimate_purchase {item_id, quantity}` (spacemolt_market) | Price per fill and the tax. At our stations every buy paid 1%, rounded down, from a player's ask and from the station's own: soma 3 x 258 cr paid 781 (station's ask, Central Nexus 23:27 UTC), ceramite 5 x 899 paid 4,539 (a player's, The Experiment 23:31 UTC), an ice harvester 1,413 paid 1,427 (Mining guidebook, section 5). A 52 cr buy paid 0: 1% of 52 rounds to 0. At Ironlight Crossroads (LHS 1140) 20 silver x 152 paid 3,040, no tax |
| Quote the craft | `craft {recipe_id, quantity, deliver_to: storage, preset: workshop, dry_run: true}` | Runs, venue Station Workshop, `have_inputs`, `effective_time_per_run` 12 ticks, no credit cost |
| Buy | `buy {item_id, quantity}` | One item per tick; goods into the hold |
| Inputs to storage | `deposit {item_id, quantity, target: self, source: cargo}` (spacemolt_storage) | A craft takes its inputs from station storage, not the hold |
| Craft | `craft {recipe_id, quantity, deliver_to: storage, preset: workshop}` | `quantity` counts output items; the job is queued and the inputs escrowed |
| Progress | `craft {}` | The queue with `progress`, `eta_ticks`; an empty queue when done |
| Output to the hold | `withdraw {item_id, quantity}` (spacemolt_storage) | `source: storage, target: self` is refused (`invalid_source`); without them it works |
| Sell | `view_market` first (every price level, each with its `source`: station or player), then `sell {item_id, quantity}` in the default tool group | `sell` takes the best bids level by level: sell no more than the units at the price wanted. `sell` under spacemolt_market is refused (`invalid_action`, 23:41 UTC) |

## 7. Open Tests

- Ironlight Crossroads (LHS 1140, 6 jumps, lawless; a player station,
  public access, refuel 7 cr a unit): its book of 2026-11-15 23:21 UTC
  (`data/market/784309214f105860a16a0c100a70eb14.json`) sells the ores of
  Solarian space that our books lack, 200 units each at the best price:
  silver 152 cr, vanadium 120, titanium 500, silicon 561, deuterium ice
  491; deep hydrogen gas at 6 cr, plasma gas 52, nitrogen ice 12, iron 4
  and copper 6. It bids for uranium ore (300 cr, 441 units), thorium ore
  (240, 386), tritium ice (400, 973) and creature goods (ember gland 480,
  verdigris curd 330, superfluid vial 600, 23 to 50 units). Against our
  six books the gaps by the depth at the best price are one load or less:
  hydrogen gas 6 cr to a Node Beta bid of 25 cr for 104 units that comes
  and goes, ceramite plating 961 cr to the station bid of a few units at
  Central Nexus. Its use for us is a mission's goods, not a gap.
- Hive Antares: its book is not in the data folder yet.
- Gaps between our stations in `data/market/history.jsonl` over a day of
  reads, by the depth at the best price.
- Resonance Substrate and what Node Beta offers after it.
