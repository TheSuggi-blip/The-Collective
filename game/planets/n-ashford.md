---
name: ashford
id: 20261117T174218Z
tier: intel
author: Unity
kind: system
system_id: ashford
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ashford

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ashford`).

| Field | Value |
|---|---|
| Position | x 3011.6, y -4711.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | alrescha, farpoint, ravensbrook, ross_128, treasure_cache |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ashford_star` | Ashford Star | sun (K4V) | -- | -- | none | 2026-11-17 17:11 UTC | `get_system`, own ship |
| `ashford_ice_shelf` | Ashford Ice Shelf | ice_field (cometary) | -- | water_ice: richness 41, 468 of 50000 left; nitrogen_ice: richness 39, 1206 of 50000 left | none | 2026-11-17 17:11 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:11 UTC | own ship | Read Ashford Ice Shelf: 1,674 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
