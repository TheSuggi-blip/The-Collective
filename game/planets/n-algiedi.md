---
name: algiedi
id: 20261117T143526Z
tier: intel
author: Unity
kind: system
system_id: algiedi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Algiedi

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where algiedi`).

| Field | Value |
|---|---|
| Position | x -635.9, y -7357.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | asterope, hd_10647, hd_85512, unukalhai, yarrowfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `algiedi_star` | Algiedi Star | sun (F8V) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |
| `algiedi_i` | Algiedi I | planet (scorched) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |
| `algiedi_ii` | Algiedi II | planet (arid) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |
| `algiedi_iii` | Algiedi III | planet (terran) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |
| `algiedi_iv` | Algiedi IV | planet (tundra) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |
| `algiedi_v` | Algiedi V | planet (glacial) | -- | -- | none | 2026-11-17 13:36 UTC | `get_system`, own ship |

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
| 2026-11-17 13:36 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
