---
name: coalridge
id: 20261117T184417Z
tier: intel
author: Unity
kind: system
system_id: coalridge
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Coalridge

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where coalridge`).

| Field | Value |
|---|---|
| Position | x 2875.7, y 1667.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | ankaa, propus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `coalridge_star` | Coalridge Star | sun (K6V) | -- | -- | none | 2026-11-17 17:54 UTC | `get_system`, own ship |
| `coalridge_i` | Coalridge I | planet (scorched) | -- | -- | none | 2026-11-17 17:54 UTC | `get_system`, own ship |
| `coalridge_ii` | Coalridge II | planet (arid) | -- | -- | none | 2026-11-17 17:54 UTC | `get_system`, own ship |
| `the_black_ridge` | The Black Ridge | asteroid_belt (mixed) | -- | carbon_ore: richness 90, 144 of 200000 left | none | 2026-11-17 17:54 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:54 UTC | own ship | Read The Black Ridge: 144 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
