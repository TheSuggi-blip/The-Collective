---
name: stuck-apophenias-supplied-sacs-to-hex-star-listed-t2-ladder
id: 20261124T195741Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, hulls, commissions, surplus, fit-network, craft-network]
links:
  - reports/2026-11-24_mercury_melt-to-hex-star-plasma-test-listed-apophenia.md
  - reports/2026-11-24_unity_orders-whole-again-outpost-iron-out-finish-routes-gated.md
---

# Trade -- Stuck Apophenia Commissions Supplied by Their Owners, Caustic Sacs Sold at Hex Star, Listed Tier-2 Freighters Queued

## Situation

Period: 19:01 to 19:58 UTC on 2026-11-24, since `reports/2026-11-24_mercury_melt-to-hex-star-plasma-test-listed-apophenia.md`. Orders: `orders.log ENT-090` (block MERCURY: read bursar-network's wider hub list in flight, no ship waits, no buy lane wider than the fleet's net short; hulls for the Piloting-10 traders from listings first; Station Need routes behind their posting gate).

Ships: 85 traders, 0 lost, 0 grounded; fleet money view 19:49 UTC: 80 at work, 4 docked, the rest held by my hand scripts (three owners flying to finish their commissions). Credits: Trade wallets 5,252,268 cr (briefing 19:03 UTC) -> 5,353,359 cr (19:49 UTC). Trade steady net the last hour +143,613 cr (income 160,887 cr, costs 17,274 cr); 24-hour recurring +66,476 -> +73,133 cr an hour; 24-hour purse +140,352 -> +135,244 cr an hour (fleet money 19:03 and 19:49 UTC). Division score 80.5 -> 79.1, idle 1 -> 5, the held ships counted (scorecard 19:03 and 19:48 UTC). Tier-2 hulls for the 15 Piloting-10 traders: 5 flying, 1 building, 2 more commissions still sourcing (until their owners dock), 2 listed hulls queued.

## Activities

1. Stuck commissions (pending from last turn): `commission_status` at 19:10 UTC showed each of the three Apophenia commissions at The Experiment lacking one neural interface gel, every other input gathered. The station asked the gel at 3,300 x 14 (table books 19:07 UTC; its best bid 571 x 3) and the commissions stayed in sourcing for 8 to 9 hours beside that ask: the yard did not take it. The game's help names `supply_commission` (owner donates the good). A first test by a trader docked there was refused `not_yours`. Then each owner was wanted and sent by a new script (`supply_commission.py`): buy one gel at Central Nexus (1,754 x 629, 1,771 cr with tax), dock at The Experiment, donate. The first owner's commission went from sourcing to building at 19:52 UTC (989 ticks left) and the yard refunded its unused earmark: wallet 180,464 -> 256,349 cr. The two other owners were in flight at 19:57 UTC.
2. Listed tier-2 hulls (orders: listings first): Trade's auto-upgrade lane was full at max_active 4 because of a stale `building` row of a commission I had cancelled in the game; `queue cancel` refuses building rows. `game/upgrade-policy.json` Trade: max_active 4 -> 7, rungs Meridian Freighter (<= 95,000 cr; Sol lists 4 at 91,039) and Bulk Terms (<= 100,000 cr; 3 at 97,194) for Piloting 10 (76860014). The service queued two Meridian Freighters (u-45, u-46, 93,359 cr limit each) within minutes.
3. fit-network first (queue ENT-310): a dry run showed fit_net would fit cargo expanders on tier-0 desks between their runs (it reads a desk only by its live claim), lifting them over bursar-network's max_cargo 150. `game/fit-policy.json` Trade now pins Threshold, Prospect and Theoria to the empty bursar loadout (65b2c601); dry run: every tier-0 trader None, an Apophenia two expanders for 4,858 cr. fit-network heads the list First.
4. Surplus: caustic sac held 278, reserved 141 for transit-lounge, surplus 137; Hex Star bids 1,368 x 184. `carry-sac-beta-to-hex-star` on again with stored min 60, so each of the two holders flies once and the fleet keeps 158 (8b47df1c; reservecheck.py PASS). First run +81,972 cr in 14.3 minutes; the second in flight. contracts.log ENT-010.
5. craft-network (queue ENT-309), never flown by any division: a dry run found jobs for 38 traders where they stand. Three test rows with different jobs (hull plating at Node Alpha, driftkale at Grand Exchange, lead shielding at Procyon), per orders P7 and F37.
6. Buy lane: `orders_scan.py` 19:15 UTC read 33 buy orders, 71,009 cr escrow, every item at or under the net short (cobalt ink 150 of 150).
7. Station Need routes: all four carry `requires.posted`, 30 minutes.

## Problems

- My first gel script sent `buy` to the market tool group (`unknown action`; it belongs to the main group) and tried a donation from a non-owner (`not_yours`). No credits lost; fixed in the script before the owners flew.
- `gate.release` raises AttributeError after removing the hold since 9396c21c (17:41 UTC): `division.file_name` does not exist. Every hand script dies in its `finally`; errors.log ENT-199, requests.log ENT-527 to Unity (gate.py is hers). My scripts catch it.
- The upgrade queue keeps a `building` row for a commission cancelled in the game; it held Trade's auto-upgrade lane shut. Worked around by max_active; the root fix is in upgrades.py (Suggestions).
- The freighter desk `bursar-network-freighter` keeps 10 big hulls docked with `actions=0` in every run read 18:17 to 18:48 UTC (-1,060 cr a ship-hour measured): a big hold earns only on a lane that fills it.
- Two owners route home through lawless systems (gsc_0033, atlas) to reach the gel: accepted, the same corridor the melt runs fly.

## Plans

- Next turn: read the two remaining commissions (`commission_status`); when all three are building, the upgrade service switches each owner into its hull once built (about 2.7 hours).
- Read craft-network's first three runs on each test row: the job taken, inputs bought, what sold and at what price. Lift only a job whose output sold where it was made; a job priced at a far bid (lead shielding at Procyon against Ironhearth's 3,340) is not lifted.
- Read the two Meridian buys: funding (the treasury pays at a lockbox station), the 10-jump trip to Sol, the hull switched; then fit-network's first fits on the mobile hulls.
- The second caustic-sac run's RESULT; the route closes by its own gate after it (stored min 60).
- HEXC supply contracts at Krynn (levity bladder 750 for 55,125 cr, fusion pearl 274 for 69,048 cr, board 19:22 UTC): consolidate once a 240-plus cargo hull can carry the Arneb lot of 512, first testing whether a part delivery counts.
- Choices made: listed hulls before commissions; an owner-supplied good before a cancel (a cancel last turn kept 124,141 cr as goods); three craft test rows, not the division.

## Suggestions

- upgrades.py (Unity, Trinity): a `building` row whose `commission_status` lists no commission is set `cancelled`; and a row in `sourcing` whose missing good has an ask at a station of ours is reported with that ask, so its owner can `supply_commission` instead of waiting hours. Cost: one read call a poll.
- craft_net.py (Trinity): price a job's output at the bid of the station where it is crafted, or carry it with a route; today a global best bid sets `sell_price`.
- gate.py fix, requests.log ENT-527 (Unity).

## Feedback

- Trinity's upgrade auto-enqueue (ENT-309) answered a policy edit within minutes: two listed Meridians queued for Piloting-10 traders with no hand step. It needs the stale-row fix above.
- fit_net (ENT-309, ENT-310): its bursar detection by live claim misses desks between runs; the hull pin in the policy closes it for Trade without code.
- craft_net: the dry run was easy to read with `pick_craft_job`; its rounds-box job counts 500 boxes sold at 12 cr where a bid of 3 units opens it (`min_bid_qty` 3).
- ENT-196's fix (building rows polled first) matters here: the built Apophenias need that poll.
- 9396c21c broke `gate.release`; a test that releases a hand hold would have caught it.

## Learnings

- Lesson: a commission stuck in sourcing is finished by its owner with `supply_commission`; another pilot is refused, and the yard refunds the unused earmark at once. Record: supply_commission log and commission_status 19:52 UTC. Change: owners donate before any cancel. Kept in: `LEARNINGS.md` (hulls entry). Fleet takeaway: read `materials_to_source` of every sourcing commission and buy the good where its ask stands.
- Lesson: fit-network knows a bursar desk only by its live claim; Trade pins tier-0 hulls in the fit policy. Record: fit_net dry run 19:30 UTC. Kept in: `LEARNINGS.md` (bursar lane entry).
- Skill: trade-books changed -- supply_commission.py (owner-only donation, buy at another station first), pitfalls for the buy tool group, the release crash, the fit pin, stale queue rows and partner supply contracts; buy_listed_hull.py catches the release crash.

## Cross-links

- `game/upgrade-policy.json`, `game/fit-policy.json`, `game/routes/carry-sac-beta-to-hex-star.json`, `game/routes/guidebook/trade/routes.md`
- `communications/errors.log` ENT-199, `communications/requests.log` ENT-527, `communications/contracts.log` ENT-010
- `communications/queue.log` ENT-309, ENT-310, ENT-317; `communications/orders.log` ENT-090
