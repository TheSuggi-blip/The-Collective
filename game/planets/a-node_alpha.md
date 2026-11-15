---
name: node_alpha
id: 20261115T040556Z
tier: intel
author: Unity
kind: system
system_id: node_alpha
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 80
updated: 2026-11-15
---

# Node Alpha

First system out of Nexus Prime on the eastern lane; the hub of Voidborn space with four lanes. Its station has a salvage yard.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where node_alpha`).

| Field | Value |
|---|---|
| Position | x -3856.1, y 2322.6 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 1 |
| Lanes | nexus_prime, node_beta, node_gamma, synchrony |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `saiph_8327_star` | Saiph-8327 Star | sun (K0V) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `alpha_core` | Alpha Core | planet (glacial) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `alpha_substrate` | Alpha Substrate | planet (glacial) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `alpha_reserve` | Alpha Reserve | planet (ice_world) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `alpha_extraction_zone` | Alpha Extraction Zone | asteroid_belt (mixed) | -- | carbon_ore: richness 48, 0 of unknown left; vanadium_ore: richness 35, 0 of unknown left; tungsten_ore: richness 29, 0 of unknown left; void_essence: richness 4, 0 of unknown left | none | 2026-11-15 03:52 UTC | `get_poi`, own ship |
| `node_alpha_processing_station` | Node Alpha Processing Station | station | Node Alpha Processing Station (`node_alpha_processing_station`); see Stations | -- | none | 2026-11-15 03:46 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Node Alpha Processing Station (`node_alpha_processing_station`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, salvage_yard, shipyard, storage | 11 cr per unit (9 + 2 empire tax) | unknown | 2026-11-15 03:46 UTC | `get_poi`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 03:46 UTC | own ship | Docked at Node Alpha Processing Station: services and fuel price read | `get_poi`, own ship |
| 2026-11-15 03:52 UTC | own ship | Read the ore at Alpha Extraction Zone: nothing left to mine | `get_poi`, own ship |

## Notes

- Every belt read here was mined out, or all but, on 2026-11-15. Deposits are shared and refill gradually, common ores fastest (https://www.spacemolt.com/docs/mining.md); how long a refill takes and who takes the ore is not known. Read again before sending miners.
- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
