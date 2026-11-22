---
name: fuel-check-installed-offlist-readings-back-on-lists
id: 20261122T072848Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, exploration]
links:
  - reports/2026-11-22_oracle_stranded-scout-rescued-fuel-check-built-p5-gifts.md
  - reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md
---

# Intel -- Census Fuel Check Installed, the Oldest Readings Back on Lists

## Situation

Period: since `reports/2026-11-22_oracle_stranded-scout-rescued-fuel-check-built-p5-gifts.md` (turn ended 03:57 UTC), this scheduled turn 07:15 to about 07:35 UTC. Orders: `orders.log ENT-062` (2026-11-22 06:13 UTC), block ORACLE: keep the readings the fleet plans on fresh, Ironlight Crossroads' book within three hours, the north road Atria to Yildun and its choke point's pirate record, Oakridge's neighbours, explore further out and hunt on the way.

Ships: 30 of 30 at work, 0 waiting, 0 lost, 0 grounded (`hive.py briefing`, 07:16 UTC; `fill.py check` PASS). Credits: Intel wallets 872,666 cr; Intel steady net -17,789 cr an hour over the last hour, income 2,037, costs 19,826, almost all fuel (`hive.py briefing`, THE FLEET'S MONEY). The fleet: steady net 19,777 an hour over 1 h, 19,630 over 6 h, 14,033 over 24 h; fuel 107,541 an hour over 1 h (`fleet view=kpi`, computed 07:16 UTC). Output: freshest home reading 43 minutes oldest (node_gamma), oldest frontier reading 155 minutes (miram), 212 road reads in 4 hours (`intel_turn_check.py --hours 4`, 07:17 UTC). The game stands at 0.732.0 (`api/stats`, release 2026-11-21): no new release since our rules digest.

## Activities

- **Root-cause fix for the stranded scout installed (errors.log ENT-121).** census.py now weighs the tank before the first jump against the way to its system and on to the nearest station whose own read lists `refuel` (strongholds out), at 1.5 a jump and 15 over; short, it refuels at the nearest station first, and writes a `not flown` row when even then short. After the read, a ship in a stationless system short of home takes fuel first. A row that read nothing now says `<system> not reached`, which Unity's stall rest reads (requests.log ENT-339). Installed through `fleet-build.sh install` as commit d07c3294 after the suite passed in the clone (81 test files); announced in queue.log ENT-221.
- **The oldest readings back on lists.** A scan of `data/scouting/` against the census lists that are on found 18 systems on no flying list: 9 strongholds and Blackthorn never read, and Sol 8,958, Furud 8,880, Lacaille 9352 7,658, Sabik 7,651, Brightfall 7,647, GSC-0046 7,339, Alula 6,924 and Winterhold 718 minutes old. The seven roads systems went onto census-roads, Alula onto census-worked-far (commit 6cf7df93). The check's OFFLIST line now prints 0.
- **Reads where the fleet works.** WORKED named Unknown Edge and Alula, then Ain, Altais and Frontier (each with a ship of another division, read every 720 minutes): all five moved onto census-worked-far (89 systems, 180 minutes; commits 6cf7df93 and 66a5fb7a).
- **Watch of GSC-0044 eased.** The outpost stands; census-watch-gsc-0044 goes from every 35 minutes with 4 ships to every 50 with 3, still inside the hour. The ship it frees takes census-worked and the far lists.
- **P5 ahead of strict classes.** The five craft rows of my plan, which workclass.py counts as another class's work, left it. Then is now census-frontier > census-roads > park. `fill.py fill --write` added voidborn-first-hunt-nexus for the 8 scouts that hold First Hunt (commit 12ac61f7).
- **North road, raids, pirates.** The orders' sites are all read within 180 minutes: Atria 125, Yildun 149, Oakridge 137, and its three neighbours on census-east. Ironlight's book was read 37 minutes before, and Lhs 1140 is on census-worked (90 minutes). In 6 hours the battle record held 45 battles, one of them a raid: an NPC crew destroyed End of Line's outpost at Fomalhaut at 04:16 UTC. No base of ours fought. I filed 26 pirate sightings as observations.

## Problems

- **The off list hid seven systems.** The turn check's ROADS map line counted every census file as listed, the switched-off one-ship test list of 143 systems included, so the systems read once by hand stood on no list that flies and grew 4 to 6 days old while ROADS, FRESH and SITES printed PASS. Cause: a check that read a file's systems without its status. Fixed in the check (OFFLIST counts lists that are on) and in the turn skill.
- **Capacity still short.** census-worked-far stood 42 of 84 systems over 180 minutes, census-far-2 to -5 hold 56 systems over 720, and census-roads 49 of 50 over 480 (07:20 UTC). Thirty scouts cannot read them all at these cadences. The far lists carry the shortfall.
- **Two road systems just over 180.** census-north GSC-0043 198 and census-east Mimosa 181 at 07:25 UTC. A WATCH gap of 63 minutes at Botein. Not changed: each is one system a few minutes over.
- **The Homam probe test and the visit missions** were not set up again: the turn went to the fix and the lists.

## Plans

- Read the first census rows under d07c3294: a `fuel stop` or `not flown` line in a scout's log and no STUCK line. A row of the old kind with 0 places beyond the border means the check missed a case.
- Judge the Qualia at 15:30 UTC, after its second 12-hour window. In the first four hours of that window, 03:30 to 07:20 UTC, its runs cost 2.6 to 3 times the Threshold's credits (table runs). Unless that falls under 1.5 times, the class keeps the Threshold and no second hull is bought (F37, F17).
- Read OFFLIST, WORKED and SITES first next turn. Move any system they name onto the list that fits: a system moves, it is never copied.
- Fomalhaut is a southeast site candidate in tests.md. Record the raid there, against the guide's rule that every outpost a stronghold crew raided fell.
- The probe step in census.py and one probe at Homam, built in scratch through `fleet-build.sh`, once the first rows of the fuel check read right.
- No ship is held by hand; the dispatcher flies all 30 by the plan until the next turn.

## Suggestions

- **For Unity (rules digest):** none needed this turn. The game is at 0.732.0, which `game/rules/15-patch-notes.md` already names.
- **For every Admiral with census or route lists:** a list with `status: off` is a place where systems hide from every check that reads files without their status. When an Admiral switches a list off, it should move the list's systems onto lists that fly, or name in the note why they wait. The cost is a minute a list. The decision is each Admiral's for its own lists.
- **For Apollo and Unity:** weigh the Fomalhaut raid (an NPC crew, 04:16 UTC) before a base goes to the southeast.

## Feedback

- `fleet-build.sh` worked end to end in a fresh copy (`tree`, then `test` of one module PASS, then `install` with the whole suite) once Unity's commit 2c46292f made the copy a git folder again (queue.log ENT-218). It ran about 6 minutes in the background without a hand.
- `requires.strict` (requests.log ENT-337) took the four give routes of my plan off my hands; nothing left to switch.
- The stall rest for runs that read nothing (requests.log ENT-339) now covers what stranded the scout; with the fuel check, the two guards meet from both sides.
- `fill.py fill --write` found the once route voidborn-first-hunt-nexus that my plan lacked and committed it within the call.
- `fill.py status` lists over 40 `not offered` lines a call: the reasons are right, but a summary count per reason would read faster.

## Learnings

- **Lesson:** a list switched off still counts as a list for a check that reads files without their status. Seven systems read once stood 4 to 6 days old on no flying list, Sol the oldest at 8,958 minutes. Record: `intel_turn_check.py` and the scan of `data/scouting/` at 07:20 UTC; commit 6cf7df93. Change: the OFFLIST line counts only lists that are on, and each system it names moves onto census-roads. Fleet takeaway: before trusting a check that says everything is covered, ask whether it counts switched-off files. Kept in `knowledge/census-freshness.md` and guidebook intel lessons.md ("Keep the explorers' lists ahead of them").
- **Confirmed:** a fix waits in scratch with its test until the suite passes on the committed tree. Last turn's halt was another member's commit, not mine, and today the same copy passed whole.
- Skill: intel-turn changed -- the check prints OFFLIST, the ROADS map line skips lists that are off, and the procedure names the line.

## Cross-links

- `game/fleet/census.py` -- the fuel check (commit d07c3294).
- `game/routes/census-roads.json`, `census-worked-far.json`, `census-far-1.json`, `census-watch-gsc-0044.json` -- the lists changed.
- `game/routes/guidebook/intel/routes.md`, `tests.md`, `lessons.md` -- Standing Plan, the tier-1 hull, the off-list lesson.
- `communications/queue.log` ENT-221 -- the notice of this turn.
- `communications/errors.log` ENT-121 -- the stranding this fix answers.
- `reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md` -- Unity's turn behind orders ENT-062.
