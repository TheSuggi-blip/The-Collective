---
name: gudja
id: 20261117T082535Z
tier: intel
author: Unity
kind: system
system_id: gudja
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Gudja

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gudja`).

| Field | Value |
|---|---|
| Position | x -269.5, y 3162.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | gsc_0017, hd_147513, pipirima, rastaban |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gudja_star` | Gudja Star | sun (M2V) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `gudja_i` | Gudja I | planet (scorched) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `gudja_ii` | Gudja II | planet (arid) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `gudja_iii` | Gudja III | planet (terran) | -- | -- | none | 2026-11-17 07:44 UTC | `get_system`, own ship |
| `gudja_ice_fields` | Gudja Ice Fields | ice_field (kuiper) | -- | water_ice: richness 65, 4548 of 50000 left; nitrogen_ice: richness 33, 50000 of 50000 left | none | 2026-11-17 07:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 07:44 UTC | own ship | Read Gudja Ice Fields: 54,548 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
