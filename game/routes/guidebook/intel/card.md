# Intel guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: hive.py levels Oracle; the plan file (tool plan, show); MISSION.md.

The scout class in short (rule F14): about a third explorers, the rest
readers (Suggi, 2026-11-17: ten of thirty); the count now: FLEET.md
and hive.py upgrades intel, by empire. Levels now: the tool fleet,
view=levels, member Oracle. Fits: ships.md; the census lists and the
plan: routes.md; what is under test: tests.md; the traps: lessons.md.

### Ships
Status: proven. Updated: 2026-11-24. Evidence: data/fleet/ships/; catalog table hulls; table ship_modules; browse_ships all_stations (2026-11-21); scouting/<system>.json `survey`; hive.py upgrades intel; ships.md.

- Tier 0, by empire: voidborn the Threshold (speed 1, hold 65, tank 95,
  two utility slots), outerrim the Cobble, nebula the Prospect; Mining
  Laser I and Pulse Laser I aboard, stance flee. The Mining Laser I
  stays while the pilot's own-empire missions that mine are open (F35).
- Fit next: a survey scanner in the second utility slot (who carries one:
  table ship_modules; Survey Scanner I has no seller, the II is fitted at
  Central Nexus). A ship with a scanner surveys every system it reads
  (census.py). Then a Mining Survey Probe for the faint signatures
  (tests.md), then Ship Scanner I.
- Next hull: tier 1 needs no Piloting (voidborn Qualia, Eigenstate;
  outerrim Warranty Void; nebula Venture). The Qualia test is closed:
  over three times the fuel a read, no second one (tests.md). Tier 2 at
  Piloting 10 (Confluence; Dust Devil, Terms and Conditions; Prospectus,
  Arbitrage) is judged by fuel a read, never bought for Piloting alone.
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
