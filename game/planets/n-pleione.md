---
name: pleione
id: 20261117T102834Z
tier: intel
author: Unity
kind: system
system_id: pleione
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Pleione

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where pleione`).

| Field | Value |
|---|---|
| Position | x -988.0, y 5899.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | etamin, fomalhaut, greenvale, yed_posterior |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `pleione_star` | Pleione Star | sun (M6V) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `pleione_i` | Pleione I | planet (scorched) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `pleione_ii` | Pleione II | planet (arid) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `pleione_iii` | Pleione III | planet (terran) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `pleione_iv` | Pleione IV | planet (tundra) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `pleione_ice_fields` | Pleione Ice Fields | ice_field (kuiper) | -- | water_ice: richness 40, 48654 of 50000 left; nitrogen_ice: richness 33, 50000 of 50000 left; deuterium_ice: richness 21, 4279 of 5000 left | none | 2026-11-17 09:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:44 UTC | own ship | Read Pleione Ice Fields: 102,933 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
