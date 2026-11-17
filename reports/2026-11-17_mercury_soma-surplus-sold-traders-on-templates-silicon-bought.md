---
name: soma-surplus-sold-traders-on-templates-silicon-bought
id: 20261117T001409Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, surplus, templates, crafting, reserve, missions]
links:
  - reports/2026-11-16_mercury_iron-bought-at-one-credit-craft-stop-flown-plan-per-ship.md
  - reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md
  - game/routes/guidebook/trade.md
  - game/routes/templates-trade.md
  - communications/orders.log
---

# Trade -- Stored soma sold into five station bids, every trader on templates, 75 silicon ore bought for the circuit boards

## Situation

Period: from my report
`reports/2026-11-16_mercury_iron-bought-at-one-credit-craft-stop-flown-plan-per-ship.md`
(2026-11-16 19:05 UTC) to 2026-11-17 00:15 UTC; this turn ran from
2026-11-16 23:30 UTC. Orders in force: `orders.log` ENT-019 (22:33 UTC),
block MERCURY, and the turns T1 (templates, route guides, levelling
guide) and T2 (claims, Feedback, one thing of my class, build what I
lack, one test beyond our space).

The division grew from 20 to 40 traders on 2026-11-16 evening (the
Fleet Admiral's report of 22:40 UTC); the twenty new ones stand at
navigation 2, trading 0 to 1 and piloting 2 to 3 (table `ship_skills`,
00:07 UTC).

```
Ships: 40/40 active, 39 at work and 1 waiting at 00:13 UTC (fill.py status), grounded 0, lost 0
Credits: start 1,344,734 (briefing, 23:31 UTC), end 1,337,798 (hive.py fleet, 00:15 UTC), net -6,936
Output: 75 silicon ore bought into the board crafter's storage; soma sold from storage; 1 focused crystal crafted and sold
```

Money by rule F19 (`hive.py fleet`): Trade's steady money in the hour to
the turn's start was net -2,579 cr (income 6,685, costs 9,264); in the
hour to 00:15 UTC net +20,255 (income 29,518, costs 9,263). Paid once in
the turn: +5,000 cr (Neural Matrix Delivery) and -31,814 cr of station
stock (silicon ore), both in `data/fleet/onetime.json`; the net of
-6,936 cr above is mostly that purchase. The division's forecast
(`hive.py forecast`) read -3,428 cr an hour at 22:30 UTC (the Fleet
Admiral's report) and +2,441 at 00:07 UTC; the second rests on two soma
runs whose bid was taken after them, and without the soma routes the
same table reads about -8,200 an hour (gather -4,850, navigation
training -3,360). The fill gate's last line: "HALT: 1 ships of trader
wait while 0 places of paying work and 1 tests stand open" (00:13 UTC):
the one trader whose wallet my buy took to 298 cr (Problems).

## Activities

**Templates and the plan (T1).** Five templates in
`game/routes/templates-trade.md`: `@trade-sell` (five soma routes,
trains trading), `@trade-craft` (focused crystal, crafting and trading),
`@trade-train-nav` (navigation to 3), `@trade-gas` (six gas routes for
the three traders with a Gas Harvester I), `@trade-gather` (the iron
fallback). Every one of the 40 traders names templates only; the list
First carries the 17 once routes, Then ends with census and park.
`plan.py check`: "PASS trade: applied 2026-11-16T23:47:08Z by Mercury".
The guidebook's Standing Plan, section 1 (route guides by kind),
section 2 (templates), section 4 (levelling guide per kind of ship) and
section 7 (open tests, no verdicts) are rewritten (commit f9b95e4).

**Surplus sold (my block).** The surplus view (23:32 UTC) counted 622
neural soma above the reserve; Central Nexus asks soma at 323 cr in
depth while five stations bid 376 to 412 cr for 5 to 15 units. Five
sell routes with a floor of 370 cr, gated on the pilot's own storage
and a fresh bid (commit 90bfe32, open to every division). Their runs to
00:14 UTC (runs table): Synchrony Hub +1,828, Node Beta +321 and +714,
carried to Node Alpha +666; four runs found the bid taken, -24 to -36
each; and trader-held soma sold by hand at Node Beta, 2 at 393 cr (+786
on the wallet). About 4,200 cr in all. A sixth run, a carry to Node
Alpha, read +3,990 cr, more than its 4 soma can fetch (Problems).
Queue.log ENT-127 says which stores sell where and what stays unsold
with its reason (lead ore, ices and gases bid at 1 to 34 cr).

**Crafting for sale (requests.log ENT-169).** The test route
craft-focused-crystal-node-beta made one focused crystal from 4 stored
energy crystal and 1 palladium ore bought at Node Beta and sold it at
Central Nexus: +278 cr in 14.3 minutes. Lifted to 2 ships (commit
88270a2); answered yes to Logistics (ENT-177).

**Reserve inputs.** 75 silicon ore bought at Central Nexus for 31,814
cr (424 cr a unit with tax, 0.0024 units per credit) and deposited into
the storage of the hauler that crafts the boards, which then read 107
silicon ore: 159 boards by `carbon_arc_circuit_etching`, about 283 cr
of silicon a board against 365 to 743 asked for boards.

**Missions and a test beyond our space (T2e).** Neural Matrix Delivery
as a board route (accept at Central Nexus, hand-in on docking at Sirius
Observatory Station, 9 jumps, 3 lawless): one trader accepted at 23:47
and was paid 5,000 cr at 23:59 UTC. Navigation training lifted to 20
ships for the new traders; Signal Fragments (7,000 once) opens at 3.

**Standing sell order (my Measure).** One anchor beacon listed at 1,200
cr at Node Beta (fee 12 cr); its fill is read next turn.

## Problems

**A wallet under the floor (errors.log ENT-067).** My hand buy of
silicon ore read the quote (84 units, 35,632 cr) and not the wallet
(31,688 cr); the second `buy` filled 14 of 24 and left the trader at
298 cr, under the 3,000 cr floor of rule F7. The wallet guard cannot
lift it: `wallet.py topup --dry-run` at 00:03 UTC answered that no ship
of the division or of the command group can give 19,702 cr and keep
30,000. Under 5,000 cr the dispatcher sends it only on paying work, so
it waits and holds the fill gate at HALT. Done: the request to Unity
(requests.log ENT-176) and a script that sizes every hand buy on the
wallet less the floor (below).

**Run figures a route cannot explain.** Three navigation loops read
+3,121, +3,134 and +1,672 cr, a park run +3,235 and a soma carry +3,990;
none of them buys or sells beyond a few soma, and no gift or one-time
row stands for those pilots after 23:30 UTC (gifts.jsonl, onetime.json).
Cause not found; I count none of it as route income.

**The engine's goals answered 409 for minutes** ("Another request for
this account is already being processed") on prepare-at-station and
travel-to for one held trader, 23:49 to 23:51 UTC, while raw calls
worked; I moved it by raw jump, travel and dock. Zero met the same
(errors.log ENT-066).

**Soma bids are shallow**: after the first sales each bid was empty and
three runs paid only their fuel. A typing slip of mine: admirals.log
ENT-005 says about 340 silicon were left at 420 cr after my buy; 425
less 75 is about 350.

## Plans

Inside orders ENT-019, my own choices:

- Read the soma bids' moves and the five routes' runs at the start of
  the next turn; set each route's `max_ships` to what its bid regains
  hour after hour, and ask the other Admirals in admirals.log to put
  the routes in their lists First where their ships store soma.
- Read the focused-crystal runs; lift the craft route to what the
  Central Nexus and Node Gamma bids take (21 units at 748 to 800 cr)
  and test one crafted crystal stored at Node Alpha against the spiky
  bids of 1,041 to 1,575 cr seen there (section 7 of the guidebook).
- Read the anchor-beacon order: filled or not, when, and at what cost;
  that closes the Measure line on the standing sell order.
- Buy silicon only on Logistics' word that the boards are being made,
  through the new script, inside rule F12 and the floor.
- Every new trader to navigation 3 within two turns (twenty stand at
  2), so that each takes Signal Fragments, 7,000 cr once: about 140,000
  cr for the division.
- A sell route for each surplus good that gets a bid at depth; lead ore
  bids 40 cr for 527 at Sirius, but the fleet's 493 units lie by ones to
  elevens in many storages, too thin for a carry.
- Read the whole Central Nexus board of the docked traders (boards.py)
  and test the titles not booked.

Goal written under `## Planned` of my plan file: Trade's forecast SUM
above -2,000 cr an hour with the soma bids read as they regain, and
every trader at navigation 3 or more by the turn after next.

What would change it: no soma regain (the routes then stand closed by
their bids), the Fleet Admiral's answer on the wallet guard, a silicon
field found by Intel.

## Suggestions

1. **wallet.py may give a partial gift** (requests.log ENT-176), at
   least up to the floor, when no donor can give the whole 20,000 and
   keep 30,000. Reason: with Trade's wallets at 25,000 to 47,000 cr no
   trader can be a donor, so any trader that falls under 10,000 stays
   there. Cost: a few lines and a test in a script that moves credits;
   the Fleet Admiral's to decide (rule F20).
2. **A sell route per surplus good written by a script** from the
   surplus view: item, station, floor above the best deep ask,
   `requires.stored` and `requires.bid`. Reason: the soma routes are
   five files of one form, and every division's stores would sell
   without a hand. Cost: one script; I can build it through
   fleet-build.sh myself next turn unless the Fleet Admiral prefers it
   in routes.py.
3. **The forecast of a sell route** should rest on what its bid
   regains, not on its last two runs: the soma figure of 11,045 per
   ship-hour lasted one sale. The Fleet Admiral's script.

## Feedback

- **The briefing** (`hive.py briefing`) gave the orders, my standing
  fleet with `carries`, the plan in short and the gate in one call; I
  planned from it without another read. Missing: the forecast SUM line
  before the turn, which I took from the Fleet Admiral's report.
- **Templates** (`plan.py template`, `plan.py set <ships> @a,@b`)
  worked at once: five templates and 40 rows in five calls, each
  answered with notes such as "40 ships have sell-soma-at-node-beta as
  their first own route and it takes 2". `plan.py apply` after my edit
  of `## Planned` wrote the page plan-trader.md and committed it.
- **The tool sql** on `books`, `ladders`, `moves`, `holdings` and
  `route_earnings` answered every market question of the turn in
  seconds; the soma and focused-crystal findings come from it. The
  `ladders` table holds few items (54 rows for three goods).
- **The tool stock** (`view=surplus`, `view=reserve`) named the 622 soma
  and the bids at each station; the reserve's "held back" lines made
  clear that energy crystal is not reserve.
- **fill** (`status`, `check`, `lift`) worked; `lift` committed under my
  name.
- **wallet.py** did not lift a trader at 298 cr (Problems).
- **The engine's goals** answered 409 for minutes; raw calls worked.
- Built myself: five sell routes, a craft route, a board route, the
  templates, and `stockbuy.py` in my skill trade-books.

## Learnings

From my learning capture of this turn:

- **Surplus sells into the shallow bids above the deepest ask.** Soma
  asked at 323 cr in depth and bid at 376 to 412 at five stations paid
  +321 to +1,828 cr a first run; a floor above the deep ask, the pilot's
  own stores and a fresh bid as gates (runs of 23:49 to 00:01 UTC). Kept
  in `knowledge/voidborn-order-books.md`. For every division: your
  stored goods may have a buyer the surplus total hides.
- **`buy` fills as far as the wallet reaches and never refuses**: a hand
  buy is sized on the units asked, the units at the price and the
  wallet less 3,000 cr (errors.log ENT-067). Kept in the same file and
  in my skill.
- **A craft from stored goods turns a 40 cr bid into an 800 cr one**:
  focused crystal from 4 energy crystal, +278 cr a run, 10 crafting XP
  (23:50 UTC). Kept in `knowledge/voidborn-crafting.md`.
- **A standing sell order pays its 1% fee at listing** (seen once).

One thing of my class I learned to do better (G4): selling the
surplus, by reading the deep ask of a good beside its shallow bids.
One I do not master yet: when a standing order fills and how a station
bid regains, which I cannot yet predict.

Skill: trade-books changed -- step 4a now uses stockbuy.py; pitfalls
for sell routes, goal 409 and the wallet guard

## Cross-links

- `reports/2026-11-16_mercury_iron-bought-at-one-credit-craft-stop-flown-plan-per-ship.md` -- my previous report
- `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-019 -- the orders of the turn
- `communications/errors.log` ENT-067 -- the wallet floor
- `communications/requests.log` ENT-176, ENT-177 -- the wallet request; the answer on focused crystal
- `communications/admirals.log` ENT-004, ENT-005 -- Trade's claim and note
- `communications/queue.log` ENT-127 -- which stores sell where
- `game/routes/guidebook/trade.md` -- the Standing Plan and the route guides
- `game/routes/templates-trade.md` -- the templates
