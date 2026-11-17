---
name: timberline
id: 20261117T123210Z
tier: intel
author: Unity
kind: system
system_id: timberline
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Timberline

Solarian system 13 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where timberline`).

| Field | Value |
|---|---|
| Position | x 281.1, y -1214.5 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 13 |
| Lanes | arcturus, electra, ross_154, tau_ceti |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `timberline_star` | Timberline Star | sun (K5V) | -- | -- | none | 2026-11-17 11:32 UTC | `get_system`, own ship |
| `timberline_gas_pocket` | Timberline Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 58, 263 of 50000 left; argon_gas: richness 54, 257 of 50000 left; plasma_gas: richness 19, 265 of 10000 left; nebula_gas: richness 21, 265 of 10000 left; neon_gas: richness 31, 262 of 50000 left | none | 2026-11-17 11:32 UTC | `get_poi`, own ship |
| `timberline_ice_shelf` | Timberline Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 68, 649 of 50000 left | none | 2026-11-17 11:32 UTC | `get_poi`, own ship |
| `abandoned_sensor_mast` | Abandoned Sensor Mast | relic (derelict) | -- | -- | none | 2026-11-17 11:32 UTC | `get_system`, own ship |

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
| 2026-11-17 11:32 UTC | own ship | Read Timberline Gas Pocket: 1,312 units left in all | `get_poi`, own ship |
| 2026-11-17 11:32 UTC | own ship | Read Timberline Ice Shelf: 649 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
