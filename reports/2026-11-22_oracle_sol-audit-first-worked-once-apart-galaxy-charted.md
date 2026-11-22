---
name: sol-audit-first-worked-once-apart-galaxy-charted
id: 20261122T193835Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, missions]
links:
  - reports/2026-11-22_oracle_claimed-hunts-dropped-qualia-verdict-claimed-line.md
  - reports/2026-11-22_unity_one-iron-figure-fund-paid-handed-over-worth.md
---

# Intel -- The Sol Audit Goes First, Once Routes Leave the WORKED Gate, the Galaxy Is Charted

## Situation

Period: since `reports/2026-11-22_oracle_claimed-hunts-dropped-qualia-verdict-claimed-line.md` (15:36 UTC), this turn 19:16 to about 19:45 UTC. Orders: `orders.log ENT-065` (block ORACLE: Ironlight Crossroads' book within three hours, the north road from Atria to Yildun and its choke point, Oakridge's neighbours, storm headings and survey power, explore further out, hunt on the way).
Ships: 30 of 30 scouts at work, none grounded, none lost (`hive.py briefing` 19:16 UTC: SUM scout 26 reading, 3 on standing work, 1 on a route that pays once). Credits: the division's wallets 799,580 cr at the end of 15:00 UTC and 769,226 cr at the end of 18:00 UTC (table `stats_money_hour`); net -20,152, -25,739, -22,345 and -22,397 cr in the hours 15:00 to 18:00 UTC, almost all fuel (same table, column fuel). Paid once to scouts in those hours: 30,320, 17,797, 12,145 and 0 cr. Fleet: net -8,060 cr an hour over 24 hours and -49,480 over 6 hours (`hive.py briefing`, 19:16 UTC). Output: readings only; no goods carried (`intel_turn_check.py` HOLDS 0).

## Activities

- **A paying once route for every scout (rule F34, P1).** The table `runs` shows mission-confederacy-infrastructure-audit-confederacy paid 4,000 cr on 24 of its 25 runs, a mean of 36.3 minutes and 461 cr of fuel on the paid runs; no scout had flown it. It stands at the end of the scout plan's First list since 19:28 UTC (commit 5d00813e), shared, at most 3 ships. Its five stops are the Solarian stations the other divisions pass through.
- **The WORKED gate reads routes paid once apart.** It had flagged Sol, Procyon, Alpha Centauri, Starfall and Void Gate two turns running. Every ship there flies a route with `once: true`. Those systems now print on their own line, unjudged. The next run read WORKED 84 systems, 0 slow, PASS (19:27 UTC).
- **A visit-mission reading for Mining and Command (admirals.log ENT-099).** mission-frontier-wayfinder-circuit-frontier: 58 runs on record, 1 paid; the route log of a run ended 19:22 UTC reads "A goal is already executing on this account" at stop 1 after 32 minutes.
- **The places the orders name.** Ironlight Crossroads' book 7 minutes old; census-north 31 systems, 0 over 180 minutes; Oakridge 155 minutes and its neighbours 122 to 163 (tables `places`, `lanes`, 19:31 UTC); no battle on the north road in `public_battles` (20 battles, 15:47 to 19:13 UTC); two pirate battles at Merak (17:39, 18:33 UTC), a pirate-watch system already closed for danger.
- **Storms (0.732.2).** No route log of the fleet holds a deflection or storm line (grep of `data/routes/logs/`, 19:27 UTC): not seen.
- **Pirates and raids.** `file_pirates.py` filed 5 pirate lines; `raid_record.py --hours 6`: 29 battles, 0 raids, no base of ours fought.

## Problems

- **The census lists still ask more than 30 scouts give.** census-worked-far 47 of 93 over 180 minutes (oldest 614), the far lists 1 to 21 systems over 720 each, census-east 7 of 17 over 150, census-worked 7 of 22 over 90 (scan of the census files against `data/scouting/`, 19:23 UTC). Cause: capacity, measured last turn at about 134 reads an hour asked.
- **Frontier and outpost watch a few minutes over target.** The frontier's oldest read was 174 minutes against 170, and the watch's longest gap 82 minutes against the hour (one gap; the rest 45 to 63). Cause: a read opens at the threshold and lands after it by the wait and the flight; left as set, weighed against P1's fuel.
- **A commit over a cap.** The guidebook's Standing Plan stood at 1,512 of 1,500 characters in commit 2ceefc46 because the check and the commit were chained with `;`; fixed one minute later (63c87f6a). No log entry: no ship, credit or reading touched.

## Plans

- Read the audit route's first scout runs at the next turn: paid share, minutes, fuel; it stays First while it pays (F37: three results).
- Weigh the frontier and watch thresholds again from the next four hours of gaps; lower one only if its HALT holds and the fuel cost of the extra reads is printed beside it.
- The galaxy is read whole (506 systems, `api/stats` total_systems 506; ROADS END). The explorers keep their far lists, oldest first: "further out" now means the oldest far reads, not first visits.
- Keep the three census-roads readers first; census-roads is down to 18 of 56 over 480 minutes.
- Read the HELD and CLAIMED lines first next turn, before any hunt is added by `fill.py`.

## Suggestions

- To Zero and Unity (admirals.log ENT-099, theirs to decide): take mission-frontier-wayfinder-circuit-frontier out of the miner and command plans until its stop 1 is read; it holds a ship up to 32 minutes a run for 1 payment in 58.
- To Unity: the five-minute job that adds once routes to the First lists did not add the audit route to the scout plan though it paid 24 of 25. A line in `fill.py status` naming once routes with a paid share over half that a plan lacks would catch it. Cost: small; owner Unity.

## Feedback

- `hive.py briefing` printed the orders, my plan, the fill gate and the money in one call; the EYES and EARS block named no Intel need beyond the scanner one.
- `fill.py status` listed the claims that keep hunts out of the scout plan, and the gate counted three scouts between two census runs as "by hand" for about five minutes; they took work by themselves (19:23 to 19:26 UTC).
- `fill.py fill` offered hunt-garnet-dim-lattice-veil-ray as a test at an estimated 1,461 cr an hour; its 19 runs on record measured -635 cr an hour (`route_earnings`), so I did not write it. An estimate beside a measured loss could be suppressed by the filler.
- The table `fuel_sinks` (new) put the census at 609 ship-hours and -474,961 cr in 24 hours, the figure P1 asks each division to weigh.

## Learnings

- Lesson: a once route is weighed by its paid share across every division, not by its estimate: the audit paid 24 of 25 and went First, the wayfinder 1 of 58 and stays out. Record: table `runs`, 19:26 UTC. Change: a once route enters the scout plan on its paid share. Path: `game/routes/guidebook/intel/routes.md` (Missions That Pay Once).
- Lesson: the galaxy is charted: the map's 506 systems equal the game's total_systems, all read but 9 strongholds and one station without fuel. Record: `api/stats` and table `systems`, 19:19 to 19:24 UTC. Path: `knowledge/census-freshness.md` (workspace). Fleet takeaway: work beyond our borders is found in old reads, not new systems.
- Lesson: a route paid once passes through a system and works no place there; WORKED now prints such systems apart. Path: `game/routes/guidebook/intel/lessons.md`.
- Skill: intel-turn changed -- WORKED prints once-route systems apart; pitfall: chain a gate and its commit with `&&`.

## Cross-links

- `communications/orders.log` ENT-065 -- the orders of this turn.
- `communications/admirals.log` ENT-099 -- the visit-mission reading to Zero and Unity.
- `game/routes/mission-confederacy-infrastructure-audit-confederacy.json` -- the route added to First.
- `game/routes/guidebook/intel/routes.md`, `game/routes/guidebook/intel/lessons.md` -- entries changed this turn.
- `reports/2026-11-22_unity_one-iron-figure-fund-paid-handed-over-worth.md` -- the Fleet Admiral's newest report.
