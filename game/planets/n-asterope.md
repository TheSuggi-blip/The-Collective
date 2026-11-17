---
name: asterope
id: 20261117T133331Z
tier: intel
author: Unity
kind: system
system_id: asterope
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Asterope

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where asterope`).

| Field | Value |
|---|---|
| Position | x -375.2, y -7468.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | algiedi, hd_85512, sadalbari, yarrowfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `asterope_star` | Asterope Star | sun (K2V) | -- | -- | none | 2026-11-17 13:29 UTC | `get_system`, own ship |
| `asterope_i` | Asterope I | planet (scorched) | -- | -- | none | 2026-11-17 13:29 UTC | `get_system`, own ship |
| `asterope_ii` | Asterope II | planet (arid) | -- | -- | none | 2026-11-17 13:29 UTC | `get_system`, own ship |
| `asterope_iii` | Asterope III | planet (terran) | -- | -- | none | 2026-11-17 13:29 UTC | `get_system`, own ship |
| `asterope_iv` | Asterope IV | planet (tundra) | -- | -- | none | 2026-11-17 13:29 UTC | `get_system`, own ship |
| `asterope_gas_plume` | Asterope Gas Plume | gas_cloud (molecular_cloud) | -- | argon_gas: richness 40, 608 of 50000 left; xenon_gas: richness 20, 359 of 10000 left; neon_gas: richness 48, 605 of 50000 left; chlorine_gas: richness 38, 357 of 10000 left | none | 2026-11-17 13:29 UTC | `get_poi`, own ship |
| `asterope_ice_shelf` | Asterope Ice Shelf | ice_field (cometary) | -- | water_ice: richness 52, 39906 of 50000 left; nitrogen_ice: richness 49, 48331 of 50000 left; ammonia_ice: richness 16, 7396 of 8000 left | none | 2026-11-17 13:29 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:29 UTC | own ship | Read Asterope Gas Plume: 1,929 units left in all | `get_poi`, own ship |
| 2026-11-17 13:29 UTC | own ship | Read Asterope Ice Shelf: 95,633 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
