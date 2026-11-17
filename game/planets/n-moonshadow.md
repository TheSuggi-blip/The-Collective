---
name: moonshadow
id: 20261117T123152Z
tier: intel
author: Unity
kind: system
system_id: moonshadow
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Moonshadow

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where moonshadow`).

| Field | Value |
|---|---|
| Position | x 3246.2, y -5561.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | 55_cancri, fafnir, gsc_0032, heze, ravensbrook, ross_128 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `moonshadow_star` | Moonshadow Star | sun (M2V) | -- | -- | none | 2026-11-17 12:06 UTC | `get_system`, own ship |
| `moonshadow_i` | Moonshadow I | planet (scorched) | -- | -- | none | 2026-11-17 12:06 UTC | `get_system`, own ship |
| `moonshadow_ii` | Moonshadow II | planet (arid) | -- | -- | none | 2026-11-17 12:06 UTC | `get_system`, own ship |
| `moonshadow_iii` | Moonshadow III | planet (terran) | -- | -- | none | 2026-11-17 12:06 UTC | `get_system`, own ship |
| `moonshadow_iv` | Moonshadow IV | planet (jovian) | -- | -- | none | 2026-11-17 12:06 UTC | `get_system`, own ship |
| `moonshadow_gas_plume` | Moonshadow Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 61, 12686 of 50000 left; argon_gas: richness 47, 26798 of 50000 left; nebula_gas: richness 13, 5284 of 10000 left; neon_gas: richness 42, 25043 of 50000 left; fluorine_gas: richness 14, 5000 of 5000 left | none | 2026-11-17 12:06 UTC | `get_poi`, own ship |
| `moonshadow_fertilizer_ice` | Moonshadow Fertilizer Ice | ice_field | -- | water_ice: richness 55, 30000 of 30000 left; nitrogen_ice: richness 45, 25000 of 25000 left; ammonia_ice: richness 20, 10000 of 10000 left; carbon_dioxide_ice: richness 18, 9000 of 9000 left | none | 2026-11-17 12:06 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:06 UTC | own ship | Read Moonshadow Gas Plume: 74,811 units left in all | `get_poi`, own ship |
| 2026-11-17 12:06 UTC | own ship | Read Moonshadow Fertilizer Ice: 74,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
