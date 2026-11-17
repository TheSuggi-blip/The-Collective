---
name: last_light
id: 20261117T174156Z
tier: intel
author: Unity
kind: system
system_id: last_light
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 30
updated: 2026-11-17
---

# Last Light

Outerrim system 15 jumps from home, police level 30. Station: Ramen's Rest.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where last_light`).

| Field | Value |
|---|---|
| Position | x -3650.4, y -2627.3 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 15 |
| Lanes | ain, fang, gsc_0046, tidewater, unknown_edge |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `eventide` | Eventide | sun (G3V) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_i` | Last Light I | planet (arid) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_ii` | Last Light II | planet (terran) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_iii` | Last Light III | planet (terran) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_iv` | Last Light IV | planet (tundra) | -- | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_mineral_fields` | Last Light Mineral Fields | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `last_light_nebula` | Last Light Nebula | gas_cloud (emission) | -- | not read | none | 2026-11-17 16:59 UTC | `get_system`, own ship |
| `ramens_rest` | Ramen's Rest | station | `ramens_rest` | -- | none | 2026-11-17 16:59 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ramen's Rest (`ramens_rest`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:59 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

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
- Not read yet: `last_light_mineral_fields`, `last_light_nebula`.
