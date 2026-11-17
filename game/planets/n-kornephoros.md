---
name: kornephoros
id: 20261117T143545Z
tier: intel
author: Unity
kind: system
system_id: kornephoros
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kornephoros

- system 17 jumps from home, police level 0. Station: The Zero Point Nexus.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kornephoros`).

| Field | Value |
|---|---|
| Position | x 3792.4, y 4639.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | albireo, arneb, dawnbreak, thuban |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kornephoros_star` | Kornephoros Star | sun (M4V) | -- | -- | none | 2026-11-17 14:04 UTC | `get_system`, own ship |
| `kornephoros_gas_plume` | Kornephoros Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 64, 4320 of 50000 left; argon_gas: richness 41, 39163 of 50000 left; plasma_gas: richness 17, 8931 of 10000 left; nebula_gas: richness 22, 2694 of 10000 left; neon_gas: richness 48, 26125 of 50000 left; ion_gas: richness 32, 1181 of 10000 left | none | 2026-11-17 14:04 UTC | `get_poi`, own ship |
| `kornephoros_frost_ring` | Kornephoros Frost Ring | ice_field (kuiper) | -- | water_ice: richness 50, 40560 of 50000 left; nitrogen_ice: richness 32, 50000 of 50000 left; deuterium_ice: richness 21, 3975 of 5000 left | none | 2026-11-17 14:04 UTC | `get_poi`, own ship |
| `kornephoros_war_shard_drift` | Kornephoros War Shard Drift | asteroid_belt | -- | iron_ore: richness 41, 5133 of 100000 left; copper_ore: richness 26, 65351 of 100000 left; darksteel_ore: richness 6, 272 of 305 left | none | 2026-11-17 14:04 UTC | `get_poi`, own ship |
| `cooling_pores` | Cooling Pores | asteroid_belt | -- | iron_ore: richness 41, 0 of 100000 left; copper_ore: richness 35, 0 of 100000 left; plasma_residue: richness 10, 0 of 1032 left | none | 2026-11-17 14:04 UTC | `get_poi`, own ship |
| `91b887ed660acdcdc166e1e659c43ba0` | The Zero Point Nexus | station | `2779fe259d6835829df185104259b3e4` | -- | none | 2026-11-17 14:04 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Zero Point Nexus (`2779fe259d6835829df185104259b3e4`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:04 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:04 UTC | own ship | Read Kornephoros Gas Plume: 82,414 units left in all | `get_poi`, own ship |
| 2026-11-17 14:04 UTC | own ship | Read Kornephoros Frost Ring: 94,535 units left in all | `get_poi`, own ship |
| 2026-11-17 14:04 UTC | own ship | Read Kornephoros War Shard Drift: 70,756 units left in all | `get_poi`, own ship |
| 2026-11-17 14:04 UTC | own ship | Read Cooling Pores: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
