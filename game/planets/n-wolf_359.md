---
name: wolf_359
id: 20261117T133414Z
tier: intel
author: Unity
kind: system
system_id: wolf_359
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Wolf 359

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wolf_359`).

| Field | Value |
|---|---|
| Position | x -4389.6, y -4208.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | gsc_0003, heathwick, menkib, skat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `wolf_359_star` | Wolf 359 Star | sun (M2V) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `wolf_359_i` | Wolf 359 I | planet (scorched) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `wolf_359_ii` | Wolf 359 II | planet (arid) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `wolf_359_iii` | Wolf 359 III | planet (terran) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `wolf_359_gas_pocket` | Wolf 359 Gas Pocket | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:46 UTC | `get_system`, own ship |

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
| 2026-11-17 12:46 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `wolf_359_gas_pocket`.
