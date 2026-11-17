---
name: quartzfield
id: 20261117T133356Z
tier: intel
author: Unity
kind: system
system_id: quartzfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Quartzfield

- system 29 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where quartzfield`).

| Field | Value |
|---|---|
| Position | x 5911.9, y -3540.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 29 |
| Lanes | ironveil, sadr, sheratan |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `quartzfield_star` | Quartzfield Star | sun (M2V) | -- | -- | none | 2026-11-17 12:45 UTC | `get_system`, own ship |
| `quartzfield_i` | Quartzfield I | planet (scorched) | -- | -- | none | 2026-11-17 12:45 UTC | `get_system`, own ship |
| `quartzfield_ii` | Quartzfield II | planet (arid) | -- | -- | none | 2026-11-17 12:45 UTC | `get_system`, own ship |
| `quartzfield_iii` | Quartzfield III | planet (terran) | -- | -- | none | 2026-11-17 12:45 UTC | `get_system`, own ship |
| `bare_frame_drift` | Bare Frame Drift | asteroid_belt | -- | aluminum_ore: richness 32, 112 of 30000 left | none | 2026-11-17 12:45 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:45 UTC | own ship | Read Bare Frame Drift: 112 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
