---
name: copernicus
id: 20261117T123134Z
tier: intel
author: Unity
kind: system
system_id: copernicus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Copernicus

Nebula system 18 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where copernicus`).

| Field | Value |
|---|---|
| Position | x 1548.3, y -3664.8 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 18 |
| Lanes | bunda, gold_run, gsc_0030, keelbreak, wealth_lane |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `copernicus_star` | Copernicus Star | sun (G5V) | -- | -- | none | 2026-11-17 12:21 UTC | `get_system`, own ship |
| `copernicus_i` | Copernicus I | planet (arid) | -- | -- | none | 2026-11-17 12:21 UTC | `get_system`, own ship |
| `copernicus_ii` | Copernicus II | planet (tundra) | -- | -- | none | 2026-11-17 12:21 UTC | `get_system`, own ship |
| `copernicus_haze` | Copernicus Haze | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:21 UTC | `get_system`, own ship |

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
| 2026-11-17 12:21 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `copernicus_haze`.
