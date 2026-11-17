---
name: unukalhai
id: 20261117T153758Z
tier: intel
author: Unity
kind: system
system_id: unukalhai
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Unukalhai

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where unukalhai`).

| Field | Value |
|---|---|
| Position | x -467.1, y -6782.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | algiedi, hd_10647, hd_85512, luyten_726, sadalbari, yarrowfield |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `unukalhai_star` | Unukalhai Star | sun (M2V) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_i` | Unukalhai I | planet (scorched) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_ii` | Unukalhai II | planet (arid) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_iii` | Unukalhai III | planet (terran) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_iv` | Unukalhai IV | planet (tundra) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_v` | Unukalhai V | planet (glacial) | -- | -- | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_haze` | Unukalhai Haze | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 15:36 UTC | `get_system`, own ship |
| `unukalhai_ice_fields` | Unukalhai Ice Fields | ice_field (cometary) | -- | water_ice: richness 57, 45381 of 50000 left; nitrogen_ice: richness 49, 50000 of 50000 left; helium_ice: richness 16, 5000 of 5000 left; ammonia_ice: richness 14, 5000 of 5000 left | none | 2026-11-17 15:36 UTC | `get_poi`, own ship |

## Stations

None on the chart.

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
| 2026-11-17 15:36 UTC | own ship | Read Unukalhai Ice Fields: 105,381 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `unukalhai_haze`.
