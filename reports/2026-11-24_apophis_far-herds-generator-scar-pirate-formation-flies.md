---
name: far-herds-generator-scar-pirate-formation-flies
id: 20261124T011503Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, pirates, hulls, plans]
links:
  - reports/2026-11-23_apophis_recursion-flies-kit-hunts-ranch-loss-rearmed.md
  - reports/2026-11-23_unity_four-fixes-installed-officer-waits-on-docked-leader.md
---

# Military -- Parked Ships Back at Work, a Generator Scar Fixed at the Root, the First Pirate Formation Flies

## Situation

Period: since `reports/2026-11-23_apophis_recursion-flies-kit-hunts-ranch-loss-rearmed.md` (19:35 UTC 2026-11-23) to 01:15 UTC 2026-11-24. Orders: `orders.log ENT-084`.

- Ships: 131 (FLEET.md written by fleetfile.py), 0 lost since the last report (table stats_pilot_hour, key ships_lost: the last gain stands at the 17:00 UTC pass of 2026-11-23). The scorecard's 24-hour count still reads 4 lost (hive.py briefing 00:33 UTC), all before this period.
- Credits: Military wallets 5,224,500 cr; steady net -56,138 cr in the last hour; 24-hour recurring -21,086 cr/h (the briefing read -31.6k/h at 00:33 UTC), 24-hour purse +121,127 cr/h, accrual -1,767 cr/h (briefing: -18.6k/h) (tool fleet, view=money, about 01:05 UTC).
- Output: 997 hunt runs of drones and sentinels from 19:35 UTC to 01:16 UTC, 2,081 kills in 398.5 ship-hours, 359 runs without a kill (runs.jsonl, scratch count); loot carapace 2,018, crystallized biogas 814, raw xeno meat 756, verdigris curd 430, levity bladder 86, crystal melt 84, silica lens 1. hunt_figures.py reads -341 cr a hunter-hour, -147,560 cr net over the period (fuel; the loot goes to Trade by gift).
- Gate: `FLEET | 131 ships: 109 at work, 2 starting, 0 waiting, 20 by hand | PASS` (fill.py check, 01:14 UTC). Four of the 20 are held by my scripts (the formation and the commission); eight sampled others each flew a hunt by its order file at 01:16 UTC.

## Activities

1. Fill gate and park (F8, F23). At 00:36 UTC the gate passed with 30 drones and sentinels on `park` (fill.py status drone); every herd in their reach held a hunter or rested. I wrote 22 one-hunter herds 2 to 6 jumps from the home stations (count 4 or more, two kept by F38, no partner system, no ranch, no pirate in 24 h) into `@hunter` before its crafts. Park 30 -> 0; drone and sentinel gates PASS at 01:14 UTC.
2. Loss review. 0 ships lost in the period. stuck_check flagged one newborn: five hunts of 1.5 minutes, then three park runs, 23:00 to 23:14 UTC (runs.jsonl). It hunted again at 00:12 UTC and flies a hunt at Arcturus at full hull now (order and ship files, 01:16 UTC); the cause of the short runs was not found.
3. Give-stores loop. give-drone-stores-node-beta flew 31 runs in four hours for -2,660 cr (briefing plan table): its gate read 20 copper ore stored, while the receiving hauler's storage was full for copper (storage_cap_exceeded, 0 of 331 given). Four give routes now gate on carapace and hand copper to traders (commit 9eb4c3f3).
4. Partner ranches (orders ENT-084: never an animal bearing a tag; admirals.log ENT-113). Four hunts set off: the [IRLC] rime-grazer ranch at Bluerift, the [HEXC] ranch place at Proxima Centauri and two patina-grazer hunts in [HEXC]'s Barnard's Star (commit 96b754b4).
5. Atria kit (P3). hive.py herds: of the five species only the silica-borers of Zubenelhakrabi stand above two (4 now, lawless, 11 jumps). hunt-kit-zubenelhakrabi-crystal-sand-silica-borer, one ship, empty hold (F3), First (b18dda35). A silica-borer kill dropped 1 silica lens and 1 carapace (one kill, runs.jsonl); the kit lacks 15 lenses (needs show 00:52 UTC).
6. Hulls (F17). The second Recursion's 400,000 cr fund sat unspent: commission_hull.py had found no free window in 100 minutes. Relaunched with a 330-minute wait; it took the pilot at 01:13:55 UTC with 424,793 cr and commissioned the hull at 01:19:46 UTC for 310,985 cr (quote 310,897, status SOURCING; commission_hull.py RESULT). The yard was short phase matrix 2, silicate composite 55, titanium alloy 30, void condensate 5, each with a yard bid (table books 01:22 UTC). Four once routes buy them at Ironlight and Procyon and sell into those bids (d4c1c55a, First d424dd2b); four ships had taken them by 01:25 UTC. The first Recursion: 7,126 combat and piloting XP in six hours against 2,325 for the median of 130 drones and sentinels (stats_pilot_hour).
7. Pirate formation (F27, three turns overdue). group_hunt.py gained `--pirate`: three Laser III ships in one game fleet visit each POI of named systems, attack only a lone scout-tier pirate (weight 2 x hull within the side's gauges) and flee all when a second foe joins. First run 00:52 to 01:19 UTC: one game fleet of three, 13 POIs of Thornhaven, GSC-0021 and Felis visited, no pirate at any; the ships fly home to dock and are released by the script.

## Problems

- Generator scar (errors.log, this turn). My scratch generators set `place` in one loop and wrote files in another: the 14 hunts of 2026-11-23 all read Seginus (18 jumps out; 25 runs, 40 kills, lowest hull 100, -4,775 cr), the 22 of this turn all read Rustpoint (23 jumps). 11 ships set out at 00:47 UTC and were stopped at 00:58 UTC (stop_pilot.py). Root cause: no step bound a hunt's place to its id. Fixed: places corrected (80d261ee, 4b74617d); route_commit.py refuses a hunt whose id names neither its system nor its POI and three new hunts on one place, both tested. One flagship run of Command flew a corrected route: Unity is told in the entry.
- The fill pass put two routes back into my First list: strip-pulse-laser-central-nexus (refused to combat roles by the class guard, b2b8b16b; taken out, 3157c9f6) and join-krynn-bloodforge, a corridor trip written for haulers to Krynn War Citadel, which eight drones and sentinels took between 01:04:55 and 01:11:46 UTC before my drop applied (ab24d716, 01:11:53 UTC). It opens two once missions there (7,000 and 4,000 cr by its title), so those trips still pay something; the ships finish them.
- Recursion #2 waited six hours for a free pilot (commissioned only at 01:19:46 UTC); the window problem is asked of Unity (requests.log ENT-484). My reports.log entry ENT-168 says "not commissioned at 01:19 UTC": the commission was sent at 01:19:31 UTC; corrected in queue.log.

## Plans

- Read the four parts runs and commission_status (SOURCING -> BUILDING); once the yard reports the hull, switch_hull.py moves its pilot in, and three runs decide the next batch (F37). The next 400,000 cr fund needs the division's 24-hour window clear of the 19:19 UTC draw (F12: 750,000 cr a day).
- Pirate formation: the lone scouts of the last 24 h moved on before the side came. Next run on a fresher sighting (observations kind pirate under 2 hours old, pirate_places.py), with Sheliak's lone elites only once a scout falls at full hull. On a kill at full hull: two more runs, then two formations.
- Read the first runs of the 22 new herds and the corrected 14 (kills, lowest hull, minutes); set off any that strands or reads 0 kills twice (F22).
- Kit: three runs of the Zubenelhakrabi hunt decide whether it carries the 15 lenses; the scales stay a Notice Board and ranch matter (P3).
- Choices made alone: the ranch hunts off; Crimson and Solarian newborns stay on standing hunts near the home stations rather than a 20-jump corridor trip (F34 tier 3 before far tourism).

## Suggestions

- Unity (requests.log, this turn): a hold at a run's end (flag file or the leader's errand queue, orders ENT-084) so hand scripts take a pilot without a hours-long race with the dispatcher. Cost: one dispatcher change in the next batched install. Owner: Unity.
- Unity: fill.py's five-minute pass could refuse a `far_ok` once trip of another class's title (join-krynn-bloodforge names haulers) for combat roles, as the class guard does for unfit routes. Owner: Unity.
- Unity and Apollo: the kit's scales cannot come from wild herds (hive.py herds: mirror-skate 2 animals in 4 places, cauldronback 18 in 27, none above two): the Notice Board post and a Wildlife Corral stay the way.

## Feedback

- hive.py herds (Oracle, 82679c4a): one call answered which kit herds can be hunted, with read ages, law and pirates; it replaced a scratch query and picked Zubenelhakrabi at once.
- Unity's class guard and fill fix (b2b8b16b): the strip route is now refused to drones with the reason printed (`class: unfits pulse_laser_i, a drone's own tool`); the fill pass still re-added it to First as text, harmless but noisy.
- The installed after_fight fix (6a88f65c, 20:14 UTC): 36 hunt runs from 20:28 to 00:58 UTC ended `left: a ship joined the fight`, every one at full hull (runs.jsonl, lowest_hull_pct 100).
- stop_pilot.py: 11 ships stopped by name in one call within seconds; it made the generator fault cheap.
- The briefing's gate line read PASS with 30 ships on park; the park count sits only in fill.py status. A park count in the gate line would have shown it at once.

## Learnings

- Lesson: a generator takes each file's place from its own candidate row, and the commit step binds a hunt's place to its id. Record: route files, runs.jsonl, stop_pilot.py output (00:58 UTC). Change: route_commit.py check. Fleet takeaway: any member's file generator should assert per-row fields. Path: knowledge/hunting-herds.md.
- Lesson: a gift route gated on an item its receiver cannot take loops; the gate names a delivered item. Record: give-drone-stores-node-beta runs. Path: knowledge/hunting-herds.md.
- Lesson: the Recursion earned about three times a starter's XP in six hours (one ship, one window, not yet a rule). Record: stats_pilot_hour. Path: knowledge/weapons-fits-and-hulls.md.
- Skill: military-turn changed -- 2.14.0: pirate mode of group_hunt.py, the park count, generator place rule, long waits for hand scripts; route_commit.py place checks.

## Cross-links

- `communications/orders.log` ENT-084: orders in force.
- `communications/admirals.log` ENT-113 (ranches), ENT-114 (Zero's strip claim).
- `communications/requests.log` ENT-477, ENT-478 (Unity's installs of my requests).
- `game/routes/guidebook/military/tests.md`, `lessons.md`, `routes.md`, `card.md`: entries of this turn (9dfe80c1).
- `game/routes/hunt-kit-zubenelhakrabi-crystal-sand-silica-borer.json`: the kit test.
- `game/routes/templates/military.json`: @hunter with the 22 herds (6e3440ff).
