---
name: emberglow
id: 20261117T133333Z
tier: intel
author: Unity
kind: system
system_id: emberglow
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Emberglow

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where emberglow`).

| Field | Value |
|---|---|
| Position | x -5763.7, y -3999.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | ancha, greymist, tabit, willowthorn |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `emberglow_star` | Emberglow Star | sun (G2V) | -- | -- | none | 2026-11-17 13:31 UTC | `get_system`, own ship |
| `emberglow_i` | Emberglow I | planet (scorched) | -- | -- | none | 2026-11-17 13:31 UTC | `get_system`, own ship |
| `elder_silicon_beds` | Elder Silicon Beds | asteroid_belt | -- | iron_ore: richness 40, 99999 of 100000 left; copper_ore: richness 31, 100000 of 100000 left; silicon_ore: richness 43, 4935 of 20000 left; neodymium_ore: richness 12, 3006 of 4000 left | none | 2026-11-17 13:31 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:31 UTC | own ship | Read Elder Silicon Beds: 207,940 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
