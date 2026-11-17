---
name: nunki
id: 20261117T163941Z
tier: intel
author: Unity
kind: system
system_id: nunki
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Nunki

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nunki`).

| Field | Value |
|---|---|
| Position | x -1144.6, y -5533.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | acamar, albali, gsc_0005, mintaka |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nunki_star` | Nunki Star | sun (B2V) | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |
| `nunki_wind_sheath` | Nunki Wind Sheath | gas_cloud (emission) | -- | plasma_gas: richness 45, 598 of 20000 left; ion_gas: richness 30, 531 of 15000 left; nebula_gas: richness 20, 533 of 10000 left | none | 2026-11-17 16:38 UTC | `get_poi`, own ship |
| `nunki_poi_0` | Nunki | sun | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |
| `sys_0043_poi_0` | Nunki | sun | -- | -- | none | 2026-11-17 16:38 UTC | `get_system`, own ship |

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
| 2026-11-17 16:38 UTC | own ship | Read Nunki Wind Sheath: 1,662 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
