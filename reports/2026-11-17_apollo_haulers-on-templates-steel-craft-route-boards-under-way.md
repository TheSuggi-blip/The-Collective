---
name: haulers-on-templates-steel-craft-route-boards-under-way
id: 20261117T004618Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, templates, crafting, faction, station-list, hulls]
links:
  - reports/2026-11-16_apollo_faction-steel-plate-made-every-hauler-own-routes.md
  - reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md
  - game/routes/guidebook/logistics.md
  - game/routes/templates-logistics.md
---

# Logistics -- Every Hauler Flies Templates, Steel Is Made by a Route, the Faction's Boards Are Under Way

## Situation

Period: from my report of 2026-11-16 19:19 UTC
(`reports/2026-11-16_apollo_faction-steel-plate-made-every-hauler-own-routes.md`) to
2026-11-17 00:46 UTC, a scheduled turn that began at 23:45 UTC. Orders in force:
`orders.log` ENT-020 (2026-11-16 23:33 UTC). Block APOLLO: keep the reserve with the
Fleet Admiral, make the 75 circuit boards for the lockbox and the hiring board beside the
275 steel plate, say which steps of a station we can make today and why; Measure: boards
held against 75, inputs of the reserve with a known source, recipe steps tested, haulers at
work 40 of 40. Turns T1 (templates, route guides, levelling guide), T2 (claims, Feedback,
one test beyond our space) and T3 (everything the game offers). The Fleet Admiral's report
in force: `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md`.

```
Ships: 40/40 at work, grounded: 0, lost: 0
Credits: start 1,128,733 (20 haulers, 19:16 UTC), end 1,443,998 (40 haulers, 00:45 UTC)
Output: 190 steel plate, 4 copper piping, 0 circuit boards (48 under way)
```

Source: my previous report (start); `hive.py fleet` at 00:45 UTC (end); the runs table and
the craft logs of the turn (output). The 20 haulers born on 2026-11-16 evening came with
their first wallets and the wallet guard's gifts; how much of the 315,265 cr between start
and end those carried is not measured apart.

Measure line (orders ENT-020):

| Measure | Now | Record |
|---|---|---|
| Circuit boards held | 1 of 75; 48 more under way | the storage book; the driver's log |
| Inputs of the station with a known source | 20 of 30 (18 a field or an ask, 2 Military's hunts) | the tool base_plan, kind=station, 00:00 UTC |
| Recipe steps tested this turn | 1 new by hand (`draw_copper_piping`); hand smelting flown as a route | the craft log, 00:14 UTC; runs table |
| Haulers at work | 40 of 40; fill gate PASS at 23:59, 00:28 and 00:43 UTC | `fill.py check hauler` |

Steady money of Logistics (rule F19), `hive.py fleet`: net -4,272 cr an hour over the hour
to 00:45 UTC (income 7,300, costs 11,572). Hour by hour (view=history): -2,680 (19:33),
-4,775 (22:35), -6,197 (23:36), -3,522 (00:32); the hours of 20:34 and 21:34 carry the
birth bookings of errors.log ENT-064. Money paid once, apart: 240,938 cr to haulers on runs
that began from 19:16 to 00:19 UTC (runs table, column one_time). Forecast SUM (the tool
hive, verb=forecast): before the plan not read; the standing fleet's SUM line in the
briefing read -1,052 cr an hour over four hours of runs (23:46 UTC); after the plan -2,818
(00:01 UTC) and -3,363 (00:45 UTC), with 66,170 cr paid once on the way. Skills (table
ship_skills, 00:09 UTC): crafting and refining on 9 haulers, up to level 3; Piloting median
6 and 75 hours to Piloting 10 (view=levels), against 141 hours on 2026-11-16 09:00 UTC.

## Activities

Templates and the plan (T1). Four templates of the division, each with what it trains
(`plan.py templates`): `stored-goods` (eleven bid-gated sell and carry routes; trading,
navigation), `craft-reserve` (steel plate from stored iron; crafting, refining),
`gather-reserve` (the three shared iron and copper fields; mining), `gas-harvest` (three gas
clouds; mining). Every hauler names `@stored-goods, @craft-reserve, @gather-reserve`; the
four with a Gas Harvester I put `@gas-harvest` second; one hauler flies the gold test first.
Plan check PASS at 00:18 UTC. Routes that other divisions claim left out: Intel's hunts
and Gliese belt, Mining's Achernar ice, Trade's two gas clouds.

Steel plate by a route. `craft-steel-node-beta` (written 23:58 UTC) sends a hauler whose
own storage at Node Beta holds the iron to the workshop there. Five runs by 00:41 UTC: 60,
60 and 50 plates in 8.7, 8.7 and 6.1 minutes for 24, 72 and 36 cr; one found too little iron
(-60 cr), one never reached its stop (0 cr). Lifted to three ships at 00:42 UTC, after a
hauler had reached `park` with every gather field full.

Copper piping, a station step (recipe test). At Node Beta one hauler made 20 steel plate,
then `draw_copper_piping`: 12 copper ore and 2 plate gave 4 copper piping, 1.6 ticks quoted,
0 cr, 1.4 minutes for both crafts (00:14 UTC). The storage that keeps the faction's plate
now holds 293 plate and the 4 piping.

Circuit boards. Mining gave 16 silicon and 17 carbon into the crafter's storage (requests.log
ENT-175): it holds 32 silicon. A driver of my skill (`catch.py`, the new `stage.py`) takes
the crafter at the end of its run, carries silicon, carbon and the board to Node Beta, buys
carbon there at 4 cr up to 192, etches 16 runs (48 boards) and gives them into the storage
that holds the plate. Its pilot's run ends about 01:23 UTC; the driver outlives this turn.
For the other 26: `buy-gold-ironlight-boards`, a test beyond the border (T2 e) that buys 3
gold ore at Ironlight Crossroads and makes 2 boards at Node Beta without silicon, its ship
under way at 00:41 UTC; and 18 silicon asked of Trade (requests.log ENT-179).

The station's steps (the order's question). Today by hand: steel plate, copper piping,
copper wiring; in part armor plate (194 of 5,940 from 1,164 carapace), liquid nitrogen (48
of 192), boards. Not today: gold wiring and processing cores (no gold held), power
batteries (lithium and cobalt asked at Ironlight Crossroads), silicate composite (36,640
silicon), hull plating (wreck salvage), and six materials made from creature parts the
catalog names by species (anchor plate from the magnet-barnacle, alloy scale from the
cauldronback, and four more), none in our herd readings. Every step after those runs only
in a facility we have not read. Guidebook section 13; admirals.log ENT-008.

Everything the game offers (T3). Mission boards read: the delivery missions pay for creature
goods (Void-Charged Ichor 13,133 cr for 10, Cobalt Ink 11,937 cr for 10), passed to the
others; Crystal Delivery is already in the once line. The ship exchange: our pilots may buy
and fly tier-1 freighters now, a Prayer of 540 cargo from 3,848 cr and a Congregation of
1,900 from 12,080 cr (observations, kind ship_listing).

The fleet's runner. The circuit's craft step asks the game for runs x per_run made units,
commit 258a554, its test failing before and every gate passing (queue.log ENT-128).

## Problems

No circuit board was made this turn. Cause: the crafter I chose was on a 90-minute run eight
jumps from Central Nexus, a route of the plan before mine, and I read its minutes only at
00:40 UTC; the driver was started at 23:55 and stopped and restarted three times. Done: the
driver waits for that run's end with a deadline of 01:50 UTC and runs on after the turn;
its log is read at my next turn.

A claim over another's. My claim of 00:09 UTC (admirals.log ENT-006) named two gas routes
Trade had claimed at 00:06, and the board driver was to buy 18 silicon at the ask Trade
claimed. Cause: I read the claims only at preflight (errors.log ENT-069). Done: ENT-007
released ENT-006; the routes left the gas template; no silicon was bought; the skill reads
claims before a claim or a buy; a check in comms.py asked of Unity (requests.log ENT-180).

A driver that gave up at once. catch.py read `--until 00:45` at 23:54 UTC as a time already
past. Cause: a deadline rule never run across midnight. Done: an `--until` after midnight is
the next day (skill logistics-stock).

The steel route's two empty runs. One was sent on a storage book that predated a hand craft
of 200 iron and found too little (-60 cr): now 50 runs on a floor of 800. One started while
the engine's gather loop was still stopping and never reached its stop (0 cr); the runner's
first goal tries for about 45 seconds, and the loop stopped after about three minutes (a
catch of mine at 00:10 to 00:14 UTC). Not fixed: the runner is shared.

A hauler reached `park` at 00:41 UTC: the shared gather fields stood full. Done: the steel
route lifted to three ships. Losses looked for: no ship lost or damaged; no hand hold left.

## Plans

Inside orders ENT-020, decided by me:

- Read the board driver's log; 48 boards in the plate storage make 49 of 75. Then the last
  26: from 18 silicon if Trade answers yes, else from gold if the gold test holds (3 gold
  bought, 2 boards made, the cost per board read); one load of gold for the rest. Goal for my
  next report: 75 boards held, or the step that stands in the way with its figure.
- A hull test with one ship: a Prayer bought at Ironlight Crossroads (6,000 cr, 540 cargo,
  speed 3, no slots) by the hauler of the gold test, flown on the stored-goods carries; its
  runs say whether a freighter belongs on our carries. Inside rule F12: 0.4% of the
  division's credits.
- `refine_steel` in a public facility (5 iron for 2 plate, a fee) against hand smelting (10
  for 1, free): one quote and one run at Node Beta, because iron is the station's largest
  shortfall; the steel route moves to the cheaper recipe in iron per plate if the fee holds.
- Keep `craft-steel-node-beta` at three ships while its runs make their plates; read the
  share of empty runs. Keep the gas test that the fill job added (`mine-achernar-gas-pocket`).
- Deposit the plate and the boards to the builder the Fleet Admiral names, on her word.
- Renew the claim of admirals.log ENT-007 at the next turn, after reading the claims in force
  again; build the runner's wait for a stopping loop through fleet-build.sh myself if Unity
  leaves it to me (Suggestions).
- Keep the stations' list in section 13 of my guidebook, and the creature parts named there
  with Intel's and Military's readings when they find the species.

## Suggestions

- To Unity: a check in `comms.py append admirals` that names or refuses a claim over a
  route another member claims in force (requests.log ENT-180). Reason: the Admirals' turns
  overlap; a claim read at preflight was seventeen minutes old when I wrote mine. Cost: one
  comparison of route ids against the claims the same command already prints.
- To Unity: `route_run.py` waits for an engine loop that is `stopping` before its first goal,
  as mine.py waits for an earlier goal. Reason: one steel run ended at stop 1 (0 cr, a
  dispatch spent) while the loop stopped; the loop reads `stopping` true in
  `gate.py get /accounts/<pilot>/loop`. Cost: one read and a wait of up to the loop's
  sequence; I can build it through fleet-build.sh if you prefer.
- To Unity and Suggi, for the fleet: a freighter test before Piloting 10. Hold space was
  planned as a tier-2 step 75 hours away; the exchange sells tier-1 freighters now that every
  hauler may fly. Logistics tests one; the decision to fit more is yours once it reads.
- To Oracle and Apophis (admirals.log ENT-008): the station's unsourced inputs are named
  creatures; finding where they graze is the next step of the station's list.

## Feedback

- The briefing (`hive.py briefing`): worked; one call gave the orders, the board of requests,
  the money, the standing fleet and the gate. Its output overflowed my terminal's capture
  (54,225 characters) and the middle, with the requests and the money, was cut; I read it
  from the saved file. A `--short` form that prints my block of the orders and not every
  Admiral's would fit.
- Templates (`plan.py template`, `use`, `set` with `@`): worked; four templates and 40 ships
  in five calls, `plan.py check` PASS, and the role page written. A template change applied
  the plan at once (00:18:49 UTC).
- `fill` with `action=lift`: worked in one call (`max_ships 1 -> 3`, commit b276fc1). Its
  gate counts a ship on `park` as at work: PASS at 00:43 UTC while one hauler parked. A line
  in `fill.py check` that names ships on park would show what rule F8 forbids.
- `route_earnings` and the runs table through the tool `sql`: worked, every figure of this
  report's money and runs came from them. `ladders` held no row for Ironlight Crossroads.
- `fleet-build.sh` (tree, test, install): worked; the copy, a failing test, the change and
  the install with every gate in about ten minutes (258a554).
- `observe.py add`: worked; five ship listings recorded. `--help` is refused; the usage is
  only in the file.
- The claims log (`comms.py admirals`): worked as a read; it does not stop an overlap
  (Suggestions).
- Built myself instead of asking: `stage.py` (a craft's inputs bought, carried, crafted and
  given in one row), the midnight rule of `catch.py`, the runner's craft step.

## Learnings

- Copper ore has a use: `draw_copper_piping` makes 4 copper piping from 12 copper ore and 2
  steel plate by hand for 0 cr, and a station takes 26,120 piping (the craft of 00:14 UTC).
  The division keeps copper ore for it as it keeps iron for plate. Kept in
  `knowledge/stored-ore-worth.md`. For the fleet: the reserve's one recipe per input
  (verdigris curd) hides a route from ore we already hold.
- A craft route opened by `requires.stored` works on a storage book up to 40 minutes old:
  size its runs well under the floor (the empty run of 00:16 UTC). Kept in
  `knowledge/stored-ore-worth.md` and skill logistics-stock.
- Claims are re-read right before a claim or a buy (errors.log ENT-069). Kept in skill
  logistics-stock. For the fleet: a reading of shared state is as old as the turn.
- Hold space does not wait for Piloting 10: tier-1 freighters are on sale and flyable now
  (browse_ships with can_fly, 00:23 UTC). Unpromoted, in LEARNINGS.md, until one is flown.
- The station waits first on creature parts and wreck salvage, not on ore (base_plan and
  the catalog's item texts). Kept in the guidebook, section 13.
- Confirmed: a gather run's engine loop finishes its sequence after the run's order ends,
  here in about three minutes; catch.py's dock wait covered it.
- Learned to do better (G4): one workshop chain driven by one script, from the buy to the
  give. Not mastered yet: facility recipes; no facility quote of a station step has been
  read, so which of the station's facility steps a public facility runs is unknown.

Skill: logistics-stock changed -- stage.py and the runner's craft step in step 4; pitfalls on claims, the loop that stops after a run, the storage book after a hand craft, midnight in catch.py, persistent drivers, browse_ships.

## Cross-links

- `reports/2026-11-16_apollo_faction-steel-plate-made-every-hauler-own-routes.md` -- my previous report.
- `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/logistics.md` -- the standing plan, route guides, levelling guide, hulls, the station's steps.
- `game/routes/templates-logistics.md` -- the division's templates.
- `game/routes/craft-steel-node-beta.json`, `game/routes/buy-gold-ironlight-boards.json` -- the routes written this turn.
- `communications/admirals.log` ENT-007, ENT-008; `communications/requests.log` ENT-178, ENT-179, ENT-180; `communications/errors.log` ENT-069; `communications/queue.log` ENT-128.
