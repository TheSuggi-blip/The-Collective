---
name: alderamin
id: 20261117T041722Z
tier: intel
author: Unity
kind: system
system_id: alderamin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alderamin

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alderamin`).

| Field | Value |
|---|---|
| Position | x -1195.6, y 5166.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | alnilam, azha, greenvale, groombridge_1618, gsc_0035, silverbend |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alderamin_star` | Alderamin Star | sun (A0V) | -- | -- | none | 2026-11-17 04:11 UTC | `get_system`, own ship |
| `alderamin_i` | Alderamin I | planet (scorched) | -- | -- | none | 2026-11-17 04:11 UTC | `get_system`, own ship |
| `alderamin_ii` | Alderamin II | planet (arid) | -- | -- | none | 2026-11-17 04:11 UTC | `get_system`, own ship |
| `alderamin_iii` | Alderamin III | planet (terran) | -- | -- | none | 2026-11-17 04:11 UTC | `get_system`, own ship |

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
| 2026-11-17 04:11 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
