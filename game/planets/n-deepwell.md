---
name: deepwell
id: 20261116T050018Z
tier: intel
author: Unity
kind: system
system_id: deepwell
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Deepwell

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where deepwell`).

| Field | Value |
|---|---|
| Position | x -832.4, y 2084.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | bluerift, gemma, goldcrest, gsc_0033, lhs_1140 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `deepwell_star` | Deepwell Star | sun (G2V) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_i` | Deepwell I | planet (scorched) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_ii` | Deepwell II | planet (arid) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_iii` | Deepwell III | planet (terran) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_iv` | Deepwell IV | planet (tundra) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_v` | Deepwell V | planet (jovian) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `deepwell_haze` | Deepwell Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 50, 3137 of 50000 left; argon_gas: richness 51, 49999 of 50000 left; plasma_gas: richness 27, 7998 of 10000 left; xenon_gas: richness 19, 10000 of 10000 left; neon_gas: richness 43, 50000 of 50000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |
| `deepwell_volatile_ice` | Deepwell Volatile Ice | ice_field | -- | water_ice: richness 50, 2857 of 30000 left; methane_ice: richness 18, 2152 of 9000 left; ammonia_ice: richness 15, 2328 of 7000 left; helium_ice: richness 12, 4000 of 4000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |
| `deepwell_void_whisper` | Deepwell Void Whisper | asteroid_belt | -- | iron_ore: richness 33, 1137 of 100000 left; copper_ore: richness 32, 1107 of 100000 left; null_matter: richness 12, 1 of 536 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 04:39 UTC | own ship | Read Deepwell Haze: 121,134 units left in all | `get_poi`, own ship |
| 2026-11-16 04:39 UTC | own ship | Read Deepwell Volatile Ice: 11,337 units left in all | `get_poi`, own ship |
| 2026-11-16 04:39 UTC | own ship | Read Deepwell Void Whisper: 2,245 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
