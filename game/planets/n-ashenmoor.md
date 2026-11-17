---
name: ashenmoor
id: 20261117T153726Z
tier: intel
author: Unity
kind: system
system_id: ashenmoor
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ashenmoor

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ashenmoor`).

| Field | Value |
|---|---|
| Position | x -5209.8, y -3203.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | gsc_0015, tabit, willowgate, winterhold |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ashenmoor_star` | Ashenmoor Star | sun (M4V) | -- | -- | none | 2026-11-17 15:02 UTC | `get_system`, own ship |
| `ashenmoor_ice_shelf` | Ashenmoor Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 53, 25851 of 50000 left; nitrogen_ice: richness 38, 50000 of 50000 left | none | 2026-11-17 15:02 UTC | `get_poi`, own ship |
| `ashenmoor_ghost_resonance` | Ashenmoor Ghost Resonance | nebula | -- | -- | none | 2026-11-17 15:02 UTC | `get_system`, own ship |
| `aftermath_haze` | Aftermath Haze | nebula | -- | -- | none | 2026-11-17 15:02 UTC | `get_system`, own ship |

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
| 2026-11-17 15:02 UTC | own ship | Read Ashenmoor Ice Shelf: 75,851 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
