# Mining guidebook -- Missions (topic-missions.md)

### Voidborn once routes for miners
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/onetime.json; the hand-in lines of data/fleet/dispatch.log; the runs of each route (hive.py route <id>).

The `once` routes of the list First: every pilot flies each once, the
Voidborn chain to its end even for the fuel alone (rules F34, F35). A
once run that found nothing counts as done for that pilot.

| Route | Pays once |
|---|---|
| `voidborn-concurrent` | 3,000 cr; its two soma come with the accept |
| `voidborn-mining-missions` | 1,500 + 1,800 cr (Iron Supply Run, Copper Requisition) |
| `voidborn-precedence` | 4,000 cr |
| `voidborn-signal-fragments` | 7,000 cr (Navigation 3) |
| `voidborn-conductive-lattice` | about 10,900 cr (the Node Beta chain) |
| `voidborn-network-expansion` | 1,500 cr |
| `voidborn-first-hunt-*` | 930 to 970 cr; the home herds are thin |
| `voidborn-crystal-resonance` | 4,000 cr, Voidborn Mastery 35: 20 energy crystal mined |
| `voidborn-material-synthesis` | 1,500 cr, Voidborn Mastery 25: 10 iron mined, 1 steel plate smelted |

The last two show only to a pilot that holds The Collective Provides;
each paid on its first run (2026-11-17) and flies 4 ships at a time from
2026-11-21. Amplification Materials (15 silver ore, 4,000 cr) has no
route: the nearest silver field with ore lay 14 jumps out (2026-11-17).

### Mining missions of the boards
Status: proven. Updated: 2026-11-21. Evidence: data/missions/*.json (2026-11-17); the hand-in lines of data/fleet/dispatch.log; knowledge/mining-missions.md of Zero.

Each counts only units the pilot mines itself, and is bounded by its
rare field, shared with every player: read the field before each lift.

| Mission | Asks | Pays | Route, state |
|---|---|---|---|
| Deep Core Prospecting (nine boards) | 20 platinum | 5,000 cr, deep core 25 XP | `mission-deep-core-prospecting-first-step` (Deep Range, 2 ships); `-nova-terra` rests: Markab Belt read 0 after 11 hand-ins |
| The Forge Tax (The Crucible Garrison) | 20 cobalt | 5,000 cr, mining 20 XP | `mission-the-forge-tax-crucible` (Hearsay Cobalt, 3 ships) |
| Titanium Extraction Contract (ten boards) | 20 titanium | 3,500 cr | none: no near field holds a load |
| The Collective Provides (Central Nexus) | 20 nickel | 2,500 cr, Voidborn Mastery 25 | Trade's `voidborn-collective-provides` |

### Chain links and hand-ins
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-103, ENT-104; data/fleet/onetime.json; fill.py.

- A chain's later links show on a board only to a pilot that holds the
  link before: before saying no board offers a mission, read the chain's
  route note, data/fleet/onetime.json and a board read by such a pilot.
- A mission is reported done only from its hand-in line in
  data/fleet/dispatch.log, never from a ship's missions_done.
- A once route that fill.py adds on another role's figure is watched
  until a miner's first run and dropped at "not offered" (Cracking the
  Shell needs First Hunt booked, 2026-11-16).
- Each turn count the pilots that have not flown the once-per-pilot
  mining missions: the ship files minus the hand-in lines.
