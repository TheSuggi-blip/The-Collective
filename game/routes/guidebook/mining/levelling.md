# Mining guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section 4.

Which skills a ship of this division levels and on which work (rules
F23, F30): the work of its own class first. A miner's class is mining,
so gathering for the reserve trains its own skills and stores what the
reserve lacks at once. Sources: the catalog 0.723.2 (table `skills`,
column `training`), the official skills page
(https://www.spacemolt.com/docs/skills.md), the pilots' files (table
`ship_skills`) and `hive.py levels Zero`, read 2026-11-17 07:13 UTC: 60
miners, 36 hours played (median).

| Skill | How the game trains it | Our routes that train it | Level of 60 miners (lowest / median / highest), XP an hour | What it gives |
|---|---|---|---|---|
| Mining | Mine at asteroid belts, ice fields or gas clouds | every gather and mine route; one XP a unit mined | 4 / 6 / 8, 154 | +1% yield a level on every resource; the pull's choice leans to rarer ores |
| Deep Core Mining | Mine with equipment of power 3 or more, or reveal deep core deposits with survey_system | every gather route (Mining Laser I has power 5) | 4 / 7 / 8, 180 | +5% a level from hidden deep core deposits only; nothing on ordinary deposits |
| Piloting | Fly: travel, jump, mine, fight; a bonus for missions | all; the more jumps, the more | 5 / 7 / 8, 171 | in-system speed; tier 2 hulls at 10, about 48 hours away at that rate |
| Navigation | Travel between systems and places | the gather shuttles (a jump each load), carries, `train-navigation-trader` | 3 / 4 / 5, 49 | -1% fuel, jump fuel and jump time a level |
| Trading | Sell and buy | the drains and carries | 0 / 2 / 3, 10 | market fees |
| Exploration | Visit a system for the first time | the far tests | 2 / 2 / 2, 10 | survey power |
| Refining | Refine ores, process gases or refine ice at a station | none of ours | 0 | workshop speed beside Crafting |
| Scanning, Drone Control | Survey or query places; deploy drones | none of ours | 0 | survey reveals deposits; drone mining yield |

- What the ships farm: iron and copper ore, about half and half, into
  storage at Node Beta and The Experiment, with a little carbon, gold
  and platinum (hive.py flow Zero, the 4 hours to 07:15 UTC: iron +7,062
  an hour, copper +7,022, carbon +112, gold +35, platinum +15).
- Mining XP is one point per unit mined; level 5 needs 900 XP, level 6
  1,285 (the pilots' files). Deep Core Mining rises as fast because the
  laser counts as advanced equipment; it pays only on deep core
  deposits, which a survey reveals and no route of ours mines yet.
- Mining level shifts which deposit a pull picks, not how much it
  yields: the rarer deposit is picked 10% of the time at level 0, 50% at
  20 (the official miner guide, read 2026-11-15).
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5; a tier 1 hull asks
  no Piloting (table `hulls`, piloting_required empty for tier 1).
- Ships on work of the class: 57 of 60 miners mined or gathered at the
  start of this turn (07:05 UTC, fleet file: 34 Schedar, 20 Ironhollow,
  one each at Echo Ejecta, Garnet and the Acubens carbon); the other
  three flew missions that pay once and an ice test. After the turn the
  same 57 plus the one returned from the null-matter tests.

| Kind of ship | Fit | Work and template | Skills it raises | Next step |
|---|---|---|---|---|
| Ice miner | Mining Laser I, Ice Harvester I, Pulse Laser I | `@ice-sell` first, then `@reserve-*` | Mining, Deep Core Mining by the laser, Piloting, Navigation; Trading on the drains | A Liminal (section 5) or Ice Harvester II when a water bid carries ships again |
| Laser miner | Mining Laser I, Pulse Laser I | `@reserve-*` and the drains of `@ice-sell` | Mining, Deep Core Mining, Piloting, Navigation | A Liminal (section 5) |
| Test miner beyond the border | Mining Laser I, empty hold | one test route, then its templates | Piloting, Navigation, Exploration, Mining | Lift the test when its RESULT line holds |
