---
name: springdale
id: 20261117T021127Z
tier: intel
author: Unity
kind: system
system_id: springdale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Springdale

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where springdale`).

| Field | Value |
|---|---|
| Position | x -6060.4, y -419.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | avior, gsc_0042, oxbow |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `springdale_star` | Springdale Star | sun (M4V) | -- | -- | none | 2026-11-17 01:19 UTC | `get_system`, own ship |
| `springdale_i` | Springdale I | planet (scorched) | -- | -- | none | 2026-11-17 01:19 UTC | `get_system`, own ship |
| `springdale_gas_cloud` | Springdale Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 44, 18362 of 50000 left; argon_gas: richness 53, 49999 of 50000 left; nebula_gas: richness 19, 4758 of 10000 left; neon_gas: richness 37, 50000 of 50000 left; krypton_gas: richness 23, 1548 of 5000 left | none | 2026-11-17 01:19 UTC | `get_poi`, own ship |

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
| 2026-11-17 01:19 UTC | own ship | Read Springdale Gas Cloud: 124,667 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
