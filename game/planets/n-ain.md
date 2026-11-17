---
name: ain
id: 20261117T133324Z
tier: intel
author: Unity
kind: system
system_id: ain
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ain

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ain`).

| Field | Value |
|---|---|
| Position | x -4179.1, y -2785.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | fang, last_light, rukbat, tarazed |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ain_star` | Ain Star | sun (K2III) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `ain_b` | Ain B | planet (jovian) | -- | -- | none | 2026-11-17 13:18 UTC | `get_system`, own ship |
| `ain_ice_belt` | Ain Ice Belt | ice_field (kuiper) | -- | not read | none | 2026-11-17 13:18 UTC | `get_system`, own ship |

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
| 2026-11-17 13:18 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `ain_ice_belt`.
