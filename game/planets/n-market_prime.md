---
name: market_prime
id: 20261117T153745Z
tier: intel
author: Unity
kind: system
system_id: market_prime
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 80
updated: 2026-11-17
---

# Market Prime

Nebula system 20 jumps from home, police level 80. Station: Market Prime Exchange.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where market_prime`).

| Field | Value |
|---|---|
| Position | x 2254.1, y -4181.9 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 20 |
| Lanes | cargo_lanes, gold_run, haven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_beacon` | The Beacon | sun (F8V) | -- | -- | none | 2026-11-17 15:05 UTC | `get_system`, own ship |
| `warehouse_world` | Warehouse World | planet (terran) | -- | -- | none | 2026-11-17 15:05 UTC | `get_system`, own ship |
| `auction_hall` | Auction Hall | planet (terran) | -- | -- | none | 2026-11-17 15:05 UTC | `get_system`, own ship |
| `market_prime_gas_plume` | Market Prime Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 15:05 UTC | `get_system`, own ship |
| `market_prime_exchange` | Market Prime Exchange | station | `market_prime_exchange` | -- | none | 2026-11-17 15:05 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Market Prime Exchange (`market_prime_exchange`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 15:05 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 15:05 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `market_prime_gas_plume`.
