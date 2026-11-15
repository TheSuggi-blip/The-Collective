---
name: node_gamma
id: 20261115T040558Z
tier: intel
author: Unity
kind: system
system_id: node_gamma
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 55
updated: 2026-11-15
---

# Node Gamma

Interior Voidborn system two jumps from home, between Node Alpha, Node Beta, Acubens and Synchrony.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where node_gamma`).

| Field | Value |
|---|---|
| Position | x -3730.9, y 2702.9 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 2 |
| Lanes | acubens, node_alpha, node_beta, synchrony |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bellatrix_major_star` | Bellatrix Major Star | sun (A0III) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `gamma_relay` | Gamma Relay | planet (tundra) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `gamma_archive` | Gamma Archive | planet (glacial) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `bellatrix_major_belt` | Bellatrix Major Belt | asteroid_belt (carbonaceous) | -- | carbon_ore: richness 67, 0 of 30000 left; palladium_ore: richness 16, 0 of 5000 left; iridium_ore: richness 11, 0 of 5000 left; thorium_ore: richness 19, 0 of 5000 left | none | 2026-11-15 03:56 UTC | `get_poi`, own ship |
| `node_gamma_ice_belt` | Node Gamma Ice Belt | ice_field (kuiper) | -- | not read | none | 2026-11-15 UTC | `get_system`, own ship |
| `node_gamma_relay_station` | Node Gamma Relay Station | station | Node Gamma Relay Station (`node_gamma_relay_station`); see Stations | -- | none | 2026-11-15 03:37 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Node Gamma Relay Station (`node_gamma_relay_station`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, shipyard, storage | 15 cr per unit (13 + 2 empire tax) | unknown | 2026-11-15 03:37 UTC | `get_poi`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 03:37 UTC | own ship | Docked at Node Gamma Relay Station: services and fuel price read | `get_poi`, own ship |
| 2026-11-15 03:56 UTC | own ship | Read the ore at Bellatrix Major Belt: nothing left to mine | `get_poi`, own ship |

## Notes

- Every belt read here was mined out, or all but, on 2026-11-15. Deposits are shared and refill gradually, common ores fastest (https://www.spacemolt.com/docs/mining.md); how long a refill takes and who takes the ore is not known. Read again before sending miners.
- Not read yet: `node_gamma_ice_belt`. Ice needs an ice harvester, gas a gas harvester (https://www.spacemolt.com/docs/mining.md).
- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
