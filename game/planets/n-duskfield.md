---
name: duskfield
id: 20261116T233959Z
tier: intel
author: Unity
kind: system
system_id: duskfield
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Duskfield

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where duskfield`).

| Field | Value |
|---|---|
| Position | x -6135.6, y 1821.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | acrab, atria, giausar, gsc_0040, sadalsuud |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `duskfield_star` | Duskfield Star | sun (M4V) | -- | -- | none | 2026-11-16 23:38 UTC | `get_system`, own ship |
| `duskfield_i` | Duskfield I | planet (scorched) | -- | -- | none | 2026-11-16 23:38 UTC | `get_system`, own ship |
| `duskfield_ii` | Duskfield II | planet (arid) | -- | -- | none | 2026-11-16 23:38 UTC | `get_system`, own ship |
| `duskfield_iii` | Duskfield III | planet (terran) | -- | -- | none | 2026-11-16 23:38 UTC | `get_system`, own ship |
| `duskfield_cryobelt` | Duskfield Cryobelt | ice_field (kuiper) | -- | water_ice: richness 43, 35328 of 50000 left; nitrogen_ice: richness 44, 50000 of 50000 left | none | 2026-11-16 23:38 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:38 UTC | own ship | Read Duskfield Cryobelt: 85,328 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
