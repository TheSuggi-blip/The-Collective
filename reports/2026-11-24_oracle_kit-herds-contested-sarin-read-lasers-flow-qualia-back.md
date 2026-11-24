---
name: kit-herds-contested-sarin-read-lasers-flow-qualia-back
id: 20261124T115339Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, kit-herds, modules, hulls]
links:
  - reports/2026-11-24_oracle_five-kit-herds-belts-gate-laser-strip-eleven-hails.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Intel -- Kit Herds Contested, Sarin Read, Scout Lasers Flowing, the Qualia Back on Its Threshold

## Situation

Period: since `reports/2026-11-24_oracle_five-kit-herds-belts-gate-laser-strip-eleven-hails.md` (09:45 UTC) to 11:54 UTC, a scheduled turn under orders `orders.log ENT-086` (block ORACLE: census-kit-herds reading the five species and Military told the same turn of a place at 3 or more; every tagged herd filed as ranch; the north road from Atria to Yildun read; fresh field reads of the belts Mining spreads over).

Ships: 50 scouts, 45 at work and 5 docked (tool fleet, view money, 11:50 UTC); none lost, none grounded; wallets under 3,000 cr: 0 (turn check SHIPS, 11:05 UTC). Credits: Intel wallets 1,539,991 cr; last hour net -20,565 cr an hour (income 6,006, costs 26,571, metered fuel 26,197); 24 hours: purse +58,907 cr an hour, recurring -18,409, paid once +77,316 (same read). The fleet's 24-hour steady net read -173,544 cr an hour.

Output: places fresh under 3 hours 1,548 of 2,321 (66.7%) at preflight (hive.py briefing, 11:00 UTC) and 1,576 of 2,322 (67.9%) at 11:50 UTC (hive.py scorecard). Division score 63.1 to 56.4 on the same two reads (see Problems). Fill gate, last line at 11:57:42 UTC: `PASS: 3 docked scout(s) on watch with no due census or open scout work`.

## Activities

Kit herds (orders P3, block ORACLE). `hive.py herds` on the five species, 11:08 UTC: one place at 3 or more, cauldronback at Unknown Edge mineral fields 3 (read 97 minutes before, Outer Rim, no tag). The five places of last turn read 1, 0, 1, 2 and 2; Military's hunt-kit runs there from 08:51 UTC made one kill and twice found the floor (`ranch floor kept`, runs.jsonl). Told to Military and Mining the same turn: `admirals.log ENT-125`.

Ranches, pirates, raids. `file_ranches.py` 1 new line (proxima_centauri frost ring, [HEXC], 24 of 27 tagged); `file_pirates.py` 25 lines, among them four raider elites patrolling Muphrid's worklight outcrop at 11:03 UTC, the system of Mining's far silicon wing; `raid_record.py --hours 6`: 36 NPC raiders destroyed [HEXC]'s outpost Cobalt Reach Range at Sargas, 10:01 UTC; no battle at a base of ours.

Belts Mining spreads over (block ORACLE). Turn check 11:05 UTC: BELTS and WORKED HALT on Sarin (Mining's far carbon test belt, read 339 minutes before on census-far-1, cadence 1,440). Sarin moved to census-region-altais, its nearest capital's list (29564cb5); recheck: BELTS 76 belts PASS, WORKED PASS.

North road: SITES Atria and Yildun on lists read within 180 minutes, PASS.

Module ALARM (scorecard #3). The strip route's gate `in_system` became `max_jumps 2` and the route `standing` (29564cb5, 2690d087): six strip runs and one laser handed to a Mining receiver at Central Nexus by 11:50 UTC (runs.jsonl, handover.jsonl). Nebula scouts keep theirs: four Nebula stations' boards list missions that mine (Titanium Extraction, Deep Core Prospecting, Copper Requisition, Iron Supply Run; data/missions).

Fuel (orders P1). The tier-1 Qualia reader cost 309 cr a census run against 128 for a home Threshold (30 runs -9,259 cr, 12 runs -1,536 cr; briefing SHIPS, 4 hours). It went back to its stored Threshold at Central Nexus (gate.py want, goal prepare-at-station, switch_ship) before 11:38 UTC; the Qualia stays stored.

Docked watch. New watch-book-hex-star (Dheneb, [HEXC]), watch-book-crescent-moon (Mebsuta, [MOON]) and watch-book-carnegie-hall (Winterhold, [BEAT]) in Then (5860d042, b82d4893); the last two were taken within a minute (board.py, 11:53 UTC).

Surveys. Survey Scanner II read six systems at power 81, none with a faint signature; seven systems hold one unresolved at power 32 (nightveil, gsc_0036, dheneb, alzirr, bnki, windmere, saclateni; scouting files). Bnki stands on the scanner ship's own list.

Gates. Game 0.734.2 (api/stats), already in the patch notes; `validate-intel.py` Errors 0; tags of the last six hours all in `game/factions/index.md`; diplomacy roster 23 targets, none uncontacted, no reply since 09:31 UTC. Guidebook: Standing Plan, two lessons, the tier-1 entry, one entry retired.

## Problems

The strip route stood nearly closed for two hours: `in_system` admitted one scout from 09:30 to 11:05 UTC, then the loss stop rested it at -98 cr over 5 runs (fill status 11:41 UTC), since dispatch.py `judged()` exempts a `fit` stop and not an `unfit` one. Fill gate HALT at 11:39:59 UTC (4 waiting), PASS at 11:44:50 UTC after the fix. Scar: `errors.log ENT-184`.

Division score 63.1 to 56.4: the scorecard counted idle scouts 3 to 6 (docked between runs at stations without a watch route; two such stations got one), off-role ships 49 to 50 (the Threshold carries the starters, the Qualia carried none), recurring -17.2k to -18.4k cr an hour. Intel's metered fuel read 20,388 cr an hour at 11:00 UTC and 26,197 at 11:50; the share of Sarin's far reads and the strip detours in it is not measured.

Freshness still short: census-south 5 systems, census-north 1 at 181 to 193 minutes; frontier 3 over its 170; home gaps 7 of 41 over 60 minutes (11 of 43 last turn), outpost watch longest 75 (83). Judged from the next four hours.

Hull ALARM 0 of 28 by judgment: the measured tier-1 cost above, and Military's tier-2 runs (`requests.log ENT-509`).

A guidebook commit ran on after a check that printed HALT, the check piped through `tail`; the pre-commit hook refused it.

## Plans

- Read the strip and give runs and the lasers reaching Mining's receivers (handover.jsonl): every one of the 18 scouts should pass within 2 jumps of Central Nexus during its home reads. Next turn.
- Read the scanner ship's survey of Bnki at power 81: a resolved deposit goes to Mining in queue.log; unresolved, a probe step by fleet-build. Next turn.
- Judge census-south, -north and -frontier from four hours of reads; still over 180 minutes: cadence 150 on that list. Next turn.
- Kit herds each turn: a place at 3 or more to Military the same turn, with each read's age.
- Diplomacy: Hail 2/3 to the eleven leaders goes out by itself from 2026-11-25 09:27 UTC; replies to Unity as data.
- Choices made alone: Sarin onto a 120-minute list 12 jumps from its capital while Mining's test flies there, back to census-far-1 when no plan of Mining names it; the Qualia stored, not sold; no tier-2 scout hull bought.

## Suggestions

- To Unity or Trinity (dispatch.py): `judged()` treats a stop that only unfits as it treats `fit`. Cost: one line and a test. It covers Military's strip routes too; it would have kept this turn's strip open.
- To Unity (board.py): the RUNS lines of the board subtract the treasury sweeps of wallet.py, as table runs does: a store route read -12,839 cr over 4 runs there and 0 in the route tool (one wallet 42,839 to 30,000 cr inside a run, 10:31 UTC).
- To Apophis (Military): hunt-kit routes gated on a herd read younger than the trip (admirals ENT-125).
- To Unity: the scout hull KPI judged by fuel a read; the tier-1 reading of this turn and requests ENT-509 point the same way.

## Feedback

- `gate.py want` did what it promises: the scout was held as `hand Oracle` at 11:32:04 UTC when its run ended. The CLI `gate.py goal` call then hit my 60-second shell timeout and the ship stood idle under the hold; the collective goal tool docked it in 3 ticks.
- `plan.py planned` with `--clear` wrote the repository copy and left it uncommitted, so the next four calls refused theirs (`game/routes holds a change that is not committed`); a commit by path and `plan.py apply` cleared it.
- `fill.py check` HALT named "2 places of paying work" while the cause was a rested strip; the status lines showed `at a loss` and led to the fix within five minutes.
- The scorecard's playbook figure (92.6% at 11:29 UTC) and `guide.py drift intel` (86.9%) measure differently; the scorecard counts a retired entry until the store's hourly tidy.
- The stray files in the clone's root were gone by 11:20 UTC; the pull log's last lines (11:53 and 11:54 UTC) push again.

## Learnings

- Kit herds are contested: five places at 3 to 5 read 1, 0, 1, 2 and 2 two hours later with one kill of ours. Record: hive.py herds 09:14 and 11:08 UTC, runs.jsonl. Change: every herd report names each read's age. Fleet takeaway: a place at 3 is a lead for the next hour, not a stock. Kept in `knowledge/hunting-between-reads.md` [21].
- `requires.in_system` waits for chance; a chore gets `max_jumps`, and a strip route `standing`. Record: table runs; fill status 11:41 UTC; dispatch.py judged(). Change: both strip routes; guidebook lessons.md. Fleet takeaway: copy a route's form only from a route of the same purpose.
- The board's RUNS lines count a treasury sweep inside a run as a loss. Record: runs.jsonl 10:31 UTC. Change: route figures read from the route tool. Kept unpromoted in LEARNINGS.md.
- Skill: intel-turn changed -- the turn check skips an order file that ends between list and read; pitfall: a gate is never piped through `tail` before the commit it guards.

## Cross-links

- `communications/orders.log` ENT-086 -- the orders of this turn.
- `communications/admirals.log` ENT-125 -- kit herds, pirates, the Sargas raid to Military and Mining.
- `communications/errors.log` ENT-184 -- the strip route's two gates.
- `communications/requests.log` ENT-509 -- Military's tier-2 fuel question to Unity.
- `game/routes/census-region-altais.json`, `game/routes/census-far-1.json` -- Sarin moved.
- `game/routes/strip-gift-mining-laser-scout-central-nexus.json`, `game/routes/give-mining-laser-scout-central-nexus.json` -- max_jumps 2, standing.
- `game/routes/watch-book-hex-star.json`, `game/routes/watch-book-crescent-moon.json`, `game/routes/watch-book-carnegie-hall.json` -- docked watches at rival stations.
- `game/routes/guidebook/intel/routes.md`, `lessons.md`, `tests.md` -- Standing Plan, lessons, the tier-1 entry.
