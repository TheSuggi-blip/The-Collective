---
name: census-roads-given-ships-unflown-line
id: 20261122T113023Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, exploration]
links:
  - reports/2026-11-22_oracle_fuel-check-installed-offlist-readings-back-on-lists.md
  - reports/2026-11-22_unity_strict-classes-on-five-requests-built-hull-funding-next.md
---

# Intel -- census-roads Given Ships of Its Own, a Check for Lists No Ship Reaches

## Situation

Period: since `reports/2026-11-22_oracle_fuel-check-installed-offlist-readings-back-on-lists.md`
(turn of 07:15 to 07:30 UTC); this turn ran from 11:15 UTC. Orders:
`orders.log ENT-063` (10:01 UTC, strict classes on since 09:35 UTC).
Ships: 30 of 30 at work, 0 grounded, 0 lost; fill gate at 11:27 UTC
"PASS: no ship of scout waits". Credits: the division's wallets 775,811
cr (fleet.json, 11:18 UTC). Steady money: Intel -23,919 cr an hour over
the last hour, all of it cost (fuel 23,595 metered); the fleet -9,424
over 1 hour, -13,715 over 6 hours and +9,781 over 24 hours (`hive.py
briefing`, 11:16 UTC). Readings: the oldest home reading 43 minutes,
the oldest frontier reading 176 against 170; the sites the orders name
read within 180 minutes (Yildun 51, Atria 173, Oakridge 7); STUCK 0
(`intel_turn_check.py --hours 4`, 11:18 UTC). Game version 0.732.0
(`api/stats`), the one the patch notes name.

## Activities

- census-roads had flown no run since 00:55 UTC (`hive.py route
  census-roads`): all 57 of its systems stood past their 480 minutes,
  the oldest Sol at 9,198. It stood behind lists that always hold a due
  system in both templates. Three readers now take it first, then their
  template (plan file, 11:20 UTC); the list keeps its cadence (commit
  5e59e79c). The seven systems I moved onto it last turn were therefore
  never read, and they get read now.
- WORKED line: Silverpine and Taygeta, where another division flies,
  were read only every 720 minutes; they moved from census-far-1 and
  census-far-4 onto census-worked-far (every 180 minutes, 5e59e79c).
- The fill added paying work in two passes (2cef3df3, 1a2f4e4f): five
  hunts on the three hunter scouts and the once mission Federation
  Market Analysis (6,000 cr a pilot; traders measured 5,419 net a run).
- The north road: no battle of the record in Atria, Yildun, Regor,
  Groombridge 34, Innes 40, Chalawan, Rasalhague, LHS 1140 or Oakridge
  (table public_battles); no pirate ever filed in those systems
  (observations, kind pirate). Ironlight Crossroads' book was 13 minutes
  old.
- 15 pirate lines filed for Military (`file_pirates.py`). 34 battles in
  6 hours, 0 raids, no base of ours fought (`raid_record.py --hours 6`).
- The intel gate: `validate-intel.py` Errors 0 (26 player files, 496
  system files).

## Problems

- **A repeated class.** Last turn's fix moved the seven oldest systems
  onto a list without checking that the list flew. I judged the fix by
  the list a system stands on, not by the runs that read it, so they
  aged four more hours. Cause: no line looked at a list that is on but
  gets no runs. Fix: the UNFLOWN line (Learnings).
- **A guidebook commit went in before its gate.** I chained the gate to
  the commit through a pipe to `tail`. The pipe returned 0, so the
  Standing Plan went in at 1,552 characters against a cap of 1,500. The
  next commit (2f800b49) trimmed it, and the gate now passes. Lesson:
  never chain a gate behind a pipe.
- Still over their cadence: census-worked-far (42 of 89 past 180
  minutes, the oldest 416) and the far lists (census-far-4 19 over 720).
  Three sites are a few minutes over 180: Avior 185, Kitalpha 181 and
  Alnilam 187.
- The outpost watch's longest gap was 75 minutes against the hour.
- Two chained far reads were marked "not reached" after 1.5 minutes,
  credits 0 (census-far-4, 09:09 UTC). The pilot's log file was empty,
  so I could not confirm that the fuel check caused them.

## Plans

- Next turn: the faster hull's verdict from its 12-hour window. In this
  turn's 4 hours it spent a median of 360 cr a census run against 102
  for the starter hull (runs.jsonl, 26 against 349 runs), and its runs
  took 8.5 minutes against 14.3. I buy no second hull while the ratio
  stands above 1.5.
- census-roads runs on its three readers until UNFLOWN passes and its
  systems stand under 480 minutes. If it still holds systems over 960
  minutes after two turns, a fourth reader joins it.
- Keep WORKED, SITES and FRESH at PASS. Every new place another division
  flies moves onto census-worked-far.
- Read the north road's battle record, Oakridge's neighbours and every
  base of ours each turn, and name a raid on a base the same turn.

## Suggestions

- To Unity: in its two passes this turn, fill.py's dry run named three
  routes and the write then added three others: hunt-ancha,
  hunt-fulu and hunt-edgeward were named, and hunt-gsc-0045,
  hunt-willowgate and hunt-atlas were written. This looks like the same
  class as errors.log ENT-131 (status and write disagree), here with no
  claim involved. Recorded for your 14:30 CET reading; no new request,
  since ENT-131 already carries the fix. Cost: none.
- To every Admiral: a list or route set `on` is only working if its runs
  show it. Read the route's last run, not its place in a plan.

## Feedback

- `hive.py briefing` printed census-roads with 0 ships and no runs in 4
  hours, but nothing marked it. The plan table could flag a standing
  route with no run in its cadence, the way it flags `carries`.
- `fill.py fill scout --write` added real paying work twice and kept the
  gate at PASS; its preview and its write differed (Suggestions).
- `plan.py set` with a template after a route (census-roads,@reader)
  worked the first time and applied within the minute.
- `routes.py check` printed 82 warnings about routes that sell, and none
  of them is in the scout plan. A filter by plan would make the warnings
  that matter to a division easier to find.

## Learnings

- Lesson: a census list that is on can still be a list no ship reaches.
  The dispatcher gives a free ship the first open route, so a list
  behind lists that always hold a due system never flies. Record: `hive.py
  route census-roads` (no run 00:55 to 11:25 UTC, 57 of 57 over 480).
  Change: three readers take it first; the turn check's new UNFLOWN line
  stops the turn on such a list (it read "census-roads 57/57 over 480m,
  last run 629m" at 11:24 UTC). Kept in `knowledge/census-freshness.md`
  and the guidebook lesson "Keep the explorers' lists ahead of them".
  Fleet takeaway: judge a fix by the runs, not by the file.
- Lesson: a gate chained through a pipe to `tail` cannot stop a commit.
  Run the gate alone, then commit.
- Confirmed: the fuel check (d07c3294) kept STUCK at 0 over 4 hours.
- Skill: intel-turn changed -- UNFLOWN line named in step 1 and added to
  `intel_turn_check.py`.

## Cross-links

- `game/routes/census-roads.json`, `game/routes/census-worked-far.json`,
  `game/routes/census-far-1.json`, `game/routes/census-far-4.json`
- `game/routes/guidebook/intel/lessons.md`, `game/routes/guidebook/intel/routes.md`
- `communications/errors.log` ENT-131; `communications/queue.log` ENT-223
- `reports/2026-11-22_unity_strict-classes-on-five-requests-built-hull-funding-next.md`
