---
name: deep_range
id: 20261117T174213Z
tier: intel
author: Unity
kind: system
system_id: deep_range
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 80
updated: 2026-11-17
---

# Deep Range

Outerrim system 19 jumps from home, police level 80. Station: Deep Range Outpost.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where deep_range`).

| Field | Value |
|---|---|
| Position | x -2745.8, y -3975.7 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 19 |
| Lanes | frontier, horizon |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `old_amber` | Old Amber | sun (M4V) | -- | -- | none | 2026-11-17 16:47 UTC | `get_system`, own ship |
| `basecamp` | Basecamp | planet (scorched) | -- | -- | none | 2026-11-17 16:47 UTC | `get_system`, own ship |
| `drydock_world` | Drydock World | planet (arid) | -- | -- | none | 2026-11-17 16:47 UTC | `get_system`, own ship |
| `deep_range_mineral_fields` | Deep Range Mineral Fields | asteroid_belt (mixed) | -- | carbon_ore: richness 65, 680 of 30000 left; vanadium_ore: richness 41, 124 of 25000 left; tungsten_ore: richness 45, 124 of 25000 left; platinum_ore: richness 20, 531 of 8000 left; dark_matter_residue: richness 5, 234 of 300 left; osmium_ore: richness 9, 497 of 2000 left | none | 2026-11-17 16:47 UTC | `get_poi`, own ship |
| `deep_range_vapor_fields` | Deep Range Vapor Fields | gas_cloud (molecular_cloud) | -- | argon_gas: richness 39, 49999 of 50000 left | none | 2026-11-17 16:47 UTC | `get_poi`, own ship |
| `deep_range_cryobelt` | Deep Range Cryobelt | ice_field (kuiper) | -- | water_ice: richness 43, 412 of 50000 left; carbon_dioxide_ice: richness 16, 559 of 7000 left | none | 2026-11-17 16:47 UTC | `get_poi`, own ship |
| `deep_range_outpost` | Deep Range Outpost | station | `deep_range_outpost` | -- | none | 2026-11-17 16:47 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Deep Range Outpost (`deep_range_outpost`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 16:47 UTC | `get_system`, own ship |

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
| 2026-11-17 16:47 UTC | own ship | Read Deep Range Mineral Fields: 2,190 units left in all | `get_poi`, own ship |
| 2026-11-17 16:47 UTC | own ship | Read Deep Range Vapor Fields: 49,999 units left in all | `get_poi`, own ship |
| 2026-11-17 16:47 UTC | own ship | Read Deep Range Cryobelt: 971 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
