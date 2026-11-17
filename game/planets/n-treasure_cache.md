---
name: treasure_cache
id: 20261117T153757Z
tier: intel
author: Unity
kind: system
system_id: treasure_cache
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Treasure Cache

Nebula system 24 jumps from home, police level 30. Station: Treasure Cache Trading Post.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where treasure_cache`).

| Field | Value |
|---|---|
| Position | x 2537.3, y -5057.3 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 24 |
| Lanes | ashford, factory_belt, pollux, ross_128 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dim_fortune` | Dim Fortune | sun (K7V) | -- | -- | none | 2026-11-17 14:56 UTC | `get_system`, own ship |
| `cache_i` | Cache I | planet (arid) | -- | -- | none | 2026-11-17 14:56 UTC | `get_system`, own ship |
| `cache_ii` | Cache II | planet (tundra) | -- | -- | none | 2026-11-17 14:56 UTC | `get_system`, own ship |
| `cache_mineral_fields` | Cache Mineral Fields | asteroid_belt (carbonaceous) | -- | carbon_ore: richness 51, 0 of 30000 left; iridium_ore: richness 10, 0 of 5000 left | none | 2026-11-17 14:56 UTC | `get_poi`, own ship |
| `treasure_cache_gas_plume` | Treasure Cache Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 47, 1991 of 50000 left; argon_gas: richness 44, 1992 of 50000 left; plasma_gas: richness 26, 698 of 10000 left; nebula_gas: richness 23, 743 of 10000 left; neon_gas: richness 35, 2026 of 50000 left | none | 2026-11-17 14:56 UTC | `get_poi`, own ship |
| `treasure_cache_trading_post` | Treasure Cache Trading Post | station | `treasure_cache_trading_post` | -- | none | 2026-11-17 14:56 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Treasure Cache Trading Post (`treasure_cache_trading_post`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:56 UTC | `get_system`, own ship |

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
| 2026-11-17 14:56 UTC | own ship | Read Cache Mineral Fields: nothing left | `get_poi`, own ship |
| 2026-11-17 14:56 UTC | own ship | Read Treasure Cache Gas Plume: 7,450 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
