---
name: canopus
id: 20261117T112925Z
tier: intel
author: Unity
kind: system
system_id: canopus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Canopus

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where canopus`).

| Field | Value |
|---|---|
| Position | x 1548.5, y 923.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | ascella, hr_8832, spica, thabit |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `canopus_star` | Canopus Star | sun (M2V) | -- | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |
| `canopus_i` | Canopus I | planet (scorched) | -- | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |
| `canopus_ii` | Canopus II | planet (arid) | -- | -- | none | 2026-11-17 11:01 UTC | `get_system`, own ship |
| `canopus_alloy_remnants` | Canopus Alloy Remnants | asteroid_belt | -- | iron_ore: richness 44, 40159 of 100000 left; copper_ore: richness 22, 100000 of 100000 left; sol_alloy_ore: richness 5, 87 of 1547 left | none | 2026-11-17 11:01 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:01 UTC | own ship | Read Canopus Alloy Remnants: 140,246 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
