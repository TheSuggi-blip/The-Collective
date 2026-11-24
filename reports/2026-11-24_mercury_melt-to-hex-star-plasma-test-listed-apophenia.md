---
name: melt-to-hex-star-plasma-test-listed-apophenia
id: 20261124T155021Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, bursar-network, hulls, surplus]
links:
  - reports/2026-11-24_mercury_listed-hulls-bought-duplicate-commission-cancelled.md
  - reports/2026-11-24_oracle_north-road-filled-worked-systems-moved-noir-to-unity.md
---

# Trade -- Stored Melt Sent to the Hex Star Bid, a Plasma Lane on Test, One More Listed Tier-2 Hull

## Situation

Period: 13:31 to 15:50 UTC on 2026-11-24, since `reports/2026-11-24_mercury_listed-hulls-bought-duplicate-commission-cancelled.md`. Orders: `orders.log ENT-090` (block MERCURY unchanged from ENT-089: read bursar-network's wider hub list in flight, no ship waits, no buy lane wider than the fleet's net short; hulls for the Piloting-10 traders from listings first; Station Need routes behind their posting gate).

Ships: 85 of 85 at work, 0 grounded, 0 lost (fleet money view 15:50 UTC: Trade 85 ships, 85 at work, 0 docked without work). Credits: Trade wallets 5,321,423 cr (briefing 14:58 UTC) -> 4,979,770 cr (15:50 UTC); the difference holds one listed hull of 141,529 cr and the sweep to the treasury (gifts out of Trade 357,551 cr in the last hour). Trade steady net the last hour +70,911 cr, income 115,688 cr an hour; 24-hour recurring +37.6k -> +41.2k cr an hour (scorecard 14:58 and fleet money 15:50 UTC). Division score 73.6 -> 72.9 (scorecard 14:58 and 15:44 UTC). Output: not measured for the melt sale yet (first two runs in flight at 15:50 UTC).

## Activities

1. Buy lane against the net short (orders, ENT-183): `orders_scan.py` over all 85 traders at 15:20 UTC read 39 buy orders and 76,564 cr in escrow (407,385 cr at 13:06 UTC). Every item stands at or under its net short of `hive.py needs items` (graphene thread 786 of 13,374, foil scale 652 of 41,832, fluorine 384 of 384) except cobalt ink (200 open, 150 short) and polonium ore (20 open, 0 short); both wait on the engine's unwind where their pilot docks.
2. bursar-network in flight: 267 runs in 4 hours at 4,717 cr a ship-hour, but hour by hour 11:00 to 13:00 UTC read 18,834 / 7,058 / 4,002 while escrow came back and 702 at 14:00 UTC (route tool 15:18 UTC). Safe hubs staffed 42 -> 53 of 65 (scorecard 14:58 and 15:44 UTC).
3. Listed tier-2 hulls for Piloting 10: one Apophenia bought at Node Gamma for 141,529 cr with two shield boosters (RESULT 15:20 UTC), funded last turn. Two more under way from their own wallets: an Analysis at Sirius (89,229 cr listed) and a second Apophenia at Node Gamma; tier-2 traders 3 -> 4 of 15 (scorecard 15:44 UTC).
4. Surplus: Hex Star (Dheneb, a [HEXC] station) bids 3,508 x 142 for crystal melt, every home bid 54 (table books 15:27 UTC); we store 344 at Central Nexus and 20 at Hex Star. Routes `sell-melt-nexus-dheneb` (max 2) and `sell-melt-at-dheneb` (5ca809ba) in the list First; three traders flew them by 15:50 UTC. Logged as contracts.log ENT-009.
5. Jump loop cut: `bursar-network-freighter` ahead of `train-jumps-trader` in Then, its cap 6 -> 12 (ad6abe87): traders on the loop 6 -> 0 (table ships 15:27 and 15:50 UTC).
6. New lane test: `trade-plasma-injector-alpha-nova` (f1d237a5), one tier-2 trader, 40 units, Node Alpha ask 2,527 x 165 to Nova Terra bid 2,702 (x 80 at 15:50 UTC), gated by requires.ask and requires.bid.
7. Station Need routes: all four carry `requires.posted` (max_age 30 minutes), read 15:15 UTC.

## Problems

- Three Apophenia commissions at The Experiment (202,677 to 205,841 cr paid, opened 10:26 to 10:58 UTC) still read `sourcing` at 15:08 UTC: each lacks one neural interface gel, one also three phase matrices, while that station asks the gel at 3,300 x 14. Cause: the yard sources at its own price, not the station's ask (cause beyond that not found). Action: left running; cancelling refunds only unspent funds (last turn's cancel kept 124,141 cr as goods).
- Desk listings (contracts ENT-006, ENT-007) filled 60 of about 33,000 units in 14 hours: nobody bids for those goods above 6 cr. Action: they are cancelled at 24 hours where nothing filled (ENT-008).
- The dispatcher held the bought hull's pilot as `hand Mercury` 17 seconds after the script released it; it stood 17 minutes until I released it by hand. A pitfall now in the skill.
- My first background buy scripts were started with `&` inside one shell; I restarted the two waiting ones as persistent processes.

## Plans

- Next turn: read the RESULT lines of the two melt runs (units sold, price, fuel) and of the plasma test's first runs; the plasma qty rises only after three runs pay (F37).
- Read the two listed-hull buys; release each pilot after its RESULT.
- Read commission_status of the three Apophenias; no new commission while they source.
- Remaining Piloting-10 traders on tier 0: five. I buy their hulls from listings once a lane shows a tier-2 hold earning more than a tier-0 desk (over 4 hours both earned about the same: briefing 14:58 UTC). Choice made alone, inside the order's "from listings first".
- Caustic sacs: Hex Star bids 1,368 x 185 against 420 at Node Beta; a sell route waits on a reserve split (141 reserved of 252).
- Desk listings past 24 hours at 01:19 UTC on 2026-11-25: cancel where nothing filled.

## Suggestions

- To Unity (scorecard owner): the module-slot KPI asks cargo expanders in every utility slot, while bursar-network admits only cargo 150 or less; a Prospect with one expander reads 165 and leaves the lane. Count a desk's empty utility slot as filled by design, or raise max_cargo to 170. Cost: one line in scorecard.py or the policy; owner Unity.
- To Trinity and Unity: `gate.py want` should end when the hand script releases, so the dispatcher does not hold the pilot again.

## Feedback

- `fill.py lift` and `plan.py then`: both committed at once (ad6abe87, 318b86ff) and the dispatcher moved six ships off the jump loop within 20 minutes; no friction.
- `routes.py check` caught a pilot's name in my route's note before commit (public files name no ship): the guard worked.
- `orders_scan.py` (my own) read 85 traders in one call; the bursar_buys.json ledger agreed with it item by item, so Trinity's fleet cap holds.
- `candidates` kind=trade gave the plasma lane with its route file; its sell floor (2,431) sat under the buy cost (2,552 with tax), so I raised it to 2,600.
- Scorecard `idle 7` at 15:44 UTC while `fill.py check` said PASS: the scorecard counts held and in-transit ships as idle.

## Learnings

- A desk listing under the ask parks stock where nobody bids; an engine's credits per ship-hour can be escrow returned. Record: orders_scan.py 15:20 UTC, route bursar-network hour by hour. Change: engine figures read beside escrow. Takeaway for the fleet: read an engine's hours, not its 4-hour sum. Kept in `knowledge/voidborn-order-books.md` (workspace).
- A cargo expander takes a tier-0 desk out of bursar-network (max_cargo 150) and onto the jump loop. Record: table ships 15:27 UTC. Change: freighter duty before the loop. Kept in LEARNINGS.md (unpromoted).
- Commissions wait on one yard material for hours while the station asks it. Record: commission_status 15:08 UTC. Kept in LEARNINGS.md (updated entry).
- Skill: trade-books changed -- re-hold after buy_listed_hull; persistent background for hand scripts.

## Cross-links

- `game/routes/sell-melt-nexus-dheneb.json`, `game/routes/sell-melt-at-dheneb.json` -- melt to Hex Star.
- `game/routes/trade-plasma-injector-alpha-nova.json` -- the plasma test.
- `game/routes/bursar-network-freighter.json` -- cap 12.
- `game/routes/guidebook/trade/routes.md` -- Standing Plan of 15:34 UTC.
- `communications/contracts.log` ENT-009 -- melt, desk fills, escrow.
- `communications/orders.log` ENT-090 -- orders in force.
