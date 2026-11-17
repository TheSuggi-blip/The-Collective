---
name: hadar
id: 20261117T133343Z
tier: intel
author: Unity
kind: system
system_id: hadar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Hadar

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where hadar`).

| Field | Value |
|---|---|
| Position | x 5333.0, y 1262.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | muphrid |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `hadar_star` | Hadar Star | sun (M2V) | -- | -- | none | 2026-11-17 13:10 UTC | `get_system`, own ship |
| `hadar_i` | Hadar I | planet (scorched) | -- | -- | none | 2026-11-17 13:10 UTC | `get_system`, own ship |
| `redline_crystals` | Redline Crystals | asteroid_belt | -- | silicon_ore: richness 39, 3518 of 20000 left; neodymium_ore: richness 13, 1845 of 4500 left | none | 2026-11-17 13:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:10 UTC | own ship | Read Redline Crystals: 5,363 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
