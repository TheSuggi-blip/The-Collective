# Trade guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/trade.md, the text above its first section.

Kept by Mercury; read by every member. What the Trade division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Mercury writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is the division's plan file
  (`/srv/collective/data/plans/plan-trade.md`); every route with its
  figure is in `game/routes/master-index.md` and its sub-indexes.

### Crafting by Hand: the Calls
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/trade.md section 6.

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

The circuit runner's `craft` stop, flown 2026-11-16 18:37 to 18:46 UTC
by one trader on a scratch route (assemble_control_node at The Experiment,
requests.log ENT-161): the four inputs bought there (2 circuit boards at
365, 4 copper wiring at 19, gold wiring 190, silver wiring 136: 1,141 cr
with the tax), the quote 0 cr and 12 ticks a run, one run queued, 2
control nodes in storage about two minutes later, taken into the hold and
stored again at the next stop. RESULT: 2/2 stops in 8 minutes, -1,196 cr
with the fuel; the nodes are kept for the station list (its foundry takes
1,500), since the best home bid stood at 40 cr (Node Gamma) against 1,013
asked at Ironlight Crossroads. The game's `craft` help says `quantity` is
the number of output items, rounded up to whole runs; the runner passes
the runs still wanted as that quantity and asks again after each job, so
it reaches `runs` x `per_run` in more jobs than one (`runs` 8, `per_run`
2: jobs of 4, 2, 1 and 1 runs, read from game/fleet/route_run.py, not
flown). With `runs` 1 it made 2 in one job, as the recipe does.

### Station Inputs Bought (plan step P4)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section 8.

Bought for storage, never for sale; a stock purchase is booked as money
paid once (data/fleet/onetime.json), not as a running cost.

| Input | Bought | Price and depth read | Against mining it | Date |
|---|---|---|---|---|
| Iron ore | 24,442 units into storage at Central Nexus for 24,686 cr with the 1% tax (one unit first, then the rest), 0.99 units per credit; `buy` with `deliver_to: storage` takes a whole ask in one call, no hold and no loop | 1 cr for 24,442 (estimate_purchase, 18:45 UTC): 6,481 from an account named as the market bot of Nexus Prime and 17,961 from ten players; 676 more at Node Gamma; the ask had read 35,923 at 14:49 UTC | The four standing gather routes bring 190 to 295 units of mixed iron and copper a ship-hour at 0.58 to 0.94 cr a unit (runs since 14:00 UTC); with half of it copper, an iron unit gathered costs about 1.2 to 1.9 cr | 2026-11-16 |
| Carbon ore | 1 unit into storage at Node Beta for 4 cr (tax 0 by rounding); no load bought | 4 cr at Node Beta (146,485), Node Gamma (100,595) and Node Alpha (83,648), books of 18:16 to 18:26 UTC; 1,000 units quoted at 4,040 cr with the tax | No home field holds carbon in depth (Gliese 876 Belt 2,901 left, Furud Belt 612); its use is circuit boards (12 carbon and 2 silicon ore make 3), and silicon ore is the limit (34 held, asks of 1 to 4 units) | 2026-11-16 |
| Silicon ore | 75 units at Central Nexus for 31,814 cr with the 1% tax (one unit first), deposited into the storage there of the hauler that crafts the circuit boards, which then read 107 silicon ore | 420 cr; 84 found at that price by `estimate_purchase` (2026-11-16 23:58 UTC); the ask had read 425 at 23:33 UTC; other asks 312 x 1 (Node Alpha), 376 x 4 (Synchrony), 561 x 200 (Ironlight Crossroads) | No field of the 63 systems read holds silicon (Intel, admirals.log ENT-003). Two silicon and 12 carbon make 3 boards by hand: a board costs about 283 cr of silicon and 16 cr of carbon, against 365 to 743 cr asked for boards (books of 23:04 to 23:33 UTC) | 2026-11-16 |
| Steel plate (not bought) | -- | 18 cr at five of our stations: Node Alpha 210,080, Node Beta 82,191, The Experiment 78,089, Node Gamma 71,787, Central Nexus 12,503 (books of 18:16 to 18:26 UTC) | One plate takes 10 iron ore by hand (basic_iron_smelting): 10 cr of bought iron, or 12 to 19 cr of gathered iron, plus the labour; the station list's 491,400 iron ore are its 49,140 steel plates | 2026-11-16 |
