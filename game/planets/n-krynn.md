---
name: krynn
id: 20261117T174158Z
tier: intel
author: Unity
kind: system
system_id: krynn
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 100
updated: 2026-11-17
---

# Krynn

Crimson system 20 jumps from home, police level 100. Station: War Citadel.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where krynn`).

| Field | Value |
|---|---|
| Position | x 5000.0, y 3000.0 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 20 |
| Lanes | blood_forge, iron_reach, the_anvil, valor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `krynns_fury` | Krynn's Fury | sun (M0III) | -- | -- | none | 2026-11-17 17:01 UTC | `get_system`, own ship |
| `krynn_prime` | Krynn Prime | planet (terran) | -- | -- | none | 2026-11-17 17:01 UTC | `get_system`, own ship |
| `war_citadel` | War Citadel | station | `crimson_war_citadel` | -- | none | 2026-11-17 17:01 UTC | `get_system`, own ship |
| `blood_arena` | Blood Arena | relic (megastructure) | -- | -- | none | 2026-11-17 17:01 UTC | `get_system`, own ship |
| `war_materials` | War Materials | asteroid_belt (metallic) | -- | iron_ore: richness 90, 10 of 100000 left; titanium_ore: richness 60, 2 of 25000 left; cobalt_ore: richness 50, 2 of 25000 left; plasma_residue: richness 25, 1 of 3000 left; darksteel_ore: richness 15, 1 of 1000 left | none | 2026-11-17 17:01 UTC | `get_poi`, own ship |
| `furnace_vents` | Furnace Vents | gas_cloud (atmospheric) | -- | hydrogen_gas: richness 80, 3137 of 50000 left; argon_gas: richness 65, 23288 of 50000 left; neon_gas: richness 15, 50000 of 50000 left | none | 2026-11-17 17:01 UTC | `get_poi`, own ship |
| `shattered_comet_graves` | Shattered Comet Graves | ice_field (cometary) | -- | water_ice: richness 70, 121 of 50000 left; nitrogen_ice: richness 55, 160 of 50000 left | none | 2026-11-17 17:01 UTC | `get_poi`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| War Citadel (`crimson_war_citadel`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:01 UTC | `get_system`, own ship |

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
| 2026-11-17 17:01 UTC | own ship | Read War Materials: 16 units left in all | `get_poi`, own ship |
| 2026-11-17 17:01 UTC | own ship | Read Furnace Vents: 76,425 units left in all | `get_poi`, own ship |
| 2026-11-17 17:01 UTC | own ship | Read Shattered Comet Graves: 281 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
