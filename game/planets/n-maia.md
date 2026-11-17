---
name: maia
id: 20261117T165710Z
tier: intel
author: Unity
kind: system
system_id: maia
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Maia

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where maia`).

| Field | Value |
|---|---|
| Position | x -5.7, y -4223.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | 36_ophiuchi, frostpeak, kurhah, stonecrest, wazn |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `maia_star` | Maia Star | sun (B8III) | -- | -- | none | 2026-11-17 15:57 UTC | `get_system`, own ship |
| `maia_reflection_nebula` | Maia Reflection Nebula | gas_cloud (reflection) | -- | nebula_gas: richness 55, 1001 of 35000 left; hydrogen_gas: richness 30, 770 of 20000 left; argon_gas: richness 20, 534 of 12000 left | none | 2026-11-17 15:57 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:57 UTC | own ship | Read Maia Reflection Nebula: 2,305 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
