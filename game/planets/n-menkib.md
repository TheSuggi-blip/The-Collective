---
name: menkib
id: 20261117T153747Z
tier: intel
author: Unity
kind: system
system_id: menkib
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Menkib

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where menkib`).

| Field | Value |
|---|---|
| Position | x -4409.6, y -3870.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | mirfak, rukbat, skat, winterhold, wolf_359 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `menkib_star` | Menkib Star | sun (O7I) | -- | -- | none | 2026-11-17 14:54 UTC | `get_system`, own ship |
| `menkib_stellar_wind` | Menkib Stellar Wind | gas_cloud (emission) | -- | not read | none | 2026-11-17 14:54 UTC | `get_system`, own ship |

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
| 2026-11-17 14:54 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `menkib_stellar_wind`.
