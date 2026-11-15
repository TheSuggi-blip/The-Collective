---
name: craft-free-bids-thin-stored-ore-waits
id: 20261115T215342Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, crafting, storage, fuel, turn-t5]
links:
  - reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md
  - reports/2026-11-15_apollo_stored-ore-unbid-ferrous-slugs-the-way-out.md
  - game/routes/guidebook/logistics.md
  - game/routes/plans/hauler.json
---

# Logistics -- Crafting From Storage Is Free, but No Bid Takes Our Ore: It Waits, and the Haulers Fly the One-Time Missions

## Situation

Period: from my previous report,
`reports/2026-11-15_apollo_stored-ore-unbid-ferrous-slugs-the-way-out.md`
(19:38 UTC), to 2026-11-15 21:53 UTC. It is the first turn in which the
division is mine to command (scheduled run turn-apollo, started 21:14
UTC).

Orders in force: `communications/orders.log` ENT-005 (turn T5, from
21:20 UTC), the block APOLLO: turn what lies in storage into credits,
fly one craft by hand with one hauler and write down each call, work
out the fuel a starter burns per jump, say which station should be the
fleet's storage home, carry what others ask. ENT-006 came in force at
21:50 UTC during the run (turn T6): my block is unchanged; the census
of the frontier stands in every plan and the report names what the
frontier holds for the division.

```
Ships: 20/20 active, grounded: 0, lost: 0
Credits: start 498,940, end 586,889, net +87,949 (one-time +96,000; without it -8,051)
Output: 1 hand craft chain (2 steel plate, 5 ferrous slug cases, 1 copper wiring); 10 iron ore sold from storage, +20 cr
Source: start from my previous report; end and CPH from data/fleet/fleet.json 21:52:40 UTC; one-time from data/fleet/onetime.json (hauler rows since 19:37 UTC)
```

The fleet file read Logistics at -2,798 cr per hour without one-time
money over the last 60 minutes, 20 cr earned per hour (the hand sale),
and no ship idle (21:52 UTC). The one-time money of the period:
Crystal Delivery 70,000, Synchrony Relay Run 25,000, First Steps in
the Void 1,000. The storage book (`ledger.py show all`, 21:26 UTC, 88
of 146 pilots read) holds 30,160 iron ore and 21,315 copper ore for
the fleet, of which Logistics holds 10,735 iron and 5,707 copper at
Central Nexus, Node Beta and Synchrony Hub. At the end of the run ten
haulers flew the one-time mining-missions circuit, two the first-steps
circuit (started before I took it out), and the rest waited docked at
Central Nexus for the next open route.

## Activities

The craft by hand (the order's test). One hauler docked at Central
Nexus, its own ore in storage there, 21:23 to 21:26 UTC; every call
and answer is in the guidebook, section 7, for the runner's craft step.
`dry_run` quotes cost nothing: the Station Workshop makes 1 steel plate
from 10 iron ore, 1 copper wiring from 8 copper ore, 5 ferrous slug
cases from 2 plate and 3 iron ore, each at 0 cr; the rented refinery
and wire mill make 2 plate from 5 iron for 19 cr and 2 wiring from 4
copper for 17 cr. The real jobs (2 plate, then 5 cases and 1 wiring)
answered with a job id and were in storage within 35 s. Then `sell`
with an empty hold sold 10 iron ore out of storage into the station's
bid at 2 cr: +20 cr in 3.0 minutes docked, no fuel, +400 cr per
ship-hour, capped by a bid of 10 units. The ship was released docked.

What each stored good is worth made into something (the recipes of
release 0.717.0, 892, read through the gate; the six books by depth at
the best price): raw iron 2 cr into bids of 10 to 65 units; iron as
steel plate 1 cr per ore (the 10 cr bid for 50 plates was gone at
21:22 UTC); iron as slug cases 3.3 cr per ore for 8 cases, then 0.4;
copper as wiring 0.25 cr per ore at The Experiment, or about 1.1 where
it replaces Mercury's 9 cr purchase; raw copper 0, no bid at any of
our stations. Knowledge file `stored-ore-worth.md`.

Fuel per jump, for every Admiral. All 146 ship files sampled every 10 s
from 21:30 to 21:45 UTC, the refuel billed at arrival for ships that
left full: a hop of one jump 2 units (115 of 116 hops), two jumps 3,
three jumps 5; 11 to 15 cr a unit by station. Central Nexus to Node
Beta and back costs 48 cr. Guidebook section 6.

Storage home: Central Nexus (guidebook section 8): every pilot's home
and park dock, where a waiting ship crafts for free; 440 items bid
there, the most of our inner stations; one jump from Node Beta.

The plan: voidborn-first-steps out at 21:32 UTC (Acubens Belt read 0
carbon at 21:01 UTC; the 21:02 run lost 109 cr), voidborn-concurrent at
the head at 21:51 UTC on Mercury's test (2,950 cr a run, nothing
bought; up to 20 runs for the haulers). One notice: queue.log ENT-039
(sale from storage; the station bid drains). Requests of other
divisions to carry: none addressed to me.

## Problems

Credits recovered from stored goods: 20 cr. The cause is demand, not
the work: no bid in our space takes ore or what ore makes in depth, and
the one station bid that took our iron emptied (20 units at 21:22, 10
at 21:25, none at 21:33 UTC) and had not refilled 8 minutes later.

My previous report and requests.log ENT-019 read `buy_quantity`, the
total of every bid level, as the depth at the best price: "15 cr for
322 slug cases, about 4,800 cr" is 15 cr for 8. No credit was lost.
Cause and fix: errors.log ENT-018 (my script now prints the depth).

The division still lost money without its one-time rewards: -8,051 cr
over the period. The finished runs of my haulers since 19:37 UTC
(`data/routes/runs.jsonl`): the three mine routes 40 runs -4,149 cr,
before mining ended at 21:00 UTC; park 19 runs -1,352 cr, the fuel to
fly home once; first-steps 3 runs -327 cr without its one reward.

Two haulers started voidborn-first-steps at 21:24 UTC, before I took
it out; their runners finish the step, up to 20 minutes of fuel for no
reward (about 110 cr each at the 21:02 run's rate). Two hand calls were
refused as busy when the dispatcher took the new haulers onto a lifted
route: the lock worked; I hold a ship first now. No ship was lost or
damaged; no hand hold of mine is left (orders files, 21:51 UTC).

## Plans

Inside orders.log ENT-006, in this order:

1. The one-time missions first, flown by the dispatcher along my plan:
   Concurrent Approval for every hauler (2,950 cr a run, nothing
   bought), then the mining missions for those that hold them. I read
   the first hauler's RESULT line of voidborn-concurrent next turn and
   take the route out if it does not pay.
2. Market Participation: Selling (1,000 cr once) for the 7 haulers that
   hold it, by hand, docked at Central Nexus after their circuit: a
   view_market first, and 10 units of what they store sold only into a
   bid that has them at the best price. If no stored good has such a
   bid, Mercury's way (queue.log ENT-038: buy 10 vanadium ore at 60 cr,
   sell at 1 cr, about 404 cr left of the reward) is one ship, one test.
3. The stored ore waits where it lies: no fuel spent to move it and no
   sale under a standing bid (F12). It moves when a bid with depth or a
   fleet need appears: a faction facility, a base (goal step 3), or a
   buyer the frontier census finds.
4. The craft-and-sell route, once the circuit runner has its craft step
   (Unity, by 2026-11-16 12:00 UTC): only where the depth at the best
   bid pays the round trip of section 6 of the guidebook.
5. The frontier: 17 lawless systems read by 21:51 UTC, none with a
   station (`data/scouting/`). There is nothing to store, refuel or sell
   out there yet; a hauler goes only when the census shows a field or a
   bid worth carrying for, one ship, hold empty (F13).
6. Watch the station bids for a refill rate in `data/market/history.jsonl`
   across a day; it decides whether thin bids are a stream or a pool.

My own choices: Central Nexus as the storage home, Concurrent Approval
at the head, no haul of ore.

## Suggestions

- A route stop that sells from storage (Unity's to decide): the circuit
  runner sells only what the hold carries (`route_run.py` line 245),
  while the game's `sell` takes storage too. With it Market
  Participation could be a route for all 52 pilots that hold it, where a
  bid with depth stands. Cost: a few lines and a test, beside the depth
  change already accepted (requests.log ENT-044).
- The faction's storage home at Central Nexus when shared storage comes
  (orders F11, Suggi's and the Fleet Admiral's): every ship parks there
  and the workshop is free there. Cost: none until the storage is built.
- The fleet's 51,475 units of iron and copper ore (88 of 146 pilots read) kept, not sold into
  2 cr pools: they cost nothing in storage and are the inputs of steel
  plate and wiring that facilities and a base will need. The Fleet
  Admiral's to confirm.

## Learnings

- Stored ore is worth almost nothing in our space, and the limit is
  demand, never the craft: workshop crafts cost 0 cr and finish within
  35 s, while the best bids for ore and its products are 8 to 65 units
  deep (hand test and books, 21:11 to 21:33 UTC). Logistics no longer
  plans a haul from a price; it plans from the depth at that price, and
  keeps the ore. Kept in: `knowledge/stored-ore-worth.md`. For the
  fleet: any chain is costed with `best_buy_qty` read live.
- A station-owned bid is a pool, not a stream: the iron ore bid at
  Central Nexus emptied in 11 minutes and was not back 8 minutes later;
  the station then sold our ore on at 2 cr. One reading; the refill
  rate stays an open question.
- Fuel is about n+1 units for a hop of n jumps, billed at the arrival
  station (116 one-jump hops, 21:30 to 21:45 UTC). The game's bill is
  the measure; a fuel gauge read between samples missed the last leg.
  Kept in: `knowledge/fuel-per-hop.md`; guidebook section 6 for every
  Admiral.
- `sell` takes storage when the hold lacks the goods, and the
  dispatcher fills a lifted route within seconds: hold a ship before a
  hand test. Kept in my skill logistics-stock.
- My mistake of the period was the fleet's recurring class, a field
  read by its name (errors.log ENT-018); the fix is in the script, so
  it fires by itself. The frontier holds nothing for Logistics yet: no
  station in 17 systems.

## Cross-links

- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- the plan this period ran under
- `reports/2026-11-15_apollo_stored-ore-unbid-ferrous-slugs-the-way-out.md` -- my previous report, the slug figure corrected here
- `game/routes/guidebook/logistics.md` -- the craft calls, fuel per hop, storage home
- `game/routes/plans/hauler.json` -- the plan in force and what is planned
- `communications/errors.log` -- ENT-018, the depth misread
- `communications/queue.log` -- ENT-037 (Zero, the depth field), ENT-038 (Mercury, Concurrent Approval), ENT-039 (mine)
- `communications/orders.log` -- ENT-005 and ENT-006
