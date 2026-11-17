---
name: mirzam
id: 20261117T123151Z
tier: intel
author: Unity
kind: system
system_id: mirzam
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mirzam

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mirzam`).

| Field | Value |
|---|---|
| Position | x 920.8, y -7448.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alcor, alniyat, embervale, gsc_0025 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mirzam_star` | Mirzam Star | sun (M4V) | -- | -- | none | 2026-11-17 12:28 UTC | `get_system`, own ship |
| `mirzam_i` | Mirzam I | planet (scorched) | -- | -- | none | 2026-11-17 12:28 UTC | `get_system`, own ship |
| `mirzam_ii` | Mirzam II | planet (arid) | -- | -- | none | 2026-11-17 12:28 UTC | `get_system`, own ship |
| `mirzam_iii` | Mirzam III | planet (terran) | -- | -- | none | 2026-11-17 12:28 UTC | `get_system`, own ship |

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
| 2026-11-17 12:28 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
