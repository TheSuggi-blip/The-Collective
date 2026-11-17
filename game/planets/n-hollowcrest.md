---
name: hollowcrest
id: 20261117T092728Z
tier: intel
author: Unity
kind: system
system_id: hollowcrest
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Hollowcrest

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where hollowcrest`).

| Field | Value |
|---|---|
| Position | x -3363.9, y -1181.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | alathfar, merak, theemin, titawin |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `hollowcrest_star` | Hollowcrest Star | sun (M4V) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `hollowcrest_i` | Hollowcrest I | planet (scorched) | -- | -- | none | 2026-11-17 09:16 UTC | `get_system`, own ship |
| `hollowcrest_frozen_drift` | Hollowcrest Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 60, 33725 of 50000 left; nitrogen_ice: richness 47, 50000 of 50000 left | none | 2026-11-17 09:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:16 UTC | own ship | Read Hollowcrest Frozen Drift: 83,725 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
