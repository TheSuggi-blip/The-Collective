---
name: sandrift
id: 20261117T184406Z
tier: intel
author: Unity
kind: system
system_id: sandrift
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sandrift

- system 15 jumps from home, police level 0. Station: ENDL:sandrift.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sandrift`).

| Field | Value |
|---|---|
| Position | x -6943.5, y -735.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | chertan, gsc_0004 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sandrift_star` | Sandrift Star | sun (G8V) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `sandrift_i` | Sandrift I | planet (scorched) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `sandrift_ii` | Sandrift II | planet (arid) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `sandrift_ice_fields` | Sandrift Ice Fields | ice_field (kuiper) | -- | water_ice: richness 54, 36611 of 50000 left; nitrogen_ice: richness 49, 50000 of 50000 left | none | 2026-11-17 18:09 UTC | `get_poi`, own ship |
| `7a30dabb88551df9cd077bcff55d2615` | ENDL:sandrift | station | `5e23bb4b74883d9c25506fb7dea5da0c` | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| ENDL:sandrift (`5e23bb4b74883d9c25506fb7dea5da0c`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:09 UTC | `get_system`, own ship |

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
| 2026-11-17 18:09 UTC | own ship | Read Sandrift Ice Fields: 86,611 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
