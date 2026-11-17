---
name: procyon
id: 20261117T082540Z
tier: intel
author: Unity
kind: system
system_id: procyon
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Procyon

Solarian system 9 jumps from home, police level 30. Station: Procyon Colonial Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where procyon`).

| Field | Value |
|---|---|
| Position | x -111.3, y 783.4 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | epsilon_eridani, markab, nihal, nova_terra, proxima_centauri |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `procyon_a` | Procyon A | sun (F5V) | -- | -- | none | 2026-11-17 07:45 UTC | `get_system`, own ship |
| `procyon_i` | Procyon I | planet (arid) | -- | -- | none | 2026-11-17 07:45 UTC | `get_system`, own ship |
| `procyon_ii` | Procyon II | planet (terran) | -- | -- | none | 2026-11-17 07:45 UTC | `get_system`, own ship |
| `procyon_iii` | Procyon III | planet (glacial) | -- | -- | none | 2026-11-17 07:45 UTC | `get_system`, own ship |
| `procyon_gas_cloud` | Procyon Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 48, 2 of 50000 left; argon_gas: richness 42, 1 of 50000 left; chlorine_gas: richness 25, 1 of 10000 left | none | 2026-11-17 07:45 UTC | `get_poi`, own ship |
| `procyon_ice_fields` | Procyon Ice Fields | ice_field (kuiper) | -- | water_ice: richness 54, 22370 of 50000 left; nitrogen_ice: richness 51, 23045 of 50000 left; deuterium_ice: richness 11, 3995 of 5000 left; helium_ice: richness 19, 2122 of 5000 left | none | 2026-11-17 07:45 UTC | `get_poi`, own ship |
| `procyon_colonial_station` | Procyon Colonial Station | station | `procyon_colonial_station` | -- | none | 2026-11-17 07:45 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Procyon Colonial Station (`procyon_colonial_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 07:45 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 07:45 UTC | own ship | Read Procyon Gas Cloud: 4 units left in all | `get_poi`, own ship |
| 2026-11-17 07:45 UTC | own ship | Read Procyon Ice Fields: 51,532 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
