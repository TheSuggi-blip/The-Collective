---
name: the_telescope
id: 20261117T174145Z
tier: intel
author: Unity
kind: system
system_id: the_telescope
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 55
updated: 2026-11-17
---

# The Telescope

Outerrim system 17 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where the_telescope`).

| Field | Value |
|---|---|
| Position | x -2538.5, y -2831.5 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 17 |
| Lanes | altais, distant_light, first_step, horizon, starfall, unknown_edge |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `zeta_minor_star` | Zeta Minor Star | sun (F8V) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `zeta_minor_i` | Zeta Minor I | planet (arid) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `the_telescope_flicker_field` | The Telescope Flicker Field | nebula | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `the_telescope_entangled_drift` | The Telescope Entangled Drift | nebula | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:07 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
