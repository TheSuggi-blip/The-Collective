# Intel guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-21. Evidence: hive.py levels Oracle; the plan file (tool plan, show); MISSION.md.

The scout class in short (rule F14): 30 scouts, about ten explorers and
twenty readers (Suggi, 2026-11-17). Levels now: the tool fleet,
view=levels, member Oracle. Fits: ships.md; the census lists and the
plan: routes.md; what is under test: tests.md; the traps: lessons.md.

### Ships
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/ships/; catalog table hulls; browse_ships all_stations (2026-11-21); scouting/<system>.json `survey`; ships.md.

- Tier 0, every scout: the starter Threshold (speed 1, hold 65, tank 95,
  two utility slots), Mining Laser I and Pulse Laser I, stance flee.
- Fit next: Survey Scanner I in the second utility slot (six scouts carry
  one; need survey-scanner-i). A ship with a scanner surveys every system
  it reads (census.py). Then a Mining Survey Probe for the faint
  signatures (tests.md), then Ship Scanner I.
- Next hull: tier 1 needs no Piloting (table hulls): Qualia (explorer,
  speed 3, tank 130, three utility slots, no weapon slot), Eigenstate
  (scout, speed 3) or Fugue (courier, speed 4). The Qualia test is closed:
  over three times the fuel a read, no second one (tests.md); tier 2 at
  Piloting 10, judged by fuel a read.
- Style: read and leave, hold empty beyond the border (rule F3), never
  fire first (F2), hunt on the way only what passes both gauges of F9,
  pirates by F27 with a test first.

### Skills
Status: proven. Updated: 2026-11-21. Evidence: catalog table skills (column training); hive.py levels Oracle; table ship_skills.

In the order a scout levels them. Levels and XP an hour: hive.py levels
Oracle; per pilot: table ship_skills.

| Skill | Why | What trains it | Next goal |
|---|---|---|---|
| Exploration | +1% survey power a level | a pilot's own first visit to a system, about 5 XP | median 4 |
| Navigation | -1% fuel and jump time a level | every jump of every census | median 7 |
| Piloting | hull tiers at 10, 20, 30, 50 | every route; missions | 10 |
| Scanning | +1% scanner effect a level | survey_system only (a scanner aboard) | 2 on the scanner scouts |
| Xenobiology, Weapons, Gunnery | molt value, damage | the scouts' hunt routes | not set |
| Mining, Deep Core Mining | not the class's | the gather fallback only | none |
