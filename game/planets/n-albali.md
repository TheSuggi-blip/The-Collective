---
name: albali
id: 20261117T163922Z
tier: intel
author: Unity
kind: system
system_id: albali
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Albali

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where albali`).

| Field | Value |
|---|---|
| Position | x -887.4, y -5771.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | acamar, mintaka, nunki, regulus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `albali_star` | Albali Star | sun (M6V) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |
| `albali_i` | Albali I | planet (scorched) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |
| `albali_ii` | Albali II | planet (arid) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |
| `albali_iii` | Albali III | planet (terran) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |
| `albali_iv` | Albali IV | planet (jovian) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |
| `albali_v` | Albali V | planet (glacial) | -- | -- | none | 2026-11-17 16:09 UTC | `get_system`, own ship |

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
| 2026-11-17 16:09 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
