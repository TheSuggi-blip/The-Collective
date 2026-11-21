# Logistics guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-21. Evidence: started by the Fleet Admiral 2026-11-15; rules F14 (Suggi, 2026-11-18) and F22.

Kept by Apollo, read by every member, so a ship born later starts where the others stand. Small capped entries (`scripts/guide.py check logistics`). A figure is named by the call that prints it (`hive.py route <id>`, the tool fleet view=levels) or carries its date; one no record holds is `not measured`.

### Fuel: What a Leg Costs (for every Admiral)
Status: proven. Updated: 2026-11-21. Evidence: ship files sampled every 10 s, 2026-11-15 19:04 to 21:45 UTC (87 jumps, 116 legs, 117 refuels); census files `fuel_price_all_in`.

- 1 unit a jump and 1 an in-system leg; dock to dock about n+1 units for a hop of n jumps (1 jump 2 units in 115 of 116 hops).
- All-in, cr a unit (2026-11-15, near-full tanks; it rises as the tank empties): Node Beta and The Experiment 11, Node Alpha and Synchrony Hub 12, Central Nexus 13, Node Gamma 15. Now: the census files.
- So Central Nexus to Node Beta and back costs about 48 cr: a load must beat its round trip before tax and the ship's time. A mine route burnt 144 to 204 cr a ship-hour.

### Storage and goods calls
Status: proven. Updated: 2026-11-21. Evidence: gate.py raw calls 2026-11-15 to 17; queue.log ENT-088; requests.log ENT-089, ENT-282.

- Storage is personal: only the pilot that stores a good crafts from it or carries it. Give it by `deposit` (spacemolt_storage), `target` the other pilot, `source` `cargo` or `storage`, docked there: the wall lets it pass between our pilots.
- `withdraw {item_id, quantity, target: self}`: storage to hold (`cargo` refused). `deposit ... target self, source cargo`: hold to storage. Read: `view {station_id}` (`storage` refused).
- `sell` takes cargo first, then storage; a route's `sell` stop sells only the hold, so it withdraws first.
- Count holds in space by `size` (plasma gas 2, a module 10), never in units.
- Holds: `cargo` of the ship files, not `stock` or `ledger.py show` (they printed nothing over 22 loaded holds, ENT-089). Over 5 units left aboard close `requires.empty_hold`: deposit them.
- Faction storage is in the storage book as member `Faction`, bunker fuel left out (ENT-282).

### Holding pilots and drivers
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-100; driver logs 2026-11-15 21:21 to 2026-11-17 21:10 UTC.

- Hold a ship (`gate.py hold`) before a hand test: the dispatcher takes a free one in seconds.
- A script that drives a pilot for minutes refreshes my hold before every call and stops when the order file names another hand or a runner: an order file 20 minutes old is dead to the dispatcher (the bunker filler lost at minute 31, ENT-100).
- A runner I kill leaves its pilot unheld: `gate.py hold` it at once.
- A batch that takes and releases pilots skips every pilot with an order file, my mark included.
- Stop a driver by PID (`kill -9`), never `pkill -f` (it kills the tool's shell); SIGTERM runs `finally` and frees the pilot.
- catch.py: `<base>` is where the row ends docked (with `--goto`, the goto's base); `--goto` waits up to 400 s for the goal: read the ship file, not the log; a row started during an earlier run catches that run's end.
- A driver that outlives the turn: `persist_on_release`; logs by absolute path in the scratch folder (one in the clone held every push).

### Engine goals and loops
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-098, ENT-109; ship files 2026-11-16 03:03 UTC; catch.py logs 2026-11-17 00:10 to 04:01 UTC; commit 0f7a36a.

- Goal options differ: `navigate-to-system` takes `targetSystemId`, `go-to-poi` `targetPoiId`, `prepare-at-station` `systemId`, `poiId`, `baseId`, `refuel`. Copy a flight from found.py.
- A raw call's `action` is a sub-action of the help's Actions (`types`, `faction_build`), never its `## facility` heading (500). Fly every call of a driver once on a free docked pilot first (rule F29).
- `prepare-at-station` can end undocked: read `docked`, send `dock`.
- The mining loop runs on after its order ends, and after a host stop file: goals answer 409 "A loop is running". catch.py deletes it after a minute (`gate.call("delete", "/accounts/<pilot>/loop")`, then `running: false`).
- `gate.py raw` cuts long answers: `gate.call` from Python, JSON `strict=False`.
- A hand circuit's `hunt` step answering `busy`: `hunt.py` by hand, then `route_run.py --from <hand-in stop>`.

### Bids, books and the storage book
Status: proven. Updated: 2026-11-21. Evidence: books 2026-11-15 (queue.log ENT-050); runs 2026-11-16 to 17; errors.log ENT-069; capacity readings 2026-11-16 to 17 (requests.log ENT-115).

- Depth is `best_buy_qty`; `buy_quantity` sums every level. Read `view_market` there before a haul or a sale.
- A station bid is a pool that drains and refills on its own clock (soma 1 to 3 in about 40 min, iron 2,375 in about 2 h): `ledger.py prices <item>` before writing a good off; never fly to a few-unit bid read minutes ago.
- `requires.bid` opens on a book up to an hour old: one ship, a lost hop now and then.
- `requires.stored` reads the storage book (each pilot about every 40 min): goods just made do not open it, goods just used still do. Size craft runs well under `min`.
- Each figure carries its own book's `read_at` (ENT-050).
- Re-read the claims (`comms.py admirals`) right before a claim or a buy at an ask (ENT-069).
- The bids, not the haulers, bound the hauling (stock view=reserve, fleet view=capacity).

### Crafting and recipes
Status: proven. Updated: 2026-11-21. Evidence: craft quotes and jobs 2026-11-15 to 17; queue.log ENT-083, ENT-114, ENT-128; commit 30a7961; the harvester chain 2026-11-16 (orders.log ENT-011).

- The Station Workshop (preset `workshop`): 0 cr, no skill asked, from the pilot's own storage there, only while it stays docked; `dry_run` quotes inputs, fee, venue, time.
- `quantity` counts made units rounded up to runs (27 liquid hydrogen = 9 runs): ask runs x per_run.
- `refine_steel` (5 iron, 2 plate) and `process_copper_wiring` are facility-only: a `craft` entry with `venue: "facility"`, `max_fee`; 29 cr a run at Node Beta (2026-11-17).
- Made by hand: basic_iron_smelting, basic_copper_processing, carbon_arc_circuit_etching, fabricate_gold_circuit_boards, build_power_cell, build_ice_harvester_i, compress_hydrogen_gas, carapace_plating, draw_copper_piping.
- An Ice Harvester I by hand pays only from our own silicon and crystal: about 680 cr against 3,130 bought input by input, 1,413 bought whole.
- Work the sum before a rule: a 24 cr hop carried 666 to 2,280 cr of armor plate (ENT-083).

### Plans, fill and the dispatcher
Status: proven. Updated: 2026-11-21. Evidence: plan.py and fill.py, 2026-11-16 to 18; requests.log ENT-279, ENT-281; rule F8.

- The dispatcher takes First, own routes, Then: bid-gated routes stand at the head of a ship's own routes.
- The fill gate halts while any ship waits; `fill write` adds what fill names, not what the orders allow: read `fill.py status <role>` first.
- The filler may lend another division's test into a ship's head: read the builder's row each turn.
- Change the plan only by plan.py (Planned and Notes: `planned`, `note`, ENT-279); a set does not apply while another member's untracked route file sits in the clone: `plan.py show --brief` after.
- A buying route loops while open: aim it at a level by `once` and `max_pilots`, or `requires.reserve` (ENT-281); fill never adds one.
- `max_price` counts the 1% tax: write the allocation x 1.01 (a kit refused, 2026-11-17).
- A `comms.py append` file carries the turn's time in its name, appended only after the write answered `verified` (errors.log ENT-101). Logs name places by data file, never per-pilot cargo.

### What the Ice Routes Leave Behind
Status: retired. Updated: 2026-11-21. Evidence: books of 2026-11-15; rule F23.

Haulers no longer gather: ice is Mining's alone (rule F23).

### The Harvester Chain: an Ice Harvester I Made by Hand
Status: retired. Updated: 2026-11-21. Evidence: orders.log ENT-011; rule F23.

Haulers no longer gather (rule F23); its lesson: crafting-and-recipes.

### Capacity of the Domain (orders F18)
Status: retired. Updated: 2026-11-21. Evidence: readings 2026-11-16 to 17.

Dated readings the tools print; its lesson: bids-books-and-the-storage-book.
