---
name: coppervale
id: 20261117T041725Z
tier: intel
author: Unity
kind: system
system_id: coppervale
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Coppervale

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where coppervale`).

| Field | Value |
|---|---|
| Position | x -1969.1, y 5812.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | elnath, etamin, greenvale, sualocin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `coppervale_star` | Coppervale Star | sun (K4V) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `coppervale_i` | Coppervale I | planet (scorched) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `coppervale_ii` | Coppervale II | planet (arid) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `coppervale_iii` | Coppervale III | planet (terran) | -- | -- | none | 2026-11-17 04:00 UTC | `get_system`, own ship |
| `coppervale_belt` | Coppervale Belt | asteroid_belt (metallic) | -- | iron_ore: richness 55, 99999 of 100000 left; copper_ore: richness 47, 100000 of 100000 left; zinc_ore: richness 20, 16000 of 16000 left | none | 2026-11-17 04:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:00 UTC | own ship | Read Coppervale Belt: 215,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
