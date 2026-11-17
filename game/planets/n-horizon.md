---
name: horizon
id: 20261117T174201Z
tier: intel
author: Unity
kind: system
system_id: horizon
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 80
updated: 2026-11-17
---

# Horizon

Outerrim system 18 jumps from home, police level 80. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where horizon`).

| Field | Value |
|---|---|
| Position | x -2636.3, y -3359.7 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 18 |
| Lanes | altais, deep_range, distant_light, first_step, frontier, the_telescope |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `theta_minor_star` | Theta Minor Star | sun (G8V) | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `theta_minor_i` | Theta Minor I | planet (arid) | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |
| `horizon_phase_drift` | Horizon Phase Drift | nebula | -- | -- | none | 2026-11-17 16:55 UTC | `get_system`, own ship |

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
| 2026-11-17 16:55 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
