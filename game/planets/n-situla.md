---
name: situla
id: 20261117T194615Z
tier: intel
author: Unity
kind: system
system_id: situla
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Situla

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where situla`).

| Field | Value |
|---|---|
| Position | x 1320.2, y -999.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | algieba, struve_2398, zaniah |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `situla_star` | Situla Star | sun (M2V) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `situla_i` | Situla I | planet (scorched) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `situla_ii` | Situla II | planet (arid) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `situla_iii` | Situla III | planet (terran) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `situla_iv` | Situla IV | planet (jovian) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `situla_v` | Situla V | planet (jovian) | -- | -- | none | 2026-11-17 19:36 UTC | `get_system`, own ship |
| `shelved_cobalt_field` | Shelved Cobalt Field | asteroid_belt | -- | iron_ore: richness 35, 99999 of 100000 left; copper_ore: richness 35, 100000 of 100000 left; cobalt_ore: richness 41, 3875 of 25000 left | none | 2026-11-17 19:36 UTC | `get_poi`, own ship |

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
| 2026-11-17 19:36 UTC | own ship | Read Shelved Cobalt Field: 203,874 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
