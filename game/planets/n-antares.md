---
name: antares
id: 20261115T225415Z
tier: intel
author: Unity
kind: system
system_id: antares
standing: neutral
standing_since: 2026-11-15
threat: medium
empire: -
police_level: 0
updated: 2026-11-15
---

# Antares

- system 5 jumps from home, police level 0. Station: Hive Antares.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where antares`).

| Field | Value |
|---|---|
| Position | x -1531.0, y 2266.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | gsc_0033, gsc_0041, homam, lhs_1140 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `antares_star` | Antares Star | sun (M6V) | -- | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |
| `antares_gas_cloud` | Antares Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 42, 2968 of 50000 left; argon_gas: richness 53, 48952 of 50000 left; plasma_gas: richness 19, 7661 of 10000 left; nebula_gas: richness 21, 5431 of 10000 left; neon_gas: richness 44, 50000 of 50000 left; chlorine_gas: richness 22, 1043 of 10000 left | none | 2026-11-15 22:01 UTC | `get_poi`, own ship |
| `antares_ice_fields` | Antares Ice Fields | ice_field (kuiper) | -- | water_ice: richness 55, 1293 of 50000 left; nitrogen_ice: richness 41, 30052 of 50000 left; deuterium_ice: richness 20, 306 of 5000 left; helium_ice: richness 24, 306 of 5000 left | none | 2026-11-15 22:01 UTC | `get_poi`, own ship |
| `afternoon_drift` | Afternoon Drift | asteroid_belt | -- | iron_ore: richness 32, 7558 of 100000 left; copper_ore: richness 31, 12522 of 100000 left; sol_alloy_ore: richness 5, 1017 of 1284 left | none | 2026-11-15 22:01 UTC | `get_poi`, own ship |
| `203ff8d9c8217ef3e04ee5e5f4347862` | Hive Antares | station | `199fa2c026d6af7bf6e938638425416c` | -- | none | 2026-11-15 22:01 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Hive Antares (`199fa2c026d6af7bf6e938638425416c`) | unknown | not tried | not read | unknown | unknown | 2026-11-15 22:01 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |
| 2026-11-15 | Threat set to medium by Oracle: lawless space, police level 0 (game/planets/BLUEPRINT.md, section 3) | `get_system`, own ship, 2026-11-15 22:01 UTC |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 22:01 UTC | own ship | Read Antares Gas Cloud: 116,055 units left in all | `get_poi`, own ship |
| 2026-11-15 22:01 UTC | own ship | Read Antares Ice Fields: 31,957 units left in all | `get_poi`, own ship |
| 2026-11-15 22:01 UTC | own ship | Read Afternoon Drift: 21,097 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Base site (Oracle, 2026-11-15, from the read of 2026-11-15 22:01 UTC): lawless, police 0, not a pirate stronghold (governance/map.md, section 4), so an outpost could stand here; no station of ours: Hive Antares stands here (one station per system, game/rules/09-factions.md). Places without a base: 3 (1 gas cloud, 1 ice field, 1 belt). Foreign pilots our ships saw here: 39 (data/intel/sightings.jsonl, 23:30 UTC). Hidden deposits and other builders are not known.
