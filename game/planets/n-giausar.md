---
name: giausar
id: 20261116T234001Z
tier: intel
author: Unity
kind: system
system_id: giausar
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Giausar

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where giausar`).

| Field | Value |
|---|---|
| Position | x -6504.1, y 1432.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | aldebaran, duskfield, gsc_0028, gsc_0040, sadalsuud |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `giausar_star` | Giausar Star | sun (M4V) | -- | -- | none | 2026-11-16 23:39 UTC | `get_system`, own ship |
| `giausar_i` | Giausar I | planet (scorched) | -- | -- | none | 2026-11-16 23:39 UTC | `get_system`, own ship |
| `giausar_frost_ring` | Giausar Frost Ring | ice_field (kuiper) | -- | water_ice: richness 61, 32541 of 50000 left; nitrogen_ice: richness 41, 50000 of 50000 left; helium_ice: richness 18, 4928 of 5000 left | none | 2026-11-16 23:39 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:39 UTC | own ship | Read Giausar Frost Ring: 87,469 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
