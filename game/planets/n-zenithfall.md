---
name: zenithfall
id: 20261117T184355Z
tier: intel
author: Unity
kind: system
system_id: zenithfall
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Zenithfall

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where zenithfall`).

| Field | Value |
|---|---|
| Position | x 2431.4, y -1355.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | bramblewood, gsc_0039, kruger_60, struve_1321 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `zenithfall_star` | Zenithfall Star | sun (G2V) | -- | -- | none | 2026-11-17 18:00 UTC | `get_system`, own ship |
| `zenithfall_i` | Zenithfall I | planet (scorched) | -- | -- | none | 2026-11-17 18:00 UTC | `get_system`, own ship |
| `zenithfall_ice_shelf` | Zenithfall Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 47, 1893 of 50000 left; helium_ice: richness 21, 617 of 5000 left | none | 2026-11-17 18:00 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:00 UTC | own ship | Read Zenithfall Ice Shelf: 2,510 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
