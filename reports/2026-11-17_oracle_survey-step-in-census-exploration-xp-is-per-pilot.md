---
name: survey-step-in-census-exploration-xp-is-per-pilot
id: 20261117T154743Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, exploration, survey, census, outpost]
links:
  - reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md
  - reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md
---

# Intel -- 97 Systems Read for the First Time Far Out, a Survey Step in Every Census of a Scanner Ship, and Exploration XP Found to Be Each Pilot's Own

## Situation

Period: from my previous report
(`reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md`,
11:47 UTC) to the end of my scheduled turn of 15:15 to about 15:50 UTC on 2026-11-17.
Orders in force: `communications/orders.log` ENT-037 (Unity, 14:00 UTC), which carried
my block of ENT-036 on: for the turns of 11:15 and 15:15 UTC ten scouts explore as far out
as they can reach (Suggi's order), the other twenty do the normal work; GSC-0044 and its six
neighbours watched hourly; a source for each input of the reserve; pirates written down;
the survey test. The Fleet Admiral's report in force is
`reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md`.

```
Ships: 30/30 at work, grounded: 0, lost: 0
Credits: start 1,082,537 (11:43 UTC), end 1,047,143 (15:39 UTC), net -35,394
Output: 303 census runs (84.9 ship-hours), 119 systems read for the first time since 11:15 UTC
Source: hive.py fleet at 11:43 and 15:39 UTC; the table runs, scout rows started from 11:47 UTC, read 15:47 UTC
```

Intel's steady net per hour read -17,646 at the briefing (15:16 UTC) and -12,388 at 15:39
UTC (`hive.py fleet`); the costs are fuel. The scout runs since 11:47 UTC by kind (table
runs): census 303 runs, 84.9 hours, -60,807 cr; circuits 25 runs, 5.2 hours, +5,111 cr
steady and 14,000 cr paid once (the Voidborn chain); hunts 16 runs, 7.5 hours, +8,561 cr;
mines 11 runs, 8.7 hours, -2,008 cr.

Against my Measure line, read in this turn:

| Measure | Reading | Record |
|---|---|---|
| Oldest reading the fleet plans on | home 28 min, frontier 192 min (target 200) | `intel_turn_check.py`, 15:39 UTC |
| Places our routes use read twice in four hours | 35 of 36 (Intercrus once) | runs.jsonl, 15:35 UTC |
| Inputs of the reserve with a known source | 24 of 28 raw inputs short | `surplus.py reserve` with the tables fields, books, herds, 15:32 UTC |
| Scouts at work | 30 of 30 | `fill.py check scout` PASS, 15:42:24 UTC |
| Exploration, navigation, scanning | exploration 2 / 2.8 / 3, navigation 4 / 4.8 / 6, scanning XP on three scouts (5 to 20) | table ship_skills, 15:33 UTC |
| Scouts exploring | 10 of 30, and the scanner scout on a far list from 15:33 UTC | plan file |
| GSC-0044 and its neighbours every hour | not met: gaps 63 to 75 minutes, Intercrus 211; fixed in this turn | WATCH line, 15:39 UTC |

## Activities

**Far exploration (Suggi's order for this turn).** The five far routes, two explorers each
with `chain` 3, read 97 systems for the first time between 11:30 and 15:16 UTC (17, 17, 19,
18 and 26 by direction), census-roads 22 more (runs.jsonl). The farthest system read in each
direction: Dustfall 27 jumps, Glenhaven 26, Alcyone 29 (with Altair, Castula, Ashmark and
Mekbuda, all 29), Quartzfield 29, Praecipua 24. No explorer ran short: the lowest tank was 46
of 95 at 15:19 UTC (table ships). The map holds 506 systems; 367 are read; of the 139 never
read, 127 stand on the explorers' lists (about 3.2 hours at 38 first reads an hour), 9 are
pirate strongholds and 3 have stations that sell no fuel. Nothing is left to widen.

**Scanning (the survey test).** I built a survey step into `game/fleet/census.py` through
`fleet-build.sh` (commit 7540393, test `ScannerTests` seen failing first): a ship whose live
file lists a survey scanner runs `survey_system` on arrival in each system it reads, before
`get_system`, so a revealed place is read in the same pass. The scanner scout flew it at
Intercrus at 15:37 UTC: "Survey complete. No hidden deposits detected", scanning 5 to 10 XP.
It now flies census-far-1 (raised to 3 ships), where Horizon, a visit objective of the two
survey missions it holds, is still unread.

**Exploration XP.** I took every scout's XP at 15:19 UTC and read it again at 15:45 UTC
against the runs between: exploration is paid for each pilot's own first visit, about 5 XP a
system (details under Learnings).

**The outpost site.** census-watch-gsc-0044 now holds GSC-0044 and all six neighbours
(Intercrus moved from census-frontier), every 45 minutes, `chain` 3, 3 ships (commit
a5f0aeb). No pirate on record in any of the seven.

**Sources for the reserve.** Silicon ore far out: GSC-0007 Dark Beacon Cluster 18,639 of
20,000 (27 jumps), Emberglow 4,935, Edasich 4,545, Muphrid 4,325, Hadar 3,518, Netherwick
3,052. Thorium ore 132 at GSC-0032; uranium ore on no field (1 unit at Acubens). New herds:
magnet barnacles (anchor plate), mirror skates (foil scale), cobalt squids (cobalt ink);
silica borers (silica lens) graze at Nexus Prime. Admirals' note ENT-041.

**Pirates.** 29 lines filed (observations kind pirate): groups of four to six at Redmarsh,
Netherwick and Violethall, two Kael raider elites at Dustfall, the two Korr raider elites
again at Felis Belt B at 14:53 UTC.

**Requests and the rest.** Apollo's ENT-221 answered yes (ENT-230): census-watch-clearwater
reads Clearwater hourly. fill.py added two one-ship hunt tests (Birchwood cinder sylph,
Pleione hollow pilgrim). The game stands at 0.723.2, which the rules digest names: no request.
`validate-intel.py` Errors 0. Claim ENT-040, note ENT-041, queue ENT-167, errors ENT-089.

## Problems

**The outpost watch was not hourly for four hours** (errors.log ENT-089). GSC-0044 and its
five listed neighbours were read 63 to 75 minutes apart from 11:15 to 15:15 UTC, and
Intercrus once (13:19 UTC), against an order to read them every hour. Cause: I set
`every_minutes` to 60, the target itself, though my own guidebook says the threshold is the
floor of a gap, never its ceiling; and I left Intercrus to Military's census-guard-ice, which
left Military's guard template at 12:18 UTC. Nothing checked either. Done: Intercrus on my
list, 45 minutes, chain 3, 3 ships; a WATCH line in my turn check stops the turn on any watch
gap or age over 60 minutes. It read HALT at 15:39 UTC, as it must until the new settings have
flown an hour. No pirate stood there, so no harm was read.

**Apollo's request came due before the readings.** ENT-221 (12:25 UTC) asked for two
readings by 15:15 UTC; my plan changes only in a turn, and the turn before it ended at 11:47
UTC. The first read started at 15:30 UTC; the request closes at my turn of 19:15 UTC.

**Intel runs at a loss of fuel**: -12,388 cr an hour at 15:39 UTC. Reading sells nothing; the
hunts brought +8,561 over 16 runs.

**A figure in my briefing was false**: mine-nightveil-dark-residue read -120,673 cr a ship-hour
from one command ship's run whose row reads -720; the store counted the 200,000 cr deposit
into the treasury. Request ENT-231 to Unity.

Checked and found clean: no ship lost or damaged (every scout's hull 75 of 75, table ships,
15:19 UTC), no wallet under 3,000 cr (SHIPS line), no census list of mine sharing a system
with another (OVERLAP PASS). Not checked: which scout routes the pirate gate closed.

## Plans

Inside orders ENT-037, at my turn of 19:15 UTC, in this order:

1. **Close ENT-221.** Two Clearwater readings with their times, the regrowth an hour (the
   second reading less the first plus what Logistics gathered between them), then
   census-watch-clearwater off and Clearwater back on census-roads.
2. **The explorers after the far lists.** The 127 never-read systems run out about 18:45 UTC.
   The orders then send about ten explorers to the three regions of D4 and the roads to them
   first. Since exploration XP is each pilot's own, I will give each explorer lists it has not
   flown (the regions and the far lists of another direction), so the class's skill keeps
   rising after the map is read; no explorer goes to gather. A list of the systems each pilot
   has been in is the figure I lack; I build it from the runs and the ship files as a script of
   my own skill first.
3. **The survey beyond the border.** I read the scanner scout's `survey:` lines on census-far-1.
   If a survey shows a place or a deposit that get_poi did not, I fit Survey Scanner I on the
   ten explorers (about 4,900 cr each, about 49,000 cr, inside rule F12's 10 percent of
   1,047,143 cr) through fit-survey-scanner-central-nexus. If two more surveys show nothing,
   the fit still trains scanning on every read, and I weigh that against the cost in the
   report.
4. **The outpost watch.** The WATCH line must read PASS: gaps under 60 minutes for all seven
   systems. If it does not, a fourth ship or a threshold of 40.
5. **The hunt tests.** Read the first RESULT lines of the Birchwood and Pleione tests; keep a
   paying one with one ship (one hunter per herd).
6. **The visit missions.** The scanner scout holds Local Sector Survey (Sirius and Horizon
   left) and Deep Space Cartography (The Crucible and Horizon); Unity plans a visit step at her
   turn of 17:30 UTC. I read its objectives again and put it on a route when the step stands.

My goal for the next turn (measure, number, turn): WATCH PASS, exploration mean at 3.0 or
above, and the scanner scout at scanning level 1, all read at 19:15 UTC. The choices above
are mine inside the orders; nothing here needs a decision from above.

## Suggestions

1. **A skill history in the store** (Unity's: `store.py` is closed to me). Reason: the
   finding that exploration is paid per pilot needed a hand snapshot of thirty ship files and a
   second read 26 minutes later; a table of each ship's skill XP by the hour would let every
   Admiral read what a route trains, as `route_earnings` reads what it pays (rules F23, F30).
   Cost: one row per ship and skill an hour, about 246 times 20 rows an hour.
2. **Every division can take the per-pilot rule** (for Unity to pass on): a ship that flies to
   a system it has never been in gains exploration XP, and by the catalog piloting pays a
   bonus for surveying new places. Routes that send ships to new systems train skills no gathering trains. Cost: none
   to say; fuel where a route is changed.
3. **Treasury deposits out of run figures** (requests ENT-231): reason and cost are in the
   request. Until it stands, a run figure near a faction payment is read with its row.
4. Weighed and not proposed: a request for more scanners now. One survey beyond the border is
   too little to spend 49,000 cr on, and the decision is mine inside F12 next turn.

## Feedback

- **The briefing** (`hive.py briefing`, 15:16 UTC) gave the orders, my standing fleet and the
  gate in one call and worked. Its plan table printed mine-nightveil-dark-residue at -120,673
  cr a ship-hour with "Measured at a Lo"; the figure was the store's, not the run's (ENT-231).
- **fill.py** (`check`, `status`, `fill --write`) worked: two one-ship tests added and applied
  in one call each (15:33 and 15:40 UTC), PASS at 15:35 and 15:42 UTC. Unclear: `status` read
  "2 by hand" at 15:35 UTC while I held no ship; both were engine goals between runs. A word
  saying "goal, no order file" would spare a search.
- **plan.py template** changed @reader and applied the plan in one call (commit 18ee1a9);
  `plan.py set` likewise (e64e0d0).
- **fleet-build.sh** (`tree`, `test`, `install`) took the census.py change through every gate
  in about a minute and committed it under my name; the test failed on the old code first, as
  the skill asks.
- **The view route_earnings and the tool sql** answered every figure of this report. Missing:
  any history of skills (`ship_skills` is now only), see Suggestions.
- **The pirate gate in dispatch.py** (1586add): I did not read which scout routes it closed in
  this period, so I cannot judge it from my side; my 29 pirate lines feed it.
- Built myself instead of asking: the survey step, the WATCH line and the ROADS END verdict of
  my turn check, the XP snapshot. With a door into `store.py` I could have built the skill
  history myself.

## Learnings

1. **Exploration XP is each pilot's own first visit.** I read every scout's XP at 15:19 UTC
   against its runs to 15:45 UTC. Scouts that read systems the fleet had read for hours, but
   they had not, gained 5 to 30: Sualocin 10, Acrux 5, Sirius 15, GSC-0016 20, Mirach 30. A
   scout on a mining mission at Rotanev, with no census at all, gained 10. Every gain was a
   multiple of 5. My guidebook had said a second read of a system gives none, and I had
   planned the explorers as if the skill stopped when the map is read. Now: explorers are
   rotated onto lists they have not flown, never to gathering. For the fleet: a route to new
   systems trains a ship whoever read them first. Kept in `knowledge/census-freshness.md`.
2. **A rule kept in a file was broken again; now a gate keeps it.** My knowledge file said a
   threshold set at the target never meets it, and I set the outpost watch at 60 minutes for
   an hourly order (errors.log ENT-089): a repeated mistake, because the first fix was a
   sentence, not a check. The WATCH line is the check. For the fleet: an order with a number
   is kept by a gate that reads that number. Kept in `knowledge/census-freshness.md`.
3. **A survey can ride on every read.** The survey step costs one action a system and trains
   scanning (5 XP a survey). It revealed nothing hidden at Nexus Prime or Intercrus: two
   readings. Two scouts also took 20 scanning XP from a link of the Voidborn chain (Collective
   Provides or Signal Protocol, not told apart). Kept in `knowledge/census-freshness.md` and
   unpromoted (`LEARNINGS.md`).

One thing of my class I learned to do better (G4): exploring by direction with a chain, sized
on fuel; 97 first reads in four hours with no tank below half. One I do not master yet:
hidden places. Two surveys found none, and I do not know where the game hides them.

Skill: intel-turn changed -- WATCH and ROADS END lines, exploration per pilot, the survey step, heredoc refusal

## Cross-links

- `reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md` -- my previous report
- `reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-037 -- the orders of this turn
- `communications/requests.log` ENT-221, ENT-230, ENT-231 -- Clearwater, my answer, the store figure
- `communications/errors.log` ENT-089 -- the outpost watch
- `communications/admirals.log` ENT-040, ENT-041 -- claim and readings
- `communications/queue.log` ENT-167 -- the census.py change
- `game/fleet/census.py` -- the survey step (7540393)
- `game/routes/guidebook/intel.md` -- Class Card and Standing Plan of this turn
