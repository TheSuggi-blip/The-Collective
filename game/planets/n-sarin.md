---
name: sarin
id: 20261117T123201Z
tier: intel
author: Unity
kind: system
system_id: sarin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sarin

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sarin`).

| Field | Value |
|---|---|
| Position | x -3896.0, y -6250.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | gsc_0026, silverpine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sarin_star` | Sarin Star | sun (A5V) | -- | -- | none | 2026-11-17 12:24 UTC | `get_system`, own ship |
| `whitesun_carbon` | Whitesun Carbon | asteroid_belt | -- | not read | none | 2026-11-17 12:24 UTC | `get_system`, own ship |

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
| 2026-11-17 12:24 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `whitesun_carbon`.
