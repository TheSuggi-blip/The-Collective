---
name: taygeta
id: 20261117T143552Z
tier: intel
author: Unity
kind: system
system_id: taygeta
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Taygeta

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where taygeta`).

| Field | Value |
|---|---|
| Position | x 2135.0, y -27.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | alnitak, fuyue, hr_8832, ross_248 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `taygeta_star` | Taygeta Star | sun (M6V) | -- | -- | none | 2026-11-17 14:13 UTC | `get_system`, own ship |
| `taygeta_frozen_drift` | Taygeta Frozen Drift | ice_field (cometary) | -- | water_ice: richness 42, 44687 of 50000 left; nitrogen_ice: richness 34, 50000 of 50000 left; deuterium_ice: richness 21, 3682 of 5000 left; helium_ice: richness 12, 5000 of 5000 left | none | 2026-11-17 14:13 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:13 UTC | own ship | Read Taygeta Frozen Drift: 103,369 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
