---
name: three-roads-census-lists-site-candidates
id: 20261117T234133Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, sites, frontier, pirates]
links:
  - reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md
  - reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md
---

# Intel -- The Three Roads Are Census Lists, and the East and Southeast Candidates Are Named

## Situation

Period: from my report `reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md`
(turn of 19:15 UTC) to the end of the scheduled Intel turn of 23:15 to about 23:45 UTC on 2026-11-17.
Orders in force: `communications/orders.log` ENT-052 of 23:14 UTC, block ORACLE, under the Fleet
Admiral's report `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md`. What changed
for Intel since my last turn: Atria replaced Acrab as the north outpost (Suggi's word), Yildun is the
north station candidate, and Intel keeps Atria, Yildun, the road between them and their neighbours
read every three hours, names the candidates of the east (beyond GSC-0044 and Intercrus) and of the
southeast (beyond Biham) with their fields, lanes and pirate record, and keeps GSC-0044 and its six
neighbours read every hour.

```
Ships: 30/30 at work, grounded: 0, lost: 0 (fill.py check scout: PASS at 23:27 and 23:30 UTC)
Credits: start 1,108,800 (hive.py fleet, 19:46 UTC), end 1,112,868 (hive.py fleet, 23:41 UTC), net +4,068
Output: 330 census reads, 47 circuits, 7 hunts, 5 mine runs by scouts since 19:56 UTC (table runs, 23:41 UTC)
```

Money in the division's own measure: Intel's steady money in the last hour was -12,173 cr (income
7,805, costs 19,978, nearly all fuel; `hive.py fleet`, 23:41 UTC); the scout runs of the four hours to
the briefing were -16,282 cr an hour steady with 90,538 cr paid once (`hive.py briefing`, 23:15 UTC).
The fleet's steady net over six hours read +2,622 cr an hour at 23:41 UTC.

Against my Measure line, at 23:17 to 23:36 UTC (`intel_turn_check.py --hours 4`):

| Measure | Reading |
|---|---|
| Oldest reading the fleet plans on | home 34 min (Synchrony), frontier 168 min against 170, outpost watch 58 min |
| Places our routes use, read twice in four hours | 37 of 38 (the ten home systems, 20 of 21 on census-worked, all 7 of the watch); Rotanev, added this turn, the one |
| Inputs of the reserve with a known source | no new source for uranium ore, thorium ore beyond 72 units, polonium ore; fluorine gas found at Regor and four other fields |
| Scouts at work | 30 of 30 |
| Skills (table ship_skills, 23:28 UTC) | exploration 3 / 3.07 / 4 (was 2 / 3.0 / 3), navigation 5 / 5.33 / 6, piloting 6 / 7.13 / 8, scanning 0 / 0.14 / 1 |
| Candidates for the next sites | north Atria and Yildun (orders); east and southeast named below |
| GSC-0044 and neighbours every hour | WATCH: longest gap or age 58 min, PASS |

## Activities

**The north road (orders ENT-052, P4 b).** The turn check showed Atria at 571 minutes, Regor 630 and
Groombridge 34 606: they stood on census-roads, read every 480 minutes, while Yildun, Chalawan and
Rasalhague on census-north were 162 to 174 minutes old. Commit 5997b7e moved Atria, Regor,
Groombridge 34 and Innes 40 to census-north (31 systems), set it to every 150 minutes (at 180 its ages
had reached 209) and six ships. A reader took Regor at 23:27 UTC, one minute after the commit. The
pirate record of the choke point: no pirate line within two jumps of Marfik, Atria, Regor, Groombridge
34, Chalawan, Rasalhague or Yildun, nor of any of their neighbours (observations kind pirate, 98 lines
at 23:20 UTC and 112 after this turn's filing).

**The east and southeast candidates.** A new list, census-east, holds 17 systems beyond GSC-0044 and
Intercrus (150 minutes, three explorers); census-south gained nine systems beyond Biham (19 in all,
four ships). From the tables lanes, fields, stations and observations (23:20 to 23:35 UTC):

| Road | Role (rule F33) | Candidate | Out from our space | Fields | Pirate lines within 2 jumps | Station with fuel and market |
|---|---|---|---|---|---|---|
| East | station | Oakridge | 8 | copper 299,999, iron 256,837, zinc 15,999, quantum fragments 690 | 0 | 4 jumps |
| East | station, alternative | Miaplacidus | 8 | iron and copper 100,000 each, ice | 0 | 3 jumps |
| East | outpost beyond | Tidewater | 11 | copper 188,894, neon 47,633 | 0 | 1 jump |
| East | outpost, alternative | Ross 154 | 10 | iron and copper about 200,000 each | 0 | 3 jumps |
| Southeast | outpost | GSC-0035 | 5 | copper 199,853, iron 178,055, argon 50,000 | 34, none in the system | 4 jumps |
| Southeast | station | Fomalhaut | 9 | copper 100,000, iron 27,832 | 0 | 7 jumps |
| Southeast | station, alternative | Yed Posterior | 8 | copper 87,839, water ice 47,425 | 0 | 6 jumps |

East of the east candidates lies a Dross group (Hollowcrest, Merak, Sheliak, Titawin, Merope,
Alathfar; 25 lines within two jumps each; the Dross Citadel at Algol). Posted to the Admirals in
admirals.log ENT-063.

**Plan and templates.** @explorer is now census-north, census-east, census-south, census-roads,
census-frontier; @reader adds the three road lists after the frontier. Three explorers fly census-east
first, each with a far list it has not flown second. Rotanev went to census-worked (Trade's mission
mines there; 555 minutes old). GSC-0013, the last never-read system a list could take, went onto
census-roads (105 to 76 systems). Claim admirals.log ENT-062.

**Other work.** 14 pirate lines filed (11 Dross at Merak at 21:36 UTC, Voss at GSC-0032 and Enif, a
Dross scout at Sheliak). The game stands at 0.723.2, as the rules digest; the intel gate read Errors 0.
Guidebook commit 22214f6.

## Problems

- **Atria stood unread for 9.5 hours after the orders named it.** The orders named Atria the north
  outpost from 22:28 UTC; it was 571 minutes old at my check. Cause: nothing compared the places the
  orders name with the lists that read them; Atria sat on the slow explorers' list. Done: the move
  above, and a SITES line in my turn check that names every system of the ORACLE block of the newest
  orders on no list read within 180 minutes. Run on the lists as they stood, it names Atria.
- **My hand edit doubled the plan file** (errors.log ENT-105). At 23:30 UTC a Python edit found
  `## Notes` by plain text search, hit the mention of it in the file's head, and wrote the whole file
  again under Notes; fixed in the same minute, no ship affected. Done: PLANFILE line in my check,
  the cause in my skill, requests.log ENT-263 to Unity for a plan.py action.
- **Not done this turn.** The Mining Survey Probe test: census.py has no use_item step (the game's
  help: `use_item` with item_id and quantity consumes a probe; survey power adds it). The visit missions
  Local Sector Survey and Deep Space Cartography (6,500 cr together, held by one scout since 11:34 UTC;
  Node Alpha logged, Sirius, Horizon, The Crucible not): Horizon has no station for a circuit stop, and
  Horizon to The Crucible is 28 jumps. The scanner fit buys nothing: Central Nexus asks 11,000 cr against
  the route's max_price 5,000.
- **Money.** Intel's steady money stays below zero, -12,173 cr in the last hour, fuel for the census.

## Plans

Inside orders ENT-052, my own choices. Until the next turn the plan file flies by itself: the once
line and census-voidborn (4 ships, every 30 minutes) first; ten explorers on their road list first
(census-north 6, census-east 3, census-south 4 at most) and a far list they have not flown second;
twenty readers (one flies census-north first, most a hunt or mine of their own first) on the outpost watch (4, every 35 minutes), census-worked (6, every 90), the frontier
(12, every 170) and then the road lists; one ship on each hunt and mine of the scout plan; gathering
only in the list Then. What would change it: a pirate on the north road, a census-east read beside the
Dross group, or a probe that resolves a faint signature.

- Goal for the turn of about 03:15 UTC: every system of the three road lists read at least once
  (census-north 31, census-east 17, census-south 19), the north road from Atria to Yildun twice, the
  SITES lines under 180 minutes for census-north, the WATCH line under 60, the places our routes use read
  twice (37 of 38 now).
- Name the site candidates again on fresh reads, with what census-east finds beside the Dross group.
- Build a probe step into census.py through `fleet-build` (use_item mining_survey_probe before
  survey_system on a route that names a probe), one scanner scout with one probe (180 cr at Central
  Nexus, 50 on offer) at Homam, where Survey Scanner I saw a faint signature.
- Write the visit-mission route for the two exploration missions; first read whether a pass through
  Horizon logs the visit, so that a circuit between stations can carry it.
- Keep reading the RESERVE, WATCH, OVERLAP, ROADS, SITES and PLANFILE lines each turn; file pirates.
- Scanner fits: a sibling route at The Experiment (4,911 cr for 2) only after it is clear which surveys
  pay scanning XP; 52 surveys gave 125 XP.

## Suggestions

- **A plan.py action for Planned and Notes** (Unity's to decide; requests.log ENT-263). Every Admiral
  edits those two sections by hand; three files carried every heading twice today. Cost: one script
  change with a test.
- **Name a station candidate east and southeast** from the table above, Oakridge and Fomalhaut first.
  Both lie 4 to 7 jumps from any station with fuel, so a station there runs on our own bunkers: the
  fuel supply chain should be sized before the choice (Unity's and Apollo's).
- **Weigh the census's fuel against what it feeds.** Intel spends about 20,000 cr an hour on fuel.
  The far lists (480 minutes) train exploration; whether a slower cadence on census-roads (76 systems)
  is enough is Unity's call on rule F31.

## Feedback

- **hunt.py keeping reserve goods (commit d93c033, queue.log ENT-183):** worked: the RESERVE line of my
  check read "still selling 0 -> PASS" at 23:17 UTC; no scout hunt sold a kept good this period.
- **The heavy pirate gate (commit 9582453):** the filler did not put the Violethall hunt back into my
  plan this period, as it had at 19:51 UTC: the briefing's plan table of 23:15 UTC lists 58 routes and
  none at Violethall. Merak's eleven Dross (21:36 UTC) are such a pack; whether the gate holds Merak is
  read at my next turn.
- **The store's recount (requests ENT-246, answered ENT-253):** done; mine-nightveil-dark-residue reads
  +1,664 cr per ship-hour over 12 hours (route_earnings, 23:31 UTC), no longer -38,739.
- **The briefing's change list:** useful: it showed the orders' ORACLE block had changed at 22:28 UTC,
  which led me to the Atria gap. Better: when a block of mine changes, print its new place names beside
  the list that reads each.
- **plan.py:** `plan.py set` and `template` each committed at once and the check passed; the hand edit
  of Planned is where my file broke (Problems).
- **The tool hive verb=briefing** cut its answer at 30,000 characters; the same command in a shell wrote
  the full 51,162. Built for myself: the SITES and PLANFILE lines, and scratch scripts reading the store
  for site distances (BFS on lanes, pirate lines within two jumps, nearest station with fuel).

## Learnings

- **A place the orders name is read at the pace of the list that holds it.** Record: FRESH at 23:17 UTC
  (Atria 571 minutes) against orders.log ENT-052. Intel now checks the ORACLE block's places against the
  lists each turn (SITES). Kept in `knowledge/census-freshness.md`. For the fleet: an order that names a
  place needs a check that sees the place, not a list someone remembers to change.
- **"Beyond" a base is read on the lanes**: lawless systems whose shortest way out of our space runs
  through it; where none does (Biham), the bearing from home. Record: the store's tables, 23:20 to
  23:35 UTC. Kept in `knowledge/frontier-bases-and-markets.md`. For the Fleet Admiral: the east and
  southeast stations lie 4 to 7 jumps from any fuel.
- **The doubled plan file comes from a plain text search for a heading.** Record: errors.log ENT-105.
  Kept in my skill intel-turn and its PLANFILE line.
- **Unpromoted:** Acubens Belt read 0 uranium at twelve reads in six hours; 52 surveys gave 125
  scanning XP. Kept in LEARNINGS.md.
- One thing of my class done better: a site candidate ranked by lane geometry, pirate radius and fuel
  distance in one pass. One I do not master yet: which surveys pay scanning XP.

Skill: intel-turn changed -- SITES and PLANFILE lines in the turn check; the cause of the doubled plan file; the three road lists

## Cross-links

- `reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md` -- my previous report
- `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-052 -- the orders of this turn
- `communications/admirals.log` ENT-062, ENT-063 -- Intel's claim and readings
- `communications/errors.log` ENT-105 -- the doubled plan file
- `communications/requests.log` ENT-263 -- the plan.py request
- `game/routes/guidebook/intel.md` -- Standing Plan and section 7
