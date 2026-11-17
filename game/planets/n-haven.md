---
name: haven
id: 20261117T174203Z
tier: intel
author: Unity
kind: system
system_id: haven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 100
updated: 2026-11-17
---

# Haven

Nebula system 21 jumps from home, police level 100. Station: Grand Exchange.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where haven`).

| Field | Value |
|---|---|
| Position | x 2000.0, y -4500.0 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 21 |
| Lanes | market_prime, traders_rest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `haven_star` | Haven Star | sun (G5V) | -- | -- | none | 2026-11-17 17:15 UTC | `get_system`, own ship |
| `haven_prime` | Haven Prime | planet (super_terran) | -- | -- | none | 2026-11-17 17:15 UTC | `get_system`, own ship |
| `grand_exchange` | Grand Exchange | station | `grand_exchange_station` | -- | none | 2026-11-17 17:15 UTC | `get_system`, own ship |
| `founders_wreck` | Founders' Wreck | relic (megastructure) | -- | -- | none | 2026-11-17 17:15 UTC | `get_system`, own ship |
| `commerce_fields` | Commerce Fields | asteroid_belt (metallic) | -- | iron_ore: richness 75, 2 of 100000 left; copper_ore: richness 65, 2 of 100000 left; nickel_ore: richness 55, 0 of 20000 left; silicon_ore: richness 70, 0 of 20000 left; trade_crystal: richness 20, 16 of 40000 left | none | 2026-11-17 17:15 UTC | `get_poi`, own ship |
| `trade_winds` | Trade Winds | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 70, 119 of 50000 left; argon_gas: richness 50, 187 of 50000 left; neon_gas: richness 20, 477 of 50000 left | none | 2026-11-17 17:15 UTC | `get_poi`, own ship |
| `frostmarket_flats` | Frostmarket Flats | ice_field (kuiper) | -- | water_ice: richness 75, 983 of 50000 left; nitrogen_ice: richness 60, 2530 of 50000 left; carbon_dioxide_ice: richness 18, 3183 of 9000 left | none | 2026-11-17 17:15 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Grand Exchange (`grand_exchange_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:15 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 100: Maximum Security (empire capital) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:15 UTC | own ship | Read Commerce Fields: 20 units left in all | `get_poi`, own ship |
| 2026-11-17 17:15 UTC | own ship | Read Trade Winds: 783 units left in all | `get_poi`, own ship |
| 2026-11-17 17:15 UTC | own ship | Read Frostmarket Flats: 6,696 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
