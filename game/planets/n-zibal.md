---
name: zibal
id: 20261117T143559Z
tier: intel
author: Unity
kind: system
system_id: zibal
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Zibal

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where zibal`).

| Field | Value |
|---|---|
| Position | x 444.1, y -3152.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | gsc_0009, keelbreak, kurhah, revati |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `zibal_star` | Zibal Star | sun (G8V) | -- | -- | none | 2026-11-17 14:13 UTC | `get_system`, own ship |
| `zibal_i` | Zibal I | planet (scorched) | -- | -- | none | 2026-11-17 14:13 UTC | `get_system`, own ship |
| `zibal_ii` | Zibal II | planet (arid) | -- | -- | none | 2026-11-17 14:13 UTC | `get_system`, own ship |
| `zibal_iii` | Zibal III | planet (terran) | -- | -- | none | 2026-11-17 14:13 UTC | `get_system`, own ship |
| `zibal_ice_shelf` | Zibal Ice Shelf | ice_field (cometary) | -- | not read | none | 2026-11-17 14:13 UTC | `get_system`, own ship |

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
| 2026-11-17 14:13 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `zibal_ice_shelf`.
