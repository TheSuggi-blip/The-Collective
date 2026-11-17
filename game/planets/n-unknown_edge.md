---
name: unknown_edge
id: 20261117T174143Z
tier: intel
author: Unity
kind: system
system_id: unknown_edge
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 55
updated: 2026-11-17
---

# Unknown Edge

Outerrim system 16 jumps from home, police level 55. Station: Unknown Edge Waystation.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where unknown_edge`).

| Field | Value |
|---|---|
| Position | x -3168.1, y -2817.4 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 16 |
| Lanes | altais, distant_light, last_light, the_telescope |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `edgelight` | Edgelight | sun (B6V) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `unknown_edge_i` | Unknown Edge I | planet (scorched) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `unknown_edge_ii` | Unknown Edge II | planet (arid) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `unknown_edge_iii` | Unknown Edge III | planet (tundra) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `unknown_edge_mineral_fields` | Unknown Edge Mineral Fields | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `unknown_edge_waystation` | Unknown Edge Waystation | station | `unknown_edge_waystation` | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Unknown Edge Waystation (`unknown_edge_waystation`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:59 UTC | `get_system`, own ship |

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
| 2026-11-17 16:59 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `unknown_edge_mineral_fields`.
