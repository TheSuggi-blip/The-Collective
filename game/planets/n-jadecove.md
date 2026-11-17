---
name: jadecove
id: 20261117T092729Z
tier: intel
author: Unity
kind: system
system_id: jadecove
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Jadecove

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where jadecove`).

| Field | Value |
|---|---|
| Position | x -586.5, y 3927.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | groombridge_1618, gsc_0020, hassaleh, menkent |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `jadecove_star` | Jadecove Star | sun (M2V) | -- | -- | none | 2026-11-17 08:38 UTC | `get_system`, own ship |
| `jadecove_i` | Jadecove I | planet (scorched) | -- | -- | none | 2026-11-17 08:38 UTC | `get_system`, own ship |
| `long_errand_band` | Long Errand Band | asteroid_belt | -- | nickel_ore: richness 40, 609 of 20000 left | none | 2026-11-17 08:38 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:38 UTC | own ship | Read Long Errand Band: 609 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
