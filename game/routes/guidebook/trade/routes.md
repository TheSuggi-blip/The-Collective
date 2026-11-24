# Trade guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-24. Evidence: plan.py show and check; fill.py check trader 10:58 UTC; view_orders of 85 traders 10:37 UTC; bursar_claims.json; data/missions 10:43 UTC; errors.log Mercury 2026-11-24 (bursar buy lane).

The plan file as set on 2026-11-24 at 11:00 UTC (orders ENT-086,
block MERCURY):

- First, every ship: the once line of every board; the Station Needs
  (`need-melt-frontier`, `need-melt-crucible`, `need-ember-gland-*`),
  each gated by `requires.stored` and `requires.posted` (the board read
  by a docked ship of ours within 30 minutes holds the title), then the
  far bids for stored loot.
- Own rows: the join corridors, the capitals' lines, `@trade-sell >
  @trade-craft`.
- Then, gated to where each ship stands: starters stripped once, the
  five Bursar desks, `bursar-network` (the engine, one trader a policed
  Exchange station: 33 stations less the five desks carry 28), steel
  from own iron, `train-jumps-trader` (Piloting to 10 for the tier-2
  hull), park.

The engine's policy (`game/bursar-policy.json`, Trade's): buy lane off
(a buy that only stores is Logistics', orders P5), policed stations
only, the nearest station first. Its books and boards are what opens
the Station Need routes.

What would change it: the unwind lane installed (buy escrow back);
Station Need copies read for goods we hold (`needscan.py`); a buy lane
with a fleet-wide cap; a HEXC supply contract that counts a part
delivery.
### Selling stores where they lie (`sell-<good>-at-<station>`, `carry-<good>-<from>-to-<to>`)
Status: proven. Updated: 2026-11-22. Evidence: the sell and carry route files with their measured figures; sellgen.py of Mercury's trade skill.

- The starter hull, nothing bought; trains trading. Each ship sells its
  own stores; the routes are open to every division (rule F24).
- Steps: `store: all`, `withdraw` from the pilot's own storage (the
  runner takes only what the bid takes when the same stop sells), `sell`
  at the floor; a carry sells one or two jumps on and stores the rest.
- Gates: `requires.stored` and `requires.bid` (a book read within the
  hour); a route opens again by itself when a docked ship reads the bid
  back.
- Floor: above the cheapest ask of the good in depth elsewhere, set again
  each turn beside `sellgen.py scan` (Mercury's trade skill): soma's deep ask
  fell from 323 to 292 cr overnight and five routes stood closed by their
  own floor (2026-11-17).
- A route whose runs last minutes is judged by credits a run times the
  runs its bid's regain allows (table `stats_refill`), never by its
  per-hour figure.
- A standing sell order (`create_sell_order`, spacemolt_market) lists
  free since game 0.732.0 (it cost 1% before); one anchor beacon at
  1,200 cr stood a day unfilled at Node Beta (2026-11-16 to 17).
- Readings: `hive.py route <id>` (sell-null-matter-at-nexus,
  sell-soma-at-node-beta, carry-soma-beta-to-gamma).
- Station-sourced bids of other empires regain (Sol melt 2 to 24 at
  4,244 in hours); read every far book from home with view_market and
  carry own stores there, one ship a bid.

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
Status: test. Updated: 2026-11-22. Evidence: runs.jsonl 2026-11-21 and 22; gaps.py (Mercury's trade skill) on table books; view_market base_id read from home 2026-11-21 23:53 UTC.

- A docked ship reads any charted station's book for free (view_market
  with `base_id`, game 0.728.0; `FULL=1 gate.py raw`): eight far
  stations read from Central Nexus in one minute.
- `gaps.py` sizes every gap to one load and wallet, with its jumps and
  the lawless ones: control nodes Node Gamma 398 x 100 to Factory Belt
  777 x 200 (about 24,000 cr a load), chemical liners Node Beta 607 to
  First Step 759 x 238 and Cargo Lanes 759 x 404 (2026-11-21 23:3x UTC).
- Every road west passes Kitalpha and Kepler-442, where a pirate crew
  fights almost daily (admirals.log ENT-077): one ship a road until its
  runs read.
- A buy-and-sell route carries `requires.ask` on its buy end and
  `stop_on_failed_buy` on that stop; size `qty` to the wallet (lessons).
- One load usually closes a far bid (silver bars to Arneb +4,099 cr once;
  The Crucible -1,475 and -2,904 cr): read the bid's depth against the
  hold, and the regain in `stats_refill`, before a second ship.

### Once missions: what they taught
Status: proven. Updated: 2026-11-23. Evidence: data/fleet/onetime.json; the voidborn-* and mission-* route files; errors.log ENT-039, ENT-058, ENT-096, ENT-158; table runs.

The `once` routes head every plan's list First; a pilot flies each one
time and a route skips a pilot that booked its reward
(data/fleet/onetime.json; `oncecheck.py`, `boards.py` of Mercury's
trade skill). What they taught:

- A board mission is accepted at the route's first stop: a route without
  the accept serves only pilots that hold the mission and counts every
  other pilot as done (the first First Steps route, retired; 2026-11-16).
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
- A join corridor's trip carries `standing: true`: it is paid by the
  missions it opens, and without it the loss stop closed
  `join-sol-trader` to 57 pilots (2026-11-23).
- A pickup dock hands out a delivery's goods: Structural Reinforcement
  (Nova Terra) paid 3,000 with nothing bought (2026-11-23).
- A board differs by birth: Filed in Triplicate is offered to the
  Nebula-born, not to the Voidborn-born (2026-11-23).
- A mobile capital's stop fails after the station moves (errors.log
  ENT-158): its routes stay off until the runner finds it.

What each title paid: its route's note and `hive.py route <id>`.
