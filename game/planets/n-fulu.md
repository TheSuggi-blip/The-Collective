---
name: fulu
id: 20261117T010824Z
tier: intel
author: Unity
kind: system
system_id: fulu
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Fulu

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where fulu`).

| Field | Value |
|---|---|
| Position | x -6956.7, y 126.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | gsc_0006, gsc_0028 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fulu_star` | Fulu Star | sun (M6V) | -- | -- | none | 2026-11-17 00:48 UTC | `get_system`, own ship |
| `fulu_vapor_fields` | Fulu Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 51, 47604 of 50000 left; argon_gas: richness 37, 50000 of 50000 left; plasma_gas: richness 29, 9844 of 10000 left; xenon_gas: richness 17, 10000 of 10000 left; chlorine_gas: richness 39, 2423 of 10000 left; ion_gas: richness 25, 10000 of 10000 left | none | 2026-11-17 00:48 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:48 UTC | own ship | Read Fulu Vapor Fields: 129,871 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
