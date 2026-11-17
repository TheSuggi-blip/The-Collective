---
name: distant_light
id: 20261117T174212Z
tier: intel
author: Unity
kind: system
system_id: distant_light
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 55
updated: 2026-11-17
---

# Distant Light

Outerrim system 17 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where distant_light`).

| Field | Value |
|---|---|
| Position | x -2925.7, y -2903.4 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 17 |
| Lanes | altais, horizon, the_telescope, unknown_edge |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rigel_minor_star` | Rigel Minor Star | sun (G5V) | -- | -- | none | 2026-11-17 16:56 UTC | `get_system`, own ship |
| `rigel_minor_i` | Rigel Minor I | planet (arid) | -- | -- | none | 2026-11-17 16:56 UTC | `get_system`, own ship |
| `rigel_minor_ii` | Rigel Minor II | planet (tundra) | -- | -- | none | 2026-11-17 16:56 UTC | `get_system`, own ship |
| `superposition_pocket` | Superposition Pocket | nebula | -- | -- | none | 2026-11-17 16:56 UTC | `get_system`, own ship |

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
| 2026-11-17 16:56 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
