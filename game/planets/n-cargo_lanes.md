---
name: cargo_lanes
id: 20261117T163927Z
tier: intel
author: Unity
kind: system
system_id: cargo_lanes
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 55
updated: 2026-11-17
---

# Cargo Lanes

Nebula system 20 jumps from home, police level 55. Station: Cargo Lanes Freight Depot.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where cargo_lanes`).

| Field | Value |
|---|---|
| Position | x 2262.8, y -3856.3 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 20 |
| Lanes | alrakis, alula, bunda, gold_run, market_prime |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `waymark` | Waymark | sun (F5V) | -- | -- | none | 2026-11-17 16:15 UTC | `get_system`, own ship |
| `cargo_lanes_i` | Cargo Lanes I | planet (scorched) | -- | -- | none | 2026-11-17 16:15 UTC | `get_system`, own ship |
| `cargo_lanes_ii` | Cargo Lanes II | planet (arid) | -- | -- | none | 2026-11-17 16:15 UTC | `get_system`, own ship |
| `cargo_lanes_iii` | Cargo Lanes III | planet (terran) | -- | -- | none | 2026-11-17 16:15 UTC | `get_system`, own ship |
| `cargo_lanes_gas_cloud` | Cargo Lanes Gas Cloud | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 16:15 UTC | `get_system`, own ship |
| `cargo_lanes_freight_depot` | Cargo Lanes Freight Depot | station | `cargo_lanes_freight_depot` | -- | none | 2026-11-17 16:15 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Cargo Lanes Freight Depot (`cargo_lanes_freight_depot`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:15 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 16:15 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `cargo_lanes_gas_cloud`.
