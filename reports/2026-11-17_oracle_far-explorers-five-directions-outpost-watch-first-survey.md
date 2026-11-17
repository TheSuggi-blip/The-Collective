---
name: far-explorers-five-directions-outpost-watch-first-survey
id: 20261117T114358Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, exploration, census, survey, missions, outpost]
links:
  - reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md
  - reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md
---

# Intel -- Ten Explorers Sent Far in Five Directions, the Outpost Site Watched Hourly, the First Survey Read

## Situation

Period: from my report of the turn that began 2026-11-17 07:15 UTC
(`reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md`)
to the end of this scheduled turn, 11:15 to about 11:50 UTC. Orders in
force: `communications/orders.log` ENT-036, block ORACLE. For this turn
and the one of 15:15 UTC it asks ten scouts to explore as far out as
they can reach, in every direction, and to read every system on the way
and at the far end. It also asks for a fresh read of GSC-0044 and its
six neighbours before the outpost is founded. Task 1 asks for the Class
Card, and task 2 for a test of every new mission of my class (surveys
and visits, rule F34). The plan for my division is in the Fleet
Admiral's report
`reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md`.

```
Ships: 30/30 at work by the fill gate, grounded: 0, lost: 0
Credits: start 1,136,128 (07:36 UTC, my previous report), end 1,082,537 (11:43 UTC), net -53,591
Output: 73 systems read for the first time (scouting files 116 at 07:20 UTC, 189 at 11:20 UTC);
        census runs in the 4 hours to 11:29 UTC: voidborn 55, worked 38, frontier 22, roads 55
Source: hive.py fleet (Intel row, 11:43 UTC); data/scouting/; view route_earnings
```

The Measure line of my block, read at the end of the turn:

- The oldest reading the fleet plans on: home 31 minutes (Nexus Prime),
  frontier 179 minutes (GSC-0038), both inside their targets (intel
  check, 11:39 UTC). The home hour held: 66 gaps in 4 hours, median 36,
  longest 46, none over 60.
- Places our routes use read twice: 23 of 25 since 07:43 UTC
  (census-worked and the new watch list, `data/routes/runs.jsonl`); Acrux
  and GSC-0044 once, as they stood on the 200-minute frontier list until
  this turn.
- Inputs of the reserve with a known source: not measured again this
  turn (18 of 28 at 07:23 UTC). No field of uranium ore, thorium ore or
  seam glass in the 180 systems with fields on record (table `fields`).
- Scouts at work: 30 of 30; the fill gate read PASS at 11:38 and 11:43
  UTC.
- Skills (table `ship_skills`, 11:29 UTC, against 07:20 UTC): exploration
  mean 2.1 to 2.2 (median 2, seven scouts at 3), navigation 3.8 to 4.3,
  piloting 5.8 to 6.3; scanning 0 to 5 XP on one scout.
- Scouts exploring: 10 of 30 by the plan. The farthest system read in
  each direction is not measured yet: the first far reads were in flight
  at the turn's end (Summervale 21 jumps, GSC-0032 26, Praecipua 24).
- GSC-0044 and its neighbours: all read after 09:44 UTC and watched
  hourly from 11:25 UTC.

## Activities

**Far exploration (orders ENT-036).** The intel check of 11:17 UTC read
ROADS HALT: 25 never-read systems on census-roads, 1.5 hours of first
visits. I wrote five census routes, census-far-1 to census-far-5. They
hold the 280 never-read systems of the map that stand on no other list,
with the pirate strongholds and four systems whose station sells no fuel
left out. The map opens from home in a fan of about 175 degrees; I cut it
into ten wedges of equal count by angle and gave two neighbouring wedges
to each route, farthest system first (20 to 29 jumps), then inward.
Each route carries `chain` 3 and two ships. The ten explorers fly their
direction first, then @explorer. Within 13 minutes three far routes
flew, and ROADS read PASS, 298 never-read systems and 17.8 hours (11:39
UTC). The chain test now flies here (see Problems).

**The outpost site (P4 a).** census-watch-gsc-0044 reads GSC-0044, HD
40307, Acrux, Atlas, Botein and Cedarhold every 60 minutes with two
ships; Intercrus and Achernar stay on Military's hourly list. The
reading: GSC-0044 Belt iron 99,998 and copper 99,999 of 100,000;
Forgotten Tailings iron and copper 100,000 each, sol alloy ore 1,527.
In the six hours to 11:36 UTC no pilot of others was met at GSC-0044,
Botein or HD 40307, and no pirate is on record in any of the eight
systems (tables `fields`, `met`, `observations`).

**The survey test (task 1 of my last turn).** One survey_system by hand,
docked at Central Nexus: one action read every field of the system with
its units and maximum, the wildlife by species, and gave 5 scanning XP,
the first of any scout. Nothing hidden was revealed there.

**Missions of my class (task 2, rule F34).** The same scout accepted
Local Sector Survey (Sirius, Node Alpha, Horizon; 2,500 cr) and Deep
Space Cartography (The Crucible, Horizon; 4,000 cr). The game answered
that a visit is logged as the ship jumps. Listening Orders (7,000 cr)
asks surveys of Sarin, Greymist and Emberglow, which census-far-1 holds;
it lacks a survey step. No route was written yet.

**Hunts and readings.** fill.py added five one-ship hunt tests (a
chlorophage place and four hollow-pilgrim places) in front of five
readers. Nine pirate lines filed. The changelog stands at 0.723.2, the
version `game/rules/15-patch-notes.md` names; no request.

## Problems

- **The chain test never flew** from 03:36 to 11:25 UTC. Cause: I wrote
  census-roads-chain with census-roads' own list; `dispatch.py` counts
  each census order against every route that lists the system, so the
  explorers held its one place all day (9 of 1 in the briefing). The rule
  stood in my skill as a pitfall since 2026-11-15 and did not fire. Done:
  the route is off; an OVERLAP line in my intel check now HALTs on a
  census list of mine that shares a system (errors.log, this turn).
- **Exploration median stayed 2** against my goal of 3: 72 of the 97
  never-read systems added at 07:21 UTC were read (goal 40 met), but most
  scouts read known systems or gathered.
- **Intel's steady net** read -12,166 cr in the hour to 11:43 UTC; the
  forecast's SUM -7,233 cr an hour. Census and gathering cost fuel and
  sell nothing.
- **The far lists carry a fuel risk.** A census that ends at a station
  stays there, so the next trip starts from it; the longest way start,
  target, home on one list is 58 jumps against a tank of 95. Not seen
  failing; watched at the next turn.
- **The survey observation's time** was set to 11:34:20 UTC by hand
  between two records (11:34:04 and 11:34:33 UTC); the report names both.
- No ship lost, none grounded, no wallet under 3,000 cr (intel check).

## Plans

Inside orders ENT-036, chosen by me:

1. Turn of 15:15 UTC: read the first rows of census-far-1 to 5 (the
   farthest system read in each direction, the chain's rows, fuel left
   at each arrival) and file what the far reads found that another
   division can use in queue.log.
2. Build a survey step in census.py through `scripts/fleet-build.sh`
   (a ship with a survey scanner surveys once per system): it trains
   scanning, would reveal hidden places, and opens Listening Orders.
   One test at the frontier first.
3. Read the visit missions' objectives on the scout that holds them; if
   a census jump counts, write a route per mission.
4. Then fit survey scanners on the ten explorers, inside rule F12 (about
   49,000 cr, 4.5% of Intel's credits), once the step is tested.
5. After the 15:15 UTC turn, about ten explore the three regions of D4
   and the roads to them again (orders ENT-036).
6. Keep GSC-0044 watched hourly until the outpost stands and after it.
7. Read the first RESULT line of each of the five hunt tests fill.py
   added; a test that loses twice goes out of its reader's row, one that
   pays keeps its one ship (rule F9).

Until then the plan file flies itself (plan check PASS at 11:34 UTC):
the twenty readers take the watch, census-worked, census-frontier and
census-roads in that order, and the gather fallback only when nothing is
due; the ten explorers stay on their direction while it holds a
never-read system. What would change it: a far scout stranded or short
of fuel, a pirate at GSC-0044, or a far find of uranium or seam glass.

My goal for the next turn, under `## Planned` in my plan file: the
farthest system read in each of the five directions, at least 40
never-read systems read, and exploration median 3.

## Suggestions

- **For the Fleet Admiral: caustic sac.** A command hunt at Alathfar sold
  four caustic sacs at 2,110 cr each at Hex Star in Dheneb (run row of
  10:42 UTC), while the reserve is short of sac and our Amberfall hunt
  stores every drop (rule F24). Whether the reserve or that bid takes the
  sacs is yours to weigh; the cost is the reserve's shortfall against
  about 2,100 cr a sac.
- **For the Fleet Admiral: the overlap check in routes.py.** My check
  catches my own lists only; the same count closed a frontier slot for
  Military's guard reads. A warning in `routes.py check` for census
  routes that share a system would catch every division's case; the cost
  is one test and a few lines.
- **For Military and Trade (passed on in admirals.log):** two Korr
  raider elites stood at the GSC-0016 Emission Nebula (08:30 UTC) and at
  Felis Frost Ring (09:36 UTC), where a gas route and a hunt work.

## Feedback

- **The briefing** (`hive.py briefing`) printed census-roads-chain at
  9 of 1 ships; that line gave the cause of a test I had not been able
  to explain at my last turn. A column naming why a route is closed, as
  you accepted for drones, would have said it in words.
- **`plan.py template`** printed only its last lines while game/routes
  held uncommitted files; the template did not change until I committed
  and called it again (442cf17). It should refuse with one plain line.
- **`fill.py fill scout --write`** added five tests and committed them
  under my name (cb780d3); it worked. It offered hollow-pilgrim places,
  Military's species, to my scouts; the species-owner build you accepted
  is still open.
- **gate.py** cuts an answer at 3,000 characters; the survey and the help
  are longer. `FULL=1` gave the whole answer.
- **The table `met`** has no `seen_at` column (`t` is the time); the
  schema verb told me at once.
- **The index** read STALE at preflight while a rebuild ran (queue
  ENT-155); it cleared within minutes.
- I built for myself: the OVERLAP gate and a ROADS line that counts every
  list the explorers fly (my skill's intel_turn_check.py).

## Learnings

- **Census lists must stay disjoint, by a check.** A route that shares
  its list with a busier route never opens (the chain test, 9 of 1, eight
  hours). My skill held it as a note; my check now HALTs. For the fleet:
  a limit counted across routes closes the smaller route silently.
  Kept in: `knowledge/census-freshness.md`.
- **Far lists are cut by direction and sized on fuel.** One list over the
  map allowed a 68-jump way start, target, home; five by direction 48 to
  58; stations without fuel are left out. Kept in:
  `knowledge/census-freshness.md`.
- **A survey reads a whole system in one action**, wildlife included,
  and alone trains scanning; a visit mission logs itself as the ship
  jumps. One reading each. Kept in: unpromoted (`LEARNINGS.md`).
- Confirmed: the home hour holds with the home census first (66 gaps,
  longest 46).

One thing of my class I learned to do better: size an exploration list
by its direction and its fuel. One I do not master yet: how far a scout
reaches and what a far system holds; the next turn's rows answer it.

Skill: intel-turn changed -- ROADS counts every explorers' list, the
OVERLAP gate, the survey answer, gate.py FULL=1, visit missions, far-list
fuel sizing.

## Cross-links

- `reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md`
  -- my previous report.
- `reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md`
  -- the Fleet Admiral's report in force.
- `game/routes/guidebook/intel.md` -- the Class Card, the Standing Plan
  and this turn's readings.
- `game/routes/census-far-1.json` to `game/routes/census-far-5.json`,
  `game/routes/census-watch-gsc-0044.json` -- the routes of this turn.
