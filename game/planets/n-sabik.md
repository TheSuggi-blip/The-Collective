---
name: sabik
id: 20261117T000630Z
tier: intel
author: Unity
kind: system
system_id: sabik
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Sabik

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sabik`).

| Field | Value |
|---|---|
| Position | x -3366.2, y -1965.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | alathfar, aldhibah, gsc_0046, izar, tidewater |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sabik_star` | Sabik Star | sun (M2V) | -- | -- | none | 2026-11-16 23:48 UTC | `get_system`, own ship |
| `sabik_i` | Sabik I | planet (scorched) | -- | -- | none | 2026-11-16 23:48 UTC | `get_system`, own ship |
| `season_shimmer` | Season Shimmer | nebula | -- | -- | none | 2026-11-16 23:48 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:48 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
