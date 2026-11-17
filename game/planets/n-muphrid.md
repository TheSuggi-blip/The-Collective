---
name: muphrid
id: 20261117T133351Z
tier: intel
author: Unity
kind: system
system_id: muphrid
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Muphrid

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where muphrid`).

| Field | Value |
|---|---|
| Position | x 4742.7, y 1092.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | 61_cygni, alsephina, hadar, minkar, zubenelgenubi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `muphrid_star` | Muphrid Star | sun (K6V) | -- | -- | none | 2026-11-17 13:11 UTC | `get_system`, own ship |
| `muphrid_i` | Muphrid I | planet (scorched) | -- | -- | none | 2026-11-17 13:11 UTC | `get_system`, own ship |
| `worklight_outcrop` | Worklight Outcrop | asteroid_belt | -- | silicon_ore: richness 43, 4325 of 20000 left | none | 2026-11-17 13:11 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:11 UTC | own ship | Read Worklight Outcrop: 4,325 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
