---
name: hamal
id: 20261115T142802Z
tier: intel
author: Unity
kind: system
system_id: hamal
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 30
updated: 2026-11-15
---

# Hamal

Voidborn system 3 jumps from home, police level 30. No station on the chart.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where hamal`).

| Field | Value |
|---|---|
| Position | x -4062.8, y 3808.5 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 3 |
| Lanes | acubens, gj_3470, megrez, okab, thornhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `hamal_star` | Hamal Star | sun (K2III) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `hamal_i` | Hamal I | planet (tundra) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `hamal_ii` | Hamal II | planet (glacial) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `hamal_iii` | Hamal III | planet (ice_world) | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |
| `hamal_crystal_bloom` | Hamal Crystal Bloom | nebula | -- | -- | none | 2026-11-15 13:12 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 13:12 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
