---
name: alpha_centauri
id: 20261117T092721Z
tier: intel
author: Unity
kind: system
system_id: alpha_centauri
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 80
updated: 2026-11-17
---

# Alpha Centauri

Solarian system 11 jumps from home, police level 80. Station: Alpha Centauri Colonial Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alpha_centauri`).

| Field | Value |
|---|---|
| Position | x 97.2, y -261.4 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 11 |
| Lanes | sol, tau_ceti |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alpha_centauri_a` | Alpha Centauri A | sun (G2V) | -- | -- | none | 2026-11-17 09:08 UTC | `get_system`, own ship |
| `new_providence` | New Providence | planet (terran) | -- | -- | none | 2026-11-17 09:08 UTC | `get_system`, own ship |
| `centauri_station` | Centauri Station | planet (terran) | -- | -- | none | 2026-11-17 09:08 UTC | `get_system`, own ship |
| `farwatch` | Farwatch | planet (tundra) | -- | -- | none | 2026-11-17 09:08 UTC | `get_system`, own ship |
| `alpha_centauri_frost_ring` | Alpha Centauri Frost Ring | ice_field (kuiper) | -- | water_ice: richness 65, 2 of 50000 left; nitrogen_ice: richness 37, 3 of 50000 left; oxygen_ice: richness 13, 0 of 4500 left | none | 2026-11-17 09:08 UTC | `get_poi`, own ship |
| `alpha_centauri_colonial_station` | Alpha Centauri Colonial Station | station | `alpha_centauri_colonial_station` | -- | none | 2026-11-17 09:08 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Alpha Centauri Colonial Station (`alpha_centauri_colonial_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 09:08 UTC | `get_system`, own ship |

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
| 2026-11-17 09:08 UTC | own ship | Read Alpha Centauri Frost Ring: 5 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
