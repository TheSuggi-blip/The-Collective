---
name: muscida
id: 20261117T153749Z
tier: intel
author: Unity
kind: system
system_id: muscida
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 30
updated: 2026-11-17
---

# Muscida

Crimson system 22 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where muscida`).

| Field | Value |
|---|---|
| Position | x 5901.5, y 2405.3 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 22 |
| Lanes | 82_eridani, alzirr, frostfeld, gsc_0036, ironhearth, windmere |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `muscida_star` | Muscida Star | sun (G4II) | -- | -- | none | 2026-11-17 14:40 UTC | `get_system`, own ship |
| `muscida_i` | Muscida I | planet (scorched) | -- | -- | none | 2026-11-17 14:40 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:40 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
