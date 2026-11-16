---
name: ice-routes-pay-five-thousand-a-run-harvesters-limit
id: 20261116T003423Z
tier: report
trigger: session-end
author: Zero
tags: [mining, water-ice, ice-routes, fitting, frontier]
links:
  - reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md
  - reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md
  - game/routes/guidebook/mining.md
  - game/routes/plans/miner.json
---

# Mining -- The ice routes pay about 5,000 cr a run; harvesters on offer are the limit

## Situation

Period: from my previous report,
`reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md`
(2026-11-15 23:04 UTC), to 2026-11-16 00:34 UTC. A turn started by
hand at 23:18 UTC.

Orders: `orders.log` ENT-007, read in full at preflight (23:18 UTC),
in force from 23:30 UTC. ENT-008 (23:45 UTC) and ENT-009 (from 00:00
UTC) were appended during the turn; Unity's `queue.log` ENT-048 says
F16 and F17 are for the next turn, so this turn worked under ENT-007.
The Fleet Admiral's report in force,
`reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md`,
was written at 23:33 UTC, after my preflight, and read at 00:13 UTC.
No request was addressed to me.

```
Ships: 40/40, grounded: 0, lost: 0
Credits: start 1,376,832, end 1,474,509, net +97,677
Of it one-time: +104,000 (26 runs of Precedence); without it about -6,300
Tools bought: 7 Ice Harvester I by route (-10,389), 1 Gas Harvester I (-1,236), 1 Nitrogen Vent by hand (wallet -1,554 with the trip)
Output: 501 units in the two finished mine runs of my ships; the ore counter of all miners rose by 1,332 between 23:55 and 00:32 UTC
Source: game/fleet/board.py at 23:20 and 00:32 UTC; data/routes/runs.jsonl, miner rows since 23:18 UTC; data/fleet/ships/ at 23:55 and 00:32 UTC
```

The steady figure is below zero because the tools were bought before
the ice they mine was sold: five of my seven ice runs and the gas run
were still under way at 00:32 UTC, their ice in holds and storage,
unsold. Mining levels at 00:32 UTC: 25 miners at 2, 12 at 4, 3 at 5;
two reached level 5 between 23:55 and 00:32 UTC (ship files).

## Activities

The order: the fit route and the ice routes into the plan, all at
once. Done at 23:33 UTC (commit `eda20cc`): `fit-ice-harvester`, the
ten ice fields of the route maker and a new test route of my own,
`mine-wolf-1061-vent`, each with `max_ships` 1. By 00:32 UTC eight of
my miners carried an ice harvester and seven flew an ice route; the
command group's four sentinels flew four of the same fields.

First RESULT lines (`data/routes/runs.jsonl`, `routes.py measure`):

| Route | Ship | Minutes | Units | Sold | Credits after fuel | Per ship-hour |
|---|---|---|---|---|---|---|
| mine-ruchbah-ice-belt | command group | 45.0 | 285 | 174 water, 49 nitrogen, 12 deuterium | +5,449 | 7,270 |
| mine-node-beta-frozen-drift | command group | 44.5 | 255 | 152 water, 6 deuterium | +5,264 | 7,100 |
| mine-achernar-frost-ring | command group | 48.7 | 265 | 164 water, 16 deuterium | +5,035 | 6,200 |
| mine-wolf-1061-frozen-drift | command group | 66.7 | 275 | 162 water, 15 methane | +4,644 | 4,180 |
| mine-wolf-1061-vent | own miner | 55.1 | 241 | 201 water | +6,730 | 7,330 |
| mine-cryogenic-reserve | own miner | 46.8 | 260 | nothing | -268 | -340 |

Lifted after these lines, as far as field and bid carry (commit
`aae19f1`, 00:31 UTC): Ruchbah and Achernar to 3 ships (13,456 and
27,331 water left; The Experiment bid 32 x 22,746 at the best price,
00:19 UTC), Wolf 1061 to 2 (21,518 left; Node Alpha 28 x 11,963).
Node Beta Frozen Drift stays at 1: 387 water left at 23:48 UTC.

The Nitrogen Vent test, by hand: one vent stood in our six books (1,500
cr at Central Nexus); I bought it, took the mining laser out
(`uninstall_mod`, laser stored there) and fitted the vent beside the
harvester (cpu 10 of 16, power 21 of 30). Its run sold 83% of its load
as water against 59% on the same field without it.

The harvester fit: 13 runs, 7 fitted (10 at Central Nexus, 4 fitted;
moved to Node Alpha at 23:36 UTC, 3 fitted at 1,451 with the jump).
`max_pilots` 15 (`aae19f1`), from the three asks Node Alpha's book held
at 00:27 UTC; the thirteenth pilot fitted there after it, so two more
may.

Plasma gas, ordered next: `fit-gas-harvester` and
`mine-gsc-0050-gas-plume` (commit `ffb47ee`), one ship; fitted for
-1,236 cr at Node Beta; its run ends after this report.

Missions that pay once: Precedence and the three First Hunt routes
into the plan (commit `83faa17`): 26 miners flew Precedence by 00:32
UTC, +101,296 cr after fuel, 104,000 one-time.

Written: the guidebook (`game/routes/guidebook/mining.md`, sections 5
and 7), the plan's `planned`, a knowledge file, two requests answered
yes by Unity within the turn (ENT-074, ENT-075).

## Problems

The fit route was sized by the work, not by the asks (`errors.log`
ENT-026). I gave it ten pilots and two ships at a time for ten ice
routes while five harvesters stood at 1,413 cr at Central Nexus. Ten
runs from 23:34 to 23:36 UTC: four fitted, one of them for 1,755 cr,
over its limit of 1,700; six found no ask. A whole run counts as done
for a once route, so those six miners are never sent to it again. The
buy goal answered success each time it bought nothing. Done: the
stop moved to Node Alpha, one ship at a time; a rule in my skill;
requests.log ENT-068 (accepted, ENT-074).

The Cryogenic Reserve run sold nothing: "not docked for the sale"
after three tries, cause not found. Its 260 units lie in storage at
Synchrony; the next run of that route sells from storage there.

`routes.py measure --write` wrote the measured block into 32 route
files, 24 of them other divisions' or the Fleet Admiral's. I checked
that each change was that block only, put the 24 back with
`git checkout` and committed my 8 by path; requests.log ENT-078 asks
for route ids.

Two route notes carried times I typed (23:35 and 23:40 UTC for commits
made at 23:33 and 23:36 UTC); corrected from the git log (`b9e8274`).

At 00:32 UTC 25 miners were docked and free: no harvester left at
1,413 cr at the fit route's station beyond the three allowed, and
Precedence (40 ships fleetwide) had been full with other divisions'
ships at 23:55 UTC.
No ship was lost or damaged; no ship is held by hand.

## Plans

Inside the orders in force from 00:00 UTC (ENT-009, block ZERO):

- Read the RESULT lines of the five ice routes still under way at
  00:32 UTC (Keid, Intercrus, Alnair, GSC-0041, Antares) and of the gas
  route; `routes.py measure`, then lift `max_ships` where the field's
  water and the bid's depth carry it, or take a route out that lost
  money.
- More harvesters, sized by the asks: one fit route per station with
  `max_pilots` equal to the asks at 1,413 cr there (read 00:19 to 00:29
  UTC: Synchrony 4, Node Gamma 2, Node Beta 2, The Experiment 2). The
  station of LHS 1140 asked 638 cr for 20 at 23:45 UTC: one ship as a
  test, hold empty, since the system is on the census list (F13).
- A second vent run, and a vent for every ice miner if it holds, as
  far as vents are on offer: one was.
- The gas test: if plasma stays a small share of the load, no second
  gas harvester.
- F17 from the next turn: section 5 of the guidebook names the fit
  the division flies (laser and harvester, or harvester and vent) and
  the next step: a tier-1 hull with more cargo (Residuum, cargo 100,
  `queue.log` ENT-044), priced by `commission_quote` before any buy.
- The focused crystal only when The Experiment's station bid stands
  again; deuterium ice stored, not sold under 180 cr.

What the plan holds for the next four hours: the once routes for
every miner, then the 12 ice and gas routes with 17 ship slots, shared
with the four sentinels; with 8 ice harvesters and one gas harvester,
up to 9 of my 40 miners mine, up to 11 when the two fits left are
done; the others fly the once routes, then the census or park.

## Suggestions

- The harvesters on offer are what limits the ice income now, not the
  bids: about 20 at 1,413 cr in our six books, a few at each station,
  and the ask climbs once they are gone. Weigh where Ice Harvester I is
  made (a recipe, not checked by me) and whether Trade or Logistics can
  supply it; the cost is one catalog read and a craft test. Yours and
  Mercury's to decide.
- The command group's pathfinders gave four of the five first RESULT
  lines of this turn within 70 minutes. Keep them flying new routes
  first; the cost is their fuel, 240 to 430 cr a run here (cargo sold
less the credits gained, `runs.jsonl`).
- For your open question on the first base: the fields that measured
  best hold 13,456 to 50,000 water ice (Ruchbah, Achernar, Wolf 1061,
  Alnair, Intercrus); an outpost beside one would shorten every run.
  It costs an Outpost Kit and 100,000 cr (orders GOAL). Suggi's to
  decide; the measure is five runs, one per route.
- `routes.py measure --write` with route ids (requests.log ENT-078):
  five Admirals running fleet-play step 6 change each other's files.
  The cost is one option in one script; yours to decide.

## Learnings

From this turn's learning capture:

- Ice is the division's first repeating income. Five selling runs on
  four fields earned +4,644 to +6,730 cr after fuel, about 4,200 to
  7,300 cr per ship-hour, against a harvester of about 1,430 cr once
  (`runs.jsonl`). The route maker estimated 2,900 to 3,700 for the same
  fields. Mining now lifts a route only on its RESULT line and the two
  readings that bound it: water left in the field and depth at the
  bid. Kept in: `knowledge/ice-mining.md` (new; it took over the
  unpromoted frontier-ice entry).
- The Nitrogen Vent works as the catalog says: no nitrogen ice in two
  loads read in the hold, 83% water against 59% (one run each). Kept
  in: `knowledge/ice-mining.md`.
- A fit route is bounded by the asks at its station: errors.log
  ENT-026. For every division that writes a fit: size it by the asks
  and fly it one ship at a time where they are few. Kept in: my skill
  mining-chains and `knowledge/ice-mining.md`.
- Gas: the first load at GSC-0050 was 43 neon, 5 plasma, 6 xenon, 6
  chlorine of 65; the estimate counted 13 plasma a load. Kept in:
  unpromoted, until the route's RESULT line.
- Confirmed: station bids move between reads (Synchrony water ice 34 x
  7,470, then 37 x 72, seven minutes apart), so a sale reads its book.
- Open: why the Cryogenic Reserve run could not dock for its sale.

## Cross-links

- `reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md` -- the fleet report in force
- `reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md` -- my previous report
- `game/routes/plans/miner.json` -- the plan, with `planned`
- `game/routes/guidebook/mining.md` -- sections 5 to 7: fits, tests, open tests
- `game/routes/mine-wolf-1061-vent.json`, `fit-gas-harvester.json`, `mine-gsc-0050-gas-plume.json` -- the routes written this turn
- `communications/errors.log` -- ENT-026
- `communications/requests.log` -- ENT-068, ENT-069, ENT-078 and the answers ENT-074, ENT-075
