---
name: wolf_1061
id: 20261115T215331Z
tier: intel
author: Unity
kind: system
system_id: wolf_1061
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Wolf 1061

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wolf_1061`).

| Field | Value |
|---|---|
| Position | x -2622.2, y 3200.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | alnair, gsc_0012, gsc_0031, pherkad, shaula |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `wolf_1061_star` | Wolf 1061 Star | sun (G5V) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `wolf_1061_frozen_drift` | Wolf 1061 Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 47, 21518 of 50000 left; nitrogen_ice: richness 36, 50000 of 50000 left; deuterium_ice: richness 14, 4752 of 5000 left; methane_ice: richness 13, 4000 of 4000 left | none | 2026-11-15 21:49 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:49 UTC | own ship | Read Wolf 1061 Frozen Drift: 80,270 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
