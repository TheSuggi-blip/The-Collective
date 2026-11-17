---
name: iron_reach
id: 20261117T143542Z
tier: intel
author: Unity
kind: system
system_id: iron_reach
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 80
updated: 2026-11-17
---

# Iron Reach

Crimson system 19 jumps from home, police level 80. Station: Iron Reach Mining Colony.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where iron_reach`).

| Field | Value |
|---|---|
| Position | x 4606.5, y 2934.5 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 19 |
| Lanes | blood_forge, krynn, the_anvil, the_crucible |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_ember` | The Ember | sun (K6V) | -- | -- | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `rustfield` | Rustfield | planet (arid) | -- | -- | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `ore_depot` | Ore Depot | planet (glacial) | -- | -- | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `iron_reach_mineral_fields` | Iron Reach Mineral Fields | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `iron_reach_mining_colony` | Iron Reach Mining Colony | station | `iron_reach_mining_colony` | -- | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `the_motherlode` | The Motherlode | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 14:31 UTC | `get_system`, own ship |
| `rubys_vigil` | Ruby's Vigil | relic | -- | -- | none | 2026-11-17 14:31 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Iron Reach Mining Colony (`iron_reach_mining_colony`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:31 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:31 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `iron_reach_mineral_fields`, `the_motherlode`.
