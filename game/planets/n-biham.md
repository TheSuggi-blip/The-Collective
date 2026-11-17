---
name: biham
id: 20261117T041724Z
tier: intel
author: Unity
kind: system
system_id: biham
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Biham

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where biham`).

| Field | Value |
|---|---|
| Position | x -2064.7, y 4920.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | elnath, felis, gliese_876, gsc_0035, jasmine, sualocin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `biham_star` | Biham Star | sun (M2V) | -- | -- | none | 2026-11-17 03:34 UTC | `get_system`, own ship |
| `biham_i` | Biham I | planet (scorched) | -- | -- | none | 2026-11-17 03:34 UTC | `get_system`, own ship |
| `biham_ice_shelf` | Biham Ice Shelf | ice_field (cometary) | -- | water_ice: richness 58, 43080 of 50000 left; nitrogen_ice: richness 49, 50000 of 50000 left | none | 2026-11-17 03:34 UTC | `get_poi`, own ship |

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
| 2026-11-17 03:34 UTC | own ship | Read Biham Ice Shelf: 93,080 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
