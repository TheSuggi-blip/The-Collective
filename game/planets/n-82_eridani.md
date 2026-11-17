---
name: 82_eridani
id: 20261117T143524Z
tier: intel
author: Unity
kind: system
system_id: 82_eridani
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: crimson
police_level: 30
updated: 2026-11-17
---

# 82 Eridani

Crimson system 22 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where 82_eridani`).

| Field | Value |
|---|---|
| Position | x 5776.0, y 2200.2 (Galactic Units) |
| Empire | crimson |
| Jumps from home | 22 |
| Lanes | frostfeld, gsc_0036, hd_20794, ironhearth, muscida, windmere |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `82_eridani_star` | 82 Eridani Star | sun (G8V) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `82_eridani_i` | 82 Eridani I | planet (tundra) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `82_eridani_ii` | 82 Eridani II | planet (glacial) | -- | -- | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `82_eridani_belt` | 82 Eridani Belt | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 14:35 UTC | `get_system`, own ship |
| `82_eridani_frozen_drift` | 82 Eridani Frozen Drift | ice_field (kuiper) | -- | nitrogen_ice: richness 32, 953 of 50000 left; helium_ice: richness 10, 1022 of 5000 left | none | 2026-11-17 14:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:35 UTC | own ship | Read 82 Eridani Frozen Drift: 1,975 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `82_eridani_belt`.
