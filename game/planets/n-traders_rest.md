---
name: traders_rest
id: 20261117T174144Z
tier: intel
author: Unity
kind: system
system_id: traders_rest
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 80
updated: 2026-11-17
---

# Trader's Rest

Nebula system 22 jumps from home, police level 80. Station: Trader's Rest Resort Station.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where traders_rest`).

| Field | Value |
|---|---|
| Position | x 1692.4, y -4911.2 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 22 |
| Lanes | factory_belt, gliese_436, haven, khambalia, ogma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `golden_hour` | Golden Hour | sun (G3V) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `the_promenade` | The Promenade | planet (oceanic) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `merchants_landing` | Merchant's Landing | planet (terran) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `garden_world` | Garden World | planet (terran) | -- | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |
| `traders_rest_resort_station` | Trader's Rest Resort Station | station | `traders_rest_resort_station` | -- | none | 2026-11-17 17:07 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Trader's Rest Resort Station (`traders_rest_resort_station`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:07 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 80: High Security (active police patrols) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:07 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- No belt, ice field or gas cloud on the chart.
