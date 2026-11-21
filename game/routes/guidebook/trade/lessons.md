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
Status: proven. Updated: 2026-11-21. Evidence: the hand calls of 2026-11-15 21:21 to 21:34 UTC and 2026-11-16 18:37 UTC (requests.log ENT-030, ENT-161).

Flown 2026-11-15 and 2026-11-16 through `game/fleet/gate.py`, each
answer read; a route's craft step is built from it (route_run.py).

| Step | Call (tool group) | Answer |
|---|---|---|
| Quote a buy | `estimate_purchase {item_id, quantity}` (spacemolt_market) | price per fill and the 1% tax, rounded down (none at Ironlight Crossroads) |
| Quote a craft | `craft {recipe_id, quantity, deliver_to: storage, preset: workshop, dry_run: true}` | runs, venue, `have_inputs`, time per run |
| Inputs to storage | `deposit {item_id, quantity, target: self, source: cargo}` (spacemolt_storage) | a craft takes its inputs from station storage |
| Craft | `craft {..., deliver_to: storage, preset: workshop}` | `quantity` counts output items, rounded up to whole runs |
| Output to the hold | `withdraw {item_id, quantity}` (spacemolt_storage) | with `source: storage, target: self` it is refused |
| Sell | `view_market` first, then `sell {item_id, quantity}` (main group) | takes the bids level by level |

The runner's craft stop made 2 control nodes from four bought inputs in
about two minutes (assemble_control_node at The Experiment, 2026-11-16
18:37 UTC, -1,196 cr with the fuel).

### Station Inputs Bought (plan step P4)
Status: proven. Updated: 2026-11-21. Evidence: the buys of 2026-11-16 (onetime bookings); the tool fleet view=supply 2026-11-21 19:42 UTC.

Bought for storage, never for sale, through `stockbuy.py` (skill
trade-books): `estimate_purchase` one unit first, then `buy` with
`deliver_to: storage` sized to the smallest of the units asked, the units
at the price and the wallet less 3,000 cr (rule F7); `buy` fills as far
as the wallet reaches without refusing (errors.log ENT-067). `deposit`
with another pilot as `target` moves goods into that pilot's storage at
the same station. Booked as money paid once (`gate.book_onetime`).

- Iron ore, 2026-11-16: 24,442 units at Central Nexus for 24,686 cr in
  one call; gathered iron cost about 1.0 cr a unit over 6,229 runs (the
  tool fleet, view=supply, 2026-11-21).
- Silicon ore, 2026-11-16: 75 units at 420 cr for the board crafter.
- Not bought: carbon ore at 4 cr in depth (it pairs 12 to 2 with silicon
  for boards, and silicon is the limit); steel plate at 18 cr in depth at
  Node Alpha (gathered iron makes a plate for about 10 cr).
- The view `fleet`, view=supply, prints per reserve good the gathered cost
  against the best ask: read it before any stock buy.
