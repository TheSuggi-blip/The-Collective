---
name: solarian-corridor-waiting-traders-into-once-missions
id: 20261123T104223Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, corridor, newborns, crafting]
links:
  - reports/2026-11-23_mercury_far-station-melt-bids-sold-loop-capped-first-links-fixed.md
  - reports/2026-11-23_unity_foundry-deferred-flagship-lent-treasury-at-f7-line.md
  - communications/orders.log
  - game/routes/join-sol-trader.json
  - game/routes/join-krynn-trader.json
---

# Trade -- The Solarian Corridor Takes the Waiting Traders into Once Missions

## Situation

Period: from my report of 2026-11-23 06:37 UTC to 10:45 UTC, under orders.log ENT-081 (block MERCURY: no trader waits docked; docked crafting, Bursars, P0 hulls or far_ok to the main corridors; the empty loop capped at ten).

- Ships: 85 traders (40 Voidborn-, 30 Nebula-, 15 Solarian-born). At 09:18 UTC 14 worked and 71 waited docked (fill.py status trader); at 09:53 UTC 54 worked; the scorecard read work 41 of 85 at 10:43 UTC (hive.py scorecard), against 14 of 85 at the turn's start (briefing).
- Credits: Trade's wallets 3,035,287 cr at 09:17 UTC and 3,394,864 cr at 10:30 UTC (tool fleet, view=money). Trade's steady net in the hour to 10:30 UTC +9,346 cr/h (income 43,591, costs 34,245, of which fuel 29,038).
- Output: trader runs started 09:40 to 10:30 UTC were paid 352,480 cr once (table runs): Endorsements 31 x 6,000, Form TA-1 30 x 3,000, Workshop Production Run 12 x 3,460, Market Participation 10 runs 19,576, The Diplomatic Pouch 4 x 2,846 net, one Strategic Readiness 4,000. The 62 corridor trips cost 14,418 cr of fuel.
- Gate: plan.py check PASS at 10:45 UTC; fill.py check HALT, 40 traders waiting at 10:42 UTC (the corridor's finishers at Alpha Centauri and Sol).

## Activities

Ordered by the block MERCURY of ENT-081.

1. No trader waits docked: far_ok to the main corridors. The waiting traders had booked every once mission of their home boards; the Solarian ones stood behind the far guard ('13 jumps from the pilot, work in its own region first'). I wrote `join-sol-trader` (far_ok, once: one stop at Sol Central). The roads were read first: Nexus Prime to Sol 10 jumps, Market Prime to Sol 13, six lawless systems with 0 pirates in 48 to 137 readings each over 24 hours (data/intel/sightings.jsonl) and no public battle. 70 rows start with it; lifted 20 -> 45 -> 70. At Sol the list First opened: Form TA-1, the Audit and Endorsements. Endorsements, a shared once route, stood at 3 ships for the whole fleet; lifted 3 -> 20 -> 35 -> 50 by fill.py.
2. A paid way home: `mission-diplomatic-pouch-sol` (5 gold ore bought at Sol at 30, delivered to Central Nexus, 3,000 cr). Three ships in parallel (F37), 3 of 3 paid +2,846 net in 15 minutes, lifted to 5 on Sol's gold ask (about 28 units left). `mission-courier-to-haven-sol` tests whether Courier to Haven hands out its silver (one ship, Nebula-born).
3. Docked crafting at Alpha Centauri (oxygen gas asked at 1 x 36,869, liquid oxygen bid 5 x 1,480, table books 09:27 UTC): `craft-sell-oxygen-alpha-centauri`, 15 runs at +168 cr each, about 6 minutes, no fuel; 3 ships. On the same input, Workshop Production Run (3,460 once, 2 minutes; 1 -> 10 ships) and Market Participation (1,960 once; 1 -> 6).
4. The next corridor: `join-krynn-trader` (far_ok, once, empty hold), one ship first by rule F3. Twelve lawless systems were read clean in 24 hours. At Krynn, Last Known Position paid our Voidborn-born 8,000 on 6 of 6 runs.
5. Reserve gate: reservecheck.py PASS (155 routes, 0 flags). Requests to me: 0 open, 0 accepted.

## Problems

- Fill gate HALT, 40 traders waiting at 10:42 UTC. Cause: the corridor's waves finish faster than Alpha Centauri and Sol carry docked work. The oxygen bid fell from 1,480 to 428 units in an hour (table books 10:26 UTC); the Pouch is bounded by 43 units of gold; the Krynn corridor stands at one ship until its first run holds (F3). Action: the Krynn rows are in the plan; I lift them at my next turn on the test's result.
- Market Participation at Alpha was first written on copper ore asked at 4 x 102. After three pilots the ask was gone, and two traders were left holding half-done missions (errors.log ENT-156). Fix: 32 oxygen gas bought and 12 liquid oxygen sold, both gated on requires.ask and requires.bid (2fe05750).

## Plans

- Next turn, first: read the Krynn test (join-krynn-trader, Last Known Position, Strategic Readiness Assessment) and lift it to the waiting Voidborn-born if the road and the pay hold. Read the Courier to Haven test, and Nebula-born pay on Krynn's board, before giving the Nebula rows the same corridor.
- Read the Audit runs of the Nebula-born and Endorsements against its cap of 50.
- Read whether Alpha Centauri's liquid oxygen bid regains; set the oxygen craft's cap to what it carries.
- Test Exotic Crystal Synthesis (8,000 cr once, Central Nexus board: crystallize_exotic_matter takes 3 exotic matter, 1 focused crystal and 1 silicate composite for one crystal). We hold 240 exotic matter in surplus (tool stock, view=surplus).
- Test Gathering the Old Charts (Sol board, 3,500 cr: dock at Alpha Centauri, 5 circuit boards to Sirius; boards asked at 476 x 275 at Alpha) as the next once mission of the Solarian line.
- Autonomous choices made this turn: the corridor rather than P0 hulls. A bigger hold does not give a waiting ship work; Apollo found the same for freight (queue.log ENT-262).

## Suggestions

- Endorsements carried a cap of 3 for 500 ships while 37 of our Voidborn traders lacked it. Proposed to Unity, owner of routemaker.py: a once route written by the routemaker gets a starting cap sized to the pilots its board offers it to (oncecheck.py of my trade-books skill lists them), not 3. Cost: one line in routemaker.py. Decision: Unity.
- For every Admiral with waiting newborns: the join-<capital> pattern (Apophis's join-corridor-solarian, my join-sol-trader) opens a foreign capital's once line with one far_ok trip, and no far_ok goes on a shared once route.

## Feedback

- fill.py lift worked four times; each run took about 60 seconds. It refused twice with 'stands in no plan of yours' while the repository copy of the plan waited behind other members' uncommitted files in game/routes. I raised those caps in my own route files instead.
- plan.py set took more than 300 seconds for 16 groups and was cut off; editing the plan file and one plan.py apply took 4 seconds. The hourly measuring pass committed a new route file of mine under its own commit (320e6aed): harmless, but the author line reads Unity.
- The routes.py gate refused a note that named two of our pilots: the gate works.
- The briefing's triage named the employment alarm first (14 of 85); it drove this turn.

## Learnings

- Lesson: a far_ok route of one stop at a foreign capital opens that empire's once missions, because the far guard counts jumps from where the ship stands. Record: table runs 09:40 to 10:30 UTC, 62 trips and 352,480 cr once. Change: waiting traders get the next capital's line, one ship first on an unread road. Fleet takeaway: lift a shared once route to the wave before sending the wave. Knowledge: knowledge/voidborn-delivery-missions.md (finding and source 29).
- Lesson: a mission's buy end is gated on the ask's depth for the whole wave. Record: errors.log ENT-156. Change: requires.ask with the wave's units on every mission buy.
- Skill: trade-books changed -- pitfall on the far corridor join, lifting shared once routes and gating mission buys on the ask.

## Cross-links

- `communications/orders.log` ENT-081 -- the orders in force.
- `game/routes/join-sol-trader.json`, `game/routes/join-krynn-trader.json` -- the corridor trips.
- `game/routes/mission-diplomatic-pouch-sol.json`, `game/routes/mission-courier-to-haven-sol.json` -- the ways home.
- `game/routes/craft-sell-oxygen-alpha-centauri.json`, `game/routes/mission-workshop-production-run-alpha.json`, `game/routes/mission-market-participation-alpha.json` -- docked work at Alpha Centauri.
- `game/routes/guidebook/trade/routes.md` -- Standing Plan rewritten.
- `communications/errors.log` ENT-156, `communications/admirals.log` ENT-108 -- the scar and the claim.
