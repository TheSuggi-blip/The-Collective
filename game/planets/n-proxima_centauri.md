---
name: proxima_centauri
id: 20261117T092735Z
tier: intel
author: Unity
kind: system
system_id: proxima_centauri
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Proxima Centauri

- system 10 jumps from home, police level 0. Station: Frost Ring Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where proxima_centauri`).

| Field | Value |
|---|---|
| Position | x 223.1, y 693.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | barnards_star, dheneb, epsilon_eridani, procyon |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `pollux_major_star` | Pollux Major Star | sun (M2V) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `pollux_major_i` | Pollux Major I | planet (scorched) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `pollux_major_ii` | Pollux Major II | planet (arid) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `pollux_major_iii` | Pollux Major III | planet (terran) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `proxima_centauri_frost_ring` | Proxima Centauri Frost Ring | ice_field (cometary) | -- | water_ice: richness 58, 43952 of 50000 left; nitrogen_ice: richness 33, 50000 of 50000 left; helium_ice: richness 19, 5000 of 5000 left | none | 2026-11-17 08:44 UTC | `get_poi`, own ship |
| `db90abb6fa02abe702f4668707871fb4` | Frost Ring Range | station | `2d7100e399b54b0e5c4af16db0ad8565` | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Frost Ring Range (`2d7100e399b54b0e5c4af16db0ad8565`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 08:44 UTC | `get_system`, own ship |

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
| 2026-11-17 08:44 UTC | own ship | Read Proxima Centauri Frost Ring: 98,952 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
