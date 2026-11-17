---
name: ridgecrest
id: 20261117T092737Z
tier: intel
author: Unity
kind: system
system_id: ridgecrest
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ridgecrest

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ridgecrest`).

| Field | Value |
|---|---|
| Position | x -1658.9, y -835.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | celaeno, cervantes, gienah, grumium, hatysa, nembus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ridgecrest_star` | Ridgecrest Star | sun (M4V) | -- | -- | none | 2026-11-17 08:49 UTC | `get_system`, own ship |
| `ridgecrest_i` | Ridgecrest I | planet (scorched) | -- | -- | none | 2026-11-17 08:49 UTC | `get_system`, own ship |
| `ridgecrest_ii` | Ridgecrest II | planet (arid) | -- | -- | none | 2026-11-17 08:49 UTC | `get_system`, own ship |
| `ridgecrest_ice_shelf` | Ridgecrest Ice Shelf | ice_field (cometary) | -- | water_ice: richness 50, 45577 of 50000 left; nitrogen_ice: richness 51, 49837 of 50000 left | none | 2026-11-17 08:49 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:49 UTC | own ship | Read Ridgecrest Ice Shelf: 95,414 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
