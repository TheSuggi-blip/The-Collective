---
name: struve_2398
id: 20261117T194613Z
tier: intel
author: Unity
kind: system
system_id: struve_2398
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Struve 2398

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where struve_2398`).

| Field | Value |
|---|---|
| Position | x 1659.3, y -534.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | algieba, fuyue, ross_248, situla |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `struve_2398_star` | Struve 2398 Star | sun (G2V) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `struve_2398_i` | Struve 2398 I | planet (scorched) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `struve_2398_ii` | Struve 2398 II | planet (arid) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `struve_2398_iii` | Struve 2398 III | planet (terran) | -- | -- | none | 2026-11-17 19:37 UTC | `get_system`, own ship |
| `struve_2398_ice_shelf` | Struve 2398 Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 57, 269 of 50000 left; helium_ice: richness 12, 262 of 5000 left | none | 2026-11-17 19:37 UTC | `get_poi`, own ship |

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
| 2026-11-17 19:37 UTC | own ship | Read Struve 2398 Ice Shelf: 531 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
