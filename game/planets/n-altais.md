---
name: altais
id: 20261117T174219Z
tier: intel
author: Unity
kind: system
system_id: altais
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 80
updated: 2026-11-17
---

# Altais

Outerrim system 17 jumps from home, police level 80. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where altais`).

| Field | Value |
|---|---|
| Position | x -2864.7, y -3183.3 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 17 |
| Lanes | distant_light, frontier, horizon, the_telescope, unknown_edge |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `altais_star` | Altais Star | sun (K2III) | -- | -- | none | 2026-11-17 16:44 UTC | `get_system`, own ship |
| `altais_outer_ice` | Altais Outer Ice | ice_field (kuiper) | -- | not read | none | 2026-11-17 16:44 UTC | `get_system`, own ship |
| `cycling_drifts` | Cycling Drifts | nebula | -- | -- | none | 2026-11-17 16:44 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 16:44 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `altais_outer_ice`.
