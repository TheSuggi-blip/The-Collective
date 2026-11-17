---
name: dubhe
id: 20261117T112927Z
tier: intel
author: Unity
kind: system
system_id: dubhe
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dubhe

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dubhe`).

| Field | Value |
|---|---|
| Position | x -637.1, y -2348.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | alfirk, maplevale |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dubhe_star` | Dubhe Star | sun (F8V) | -- | -- | none | 2026-11-17 11:16 UTC | `get_system`, own ship |
| `dubhe_i` | Dubhe I | planet (scorched) | -- | -- | none | 2026-11-17 11:16 UTC | `get_system`, own ship |
| `dubhe_ii` | Dubhe II | planet (arid) | -- | -- | none | 2026-11-17 11:16 UTC | `get_system`, own ship |
| `dubhe_iii` | Dubhe III | planet (terran) | -- | -- | none | 2026-11-17 11:16 UTC | `get_system`, own ship |

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
| 2026-11-17 11:16 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
