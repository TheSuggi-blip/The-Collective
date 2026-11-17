---
name: highcrest
id: 20261117T153740Z
tier: intel
author: Unity
kind: system
system_id: highcrest
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Highcrest

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where highcrest`).

| Field | Value |
|---|---|
| Position | x -882.6, y -4541.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | 36_ophiuchi, almaaz, azelfafage, gsc_0005, zosma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `highcrest_star` | Highcrest Star | sun (M2V) | -- | -- | none | 2026-11-17 15:28 UTC | `get_system`, own ship |
| `highcrest_i` | Highcrest I | planet (scorched) | -- | -- | none | 2026-11-17 15:28 UTC | `get_system`, own ship |
| `highcrest_ii` | Highcrest II | planet (arid) | -- | -- | none | 2026-11-17 15:28 UTC | `get_system`, own ship |
| `highcrest_iii` | Highcrest III | planet (terran) | -- | -- | none | 2026-11-17 15:28 UTC | `get_system`, own ship |
| `highcrest_iv` | Highcrest IV | planet (tundra) | -- | -- | none | 2026-11-17 15:28 UTC | `get_system`, own ship |
| `highcrest_belt` | Highcrest Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 15:28 UTC | `get_system`, own ship |

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
| 2026-11-17 15:28 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `highcrest_belt`.
