---
name: tianyi
id: 20261117T163951Z
tier: intel
author: Unity
kind: system
system_id: tianyi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tianyi

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tianyi`).

| Field | Value |
|---|---|
| Position | x 3571.7, y -3307.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | barnard_77, graffias |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tianyi_star` | Tianyi Star | sun (M2V) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_i` | Tianyi I | planet (scorched) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_ii` | Tianyi II | planet (arid) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_iii` | Tianyi III | planet (terran) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_iv` | Tianyi IV | planet (tundra) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_v` | Tianyi V | planet (glacial) | -- | -- | none | 2026-11-17 16:17 UTC | `get_system`, own ship |
| `tianyi_cryobelt` | Tianyi Cryobelt | ice_field (kuiper) | -- | water_ice: richness 65, 25839 of 50000 left; nitrogen_ice: richness 49, 50000 of 50000 left | none | 2026-11-17 16:17 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:17 UTC | own ship | Read Tianyi Cryobelt: 75,839 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
