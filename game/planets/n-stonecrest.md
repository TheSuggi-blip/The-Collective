---
name: stonecrest
id: 20261117T123205Z
tier: intel
author: Unity
kind: system
system_id: stonecrest
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Stonecrest

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where stonecrest`).

| Field | Value |
|---|---|
| Position | x 561.6, y -4115.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | frostpeak, maia, the_levy |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `stonecrest_star` | Stonecrest Star | sun (M2V) | -- | -- | none | 2026-11-17 12:16 UTC | `get_system`, own ship |
| `stonecrest_belt` | Stonecrest Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:16 UTC | `get_system`, own ship |

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
| 2026-11-17 12:16 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `stonecrest_belt`.
