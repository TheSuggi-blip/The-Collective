---
name: bramblewood
id: 20261117T184420Z
tier: intel
author: Unity
kind: system
system_id: bramblewood
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Bramblewood

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where bramblewood`).

| Field | Value |
|---|---|
| Position | x 2335.8, y -1143.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | gsc_0039, kruger_60, struve_1321, zenithfall |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bramblewood_star` | Bramblewood Star | sun (M2V) | -- | -- | none | 2026-11-17 18:04 UTC | `get_system`, own ship |
| `bramblewood_i` | Bramblewood I | planet (scorched) | -- | -- | none | 2026-11-17 18:04 UTC | `get_system`, own ship |
| `bramblewood_ii` | Bramblewood II | planet (arid) | -- | -- | none | 2026-11-17 18:04 UTC | `get_system`, own ship |
| `bramblewood_iii` | Bramblewood III | planet (terran) | -- | -- | none | 2026-11-17 18:04 UTC | `get_system`, own ship |
| `bramblewood_belt` | Bramblewood Belt | asteroid_belt (metallic) | -- | iron_ore: richness 57, 80869 of 100000 left; copper_ore: richness 33, 100000 of 100000 left; zinc_ore: richness 24, 19074 of 20000 left | none | 2026-11-17 18:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:04 UTC | own ship | Read Bramblewood Belt: 199,943 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
