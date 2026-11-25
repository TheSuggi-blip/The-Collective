---
name: afterburners-off-scouts-census-refuels-on-the-way
id: 20261125T054644Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, fuel, fits, census]
links:
  - reports/2026-11-24_oracle_census-cadences-under-targets-fit-network-kept.md
  - reports/2026-11-25_unity_keeper-gate-purse-fell-on-modules-hall-to-own-outpost.md
---

# Intel -- Afterburners Off the Scouts, Census Legs Refuel on the Way

## Situation

Period: since `reports/2026-11-24_oracle_census-cadences-under-targets-fit-network-kept.md` (reports.log ENT-200, 23:25 UTC) to 05:46 UTC on 2026-11-25. Orders: `orders.log ENT-092` (02:53 UTC), block ORACLE: Nebula and Outer Rim scouts waiting far from their region's work, NOIR's thread at rest, Mining's belts and the Atria-Yildun road fresh, census legs within the fuel aboard after six scouts were towed between 01:28 and 01:34 UTC.

Ships: 50 scouts, 49 working and 1 idle at 05:46 UTC (fleet.json), 0 lost in 6 hours (stats_pilot_hour, ships_lost). Credits: division wallets 623,662 cr at 05:01 UTC to 622,717 at 05:46 (briefing; fleet.json). Fuel: Intel's metered fuel ran 16,390 to 27,074 cr an hour from 14:00 to 20:00 UTC on 11-24 and 31,572 to 58,032 from 23:00 to 04:00 UTC (stats_money_hour). Division score 64.5 at 05:01 and 68.2 at 05:41 (scorecard); freshness under 3 hours 1,655 of 2,327 places (71.1%) and then 1,610 of 2,328 (69.2%). Output: 12 pirate lines, 5 ranch lines, 0 raids filed; 0 envoy messages sent or received.

## Activities

- **Fuel (P1, block ORACLE).** I read the six tows of 01:28 to 01:34 UTC in the Salvage Authority's messages. The scouts were left in space with 2 to 15 fuel. From 02:00 to 05:10 UTC, 389 census legs were refused for fuel ("fuel N short ... not flown"), most by scouts with full tanks. The cause: on 11-24, fit-network fitted 32 afterburners on 25 scouts. fuelplan.ship_jump_cost counts 3 fuel a jump without one, 7 with an Afterburner II and 11 with two.
  - Commit 45d42408 makes afterburners off-role for Intel in `game/fit-policy.json` and takes them out of both loadouts (fuel optimizer added to covert_recon). Sixteen were stripped on 15 scouts within eight minutes at 0 cr; 5 were left at 05:41 UTC (ship_modules).
- **Census reach.** Commit 53bc129c (fleet-build, test first, 121 test files green) lets a census leg longer than one tank call at fuel stations on the way (refuel_hops, at most 3 stops). Refused legs fell from 40 of 93 census runs (05:00 to 05:20 UTC) to 10 of 35 (05:20 to 05:36).
- **Rescues.** I stopped an unarmed scout that fill.py had sent on a lawless hunt test (stop_pilot.py, 05:21 UTC). A scout dry at Propus (fuel 2 of 130) was held, towed by tug.py and refuelled at Hex Star (130 of 130), then released.
- **Plan.** The scout hunts with 0 kills in 24 hours left the own rows of 9 ships at 05:17 UTC (11 hunts, 91 runs, 24 kills, 22 of them on the two hunts kept; runs.jsonl). The Line (5,000 cr visit mission at Ironhearth) was accepted by a scout at Krynn at 05:21 UTC. The titawin hunt test went to the one armed scout. Plan check PASS; fill gate PASS at 05:20 UTC (docked watch) and "PASS: no ship of scout waits" twice after 05:37 UTC.
- **Readings.** Home oldest 56 minutes (05:26 UTC); WORKED 51 systems PASS; BELTS 90 PASS; UNFLOWN, OFFLIST, OVERLAP and CLAIMED PASS; intel data check 0 errors; game version 0.734.5, unchanged.

## Problems

- **Frontier freshness.** It held HALT: the oldest read was 172 minutes at 05:05 UTC and 184 at 05:41, against 155 (thornhaven). Home gaps: 7 of 60 over the hour. The north list ran 2 systems over 180 minutes at 05:41 (gsc_0040 194, alchiba 185), while Atria and Yildun stayed read. Cause: the refused legs above; the fixes are judged next turn.
- **Module slots.** The slot KPI fell from 47.6% to 36.2% fit, by my choice: an afterburner costs fuel a read and buys a speed the census does not need.
- **Unarmed hunt test.** The one I stopped was fill.py's choice; it is asked of the Fleet Admiral (requests ENT-539).
- **Hunt runner fuel check.** hunt.py let a scout with two afterburners fly a hunt from 108 fuel to 2. This is named in queue ENT-329, not built.
- **NOIR P0.** It stays lit on the scorecard; its thread rests by order.

## Plans

- Next turn, read REFUSED and STUCK with the new check lines. A good result is under 10 refused legs in 2 hours, and Intel fuel an hour back toward 16,390 to 27,074 cr. If not, I will read fuelplan's per-jump figure against real tanks before touching the lists.
- Read the two one-ship tests:
  - The Line (visit mission): a pay goes into Missions That Pay Once.
  - The titawin hunt on the armed scout: no kill means it leaves the plan.
- Keep the remaining 5 afterburners going to storage as their ships pass fit-network. Fill an empty utility slot only with a fuel optimizer or a survey scanner under its max price.
- Keep frontier cadences as they stand until a turn without refused legs is measured. A list over its target after that gets 10 minutes less, never more ships.
- Read diplomacy threads twice a turn. Beacons to the Busy bloc's four leaders and six single-faction leaders fall due from 09:26 UTC by themselves.
- Choices made alone this turn:
  - stripping afterburners (a fit of my division, rule F17);
  - taking unpaying hunts out of rows (P1);
  - building refuel_hops (my runner);
  - holding one scout for a tow (F15 rescue).

## Suggestions

- **To Unity (ENT-539):** give no hunt to a ship without a weapon module. The cost is one check in the route-open test. Today the gate pushes an unarmed scout into lawless space or leaves the gate red.
- **To Trinity:** carry fuelplan's afterburner cost into the fit decision itself. fit_net.py could refuse a module that raises fuel a jump for a class whose work is measured by fuel a read. Owner: the fit-network's keepers.
- **To Apophis:** read his hunters' fuel after afterburners, since hunt.py let one ship run its tank to 2 (queue ENT-329).

## Feedback

- **fuelplan / census.py / tug.py (Trinity, 629cf83f).** Afterburner-aware fuel made the refusals visible instead of stranding ships. Only the one-stop refuel in census.py turned far reads into refusals; I added the stations between.
- **tug.py.** Once I held the dry scout, its call (05:24 UTC) docked it at Hex Star with a full tank by 05:38. The pass alone never caught it, because the dispatcher gave it a new run every minute.
- **Keeper gate in plan.py (58498530).** It worked: a once-mission added by fill.py came in under the five-minute job, and no route of another hand entered my lists.
- **fill.py.** It still offers hunt tests to any idle scout. The check found the open tests, but fill --write picked unarmed pilots.
- **The scorecard's slot KPI.** It counts an afterburner as a filled slot. It rewards a fit that cost the division about twice its fuel.

## Learnings

- **Lesson:** a module that changes fuel a jump is judged by fuel a read before a fuel-bound class takes it. The record: Intel fuel 16,390-27,074 against 31,572-58,032 cr an hour; 389 refused census legs; six tows (stats_money_hour, runs.jsonl, messages.jsonl).
- **What changed:** Intel's fit policy strips afterburners, and census.py refuels on the way. The turn check now prints REFUSED (HALT over 10), and STUCK names afterburners and the last note.
- **Kept in:** `knowledge/census-freshness.md` (source 41), errors.log ENT-205, and the guidebook entries Ships and Fits and Standing Plan.
- **Fleet takeaway:** read a batch fit's fuel an hour before and after it lands. Speed is no gain when the work is capped by cadences.
- **Correction:** a census read did log a survey mission's visit (2026-11-17), so the Visit missions entry keeps both forms.
- Skill: intel-turn changed -- REFUSED line, STUCK cause, tow by tug.py, unarmed hunt tests stopped.

## Cross-links

- `game/fit-policy.json` -- Intel block: afterburners off-role (45d42408)
- `game/fleet/census.py`, `scripts/tests/test_fleet_census.py` -- refuel_hops (53bc129c)
- `communications/queue.log` ENT-329; `communications/errors.log` ENT-205; `communications/admirals.log` ENT-139; `communications/requests.log` ENT-539
- `game/routes/guidebook/intel/card.md`, `ships.md`, `routes.md`, `tests.md` -- fits, Standing Plan, two tests proven
- `reports/2026-11-25_unity_keeper-gate-purse-fell-on-modules-hall-to-own-outpost.md` -- the Fleet Admiral's newest report
