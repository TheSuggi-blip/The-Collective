---
name: tanglewood
id: 20261115T235527Z
tier: intel
author: Unity
kind: system
system_id: tanglewood
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Tanglewood

- system 6 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tanglewood`).

| Field | Value |
|---|---|
| Position | x -3253.3, y 4494.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 6 |
| Lanes | coldwater, felis, gsc_0016, stormwatch |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tanglewood_star` | Tanglewood Star | sun (M6V) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `tanglewood_i` | Tanglewood I | planet (scorched) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `tanglewood_frost_ring` | Tanglewood Frost Ring | ice_field (kuiper) | -- | water_ice: richness 66, 50000 of 50000 left; nitrogen_ice: richness 42, 50000 of 50000 left; helium_ice: richness 13, 5000 of 5000 left | none | 2026-11-15 23:34 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 23:34 UTC | own ship | Read Tanglewood Frost Ring: 105,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
