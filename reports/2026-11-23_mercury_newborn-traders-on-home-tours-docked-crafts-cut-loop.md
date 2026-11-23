---
name: newborn-traders-on-home-tours-docked-crafts-cut-loop
id: 20261123T004130Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, newborns, crafting, bursar, levelling]
links:
  - reports/2026-11-22_mercury_docked-gas-crafts-sell-where-it-lies-first-bursar-order.md
  - reports/2026-11-22_unity_jump-loops-capped-hunts-fuel-first-newborns-held-near.md
  - communications/orders.log
  - communications/contracts.log
---

# Trade -- Newborn Traders on Their Home Tours, Docked Crafts Cut the Loop, the Order Step Held at the Gate

## Situation

Scheduled turn, 23:31 UTC on 2026-11-22 to about 00:45 UTC on
2026-11-23, under orders.log ENT-068 (Suggi's goals G1 to G5 and
subgoals O1 to O9, Unity's PLAN P1 to P6 and block MERCURY: sell what is
handed over where it lies, cap the empty jump loop at the ten traders
nearest Piloting 10 in the same turn that docked crafts, sells, Bursar
orders and loads carried to bids take the others, standing buy orders
within 100,000 cr of escrow, build the order steps myself, one order
first). The division grew in the turn from 43 to 85 ships: 40 born
Voidborn, 30 born Nebula at Haven, 15 born Solarian (table ships, 00:18
UTC). At the turn's start 42 newborns waited and the fill gate read HALT
(`fill.py check trader`, 00:17 UTC). Money (the tool fleet, view=money,
00:39 UTC): Trade net +6,645 cr in the last hour (income 27,263, costs
20,618); the fleet -106,986 in the last hour, -67,082 an hour over 6
hours, -36,394 an hour over 24 hours. The fill gate's last line at
00:39 UTC: `PASS: no ship of trader waits`.

## Activities

- **Newborns at work in their home regions (P6, O1).** The four once
  tours of the Nebula and Solarian boards stood at 3 ships each and were
  full of every division's newborns. Lifted with `fill.py lift`:
  Federation Market Analysis and Federation Trade Route Prospectus 3 to
  80, Form TA-1 and Confederacy Infrastructure Audit 3 to 50 (commits
  01bdff45 to f3117b5c). By 00:37 UTC all 30 Nebula-born traders flew
  Market Analysis and the 12 Solarian-born at Sol flew the Audit or Form
  TA-1 (table ships).
- **Docked crafts took traders off the jump loop (block MERCURY, F8).**
  Seven new crafts from own stores, docked, no jump (bbfdf4d7): biogas
  into fuel cells at Node Beta, Central Nexus, The Experiment, Synchrony
  and First Step (`craft-biogas-own-*`; the reserve keeps fuel cells
  whole, so the pull rule does not close them), carapace into armor
  plate at Nova Terra and Sirius (armor open: 2,212 of min 5,346,
  `pull.py levels` 23:38 UTC). Steel crafts gated at 20 iron ore instead
  of 100, plus Synchrony (b226cc21; steel open at 53,681 of max
  54,714). The template @trade-craft carries them (6128bab6). The loop
  fell from 35 traders (`fill.py status`, 23:34 UTC) to 20 (table ships,
  00:39 UTC); 22 Voidborn-born traders flew crafts or sells at 00:32 UTC.
- **The Bursar order step (requests ENT-373 point 2).** Built a
  `sell_order` stop step for route_run.py: reads the pilot's own orders
  (`view_orders`), reprices one at another price (`modify_order`) and
  lists what it holds up to `qty` (`create_sell_order`), never under its
  floor or the best bid; eight new tests pass in the copy (Ran 52 tests,
  OK). Not installed: see Problems. The first route that uses it,
  `bursar-melt-central-nexus`, waits in scratch.
- **Contracts.** ENT-002's resting ask (1 melt at 2,950 cr) left the
  book between 19:52 and 20:07 UTC; no own order stands now
  (contracts.log ENT-003). No buy order was placed: escrow 0 cr.
- **Requests.** None open to me. Asked Zero to open two claimed once
  missions to traders (requests ENT-388).

## Problems

- **The order step was not installed.** `fleet-build.sh install`
  halted twice for causes outside the change: (1)
  scripts/tests/test_changelog_and_governance.py fails on the clean
  clone (KeyError 'balance_sheet', Ran 4 tests, errors=1); (2) the gate
  runs test files four at a time at 120 s each, and test_fleet_fill.py
  (41 s alone) timed out. Filed to Trinity and Unity (queue ENT-241);
  the patch is kept in scratch for my next turn.
- **The loop is not yet capped at ten.** 20 traders fly it, 3 of them
  Solarian-born that took it from Nova Terra (why the newborn guard let
  them is not read yet). The crafts drain small stores in minutes; no sustained
  docked work exists for the rest, so by Unity's answer (ENT-373 point
  3) the loop keeps them until it does.
- **The melt ask's fill is not verified**: no record of ours shows a
  fill.
- **No home-region trade for the newborns.** The fresh books of the
  Nebula region (2 hours) show no gap inside it (`gaps.py --from haven`,
  00:2x UTC): once the tours end they wait.

## Plans

- Install the `sell_order` step once the gate stands, then fly
  `bursar-melt-central-nexus` with one ship, one order first, and log it
  in contracts.log (F39, F12, F37) | next turn.
- Cap train-jumps-trader at ten (`requires.skills` piloting 9 and
  `max_ships` 10) in the turn Bursar order keeping and the crafts hold
  the rest; read the craft routes' first three runs each.
- Newborns: read the Haven and Sol books and boards for trade they can
  fly at home (Nebula is the trading empire), one ship and one unit
  first; add Zero's two once missions if ENT-388 says yes; read the
  Trade Run missions of Grand Exchange and Confederacy.
- Keep the gate PASS: after the tours, the newborns' row needs local
  work and a local fallback, never the Voidborn loop.
- Choices made: shared once tours lifted for the whole fleet's
  newborns, not only ours; no standing buy order until the order step
  can keep it.

## Suggestions

- To Trinity and Unity: make the gate's per-file limit match the
  slowest file's own time under four workers, and fix the failing
  governance test, so synchronous builds (queue ENT-233) can land
  (queue ENT-241; decision theirs).
- To Unity: a `requires.empire` (or the newborn guard reading a home
  region) would keep newborns off a home loop of another empire; three
  Solarian-born traders flew ours.
- To Zero: open the two claimed once missions to every class (ENT-388).

## Feedback

- `fill.py lift` worked on shared routes and committed each change
  under my name; it refused while another member's file stood
  uncommitted, and a retry loop of 20 s carried it through.
- `fill.py status` named why every newborn waited (born nebula, 13
  jumps; max_ships reached) and made the fix plain.
- `fleet-build.sh test <copy> <module>` ran my module in 14 s and
  passed; the whole-suite gate failed on files I did not touch, with a
  grep that hid the cause line (`grep Error` printed the traceback, not
  the file name); I ran the suite myself with no limit to find it.
- `hive.py briefing` showed the plan file failing on 12 ship rows
  before the births reached the fleet file; `plan.py template` applied
  it clean 40 minutes later.

## Learnings

- A once route in every division's plan fills first come with all
  divisions' newborns: a lift from 3 was full within a minute at 10 and
  at 25, and all 30 of ours flew only at 80 (fill.py status trader
  00:27 and 00:33 UTC; table ships 00:37 UTC). Size such a lift to the
  fleet's newborns. Kept unpromoted in LEARNINGS.md.
- A docked craft's gate is set from the smallest useful stack: steel at
  100 ore took nobody, at 20 it took eight traders in ten minutes
  (holdings 23:37 UTC; ships 00:32 UTC). Kept unpromoted in
  LEARNINGS.md.
- Fleet takeaway: every Admiral with newborns lifts shared once tours
  for all of them, and gates crafts by the stacks that exist.
- Skill: trade-books changed -- three pitfalls (shared once routes, the
  install gate, craft gates) and gaps.py reads a book row with no depth
  as 0 instead of crashing.

## Cross-links

- communications/orders.log (ENT-068)
- communications/requests.log (ENT-373, ENT-375, ENT-388)
- communications/queue.log (ENT-241)
- communications/contracts.log (ENT-002, ENT-003)
- game/routes/craft-biogas-own-node-beta.json
- game/routes/craft-steel-own-synchrony.json
- game/routes/templates/trade.json
- game/routes/guidebook/trade/routes.md (Standing Plan)
- game/fleet/route_run.py
