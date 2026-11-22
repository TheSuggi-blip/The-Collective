---
name: far-gaps-sized-from-home-two-far-tests-flying
id: 20261122T001733Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, far-trade, order-books, trade-run-missions, fill-gate]
links:
  - reports/2026-11-21_mercury_silver-to-arneb-paid-once-home-bids-gone-freighter-bought.md
  - reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md
  - communications/orders.log
---

# Trade -- Far Gaps Sized From Home, Two Far Tests Flying, 37 Traders Still Docked

## Situation

Period: from my report of 2026-11-21 20:44 UTC
(`reports/2026-11-21_mercury_silver-to-arneb-paid-once-home-bids-gone-freighter-bought.md`,
reports.log ENT-089) to this scheduled turn, 2026-11-21 23:30 to
2026-11-22 00:20 UTC. Orders in force: orders.log ENT-059 of 2026-11-21
22:51 UTC (Suggi's new standing orders S2 and S3, goal G5; block
MERCURY: find buyers and trade that repeats, sell every division's
surplus, take trading beyond our borders so every trader trades instead
of docking; P5: research the game online and the role).

```
Ships: 40/40, at work 3, waiting docked 37, grounded 0, lost 0 (fill.py status trader, 00:09 UTC)
Credits: start 1,837,630 (my last report, 20:33 UTC), end 1,816,636 (table ships, 00:15 UTC), net -20,994
Output: 7 route files written, 2 far buy-and-sell tests flying, 1 far carry flown (+431 cr), 16 receivers named, 8 far books read from home
```

Of the net, 19,618 cr is in one trader's hold as 32 chemical liners on
the way to First Step's bid of 759 cr (the trader's log, 00:05 UTC);
the rest is the once runs' fuel and the far carries. Steady money of
the division over the last hour reads -21,007 cr (`hive.py fleet`,
00:15 UTC): its costs hold the liner buy, metered fuel and repairs were
1,652 cr. The fleet's steady net reads +43,700 cr an hour over 6 hours
and +10,942 over 24 hours (same call). Paid once to traders in the 4
hours to 23:31 UTC: 63,110 cr (briefing, SUM trader). No request was
open to me at the start (`comms.py requests --to Mercury`: 0 open, 0
accepted); Unity answered both of mine of last turn: no pick on the
trader fallback, decide myself (ENT-293), and `requires.ask` built and
installed (ENT-305, ENT-309). The briefing's fill gate read HALT with
35 traders waiting at the start of the turn.

## Activities

**Research of the role (P5).** A research subagent read the game's own
trader, arbitrage and market guides and the changelog to 0.732.0. What
matters for us: missions first, then arbitrage, then crafting; cargo
over speed; thin far books show the widest spreads; exchange orders
list free since 0.732.0. The class card and the order-books knowledge
file carry it now.

**Far books read from home.** One docked trader read eight far
stations by `view_market` with `base_id` in about a minute (23:53 UTC):
Confederacy Central Command, Frontier Station, Market Prime, Cargo
Lanes, Unknown Edge, Ramen's Rest, Starfall Salvage, Void Gate. I wrote
`gaps.py` (skill trade-books), which sizes every gap of fresh books to
one hold and one wallet with its jumps. Best loads: control nodes Node
Gamma 398 x 100 to Factory Belt 777 x 200 (about 24,400 cr a Threshold
load, 22 jumps); chemical liners Node Beta 607 x 600 to First Step 759
x 238 and Cargo Lanes 759 x 404 (about 4,700 cr a load).

**Routes.** Two buy-and-sell tests, one ship each, with `requires.ask`
on the buy end, `requires.bid` on the sell end and `stop_on_failed_buy`
(commits 64e51631, b73da411): the control node route waits, Node
Gamma's ask read 0 at 23:56 UTC; the chemical liner route bought 32 at
607 at 00:05 UTC and flies to First Step. Five far carries of stored
surplus lead `@trade-sell` (commit 632751aa): hydrogen to Nova Terra
(flown: +431 cr in 25 minutes, 43 units sold at 38), lead ore to Grand
Exchange (240 x 752), verdigris curd to Procyon (330 x 50). Lead and
curd lie in miners' and drones' storage, so I offered the routes to Zero
and Apophis (admirals.log ENT-080).

**Strict classes (queue.log ENT-200, ENT-201).** I named the trader
receivers per station: 15 stations and a default
(data/fleet/receivers.json), ready for the switch.

**Guidebook, plan, gate.** Standing Plan, far trade, open tests and the
card rewritten; `guide.py check trade` PASS. `plan.py check` PASS. The
fill gate at 00:09 UTC: "HALT: 37 ships of trader wait and nothing that
pays is open to them".

## Problems

**A test looped 18 times (errors.log ENT-118).** I sized the chemical
liner buy at 76 units for a freighter's hold (47,652 cr) and gave it to
a Threshold with 46,130 cr. The runner refuses a buy whole when it would
take the wallet under 3,000 cr; stop_on_failed_buy ended each run at
stop 1, and the dispatcher, reading only `requires.ask`, sent the same
pilot again every 44 s: 18 runs of 0 minutes and 0 cr from 23:51 to
00:04 UTC. Nothing was lost, the pilot stayed docked. Cause: my sizing,
and rule F12's one unit first skipped; the loop is the third of its
class (ENT-027, ENT-113). Fixed in the route at 00:05 UTC; the loop
guard is asked of Unity (requests.log ENT-317).

**37 traders docked, the gate HALT.** Home bids are still gone. Far
buyers are one load deep. No route trains trading without a buy. I
weighed a jump loop and declined it on its numbers (Plans): it costs
about 358 cr a ship-hour.

**The western road.** Every road to First Step, Cargo Lanes, Factory
Belt and Haven passes Kitalpha and Kepler-442, where a pirate crew
fights almost daily (admirals.log ENT-077). The chemical liner test
carries 19,618 cr through it; the dispatcher's pirate stop reads a
route's places, not its road.

**The freighter's first carry** (last turn) lost 2,904 cr: it carried
3,563 cr of heat sinks to a bid of 24, and spent about 1,337 cr on 18
jumps beside the goods. Its 160 hydrogen and 19 heat sinks stay at The
Crucible.

## Plans

Inside orders ENT-059, block MERCURY, these are my own choices:

1. **Read the far tests and lift what pays twice.** Next turn I read the
   chemical liner run's RESULT line (the sale at First Step, the fuel
   over 18 jumps, the bid left) and whether the control node ask came
   back at Node Gamma. A test that pays on two runs gets one ship more,
   never more than the buyer's depth carries. One that loses rests by
   itself.
2. **Trade Run missions.** The boards of Node Gamma, Node Beta and
   Central Nexus offer Trade Runs that pay 260 to 460 XP for the very
   hauls my tests fly: 70 control nodes to Factory Belt, 27 to 35
   chemical liners to First Step or Cargo Lanes, 5 reinforced frames to
   Ramen's Rest. Next turn one trader takes one by hand. I read its
   deadline, where it is handed in and which skill gets the XP, then
   put an `accept` stop on the route. A Trade Run carried on a paying
   gap is the trader's levelling path, and the jump loop is not.
3. **Freighter.** The Prayer measured about 46 cr a jump on its way home
   (26 jumps, Crucible to Node Beta to Nova Terra, +431 cr net). Before a
   second Prayer is bought, a load deep enough for 540 units must stand
   at both ends of one road. Control nodes are bounded at 100 by Node
   Gamma's ask; none yet is.
4. **Docked traders.** They stay docked until a route opens for them.
   Weighed: Apollo's jump loop measured -358 cr a ship-hour over 508
   runs (route_earnings, 12 hours) for about 80 piloting XP an hour
   (stats_pilot_hour). That is about 46 hours and 16,500 cr a trader to
   reach Piloting 10 and a 240-cargo hull, while a 540-cargo Prayer
   costs 5,000 cr at tier 1. For 37 ships it would cost about 13,000 cr
   an hour against P1. What would change this: Unity's or Suggi's word
   that F8 wants the loop flown anyway, or Trade Runs that pay piloting
   on a paying haul.
5. **Strict classes.** When the switch goes on, the receivers sell the
   other divisions' goods through the existing sell and carry routes,
   whose `requires.stored` now reads the receiver's own storage.

## Suggestions

1. **A loop guard in the dispatcher** (requests.log ENT-317, Unity's to
   decide). A run ended by stop_on_failed_buy for any cause but a
   missing ask should rest that route for that pilot, and three runs in
   a row of under a minute and 0 cr should rest it until a turn reads
   it. Cost: a small change to dispatch.py. Gain: the class of ENT-027,
   ENT-113 and ENT-118 ends by itself.
2. **A road check for circuits beyond the border** (Unity's). The pirate
   stop reads a route's places. The roads west all pass Kitalpha and
   Kepler-442. A check of the jumps of `scripts/map.py route` against
   the six-hour sightings would close a far trade the hour a crew
   fights on its road. Cost: one function; it would close the far tests
   more often.
3. **F8 for a class with no work open** (Suggi's and Unity's). The gate
   cannot pass for Trade while the far buyers are one load deep, short
   of a training loop at about 13,000 cr an hour. I propose that a docked
   trader whose every route is closed by its book counts as waiting for
   work, not idle, until the Trade Runs are tested.

## Feedback

- **requires.ask** (ENT-305, ENT-309) worked in my hands. `fill.py
  status trader` named the control node route closed with "no ask for
  control_node at node_gamma_relay_station: best 0 cr x 0" at 23:56 UTC,
  and it opens by itself when a dock reads the ask back.
- **stop_on_failed_buy** worked: the RESULT line said "stop 1: the buy of
  chemical_liner got nothing: run ended (stop_on_failed_buy)" and no ship
  flew 18 jumps empty. With a refused buy whose ask still stands, it
  loops (ENT-118, ENT-317).
- **The buy's wallet floor** changed since the guidebook was written:
  `buy` once filled as far as the wallet reached; now it buys nothing. I
  found it only in the pilot's log. A line in BLUEPRINT.md for `buy`
  would have saved the loop.
- **handover.py receivers** worked at once, 16 receivers named and listed
  back. **The briefing** printed the orders, my plan and the gate in one
  call. Its money line counts a buy for resale as a cost of its hour,
  which is right but reads hard: Trade's -21,007 cr an hour is mostly 32
  liners in a hold.
- **candidates kind=trade** listed control nodes and chemical liners
  first, with "depth at the best price" warnings. It matched what
  `gaps.py` found from the same books. I built `gaps.py` for one thing
  candidates lacks: the load sized to the pilot's own wallet and hold.
- **gate.py raw** cuts at 3,000 characters without `FULL=1`. A far book
  needs it; I lost one round of eight calls to it.
- **plan.py planned** takes its time with `--when`. A second positional
  word went into the text; the tool's description says `when`, the
  script's usage says `--when`.

## Learnings

From this turn's learning capture:

- **Far books are read from home, and the stations name their own far
  trades.** A docked ship reads any charted station's book for free
  (eight far books in a minute, 23:53 UTC). The boards' Trade Run
  missions ask for the same hauls the books show as gaps: control nodes
  to Factory Belt, chemical liners to First Step and Cargo Lanes,
  reinforced frames to Ramen's Rest (table missions, 00:05 UTC). I now
  look for a Trade Run on the road of every far gap before I test it.
  Kept in `knowledge/voidborn-order-books.md`. For Intel and Logistics:
  a remote read costs no flight, so a census dock is worth eight far
  books.
- **Size a buy to the poorest pilot.** The runner buys nothing when qty
  x price would cross the 3,000 cr floor (the trader's log, 00:04 UTC).
  Kept in the guidebook (lessons.md, Money, calls and the runner) and
  the skill trade-books. This was a repeat of a known class: a test
  flown again because nothing stops its next run. My route-side fix was
  real, but the gate belongs to the dispatcher (ENT-317).
- **A jump loop buys piloting at a price a freighter beats.** About 358
  cr a ship-hour for about 80 XP; Piloting 10 is about 46 hours away for
  the best trader (catalog xp_per_level). Unpromoted, in LEARNINGS.md,
  until a Trade Run's piloting XP is measured beside it. For Logistics:
  the same numbers stand for the 40 haulers on train-jumps-hauler.
- **The game's guide confirms** what the record taught: home markets are
  deep only at floor prices, and the thin far books pay.

Skill: trade-books changed -- gaps.py added to step 3 with remote reads
and Trade Runs; two pitfalls (the buy's wallet floor, withdraw sized to
the buyer).

## Cross-links

- `reports/2026-11-21_mercury_silver-to-arneb-paid-once-home-bids-gone-freighter-bought.md` -- my previous report.
- `reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md` -- the Fleet Admiral's report in force.
- `communications/orders.log` ENT-059 -- the orders this turn worked under.
- `communications/errors.log` ENT-118 and `communications/requests.log` ENT-317 -- the loop and the guard asked for.
- `communications/admirals.log` ENT-080 -- Trade's claims, the lead and curd routes offered, the western road.
- `game/routes/guidebook/trade/routes.md` -- the Standing Plan and Trade beyond the border.
