---
name: every-trader-operating-network-commerce-paid
id: 20261122T040634Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, standing-work]
links:
  - reports/2026-11-22_mercury_far-gaps-sized-from-home-two-far-tests-flying.md
  - reports/2026-11-22_unity_atria-funded-requests-answered-trinity-build-checked.md
  - communications/orders.log
---

# Trade -- Every Trader Operating; Network Commerce Pays, Trade Runs Wait on the Runner

## Situation

Period: since `reports/2026-11-22_mercury_far-gaps-sized-from-home-two-far-tests-flying.md` (turn of 23:30 to 00:25 UTC); this turn 03:31 to 04:3x UTC. Orders: `orders.log` ENT-061 (standing order S5, block MERCURY: every trader operating; P5: sell routes for what other divisions give the receivers).

Ships: 40 of 40 at work at 03:51 UTC and at 04:00 UTC, 0 waiting, 0 lost (`fill.py status trader`; the tool `fleet` view=money). At the turn's start all 40 waited docked (briefing, 03:31 UTC). Credits: 1,816,636 at the last report -> 1,849,028 at 03:31 UTC -> 1,845,666 at about 04:00 UTC (the tool `fleet` view=money, division Trade). Trade steady net the last hour at 04:00 UTC: -1,934 cr (income 2,050, costs 3,984). Fleet steady net: -43,198 cr an hour over 1 hour, -9,875 over 6 hours, +11,814 over 24 hours (same call). Output this turn: one once mission paid 1,500 cr (runs.jsonl, voidborn-network-commerce); one Trade Run handed in for 637 trading XP; 26 chemical liners sold far for 19,734 cr in the last turn's test, read this turn. Fill gate at 04:05 UTC: PASS.

## Activities

S5, every trader operating (orders ENT-061, block MERCURY):
- New standing work `train-jumps-trader`: five jumps through our stations for piloting and navigation, last before park in the list Then. 34 traders took it at 03:51 UTC (data/fleet/orders). Its first runs: 5 stops in 13.4 minutes for -93 cr (runs.jsonl, 03:50 UTC run).
- Missions that pay the trader's skills, in the list First: the two Federation once missions, three ships each (rule F37: once per pilot, no shared buyer), 5 ships flying at 03:51 UTC; `voidborn-network-commerce` (rule F35), written this turn: its first run took 13 minutes and paid 1,500 cr (+960 cr after the freighter's fuel), so I lifted it to 3 ships (commit 3b1aa8c7).
- Trade Runs: the board files name each mission's XP by skill (`data/missions/*.json`): 20 to 40 trading, 80 to 580 piloting, never credits. One trader accepted Trade Run: Cinderspice to Nova Terra Central by hand at 03:48 UTC (292 ticks to finish), bought 10 cinderspice at Central Nexus at 3,011 (30,411 cr with tax, 04:04 UTC), sold them into Nova Terra's bid of 3,017 (+30,170 cr, 04:15 UTC) and handed the mission in by hand at Node Alpha (04:25 UTC). The run: 21 minutes, about -241 cr on the goods before fuel, 637 trading XP (level 3 to 4) and 211 piloting XP (`xpsnap.py diff` against 04:02 UTC). Its RESULT line reads +13,185 cr because the wallet service topped the pilot up after the buy; that is a move between our purses, not income.

Far trade and the receivers (P5):
- The liner test of last turn: 32 bought for 19,618 cr, 26 sold at First Step for 19,734 cr, 6 stored there (runs.jsonl and the pilot's log, 00:05 to 00:31 UTC). Its -84 cr figure is the 6 unsold units, not a loss.
- `carry-lead-beta-to-sirius` and `carry-lead-nexus-to-sirius`: Sirius bids lead ore 40 x 526 (book of 03:49 UTC), for the lead Mining gives the receivers (requests.log ENT-332); in `@trade-sell`.
- `sell-plasma-node-beta` added by `fill.py --write` for a trader's own stored plasma (12 runs of about 900 cr each, the tool `route`).
- Buyers passed on (admirals.log ENT-086): exotic matter 60 x 701 at Node Beta for 270 miners' units no route sells; ember gland 4,978 x 94 at a station of another faction.

## Problems

- The route runner cannot fly a Trade Run. It accepts a mission only by `template_id`, and its `active()` reads only 32-hex mission ids, while a Trade Run's id is its name. The first run passed every stop in 0 minutes for 0 cr (runs.jsonl 03:49 UTC). Cause: the runner's mission parser (game/fleet/route_run.py, lines 536 and 794). Action: the route is `once` and flown by hand, and the fix is asked of the Fleet Admiral (requests.log ENT-335).
- A trader docked 18 jumps out at First Step took the home training loop when its local carry closed (Ramen's Rest's bid read 1,060 x 1 at 03:46 UTC, against my gate of 6 units), and flew home through the lawless west with an empty hold. Cause: my plan gives every ship the same home fallback wherever it stands. Action: a guidebook lesson and a skill pitfall; local fallbacks for far ships next turn.
- I committed a guidebook entry 14 characters over its cap (commit 6726c916): the gate printed HALT, but my commit ran in the same shell line. Cause: a check chained to its action, the class of errors.log ENT-120. Action: refined at 6f53f6e8; `guide_commit.sh` in my skill commits only on the gate's PASS (errors.log ENT-124).
- My first hand hold ended with the first hand run, and the dispatcher put the test ship on the loop for 13 minutes. Cause: `route_run.py` gives the pilot back at its end. Action: the later steps chained in one shell (`catch.py`, route, hand-in); a skill pitfall.

## Plans

- Fly the cinderspice Trade Run twice more by hand (rule F37: one buyer, one ship three times) while both ends stand, until the runner fix lands (requests.log ENT-335); then an `accept` stop takes Trade Runs on every far haul with a bid at its end.
- Test the Trading trainer it showed: a dear good bought and sold near one price trains Trading at about 1 XP per 100 cr each way, for the fees alone.
- Read the Federation once missions: whether docking collects their market data, and what they pay. If three runs pay, every trader gets them in the list First.
- Lift `voidborn-network-commerce` to all 16 pilots left that hold The Collective Provides, once three runs have paid.
- Give far ships local work: a carry or a loop of the stations where they lie, so the home loop never calls them across a lawless road.
- Weigh `train-jumps-trader`'s fuel against the fleet's steady net each turn (`hive.py route train-jumps-trader`).

## Suggestions

- To Unity: a Trade Run step in the runner (requests.log ENT-335). The boards hold 58 trading missions, and most pay 80 to 580 piloting XP for a haul a trader flies anyway. That is the cheapest way I see to Piloting 10 and the Apophenia for the 39 Threshold traders. Cost: one parser change with a test. Decision owner: Unity.
- To Oracle (rule F34, visits are Intel's to test): Local Sector Survey (2,500 cr, 280 piloting XP) and Deep Space Cartography (4,000 cr, 380 piloting XP) stand on 30 boards each, and no route of ours flies them (`game/routes`, grep).

## Feedback

- Unity's loop guard (requests.log ENT-330, dispatch.py since 02:37 UTC): no route of mine looped this turn. Two zero-minute Trade Run runs (03:49, 03:50 UTC) ended without a third.
- `fill.py check` and `fill.py fill` named the one paying route open to ships on standing work (`sell-plasma-node-beta`) and wrote it in one call. That is useful.
- `dispatch.why_not` answered exactly why the liner carry was closed ("best 1060 cr x 1"), but only by importing dispatch.py by hand: the tool `fill` explains only the routes of waiting ships. A why-not for one pilot and one route in the tool `fill` would save a turn's minutes.
- The `briefing`'s EYES & EARS section showed the P1 needs' buy gaps at once; it showed that caustic sac has no ask in any book of ours.

## Learnings

- A Trade Run's board file names its XP by skill (20 to 40 trading, 80 to 580 piloting), and its id is its name, so the runner cannot fly it yet. Record: `data/missions/*.json`; accept by hand at 03:48 UTC. Change: Trade Runs lead the levelling plan once ENT-335 lands. Kept in: `knowledge/voidborn-order-books.md` (workspace).
- A sale trains Trading as a buy does, about 1 XP per 100 cr each way: one Trade Run of 60,581 cr in goods gave 637 trading XP with the mission's 35. Record: `xpsnap.py diff`, 04:2x UTC. Change: a dear good traded near one price is the class trainer; one run, two more to confirm. Kept in: guidebook trade, levelling.
- A far bid read deep can be gone before the load arrives: 26 of 32 sold into a bid read at 238 units, and 1,010 x 10 read 1,060 x 1 an hour later. Record: runs.jsonl 00:30 UTC; `data/market/ramens_rest.json` 03:46 UTC. Change: far loads sized to a share of the depth. Kept in: the same knowledge file.
- A fallback is flown from where the ship stands. Record: data/fleet/orders 03:51 UTC. Fleet takeaway: every Admiral whose ships work far out gives them a local fallback. Kept in: guidebook trade, lessons; LEARNINGS.md (unpromoted).
- Skill: trade-books changed -- Trade Run facts in the boards step; two pitfalls (a hand run gives its pilot back; the list Then flown from where a ship stands).
- Skill: trade-books changed -- guide_commit.sh: the guidebook committed only on the gate's PASS (step 13).

## Cross-links

- `communications/orders.log` ENT-061: the orders of this turn.
- `communications/requests.log` ENT-335: the runner request for Trade Runs.
- `communications/admirals.log` ENT-086: the buyers passed to Mining and Military.
- `communications/errors.log` ENT-124: the gate chained to its commit.
- `game/routes/voidborn-network-commerce.json`, `game/routes/train-jumps-trader.json`, `game/routes/trade-run-cinderspice-nova-terra.json`, `game/routes/carry-lead-beta-to-sirius.json`, `game/routes/carry-liner-first-step-to-ramens.json`: the routes of this turn.
- `game/routes/guidebook/trade/tests.md`, `levelling.md`, `routes.md`, `lessons.md`: the guidebook entries rewritten.
