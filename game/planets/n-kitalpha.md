---
name: kitalpha
id: 20261117T041731Z
tier: intel
author: Unity
kind: system
system_id: kitalpha
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kitalpha

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kitalpha`).

| Field | Value |
|---|---|
| Position | x -2353.3, y -246.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | intercrus, kepler_442, lacaille_8760, nembus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kitalpha_star` | Kitalpha Star | sun (M2V) | -- | -- | none | 2026-11-17 04:12 UTC | `get_system`, own ship |
| `kitalpha_i` | Kitalpha I | planet (scorched) | -- | -- | none | 2026-11-17 04:12 UTC | `get_system`, own ship |
| `kitalpha_ii` | Kitalpha II | planet (arid) | -- | -- | none | 2026-11-17 04:12 UTC | `get_system`, own ship |
| `kitalpha_iii` | Kitalpha III | planet (terran) | -- | -- | none | 2026-11-17 04:12 UTC | `get_system`, own ship |
| `lonesweep_field` | Lonesweep Field | asteroid_belt | -- | iron_ore: richness 41, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; antimatter_containment_cell: richness 2, 167 of 167 left | none | 2026-11-17 04:12 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:12 UTC | own ship | Read Lonesweep Field: 200,167 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
