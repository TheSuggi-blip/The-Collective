---
name: rimegate
id: 20261117T163946Z
tier: intel
author: Unity
kind: system
system_id: rimegate
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rimegate

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rimegate`).

| Field | Value |
|---|---|
| Position | x -6410.3, y -2695.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | betelgeuse, dabih, gsc_0037, tejat, veritate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rimegate_star` | Rimegate Star | sun (F8V) | -- | -- | none | 2026-11-17 16:19 UTC | `get_system`, own ship |
| `rimegate_i` | Rimegate I | planet (scorched) | -- | -- | none | 2026-11-17 16:19 UTC | `get_system`, own ship |
| `rimegate_ii` | Rimegate II | planet (arid) | -- | -- | none | 2026-11-17 16:19 UTC | `get_system`, own ship |
| `rimegate_iii` | Rimegate III | planet (terran) | -- | -- | none | 2026-11-17 16:19 UTC | `get_system`, own ship |
| `hollow_light` | Hollow Light | nebula | -- | -- | none | 2026-11-17 16:19 UTC | `get_system`, own ship |

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
| 2026-11-17 16:19 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
