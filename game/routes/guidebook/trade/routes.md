# Trade guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: plan.py show; fill.py status trader (20:01 UTC); table books (19:36 to 19:52 UTC).

What the traders fly between two turns: the division's plan file
(`/srv/collective/data/plans/plan-trade.md`, the tool `plan`), as set on
2026-11-21 at 20:00 UTC, the first turn after the pause.

- First, every ship: the once line of 24 routes; for the traders nearly
  all are booked or full (`fill.py status trader`).
- Own routes: `@trade-sell > @trade-craft` for all 40; ahead of them one
  ship each on a test beyond the border (entry `Trade beyond the border`):
  trade-silver-bar-alpha-to-arneb, carry-hydrogen-beta-to-crucible (two
  hydrogen holders, one ship at a time), go-ironlight-trader then
  carry-hydrogen-beta-to-crucible-bulk (the freighter test).
- Then: craft-steel-node-beta, craft-steel-central-nexus,
  craft-steel-synchrony-hub, park.

What it carries: little. After the pause the home bids that paid on
2026-11-17 are gone (null matter and hydrogen 0 at every home station,
soma 2 to 3 units; books of 19:36 to 19:52 UTC), the traders' own iron is
used up (under 100 a pilot) and copper wiring stands far over its max, so
most traders wait docked at no cost and the gate reads HALT.

What opens work: a home bid back (`requires.bid` opens a sell route by
itself), a far bid with depth on a fresh book, a freighter whose load is
worth the road, the Fleet Admiral's word on the trader fallback
(requests.log, 2026-11-21).

### Selling stores where they lie (`sell-<good>-at-<station>`, `carry-<good>-<from>-to-<to>`)
Status: proven. Updated: 2026-11-21. Evidence: the sell and carry route files with their measured figures; sellgen.py of the skill trade-books.

- The starter hull, nothing bought; trains trading. Each ship sells its
  own stores; the routes are open to every division (rule F24).
- Steps: `store: all`, `withdraw` from the pilot's own storage (the
  runner takes only what the bid takes when the same stop sells), `sell`
  at the floor; a carry sells one or two jumps on and stores the rest.
- Gates: `requires.stored` and `requires.bid` (a book read within the
  hour); a route opens again by itself when a docked ship reads the bid
  back.
- Floor: above the cheapest ask of the good in depth elsewhere, set again
  each turn beside `sellgen.py scan` (skill trade-books): soma's deep ask
  fell from 323 to 292 cr overnight and five routes stood closed by their
  own floor (2026-11-17).
- A route whose runs last minutes is judged by credits a run times the
  runs its bid's regain allows (table `stats_refill`), never by its
  per-hour figure.
- A standing sell order (`create_sell_order`, spacemolt_market) costs 1%
  of the listed value at once; one anchor beacon at 1,200 cr stood a day
  unfilled at Node Beta (2026-11-16 to 17).
- Readings: `hive.py route <id>` (sell-null-matter-at-nexus,
  sell-soma-at-node-beta, carry-soma-beta-to-gamma).

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/trade.json; plan.py templates.

The division's kinds of work are templates in
`game/routes/templates/trade.json`, listed in
`game/routes/templates-trade.md`: `@trade-sell` (stored goods into the
bids where they lie; trading), `@trade-craft` (making from own stores;
crafting, refining), `@trade-train-nav` (navigation to 3 for Signal
Fragments). A ship's row names one as `@<name>`; `plan.py template` and
`plan.py use` change them. `@trade-gas` and `@trade-gather` are gone since
2026-11-18: gathering is the miners' work (rule F23). This guidebook keeps
no list of routes that did not pay (rule F22): what a route earns now is
the view `route_earnings`.

### Making goods from own stores
Status: proven. Updated: 2026-11-21. Evidence: craft-steel-own-node-beta, craft-wiring-synchrony-hub, craft-piping-node-beta (route files, runs.jsonl 2026-11-17).

Routes `craft-steel-own-<station>`, `craft-wiring-<station>`,
`craft-piping-<station>`: the starter hull, one hop of fuel, nothing
bought; they train crafting and refining.

- One stop at the workshop; its `craft` list asks one recipe in halving
  sizes (32, 16, 8, 4, 2, 1 runs). An entry the pilot's storage cannot
  fill makes nothing (`have_inputs` False) and the next is tried, so one
  visit makes exactly what the pilot holds. Two crafts in one list chain
  (a smelt, then piping): the runner withdraws only after the last.
- Gate: `requires.stored` the input at that station; a pilot goes again
  only after the ledger read its storage (about 40 minutes).
- Read: 20 steel plates in 1.7 minutes for 0 cr (craft-steel-own-node-beta,
  2026-11-17 23:42 UTC); a smelt about 0.23 ticks, a wiring run 0.26 to
  0.28.
- For sale only when every input and the output have surplus
  (`reservecheck.py`, rule F24): focused crystal made from held-back
  energy crystal was sold once (errors.log ENT-090).
- The pull rule closes a craft whose output stands at its max: copper
  wiring 10,732 of 96 on 2026-11-21 (`fill.py status trader`).
- The calls behind a craft step: lessons.md, `Crafting by Hand: the Calls`.

### Trade beyond the border
Status: test. Updated: 2026-11-21. Evidence: table books 2026-11-21; scripts/map.py route; data/intel/sightings.jsonl; route files of the four tests.

Home bids are thin and come back slowly; the far books hold the depth
(table `books`, 2026-11-21 19:36 to 19:52 UTC): The Obsidian Well, a
player station at Arneb (16 jumps, lawless), bids silver bar 501 x 44,527
and silver ore 101 x 502,177; The Crucible Garrison (Crimson, 18 jumps)
bids hydrogen 37 x 184 and heat sink 193 x 24.

- Tests, one ship each, from 2026-11-21 20:00 UTC:
  trade-silver-bar-alpha-to-arneb (Node Alpha asks 50 at 414),
  carry-hydrogen-beta-to-crucible (41 of our own hydrogen and 24 heat
  sinks bought at Node Beta at 147 in a hold of 65), go-ironlight-trader
  then carry-hydrogen-beta-to-crucible-bulk (a Prayer freighter of 540).
- The road: past Pherkad every system to Arneb or The Crucible is
  lawless; no pirate on our record in any of them
  (`scripts/map.py route`, data/intel/sightings.jsonl). Each test leaves
  home with an empty hold or our own goods, carries price limits at both
  ends, and stores at the far station what its bid left.
- A far book read days ago is a guess, not a price: most foreign books in
  the routemaker's trade candidates date from 2026-11-17; a ship that
  docks reads the book again.
- Each test answers: what the far bid takes and regains, what the road
  costs, whether Node Alpha's silver bar ask comes back.

### Once missions: what they taught
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/onetime.json; the voidborn-* and mission-* route files; errors.log ENT-039, ENT-058, ENT-096.

The `once` routes head every plan's list First; a pilot flies each one
time and a route skips a pilot that booked its reward
(data/fleet/onetime.json; `oncecheck.py`, `boards.py` of the skill
trade-books). What they taught:

- A board mission is accepted at the route's first stop: a route without
  the accept serves only pilots that hold the mission and counts every
  other pilot as done (voidborn-first-steps, 2026-11-16).
- One accept with an empty hold decides whether a delivery hands out its
  goods: Concurrent Approval, Final Calibration and Neural Matrix Delivery
  do; Conductive Lattice, Resonance Substrate and The Crimson Resonance do
  not.
- An acquire-module mission counts a module bought after the accept and
  carried in the hold; one owned before does not.
- A board is one pilot's: Signal Fragments is offered from navigation 3
  (`requires.skills`).
- A chain is sized on its scarcest input and gets a finisher
  (voidborn-resonance-finish, `requires.booked` its first link).
- A mining mission is bounded by one shared field: read its census and
  set `min_left` (voidborn-collective-provides).

What each title paid: its route's note and `hive.py route <id>`.
