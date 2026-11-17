---
name: porrima
id: 20261117T102835Z
tier: intel
author: Unity
kind: system
system_id: porrima
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Porrima

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where porrima`).

| Field | Value |
|---|---|
| Position | x 1169.0, y 3070.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | adhara, alshain, mebsuta, subra, toi_1452 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `porrima_star` | Porrima Star | sun (K2V) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `porrima_i` | Porrima I | planet (scorched) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `porrima_ii` | Porrima II | planet (arid) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `porrima_iii` | Porrima III | planet (terran) | -- | -- | none | 2026-11-17 09:44 UTC | `get_system`, own ship |
| `redcrumble_field` | Redcrumble Field | asteroid_belt | -- | aluminum_ore: richness 44, 120 of 30000 left | none | 2026-11-17 09:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:44 UTC | own ship | Read Redcrumble Field: 120 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
