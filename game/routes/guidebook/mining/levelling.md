# Mining guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-21. Evidence: catalog table skills (column training); spacemolt.com/docs/skills.md; hive.py levels Zero; hive.py stats xp --member Zero.

A miner levels the work of its class first (rule F23): gathering for
the reserve trains its skills and stores what the reserve lacks.

| Skill | How the game trains it | Our routes | What it gives |
|---|---|---|---|
| Mining | mine at belts, ice fields, gas clouds; 1 XP a unit | every gather and mine route | +1% yield a level; rarer deposits picked more often |
| Deep Core Mining | mine with power 3 or more, or survey | every laser route | +5% a level, deep core deposits only |
| Piloting | travel, jump, mine, fight; missions | all | tier 2 hulls at 10 |
| Navigation | travel between systems | the shuttles, carries | -1% fuel a level |
| Refining, Crafting | refine and craft at a station | craft-steel-*, craft-piping-* | workshop speed |
| Trading | sell and buy | drains, carries | fees |
| Exploration | a first visit | far tests | survey power |

- Mining level shifts which deposit a pull picks, not how much it
  yields: the rarer one 10% of pulls at level 0, 50% at 20, 73% at 60
  (official miner guide, 2026-11-15). Richness sets the yield.
- Levels and XP an hour: hive.py levels Zero; XP per route: hive.py
  stats xp --member Zero.

### Levelling by kind of ship
Status: proven. Updated: 2026-11-21. Evidence: the plan file (tool plan, show); game/routes/templates/mining.json.

| Kind | Fit | Work | Next step |
|---|---|---|---|
| Ice miner | Mining Laser I, Ice Harvester I | `@ice-sell`, then a reserve template | a Liminal, or Ice Harvester II when a water bid carries ships |
| Laser miner | Mining Laser I | a reserve template; the drains | a Liminal |
| Seated miner | as above, a seat in the faction | the outpost's belts into faction storage | the next belts around the outpost |
| Test miner | Mining Laser I, empty hold | one test route, then its templates | lift the test on its RESULT line |

A ship without XP since the last turn is moved (rule F23).
