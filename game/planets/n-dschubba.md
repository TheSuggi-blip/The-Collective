---
name: dschubba
id: 20261117T021123Z
tier: intel
author: Unity
kind: system
system_id: dschubba
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dschubba

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dschubba`).

| Field | Value |
|---|---|
| Position | x -5213.0, y -927.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | alchiba, hawthorne |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dschubba_star` | Dschubba Star | sun (M2V) | -- | -- | none | 2026-11-17 01:23 UTC | `get_system`, own ship |
| `dschubba_i` | Dschubba I | planet (scorched) | -- | -- | none | 2026-11-17 01:23 UTC | `get_system`, own ship |
| `dschubba_belt` | Dschubba Belt | asteroid_belt (metallic) | -- | iron_ore: richness 62, 99999 of 100000 left; copper_ore: richness 28, 100000 of 100000 left | none | 2026-11-17 01:23 UTC | `get_poi`, own ship |

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
| 2026-11-17 01:23 UTC | own ship | Read Dschubba Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
