---
name: factory_belt
id: 20261117T153732Z
tier: intel
author: Unity
kind: system
system_id: factory_belt
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 55
updated: 2026-11-17
---

# Factory Belt

Nebula system 23 jumps from home, police level 55. Station: Factory Belt Manufacturing Hub.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where factory_belt`).

| Field | Value |
|---|---|
| Position | x 1901.4, y -5147.9 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 23 |
| Lanes | khambalia, pollux, traders_rest, treasure_cache |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `steadyburn` | Steadyburn | sun (G8V) | -- | -- | none | 2026-11-17 15:00 UTC | `get_system`, own ship |
| `assembly_world` | Assembly World | planet (terran) | -- | -- | none | 2026-11-17 15:00 UTC | `get_system`, own ship |
| `factory_belt_haze` | Factory Belt Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 45, 1 of 50000 left; argon_gas: richness 33, 2 of 50000 left; neon_gas: richness 21, 4 of 50000 left | none | 2026-11-17 15:00 UTC | `get_poi`, own ship |
| `factory_belt_manufacturing_hub` | Factory Belt Manufacturing Hub | station | `factory_belt_manufacturing_hub` | -- | none | 2026-11-17 15:00 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Factory Belt Manufacturing Hub (`factory_belt_manufacturing_hub`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 15:00 UTC | `get_system`, own ship |

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
| 2026-11-17 15:00 UTC | own ship | Read Factory Belt Haze: 7 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
