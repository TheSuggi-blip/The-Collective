---
name: homam
id: 20261115T235524Z
tier: intel
author: Unity
kind: system
system_id: homam
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Homam

- system 6 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where homam`).

| Field | Value |
|---|---|
| Position | x -1361.9, y 1612.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 6 |
| Lanes | antares, bluerift, furud, gsc_0033 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `homam_star` | Homam Star | sun (M4V) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `homam_i` | Homam I | planet (scorched) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `homam_ii` | Homam II | planet (arid) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `homam_belt` | Homam Belt | asteroid_belt (metallic) | -- | iron_ore: richness 55, 560 of 100000 left; copper_ore: richness 26, 14746 of 100000 left | none | 2026-11-15 23:34 UTC | `get_poi`, own ship |
| `homam_cryobelt` | Homam Cryobelt | ice_field (cometary) | -- | water_ice: richness 57, 1298 of 50000 left; nitrogen_ice: richness 41, 49855 of 50000 left; helium_ice: richness 13, 5000 of 5000 left | none | 2026-11-15 23:34 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 23:34 UTC | own ship | Read Homam Belt: 15,306 units left in all | `get_poi`, own ship |
| 2026-11-15 23:34 UTC | own ship | Read Homam Cryobelt: 56,153 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
