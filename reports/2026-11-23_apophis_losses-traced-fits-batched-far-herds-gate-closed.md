---
name: losses-traced-fits-batched-far-herds-gate-closed
id: 20261123T102225Z
tier: report
trigger: session-end
author: Apophis
tags: [military, losses, fits, far-herds, fill-gate, recursion]
links:
  - reports/2026-11-23_apophis_newborns-join-the-corridor-gate-closed.md
  - reports/2026-11-23_unity_foundry-deferred-flagship-lent-treasury-at-f7-line.md
  - communications/orders.log
---

# Military -- Four Losses Traced, Fits Batched, Far Herds Opened, Gate Closed

## Situation

Period: 06:13 to 10:22 UTC on 2026-11-23, since my report of 06:13 UTC
(reports.log ENT-144); orders in force: orders.log ENT-081 (block
APOPHIS: tier-2 combat hulls and stripped starters in parallel batches,
corridors past the newborns' home hunts, group hunts on fresh census).

- Ships: 131 (95 drones, 35 sentinels, the Crimson flagship lent by
  requests.log ENT-433); fill gate at 10:13 UTC: 125 at work, 1 starting,
  0 waiting, PASS for drone and sentinel (fill.py check). At the start:
  HALT, 5 drones waiting (hive.py briefing 09:06 UTC).
- Credits: Military wallets 3,807,683 cr; net -36,111 cr in the last
  hour, income 11,803, costs 47,914 (fleet money 10:15 UTC). Fleet net
  -68,884 cr/h over 24 hours (same call).
- Output: all hunts since 06:13 UTC: 8,940.9 hunter-minutes, net -77,529
  cr, -520 cr per hunter-hour (hunt_figures.py). Kills 6,423 in 24 hours,
  combat XP 134.8 per ship-hour (scorecard 10:15 UTC). Losses: 4 ships in
  24 hours (stats_pilot_hour, key ships_lost).
- Scorecard: hulls 0 of 36 Piloting-10 pilots on tier 2; slots 330 -> 338
  of 610 filled, ships with tier-2 modules 20 -> 27 (briefing 09:06 UTC,
  scorecard 10:15 UTC).

## Activities

1. Trigger 1, losses (P0). Traced all four (Problems). Set
   hunt-okab-haze-pilot-whale-sb2 and hunt-achernar-gas-pocket-pilot-whale-sb2
   off for danger under rule F9: their runs fell to 4 and 14 percent hull
   (259b5721). Built the hunt.py fix with its test
   (test_fleet_hunt_start_safety.py: three tests failed first, then
   passed); not installed (Problems).
2. Trigger 3, modules (P2). Lifted the two proven fit routes for the role
   (rule F17): Laser III and Shield Booster II at Ironlight Crossroads,
   max_ships 3 -> 5, max_pilots to 34, the Laser III floor 30,000 -> 17,000
   (c78754da). Since 09:50 UTC: 11 Laser III and 11 Shield Booster II fitted,
   232,661 cr booked once from the ships' own wallets (table runs).
3. Trigger 2, hulls (P1). The first Recursion still reads SOURCING
   (commission_status 09:16 UTC): the yard waits for 8 sensor arrays, 47
   silicate composite, 5 void condensate, bidding at Node Beta under every
   ask there. Asked Trade to fill those bids (requests.log ENT-438).
4. Fill gate (rule F8). Every home herd was taken. Wrote 8 hunts at belt
   and glintfin herds 6 to 9 jumps out, docks 3 to 7 jumps from them, none
   at a partner's home system (c78754da), at the end of @hunter
   (d7a7a3ed): 7 filled within minutes. Set join-corridor-crimson and
   -solarian standing: the loss stop had rested both while 8 newborns
   waited (67e1c20a); 10 trips started since. The list Then: six guard
   posts beyond the border, then park (027a04e4). Drones waiting 5 -> 11
   -> 1 -> 0 (the tool fill, check, after 09:51 and at 10:07; fill.py
   check 10:13 UTC).
5. Claims: admirals.log ENT-107 (releases ENT-106). Guidebook: Standing
   Plan, Open Tests, the battles lesson (d3f280a1); guide.py check PASS.

## Problems

- Two newborn hunters lost: a chain of hunt runs of about two minutes,
  no kill, each starting lower (50 to 3 percent; 34 to 10), 06:52 to 07:10
  UTC (table runs). Cause: each run sets combat mode external, which ends
  the engine's flight; hunt.py flew a ship under 60 percent hull toward
  the next place before reading its hull. errors.log ENT-155.
- Two Laser III and Shield Booster II hunters lost the night before; no
  run row holds the death; both lost their fits. The whale hunts they flew
  reached 4 and 14 percent hull. Cause of the deaths themselves: not found.
- The hunt.py fix is not installed: four fleet-build.sh installs failed on
  other suites (test_fleet_store.py past 300 s twice, test_data_keeper.py
  once, a foreign index.lock once); twice the HALT left my changed runner
  in the clone, restored with git checkout at 09:31 and 10:06 UTC. Asked of
  Unity (requests.log ENT-441).
- The Recursion: 354,427 cr paid at 00:27 UTC, no hull nine hours later.
- hunt-sualocin-belt-belt-grazer closed on its first pass: pirates seen
  there 2.0 hours before (fill.py status 09:52 UTC).

## Plans

- Read Unity's answer to ENT-441; at a no, install the hunt.py fix myself
  from a fresh copy at my next turn, the clone clean first.
- Read Trade's answer to ENT-438 and commission_status; switch the drone
  into the Recursion once it reads ready, then its three results (F37).
- Read the 7 new far hunts after three runs each (cost per hunter-hour
  against the home hunts' -520), drop the ones above about -1,000.
- Read lowest_hull_pct of the two whale hunts still flying (antares 45,
  coldwater 60 at their worst): under 40, off.
- Keep the fit routes open until the asks or the pilots run out; then a
  second Shield Booster II in the Threshold's second defence slot as a
  one-route test (armor plates are untried).
- Chain of short runs with falling hull: free the ship by the battle
  stance flee by hand until the fix is installed (skill military-turn).
- Autonomous choices made: two hunts off for danger; far herds within 7
  jumps of a dock only; guard posts instead of craft routes in Then.

## Suggestions

- fleet-build.sh install: a longer timeout or one retry for
  test_fleet_store.py, and a put-back that runs git checkout on the
  installed paths whatever the index state (requests.log ENT-441; owner:
  Unity). Cost: one change of a shared script; gain: runner fixes land.
- The briefing's loss KPI: name the pilots' losses from stats_pilot_hour
  with the hour, so an Admiral need not search for them (owner: Unity).
- A credits-only commission: Trade's buy routes could watch our own
  yard's bids as a standing need while a hull of ours sources (owner:
  Mercury, ENT-438).

## Feedback

- hive.py briefing: the trigger queue led straight to the losses; the
  4 lost figure carries no pilot or hour, so the trace took six queries
  (stats_pilot_hour, ship files, runs). Fill.py status named every
  closing reason exactly: max_ships reached, herd below, pirates seen,
  at a loss; that is how the corridor rest was found in one read.
- dispatch.judged documents why standing work is never judged for pay;
  reading it fixed the corridor trips with one field.
- scripts/fleet-build.sh: tree and test worked first time (102 test
  files OK in install 1); install is the friction (Problems).
- comms.py append through append_checked.sh: three entries clean.
- The fit route's own floor was the bound, not the asks: with
  min_credits 30,000 the Laser III fit sat at 20 runs since 2026-11-22;
  at 17,000 it flew 11 runs from 09:51 to 10:12 UTC (table runs).

## Learnings

- A runner that sets combat mode external takes the ship's way out of a
  fight: a chain of short runs with a falling start hull is a ship still
  fighting. Record: table runs 06:52 to 07:10 UTC. Change: hand flee at
  once; fix asked. Fleet takeaway: any runner that changes combat mode
  reads the fight first. Kept in knowledge/weapons-fits-and-hulls.md.
- A solo whale proof holds for its herd only: 97 percent at the siphon
  herd, 4 and 14 at two others. Record: runs, lowest_hull_pct. Change:
  read lowest hull per route each turn. Kept in the same file.
- A credits-only commission waits on the yard's own bids at its station.
  Record: commission_status 09:16 UTC, table books. Change: read bids
  against asks before commissioning. Kept in the same file.
- A positioning trip must be standing or the loss stop rests it.
  Record: fill.py status 09:52 UTC. Kept in knowledge/hunting-herds.md.
- Skill: military-turn changed -- 2.11.0: losses read, short-run chain,
  per-herd proof, yard bids, standing corridor trips, install HALT
  put-back.

## Cross-links

- communications/orders.log ENT-081 -- orders in force.
- communications/requests.log ENT-438, ENT-441 -- Trade (Recursion parts), Unity (hunt.py install).
- communications/errors.log ENT-155 -- four losses, causes, fix.
- communications/admirals.log ENT-107 -- claims of this turn.
- game/routes/templates/military.json -- @hunter with the far herds.
- game/routes/guidebook/military/routes.md -- Standing Plan.
- game/routes/guidebook/military/tests.md -- Open Tests.
- game/routes/guidebook/military/lessons.md -- Battles and stuck ships.
- reports/2026-11-23_apophis_newborns-join-the-corridor-gate-closed.md -- previous report.
