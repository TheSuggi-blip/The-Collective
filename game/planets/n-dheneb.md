---
name: dheneb
id: 20261117T092724Z
tier: intel
author: Unity
kind: system
system_id: dheneb
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dheneb

- system 11 jumps from home, police level 0. Station: Hex Star.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dheneb`).

| Field | Value |
|---|---|
| Position | x 639.4, y 656.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | aspidiske, barnards_star, mira, proxima_centauri, thabit |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dheneb_star` | Dheneb Star | sun (M6V) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `dheneb_i` | Dheneb I | planet (scorched) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `dheneb_ii` | Dheneb II | planet (arid) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `dheneb_belt` | Dheneb Belt | asteroid_belt (metallic) | -- | iron_ore: richness 50, 10 of 100000 left; copper_ore: richness 20, 10 of 100000 left; zinc_ore: richness 19, 1 of 15000 left | none | 2026-11-17 09:16 UTC | `get_poi`, own ship |
| `dheneb_gas_cloud` | Dheneb Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 52, 4482 of 50000 left; argon_gas: richness 46, 49999 of 50000 left; xenon_gas: richness 27, 10000 of 10000 left; nebula_gas: richness 24, 10000 of 10000 left; neon_gas: richness 49, 50000 of 50000 left; krypton_gas: richness 18, 3574 of 5000 left | none | 2026-11-17 09:16 UTC | `get_poi`, own ship |
| `dheneb_cryobelt` | Dheneb Cryobelt | ice_field (kuiper) | -- | water_ice: richness 52, 5819 of 50000 left; nitrogen_ice: richness 53, 31710 of 50000 left; helium_ice: richness 14, 4608 of 5000 left; methane_ice: richness 17, 2266 of 8000 left | none | 2026-11-17 09:16 UTC | `get_poi`, own ship |
| `98eba8b1a7ad0520d6a7c8ea44b2d6aa` | Hex Star | station | `b495c6003fc83e18f6d8cecbe6929133` | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Hex Star (`b495c6003fc83e18f6d8cecbe6929133`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 09:16 UTC | `get_system`, own ship |

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
| 2026-11-17 09:16 UTC | own ship | Read Dheneb Belt: 21 units left in all | `get_poi`, own ship |
| 2026-11-17 09:16 UTC | own ship | Read Dheneb Gas Cloud: 128,055 units left in all | `get_poi`, own ship |
| 2026-11-17 09:16 UTC | own ship | Read Dheneb Cryobelt: 44,403 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
