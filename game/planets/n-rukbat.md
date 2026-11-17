---
name: rukbat
id: 20261117T174151Z
tier: intel
author: Unity
kind: system
system_id: rukbat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rukbat

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rukbat`).

| Field | Value |
|---|---|
| Position | x -4199.1, y -3241.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | ain, menkib, mirfak, skat, tarazed |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rukbat_star` | Rukbat Star | sun (M4V) | -- | -- | none | 2026-11-17 17:12 UTC | `get_system`, own ship |
| `rukbat_belt` | Rukbat Belt | asteroid_belt (metallic) | -- | iron_ore: richness 32, 97108 of 100000 left; copper_ore: richness 47, 91210 of 100000 left | none | 2026-11-17 17:12 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:12 UTC | own ship | Read Rukbat Belt: 188,318 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
