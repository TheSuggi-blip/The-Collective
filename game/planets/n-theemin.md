---
name: theemin
id: 20261117T092740Z
tier: intel
author: Unity
kind: system
system_id: theemin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Theemin

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where theemin`).

| Field | Value |
|---|---|
| Position | x -3061.5, y -772.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | 70_ophiuchi, hollowcrest, kepler_442, lacaille_8760 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `theemin_star` | Theemin Star | sun (F8IV) | -- | -- | none | 2026-11-17 09:04 UTC | `get_system`, own ship |
| `theemin_belt` | Theemin Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 2480 of 28000 left; copper_ore: richness 35, 2361 of 20000 left; aluminum_ore: richness 20, 2216 of 10000 left | none | 2026-11-17 09:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:04 UTC | own ship | Read Theemin Belt: 7,057 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
