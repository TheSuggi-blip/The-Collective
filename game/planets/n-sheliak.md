---
name: sheliak
id: 20261117T112931Z
tier: intel
author: Unity
kind: system
system_id: sheliak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sheliak

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sheliak`).

| Field | Value |
|---|---|
| Position | x -4065.3, y -1433.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | alathfar, alsciaukat, merak, merope, titawin, zubenelhakrabi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sheliak_star` | Sheliak Star | sun (M4V) | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `sheliak_belt` | Sheliak Belt | asteroid_belt (metallic) | -- | iron_ore: richness 48, 85834 of 100000 left; copper_ore: richness 37, 99607 of 100000 left; aluminum_ore: richness 48, 2060 of 30000 left; manganese_ore: richness 22, 378 of 14000 left | none | 2026-11-17 10:27 UTC | `get_poi`, own ship |
| `rayfall_shimmer` | Rayfall Shimmer | nebula | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |
| `sheliak_weak_superposition` | Sheliak Weak Superposition | nebula | -- | -- | none | 2026-11-17 10:27 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 10:27 UTC | own ship | Read Sheliak Belt: 187,879 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
