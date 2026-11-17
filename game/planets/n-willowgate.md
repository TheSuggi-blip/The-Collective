---
name: willowgate
id: 20261117T153801Z
tier: intel
author: Unity
kind: system
system_id: willowgate
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Willowgate

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where willowgate`).

| Field | Value |
|---|---|
| Position | x -5011.8, y -3753.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | ashenmoor, gsc_0015, shadowmere, tabit, winterhold |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `willowgate_star` | Willowgate Star | sun (K5V) | -- | -- | none | 2026-11-17 15:06 UTC | `get_system`, own ship |
| `willowgate_vapor_fields` | Willowgate Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 59, 13555 of 50000 left; argon_gas: richness 32, 49999 of 50000 left; xenon_gas: richness 22, 10000 of 10000 left; neon_gas: richness 53, 50000 of 50000 left; ion_gas: richness 20, 10000 of 10000 left | none | 2026-11-17 15:06 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:06 UTC | own ship | Read Willowgate Vapor Fields: 133,554 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
