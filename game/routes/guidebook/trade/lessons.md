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

### Reading order books
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-016, ENT-028; the skill trade-books (its pitfalls, moved here on queue.log ENT-189).

- A total is not a depth: `buy_quantity` and `sell_quantity` add every
  price level; the units at the best price are `best_buy_qty` and
  `best_sell_qty`. `view_market` at the station lists every level
  (focused crystal "1,466 for 879" was 1 unit, 2026-11-15).
- `best_buy` is the bid, `best_sell` the ask. A copy is not a read:
  `held.py` counts reads by `read_at`.
- A thin ask can vanish between reads (water ice 125, 83, then none in
  14 minutes); after a game update every book is read again (v0.721.1 put
  new bids into every station at once).
- A floor in a file goes stale as the deep ask moves: set it each turn
  beside `sellgen.py scan`.
- A far book read days ago is a guess; the ship that docks reads it again.
- `view_orders` answers for the station where the pilot is docked.
- Tax: 1% rounded down on every buy at our stations; none at Ironlight
  Crossroads; a player station adds its market fee. A rule needs two
  readings that could tell its explanations apart: "no tax on a station's
  ask" came from one 52 cr buy, where rounding explains it too.

### Routes, plans and the clone
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-035, ENT-039, ENT-106; requests.log ENT-148, ENT-216; the skill trade-books.

- A file in the clone is live before it is committed, and the hourly
  measure pass commits a modified route under its own name: draft in
  scratch, then copy, `routes.py check`, `routes.py index` and commit by
  explicit paths in one shell call; never a directory pathspec.
- `fill.py` and `plan.py` refuse while a file under game/routes is
  modified and not committed, another member's too.
- `max_ships` limits ships at one time, not runs: a gap one load closes
  is flown once (a route with `once` and `max_pilots` 1, or by hand).
- No `lift_to` on a route that has not flown: the filler lifts it at once.
- A time in a note is the clock's: `{NOW}` and `stamp.py`.
- A once route without the accept serves only holders; a chain is sized
  on its scarcest input; a mining mission is bounded by its field.
- A ship that waits where the plan says it flies: open its log in
  data/routes/logs the same turn (a crashed runner writes no row).
- Each turn the reserve first: a target met between turns kept 27 traders
  gathering for two hours (errors.log ENT-106).
- Read the plan file's `## ` headings once a turn.

### Money, calls and the runner
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-047, ENT-066, ENT-067, ENT-090, ENT-107; requests.log ENT-176; the skill trade-books.

- `buy` never refuses: it fills as far as the wallet reaches (a trader
  left at 298 cr); `stockbuy.py` cuts the units to keep 3,000 cr.
- `gate.py raw` cuts its answer at 3,000 characters unless `FULL=1`.
- The engine's goals can answer 409 for minutes while raw calls work:
  move a held ship by `jump`, `travel`, `dock`.
- The weekly tax lands in the runs in flight; read them without it.
- An acquire-module mission counts a module bought after the accept.
- A craft is all or nothing: ask it in halving sizes. The runner's
  `sell` takes the best level only.
- Held back is not surplus: `reservecheck.py` decides, not the books.
- A carry needs a load in one pilot's storage: read the per-pilot spread.
- A mine test the filler offers can rest on a bid our stores already fill.
- The watcher rebases unpushed commits: cite a hash only after the push
  (`refs.py`).
- `wallet.py topup --dry-run` before a spend that nears the floor.
- A listed ship is bought docked at its station (`buy_listed_ship`,
  spacemolt_ship); the old ship stays stored there.
