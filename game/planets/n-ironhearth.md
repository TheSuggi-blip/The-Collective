---
name: ironhearth
id: 20261117T174159Z
tier: intel
author: Unity
kind: system
system_id: ironhearth
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 55
updated: 2026-11-17
---

# Ironhearth

Crimson system 21 jumps from home, police level 55. Station: Ironhearth Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ironhearth`).

| Field | Value |
|---|---|
| Position | x 5377.7, y 2360.1 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 21 |
| Lanes | 82_eridani, frostfeld, gsc_0036, hd_20794, muscida, the_anvil |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `hearthfire` | Hearthfire | sun (G5V) | -- | -- | none | 2026-11-17 16:49 UTC | `get_system`, own ship |
| `ironhearth_prime` | Ironhearth Prime | planet (terran) | -- | -- | none | 2026-11-17 16:49 UTC | `get_system`, own ship |
| `ironhearth_ii` | Ironhearth II | planet (terran) | -- | -- | none | 2026-11-17 16:49 UTC | `get_system`, own ship |
| `ironhearth_iii` | Ironhearth III | planet (tundra) | -- | -- | none | 2026-11-17 16:49 UTC | `get_system`, own ship |
| `ironhearth_fields` | Ironhearth Fields | asteroid_belt (mixed) | -- | carbon_ore: richness 42, 0 of 30000 left; vanadium_ore: richness 34, 0 of 25000 left; platinum_ore: richness 18, 0 of 8000 left; palladium_ore: richness 30, 0 of 5000 left; rhodium_ore: richness 9, 0 of 2000 left | none | 2026-11-17 16:49 UTC | `get_poi`, own ship |
| `ironhearth_thermal_vents` | Ironhearth Thermal Vents | gas_cloud (atmospheric) | -- | hydrogen_gas: richness 63, 530 of 50000 left; xenon_gas: richness 23, 4527 of 10000 left; neon_gas: richness 33, 29200 of 50000 left; chlorine_gas: richness 22, 566 of 10000 left | none | 2026-11-17 16:49 UTC | `get_poi`, own ship |
| `ironhearth_ice_ring` | Ironhearth Ice Ring | ice_field (kuiper) | -- | nitrogen_ice: richness 46, 42232 of 50000 left | none | 2026-11-17 16:49 UTC | `get_poi`, own ship |
| `ironhearth_station` | Ironhearth Station | station | `ironhearth_station` | -- | none | 2026-11-17 16:49 UTC | `get_system`, own ship |
| `the_old_seam` | The Old Seam | asteroid_belt (metallic) | -- | iron_ore: richness 85, 94 of 90000 left | none | 2026-11-17 16:49 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ironhearth Station (`ironhearth_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:49 UTC | `get_system`, own ship |

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
| 2026-11-17 16:49 UTC | own ship | Read Ironhearth Fields: nothing left | `get_poi`, own ship |
| 2026-11-17 16:49 UTC | own ship | Read Ironhearth Thermal Vents: 34,823 units left in all | `get_poi`, own ship |
| 2026-11-17 16:49 UTC | own ship | Read Ironhearth Ice Ring: 42,232 units left in all | `get_poi`, own ship |
| 2026-11-17 16:49 UTC | own ship | Read The Old Seam: 94 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
