# Trade guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-24. Evidence: migrated from guidebook/trade.md, the text above its first section.

Kept by Mercury at the end of every turn, read by every member: what
Trade learned about its routes, levelling and ships. A figure comes
from `routes.py measure` or a RESULT line, with its date; a number no
record holds is `not measured`. The plan in force is
`/srv/collective/data/plans/plan-trade.md`.

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
  one call; gathered iron cost about 1.0 cr a unit (fleet view=supply).
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
Status: proven. Updated: 2026-11-24. Evidence: errors.log ENT-035, ENT-039, ENT-106; requests.log ENT-148, ENT-216, ENT-457; sell-loot-at-krynn; fill.commit's route gate 07:38 UTC; the skill trade-books.

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
- `routes.py index` by hand defers the plan's repository copy 15
  minutes (index debounce): fill.py reads that copy, the dispatcher
  flies by assign.json at once; a route just put into First or Then
  is missing to `fill.py check` until the five-minute job writes it.
- A mission board file (data/missions) is one pilot's: before a once
  route is written from it, read `get_missions` of one pilot of the
  route's empire (Scouting the Lanes: 4 of 4 runs not offered).
- A request answered by a route: first `git log --since=<request> --
  game/routes` for a route the asker wrote meanwhile, then admirals.log
  (a Recursion parts route duplicated one written 18 minutes before).
- Within one stop the runner stores before it sells: a sale and a
  `store: all` go in two stops at the same base.

### Money, calls and the runner
Status: proven. Updated: 2026-11-22. Evidence: errors.log ENT-047, ENT-066, ENT-067, ENT-090, ENT-107; requests.log ENT-176; the skill trade-books.

- A circuit `buy` whose qty x max_price would take the wallet under
  3,000 cr buys nothing (2026-11-22): size qty to the poorest pilot.
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

### A fallback is flown from where the ship stands
Status: proven. Updated: 2026-11-22. Evidence: data/fleet/orders 03:51 UTC; dispatch.why_not on carry-liner-first-step-to-ramens (best bid 1060 x 1, book of 03:46 UTC).

The dispatcher gives a ship the first open route of its row wherever
the ship stands. A trader docked 18 jumps out, whose local carry closed
on a bid sold out, took the home training loop and flew home with an
empty hold through the lawless west. A far ship's row holds local work
first and a local fallback (a carry or a loop of the stations where it
lies), so no ship crosses a lawless road for training alone.

### Station Need missions pay above the bid
Status: proven. Updated: 2026-11-24. Evidence: need-ember-gland-krynn by hand 2026-11-23; boards and books 2026-11-24 06:50 to 07:23 UTC (data/missions, table books); mission-workshop-production-run-krynn and mission-market-participation-nova-terra first runs, 07:23 and 07:26 UTC.

Stations post `Station Need: <good>` missions, copies of 1 to 20
units, each its own id (`creature_<base>_<good>~<hash>`, no
template), above the standing bid: 8,112 cr a gland at the War
Citadel against 7,054; 5,536 to 5,636 a gland at The Crucible against
480 there; 4,160 a crystal melt at Frontier Station against 54 at
home. Scan every board's deliver objectives against our holdings
(`data/missions/*.json` x table holdings) before a sell route. The
runner accepts by title the first copy posted and `needs` only checks
the hold: one accept-and-redock pair per copy, largest copy first,
goods aboard equal to the copies' sum. Boards differ by birth: Krynn's
Workshop Production Run paid a Nebula-born trader; Nova Terra's
Market Participation and Node Beta's workshop are offered to their
own empire only: one ship first. A reservecheck FLAG holds a good back.

### A docked craft's cost is its craft runs per hour
Status: test. Updated: 2026-11-24. Evidence: hive.py briefing 01:01 UTC (craft-sell-neon-krynn -1,089, craft-sell-oxygen-krynn -2,760 cr a ship-hour); route logs of bursar-desk-krynn and bursar-desk-alpha 01:16 to 01:18 UTC; pull.json; contracts.log ENT-006.

A docked craft costs its inputs and nothing else, so its cost per
ship-hour is the crafts it runs in an hour: three buy-and-craft stops in
8 minutes cost over 1,000 cr a ship-hour. One craft stop and a desk
watch (`watch_minutes`, 0 fuel) set the cost: 60 neon at 1 cr and a
15-minute watch is about 65 cr a run of 18 minutes. A craft whose output
stands in the pull record (`pull.json` items: liquid nitrogen, purified
argon) is closed at its max; craft one outside it (ionized neon, liquid
oxygen). The same stop lists the pilot's own surplus (`sell_order`)
under the station's ask: no `undercut_pct` where many of our ships list
one good, or they undercut each other to the floor.
