---
name: crosshaven
id: 20261117T153729Z
tier: intel
author: Unity
kind: system
system_id: crosshaven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Crosshaven

- system 16 jumps from home, police level 0. Station: Private Rain.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where crosshaven`).

| Field | Value |
|---|---|
| Position | x 2551.2, y 5083.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | alpheratz, diphda, gsc_0019, gsc_0034, lilii_borea, thuban, tiaki |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `crosshaven_star` | Crosshaven Star | sun (M4V) | -- | -- | none | 2026-11-17 15:31 UTC | `get_system`, own ship |
| `crosshaven_i` | Crosshaven I | planet (scorched) | -- | -- | none | 2026-11-17 15:31 UTC | `get_system`, own ship |
| `crosshaven_ii` | Crosshaven II | planet (arid) | -- | -- | none | 2026-11-17 15:31 UTC | `get_system`, own ship |
| `crosshaven_iii` | Crosshaven III | planet (terran) | -- | -- | none | 2026-11-17 15:31 UTC | `get_system`, own ship |
| `crosshaven_ice_belt` | Crosshaven Ice Belt | ice_field (cometary) | -- | water_ice: richness 43, 624 of 50000 left; nitrogen_ice: richness 34, 43794 of 50000 left; helium_ice: richness 13, 4465 of 5000 left; methane_ice: richness 18, 640 of 9000 left | none | 2026-11-17 15:31 UTC | `get_poi`, own ship |
| `black_thread` | Black Thread | asteroid_belt | -- | iron_ore: richness 40, 45876 of 100000 left; copper_ore: richness 35, 88654 of 100000 left; darksteel_ore: richness 5, 1 of 325 left | none | 2026-11-17 15:31 UTC | `get_poi`, own ship |
| `warm_stain_vent` | Warm Stain Vent | asteroid_belt | -- | iron_ore: richness 43, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; plasma_residue: richness 8, 987 of 987 left | none | 2026-11-17 15:31 UTC | `get_poi`, own ship |
| `d1c54e3a473f4d3ce9c7603c5e0c6b38` | Private Rain | station | `b866042eb326d851de78e888deac8515` | -- | none | 2026-11-17 15:31 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Private Rain (`b866042eb326d851de78e888deac8515`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 15:31 UTC | `get_system`, own ship |

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
| 2026-11-17 15:31 UTC | own ship | Read Crosshaven Ice Belt: 49,523 units left in all | `get_poi`, own ship |
| 2026-11-17 15:31 UTC | own ship | Read Black Thread: 134,531 units left in all | `get_poi`, own ship |
| 2026-11-17 15:31 UTC | own ship | Read Warm Stain Vent: 200,987 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
