---
name: regulus
id: 20261117T163945Z
tier: intel
author: Unity
kind: system
system_id: regulus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Regulus

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where regulus`).

| Field | Value |
|---|---|
| Position | x -948.5, y -6182.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | albali, hd_10647, kepler_186, mintaka |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `regulus_star` | Regulus Star | sun (M2V) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_i` | Regulus I | planet (scorched) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_ii` | Regulus II | planet (arid) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_iii` | Regulus III | planet (terran) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_iv` | Regulus IV | planet (tundra) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_v` | Regulus V | planet (glacial) | -- | -- | none | 2026-11-17 15:44 UTC | `get_system`, own ship |
| `regulus_vapor_fields` | Regulus Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 65, 15472 of 50000 left; plasma_gas: richness 30, 4182 of 10000 left; xenon_gas: richness 27, 5401 of 10000 left; neon_gas: richness 41, 50000 of 50000 left | none | 2026-11-17 15:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:44 UTC | own ship | Read Regulus Vapor Fields: 75,055 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
