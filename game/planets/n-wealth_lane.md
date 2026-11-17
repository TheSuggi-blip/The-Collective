---
name: wealth_lane
id: 20261117T174140Z
tier: intel
author: Unity
kind: system
system_id: wealth_lane
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Wealth Lane

- system 19 jumps from home, police level 0. Station: Pale Lantern Anchorage, The Full Moon.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wealth_lane`).

| Field | Value |
|---|---|
| Position | x 1350.6, y -4117.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | copernicus, gold_run, the_levy |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `trappist_prime_belt` | TRAPPIST- Prime Belt | asteroid_belt (metallic) | -- | iron_ore: richness 53, 4835 of 100000 left; copper_ore: richness 41, 90858 of 100000 left | none | 2026-11-17 17:25 UTC | `get_poi`, own ship |
| `wealth_lane_gas_cloud` | Wealth Lane Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 43, 685 of 50000 left; argon_gas: richness 31, 690 of 50000 left; plasma_gas: richness 33, 451 of 10000 left; xenon_gas: richness 21, 514 of 10000 left; neon_gas: richness 36, 687 of 50000 left; krypton_gas: richness 22, 514 of 5000 left | none | 2026-11-17 17:25 UTC | `get_poi`, own ship |
| `wealth_lane_ice_belt` | Wealth Lane Ice Belt | ice_field (kuiper) | -- | nitrogen_ice: richness 54, 50000 of 50000 left | none | 2026-11-17 17:25 UTC | `get_poi`, own ship |
| `22c5a816fd981e235ccbbb202795e494` | Pale Lantern Anchorage | station | `71239823874fe5e4a49786e8db30f2fb` | -- | none | 2026-11-17 17:25 UTC | `get_system`, own ship |
| `cfe6ce3b10657f7b8107a3700907a538` | The Full Moon | station | `4e89fb5d4df8bdd7c1c408e1713dc161` | -- | none | 2026-11-17 17:25 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Pale Lantern Anchorage (`71239823874fe5e4a49786e8db30f2fb`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:25 UTC | `get_system`, own ship |
| The Full Moon (`4e89fb5d4df8bdd7c1c408e1713dc161`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:25 UTC | `get_system`, own ship |

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
| 2026-11-17 17:25 UTC | own ship | Read TRAPPIST- Prime Belt: 95,693 units left in all | `get_poi`, own ship |
| 2026-11-17 17:25 UTC | own ship | Read Wealth Lane Gas Cloud: 3,541 units left in all | `get_poi`, own ship |
| 2026-11-17 17:25 UTC | own ship | Read Wealth Lane Ice Belt: 50,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
