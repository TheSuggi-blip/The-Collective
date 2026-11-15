---
name: the_experiment
id: 20261115T040602Z
tier: intel
author: Unity
kind: system
system_id: the_experiment
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 30
updated: 2026-11-15
---

# The Experiment

Voidborn border system three jumps from home, with three lanes into lawless space. The lowest police level of the six visited.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where the_experiment`).

| Field | Value |
|---|---|
| Position | x -3031.2, y 1781.6 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 3 |
| Lanes | achernar, ironhollow, ruchbah, synchrony |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `theta_serpentis` | Theta Serpentis | sun (M4V) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `experiment_prime` | Experiment Prime | planet (terran) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `experiment_substrate_fields` | Experiment Substrate Fields | asteroid_belt (carbonaceous) | -- | carbon_ore: richness 66, 1 of 30000 left; palladium_ore: richness 28, 0 of 5000 left; lithium_ore: richness 45, 0 of 25000 left; void_essence: richness 4, 1 of 200 left | none | 2026-11-15 03:58 UTC | `get_poi`, own ship |
| `the_experiment_haze` | The Experiment Haze | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-15 UTC | `get_system`, own ship |
| `the_array` | The Array | relic (alien_artifact) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `the_experiment_research_station` | The Experiment Research Station | station | The Experiment Research Station (`the_experiment_research_station`); see Stations | -- | none | 2026-11-15 03:42 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Experiment Research Station (`the_experiment_research_station`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, shipyard, storage | 11 cr per unit (9 + 2 empire tax) | unknown | 2026-11-15 03:42 UTC | `get_poi`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | ally | Unity | Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 03:42 UTC | own ship | Docked at The Experiment Research Station: services and fuel price read | `get_poi`, own ship |
| 2026-11-15 03:58 UTC | own ship | Read the ore at Experiment Substrate Fields: 2 units left in all | `get_poi`, own ship |

## Notes

- Every belt read here was mined out, or all but, on 2026-11-15. Deposits are shared and refill gradually, common ores fastest (https://www.spacemolt.com/docs/mining.md); how long a refill takes and who takes the ore is not known. Read again before sending miners.
- Not read yet: `the_experiment_haze`. Ice needs an ice harvester, gas a gas harvester (https://www.spacemolt.com/docs/mining.md).
- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
