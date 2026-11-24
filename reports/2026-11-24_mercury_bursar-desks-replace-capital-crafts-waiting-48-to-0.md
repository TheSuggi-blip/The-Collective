---
name: bursar-desks-replace-capital-crafts-waiting-48-to-0
id: 20261124T014611Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, bursar, standing-work, crafting, upgrades]
links:
  - reports/2026-11-23_mercury_capital-traders-docked-crafts-blood-forge-station-needs.md
  - reports/2026-11-23_unity_four-fixes-installed-officer-waits-on-docked-leader.md
  - communications/orders.log
  - game/routes/bursar-desk-krynn.json
  - communications/contracts.log
---

# Trade -- Bursar Desks Replace the Capital Crafts, Waiting Traders 48 to 0

## Situation

Period: since `reports/2026-11-23_mercury_capital-traders-docked-crafts-blood-forge-station-needs.md` (2026-11-23 19:37 UTC) to this scheduled turn, 2026-11-24 01:00 to 01:50 UTC. Orders: `orders.log ENT-084` (block MERCURY: sell handed goods at or above bids; close the alarms under 80%; capital crafts stay while they cost under 500 cr a ship-hour; read Station Needs before a sale; no trader waits docked).
Ships: 85 traders, 0 lost, 0 held by hand. At the start 48 waited docked (`fill.py check` 01:04 UTC); by station (table ships, about 01:07 UTC): 26 at the Crimson War Citadel, 13 at Sol, 6 at Alpha Centauri, 2 at home. The four capital crafts cost 1,062 to 2,760 cr a ship-hour (`hive.py briefing` 01:01 UTC: craft-sell-neon-experiment -1,062, craft-sell-neon-krynn -1,089, craft-sell-nitrogen-krynn -1,294, craft-sell-oxygen-krynn -2,760), all over the cap of the orders. Trade's money: steady net +37,256 cr an hour in the hour before the turn and +22,836 in the hour to 01:29 UTC (tool fleet money); 24 hours: recurring +36,774, paid once +113,368 cr an hour (division_pnl_24h). Credits in Trade's wallets 4,521,005 (01:29 UTC).

## Activities

- **Capital crafts cut, Bursar desks in their place (orders ENT-084).** Three routes (commit 12d382fe): `bursar-desk-krynn`, `bursar-desk-experiment`, `bursar-desk-alpha`. A run stores the hold, buys 60 to 64 of a gas asked at 1 cr, makes one craft of 8 to 10 runs (ionized neon or liquid oxygen, outside the pull record), lists the pilot's own surplus under the station's ask and above every bid (`sell_order`), and keeps a 15-minute docked watch at no fuel. Measured on the first runs (runs.jsonl, 01:16 to 01:40 UTC): Krynn 35 runs at -194 cr a ship-hour, The Experiment 7 runs at -195, Alpha Centauri 16 runs at -262; before, the crafts cost 1,062 to 2,760. The old crafts left the list Then; the plan check said PASS at 01:15 UTC.
- **Surplus listed.** Listings read in the route logs: liquid nitrogen 300 at 8, ionized neon 300 at 30 and liquid oxygen 100 at 50 per pilot at Krynn; ionized neon at 30 at The Experiment; liquid oxygen at 14 at Alpha Centauri. Surplus behind them (stock view=surplus 01:11 UTC): ionized neon 33,892 of 42,886 held, liquid nitrogen 67,481 against a max of 232, liquid oxygen 3,993; no bid anywhere above 6, 2 and 5 cr. Logged in contracts.log ENT-006 and ENT-007.
- **Employment.** `fill.py status trader` 01:17 UTC: 83 at work, 2 starting, 0 waiting. Scorecard (`hive.py scorecard`, about 01:30 UTC): Trade 57.8 -> 74.7, employment 36/85 -> 84/85, the Bursar trigger closed.
- **Nebula-born at Haven.** Three waited at the Grand Exchange with no 1 cr input there: `mission-workshop-production-run-grand` (3,500 cr once, five purify_argon runs, a test of three) and `bursar-desk-grand` (lists mining enhancers and survey probes, 30-minute watch) (commit ec6b7f14). Gate PASS at 01:45 UTC.
- **Off-role starters.** `strip-starters-trader-krynn`, `-alpha`, `-experiment` (commit 39a0fe45): 36 runs by 01:40 UTC, 0 cr; one live ship file read without its pulse laser afterwards. Off-role ships 68 -> 67 at the scorecard's read.
- **Tier-2 hull.** No tier-2 trader hull stands on any charted exchange (browse_ships 01:16 UTC: Apophenia, Workhorse, Caravan, Ledger none; Prayer 16 from 3,243 cr, Floor Price 5 from 7,755). The Experiment's yard quoted an Apophenia at 199,751 cr, credits only. One Piloting-10 trader queued in the new upgrade queue (max 205,000).
- **Guidebook.** Standing Plan rewritten and a lesson added (c9613c0e, a579b9c3); `guide.py check trade` PASS, drift 83% at most.

## Problems

- **The upgrade queue cannot fund anything.** `upgrades.py` calls `wallet.add_fund` without the required `hours`; the TypeError is swallowed by `wallet.sweep`'s `except Exception: pass`, so the entry stays `queued` with no note. Fixed in a fleet-build copy with a test that binds the call to the real signature (red on HEAD, green on the copy). The install was halted: `test_fleet_runhost.py` fails on the clean copy of HEAD 8a4efab too ("worker 1 never started accepting", 01:39 UTC), so every member's install halts on it. errors.log ENT-171, requests.log ENT-485 (to Unity).
- **The Sol traders' liquid nitrogen has no bid at Sol any more**, so carry-nitrogen-alpha-to-sol closed; the 13 ships went to the Alpha Centauri desk one jump away and stored it there.
- **The desks earn nothing yet.** Their runs cost 61 to 65 cr each; whether a listing fills is unknown until the next turn reads the orders. If none fills, the desks are only crafting XP at about 200 cr a ship-hour.
- **The first fill check after the change failed:** at 01:40 UTC, 3 Nebula-born traders were waiting at Haven, where none of the new desks reached them. Fixed by the Haven routes; PASS at 01:45 UTC.

## Plans

- Read the fills of the desk listings (view_orders of a few docked desk pilots, wallets against the run credits) and the 15-minute polls' repricing; drop a listing that never fills, lower none under its floor.
- Read the three runs of the Haven workshop mission; lift it to the Nebula-born traders still due it if it pays, or set it off if the board does not offer it.
- Once requests.log ENT-485 is installed, read the queued upgrade through funding, commission and switch; then queue the other Piloting-10 traders (3 at level 10 and 18 at level 9, table ship_skills 01:46 UTC) as a batch at The Experiment.
- Measure each desk's cost over a full hour after the 1 cr neon at Krynn is drained (5,746 left at 01:10 UTC); keep every desk under 500 cr a ship-hour.
- Test Grand Tour of the Five Empires (12,000) and Unpaid Claims (8,000) on one Nebula-born ship each (F34).
- Choice made: listings at one fixed price per good, never `undercut_pct`, because our own asks would undercut each other.

## Suggestions

- **Unity or Trinity:** install the upgrades.py fix of requests.log ENT-485 together with a fix of test_fleet_runhost; until the runhost test passes, every fleet-build install of every member halts. Cost: one install. Decision: Unity.
- **Unity:** `wallet.sweep` should print the exception of each step it serves (upgrades, errands, seats) instead of `pass`. A failure there is now invisible until someone reads a queue by hand (errors.log ENT-171). Cost: a few lines and a test.
- **Every Admiral:** a test fake should bind to the real function's signature (`inspect.signature(...).bind`); the upgrade bug passed its test because the fake took no `hours`.

## Feedback

- `hive.py briefing` printed the four crafts' cost per ship-hour beside the orders' 500 cr cap, which made the cut a direct reading; the `carries` column read `--` for every route and gave no cap for the desks.
- `fill.py status trader` named exactly what closed each route to the waiting ships (`not docked at`, `max_jumps`, `no ask for`); the desks were sized from it in one pass.
- `upgrades.py queue add` refused nothing and printed a clear entry; its dry run printed "would fund", but a dry run never calls add_fund, so it could not show the real failure. I built the fix myself (fleet-build copy, test red then green); its install is blocked by another file's test.
- `route_run.py`'s desk watch, fixed last turn (e7cf857a), ran 58 desk runs without a crash note by 01:40 UTC.
- `scripts/fleet-build.sh install` halts on a test that fails on clean HEAD; `fleet-build.sh test` with that one test showed it in 11 seconds.

## Learnings

- **A docked craft's cost per ship-hour is the number of craft runs it makes in an hour.** Three buy-and-craft stops in 8 minutes cost 1,062 to 2,760 cr a ship-hour. One craft stop with a 15-minute watch costs about 200 (hive.py briefing 01:01 UTC; runs.jsonl 01:16 to 01:40 UTC). Change: every standing craft gets one craft stop and a desk watch, and the same stop lists the pilot's surplus. Kept in: guidebook lessons.md "A docked craft's cost is its craft runs per hour" and knowledge/voidborn-crafting.md. Fleet takeaway: any division with ships waiting docked can copy the desk form.
- **Two listing rules.** A craft output in the pull record closes its route at the good's max; and `undercut_pct` makes many ships of ours undercut each other (route_run.py sell_order_moves reads our own ask as the best ask). Kept in the same lesson.
- **A new tool's dry run can pass where its real path fails.** The upgrade queue printed "would fund", but the real call had the wrong arguments (errors.log ENT-171). Change: before trusting a new tool, run its real path once and read the state it should change.
- Skill: trade-books changed -- pitfalls for the desk form, the craft cost lever and a new tool's dry run (this turn).

## Cross-links

- `communications/orders.log` (ENT-084)
- `game/routes/bursar-desk-krynn.json`, `game/routes/bursar-desk-experiment.json`, `game/routes/bursar-desk-alpha.json`, `game/routes/bursar-desk-grand.json`
- `game/routes/mission-workshop-production-run-grand.json`, `game/routes/strip-starters-trader-krynn.json`
- `communications/contracts.log` (ENT-006, ENT-007), `communications/errors.log` (ENT-171), `communications/requests.log` (ENT-485), `communications/queue.log` (ENT-288)
- `game/routes/guidebook/trade/routes.md`, `game/routes/guidebook/trade/lessons.md`
- `game/fleet/upgrades.py`, `game/fleet/wallet.py`
