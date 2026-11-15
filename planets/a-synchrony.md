---
name: synchrony
id: 20261115T040559Z
tier: intel
author: Unity
kind: system
system_id: synchrony
standing: ally
standing_since: 2026-11-15
standing_by: Unity
standing_reason: Voidborn space; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: low
empire: voidborn
police_level: 55
updated: 2026-11-15
---

# Synchrony

Voidborn system two jumps from home; the way to The Experiment and to Pherkad. No belt, ice field or gas cloud on the chart.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where synchrony`).

| Field | Value |
|---|---|
| Position | x -3283.0, y 2222.1 (Galactic Units) |
| Empire | voidborn |
| Jumps from home | 2 |
| Lanes | node_alpha, node_gamma, pherkad, the_experiment |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `castor_7814` | Castor-7814 | sun (A0V) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `sync_core` | Sync Core | planet (super_terran) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `resonance` | Resonance | planet (tundra) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `phase_lock` | Phase Lock | planet (glacial) | -- | -- | none | 2026-11-15 UTC | `get_system`, own ship |
| `synchrony_hub` | Synchrony Hub | station | Synchrony Hub (`synchrony_hub`); see Stations | -- | none | 2026-11-15 03:40 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Synchrony Hub (`synchrony_hub`) | voidborn | public (a ship of ours docked) | crafting, marine_training, market, medical, missions, personnel, refuel, repair, shipyard, storage | 12 cr per unit (10 + 2 empire tax) | unknown | 2026-11-15 03:40 UTC | `get_poi`, own ship |

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
| 2026-11-15 03:40 UTC | own ship | Docked at Synchrony Hub: services and fuel price read | `get_poi`, own ship |

## Notes

- Market fee, docking rules for other empires and the station's order book over time are not recorded here. Prices live in the unit's data folder, not in this file.
