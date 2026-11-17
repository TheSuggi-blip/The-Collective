---
name: jishui
id: 20261117T092730Z
tier: intel
author: Unity
kind: system
system_id: jishui
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Jishui

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where jishui`).

| Field | Value |
|---|---|
| Position | x -91.7, y 5753.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | alnilam, fomalhaut |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `jishui_star` | Jishui Star | sun (K4V) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `jishui_i` | Jishui I | planet (scorched) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `jishui_ii` | Jishui II | planet (arid) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `jishui_iii` | Jishui III | planet (terran) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `plainrock_field` | Plainrock Field | asteroid_belt | -- | carbon_ore: richness 31, 1266 of 30000 left | none | 2026-11-17 09:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:16 UTC | own ship | Read Plainrock Field: 1,266 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
