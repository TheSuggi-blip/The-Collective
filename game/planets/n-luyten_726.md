---
name: luyten_726
id: 20261117T163939Z
tier: intel
author: Unity
kind: system
system_id: luyten_726
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Luyten 726

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where luyten_726`).

| Field | Value |
|---|---|
| Position | x -108.2, y -6301.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | gsc_0048, kepler_186, poerava, unukalhai |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `luyten_726_star` | Luyten 726 Star | sun (G8V) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_i` | Luyten 726 I | planet (scorched) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_ii` | Luyten 726 II | planet (arid) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_iii` | Luyten 726 III | planet (terran) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_iv` | Luyten 726 IV | planet (jovian) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_v` | Luyten 726 V | planet (glacial) | -- | -- | none | 2026-11-17 15:39 UTC | `get_system`, own ship |
| `luyten_726_frost_ring` | Luyten 726 Frost Ring | ice_field (kuiper) | -- | water_ice: richness 50, 25738 of 50000 left; nitrogen_ice: richness 32, 47577 of 50000 left; helium_ice: richness 20, 1678 of 5000 left | none | 2026-11-17 15:39 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:39 UTC | own ship | Read Luyten 726 Frost Ring: 74,993 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
