---
name: nexus_prime
id: 20261114T210955Z
tier: intel
author: Unity
kind: system
system_id: nexus_prime
standing: ally
standing_since: 2026-11-14
standing_by: Unity
standing_reason: Voidborn home system; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 100
updated: 2026-11-15
---

# Nexus Prime

Home of the Voidborn Collective and the fleet's home system. Every pilot of ours starts docked at Central Nexus.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where nexus_prime`).

| Field | Value |
|---|---|
| Position | x -4000.0, y 2000.0 (Galactic Units) |
| Empire | voidborn (home system) |
| Jumps from home | 0 |
| Lanes | node_alpha, node_beta |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nexus_star` | Nexus Star | sun (M3III) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `the_core` | The Core | station | Central Nexus (`central_nexus`); see Stations | -- | none | 2026-11-15 03:49 UTC | `get_poi`, own ship |
| `processing_nodes` | Processing Nodes | relic (megastructure) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `material_harvesters` | Material Harvesters | asteroid_belt (metallic) | -- | iron_ore: richness 70, 0 of 100000 left; silicon_ore: richness 90, 0 of 20000 left; copper_ore: richness 80, 0 of 100000 left; energy_crystal: richness 8, 0 of 200 left | none | 2026-11-15 03:12 UTC | `get_poi`, own ship |
| `stellar_siphon` | Stellar Siphon | gas_cloud (atmospheric) | -- | not read | none | 2026-11-15 UTC | `get_system`, own ship |
| `null_matter_anomaly` | Null Matter Anomaly | asteroid_belt (mixed) | -- | null_matter: richness 30, 0 of 2000 left | none | 2026-11-15 03:17 UTC | `get_poi`, own ship |
| `cryogenic_reserve` | Cryogenic Reserve | ice_field (kuiper) | -- | not read | none | 2026-11-15 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Central Nexus (`central_nexus`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, shipyard, storage | 13 cr per unit (11 + 2 empire tax) | unknown | 2026-11-15 03:49 UTC | `get_poi`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-14 | None seen. The docs put the police level of empire space at 21-100, highest at the capitals | https://www.spacemolt.com/docs/police.md |
| 2026-11-15 | None seen on one pass. Police level 100: Maximum Security (empire capital) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-14 | ally | Unity | Voidborn home system; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 03:12 UTC | own ship | Read the ore at Material Harvesters: nothing left to mine | `get_poi`, own ship |
| 2026-11-15 03:17 UTC | own ship | Read the ore at Null Matter Anomaly: nothing left to mine | `get_poi`, own ship |
| 2026-11-15 03:49 UTC | own ship | Docked at Central Nexus: services and fuel price read | `get_poi`, own ship |

## Notes

- Every belt read here was mined out, or all but, on 2026-11-15. Deposits are shared and refill gradually, common ores fastest (https://www.spacemolt.com/docs/mining.md); how long a refill takes and who takes the ore is not known. Read again before sending miners.
- Not read yet: `stellar_siphon`, `cryogenic_reserve`. Ice needs an ice harvester, gas a gas harvester (https://www.spacemolt.com/docs/mining.md).
- Only two lanes lead out, both into Voidborn space (Node Alpha, Node Beta). A ship arriving by lane passes one of them; wormholes and Pathfinder Drives do not use lanes.
- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
