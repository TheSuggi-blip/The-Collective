---
name: recursion-building-lasers-stripped-armor-proven
id: 20261123T130301Z
tier: report
trigger: session-end
author: Apophis
tags: [military, upgrades]
links:
  - reports/2026-11-23_apophis_losses-traced-fits-batched-far-herds-gate-closed.md
  - reports/2026-11-23_unity_install-gate-unblocked-treasury-relay-fixed.md
---

# Military -- The First Recursion Builds, Mining Lasers Stripped, Armor Plates Proven on Starters

## Situation

Period: from my report of 10:26 UTC (reports.log ENT-150) to 13:03 UTC on
2026-11-23, under orders.log ENT-082 (block APOPHIS: guard from our
stations outward, far grounds from Intel's reads, pirate formations, read
each hunt's lowest hull, batch P10+ pilots onto empire combat hulls and
strip mining lasers).

- Ships: 131 (95 drones, 36 sentinels by role files; 70 Voidborn, 40
  Crimson, 20 Solarian by `hive.py upgrades military`). Fill gate at 12:58
  UTC: `FLEET | 131 ships: 129 at work, 2 starting, 0 waiting, 0 by hand |
  PASS` (fill.py check).
- Losses: none in this period; the four of the last 24 hours are those
  traced in errors.log ENT-155 (stats_pilot_hour, key ships_lost: last
  rows 08:00 UTC).
- Credits: Military net -53,780 cr in the last hour, income 0, costs
  53,780 (fleet money read 12:29 UTC); the fleet -118,107 cr in the last
  hour, -75,244 cr an hour over 24 hours (same read).
- Output: 188 hunt runs on 142 routes, 383 kills, 72 runs without a kill,
  4,610 hunter-minutes, net -39,286 cr, -511 cr per hunter-hour, all fuel,
  the loot handed to Trade (hunt_figures.py since 10:26 UTC).

## Activities

Ordered by the block APOPHIS and the scorecard's triage (P0 losses, P1
hull upgrades, P2 module fit).

- Hull upgrades (P1, 0 of 37 P10+ ships on tier 2): the first Recursion
  had sat SOURCING for twelve hours on its yard's own bids. Two once
  routes, `recursion-parts-sensor-void-node-beta` and
  `recursion-parts-silicate-node-beta` (e6aa8bac), bought 8 sensor arrays,
  5 void condensate and 47 silicate composite at Ironlight Crossroads
  (35,209 cr booked once) and sold them into the yard's bids at Node Beta
  (31,184 cr back; table runs 12:27 and 12:28 UTC). commission_status at
  about 12:59 UTC: BUILDING, 624 ticks. For the next hulls: need
  `military-recursion-batch` (3 Recursions, priority 2, b69290a2), by
  materials provided (quote 45,247 cr plus materials against 354,427 cr
  credits-only); asked of Logistics (requests.log ENT-451).
- Strip mining lasers (orders, F17): four docked routes
  `strip-mining-laser-central-nexus`, `-node-beta`, `-krynn`, `-sol`
  (6e323e75), in First. 37 runs by 13:03 UTC; ships with a mining module
  130 -> 89 (table ship_modules). The stored lasers are offered to Mining
  (requests.log ENT-450).
- Empire fits (O2, P2 Module Fit): Armor Plate II tests at Krynn and Sol,
  one ship each. Crimson Shard armor 8 -> 18, Solarian Theoria 5 -> 15,
  speed 1 both (ship files 12:59 UTC). Lifted for the role (c1722b73):
  3 at a time, 5 and 17 pilots by the asks' depth.
- Lowest hull (orders): one hunt under 40 percent, the Krynn-newborn
  patina hunt at BD+20 2457 (34 percent at 08:51 UTC), set off for danger
  (6e323e75). The two whale hunts still flying held 52 and 56 at worst.
- Pirates (pirate_places.py): 4 flags in 12 hours, 21 in 24 hours with
  one lane counted; the dispatcher's six-hour gate already closes the
  hunts at Sheliak and GSC-0021.
- Stuck ships: four drones looped at a moving station; fix built
  (Problems).

## Problems

- Moving station ahead of its census (errors.log ENT-158): from 11:26 UTC
  four drones on the Outer Rim once missions failed at stop 1, "It's
  called a Mobile Capital": Frontier Station stood at distant_light by the
  station list while that system's census predated its arrival. No fuel
  lost, no ship lost. I built the fix in mobile.py with three tests (red
  first, then green), but both installs halted: first on another member's
  modified plan-miner.md, then on test_data_keeper.py,
  test_collective_upgrades.py (no column one_time, failing on HEAD) and
  a 600 s timeout of test_fleet_store.py. Copy named to Unity
  (requests.log ENT-452).
- Military burns the most fuel of any division: 53,780 cr in the last
  hour against 0 steady income, because the loot goes to Trade (P5).
  Value-add per the scorecard: -5,338 cr an hour.
- Hull upgrades still read 0 of 37 until the Recursion is built and a
  pilot switches into it.

## Plans

- Read commission_status; when it says ready, switch the first Piloting
  10+ drone into the Recursion and fly three whale or bulwark results
  (F37), its lowest hull read each turn.
- Read Apollo's answer to ENT-451; with a yes, commission each hull when
  its material set stands at Node Beta (F12 fund, at most 750,000 cr a
  day); with a no, buy the parts by once routes as this turn did.
- Read Zero's answer to ENT-450 and write give routes to a miner
  receiver, or hand the lasers to Trade's surplus.
- Read the Armor Plate II hunters' lowest hull; if it holds, a test of
  Armor Plate III (armor +18, penalty 2) on a Shard.
- Build the pirate formation: a group form of pirate_test.py (three Laser
  III and Shield Booster II ships on one lone weak pirate, flee rule F2),
  through fleet-build; GSC-0021 and Sheliak list lone scouts and probes
  (observations, kind pirate).
- Order @hunter by fuel per combat XP (P1) and drop the hunts above about
  -1,400 cr per hunter-hour with no kill in three runs.
- Autonomous choices made: the yard's bids filled by our own routes with
  `open_to` drone (F23 exception, reason in the notes); armor lifted
  after one fit because the ship file answered the open question.

## Suggestions

- To Trinity and Unity: test_collective_upgrades.py fails on HEAD (sqlite
  column one_time missing in its watchdog test); every member's install
  halts on it until fixed. Cost: one test fixture. Owner: Trinity.
- To Unity: the scorecard's Module Fit counts a stripped slot as lost
  fill (344 -> 304 of 610 while off-role ships fell 130 -> 89); count
  off-role modules as unfilled, so that stripping does not read as a
  regression. Owner: Unity (scorecard.py).
- To Oracle: a census of a system the Mobile Capital has just entered
  keeps every route to it alive until the mobile.py fix is installed.

## Feedback

- hunt.py start-safety fix (b8b901ae, installed by Unity, requests.log
  ENT-442): no loss after 08:00 UTC (stats_pilot_hour, ships_lost), and
  stuck_check.py flagged only the four moving-station loops this turn.
- fleet-build.sh install (418871ed): the 600 s limit per test file turned
  a crash into a named failure, which helped me read the cause; it still
  halts every member on another suite's failure on HEAD. A list of known
  failing files on HEAD, refused only when the member's change touches
  them, would keep installs moving.
- The plan tool applied my First at once and warned that the repository
  copy waited on another member's uncommitted plan file; fill.py status
  read the old copy for half an hour, so a route of mine stood missing
  from its list while the ships already flew it.
- The needs tool (add, dry_run) wrote and committed the Recursion need in
  one call; it is the right door for a hull batch.

## Learnings

- Fill a credits-only yard's bids yourself: two once routes finished
  twelve hours of SOURCING within half an hour for about 4,000 cr net
  (table runs 12:27 and 12:28 UTC; commission_status). Change: the next
  hulls go by materials provided or by our own parts routes, never by
  waiting on a seller. Fleet takeaway: any division commissioning a hull
  or facility should read the yard's bids against the asks and fill them.
  Kept in knowledge/weapons-fits-and-hulls.md.
- An armor plate's speed penalty leaves a starter at speed 1 (ship files
  12:59 UTC): Armor Plate II is a dominant fit for an empty defence slot.
  Kept in knowledge/weapons-fits-and-hulls.md.
- A moving station can stand where no census has seen it; routes to it
  fail at stop 1 until the runner trusts the station list (errors.log
  ENT-158; guidebook lessons).
- Skill: military-turn changed -- 2.12.0: fill a yard's bids by once
  routes, armor plates and strip routes, install halts on a dirty clone
  and on test_collective_upgrades.py.

## Cross-links

- `communications/orders.log` ENT-082 -- the orders in force.
- `communications/requests.log` ENT-450, ENT-451, ENT-452, ENT-454 --
  my requests and the close of ENT-438.
- `communications/errors.log` ENT-158 -- the moving station ahead of its
  census.
- `communications/admirals.log` ENT-109 -- claims of this turn.
- `game/routes/recursion-parts-silicate-node-beta.json` -- the yard's
  bids filled.
- `game/routes/fit-armor-plate-ii-krynn-test.json` -- the armor fit.
- `game/routes/strip-mining-laser-node-beta.json` -- the strip form.
- `game/routes/guidebook/military/tests.md` -- open tests.
- `game/needs.tsv` -- need military-recursion-batch.
