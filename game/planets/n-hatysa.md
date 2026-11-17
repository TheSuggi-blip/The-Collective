---
name: hatysa
id: 20261117T000627Z
tier: intel
author: Unity
kind: system
system_id: hatysa
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Hatysa

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where hatysa`).

| Field | Value |
|---|---|
| Position | x -1913.8, y -1081.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | cervantes, gienah, nembus, oakridge, ridgecrest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `hatysa_star` | Hatysa Star | sun (G5V) | -- | -- | none | 2026-11-16 23:45 UTC | `get_system`, own ship |
| `hatysa_i` | Hatysa I | planet (scorched) | -- | -- | none | 2026-11-16 23:45 UTC | `get_system`, own ship |
| `hatysa_ii` | Hatysa II | planet (arid) | -- | -- | none | 2026-11-16 23:45 UTC | `get_system`, own ship |
| `hatysa_iii` | Hatysa III | planet (terran) | -- | -- | none | 2026-11-16 23:45 UTC | `get_system`, own ship |
| `hatysa_vapor_fields` | Hatysa Vapor Fields | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-16 23:45 UTC | `get_system`, own ship |
| `hatysa_ice_shelf` | Hatysa Ice Shelf | ice_field (kuiper) | -- | not read | none | 2026-11-16 23:45 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:45 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `hatysa_vapor_fields`, `hatysa_ice_shelf`.
