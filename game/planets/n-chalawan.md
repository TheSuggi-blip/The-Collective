---
name: chalawan
id: 20261117T000623Z
tier: intel
author: Unity
kind: system
system_id: chalawan
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Chalawan

- system 9 jumps from home, police level 0. Station: Quiet Seam Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where chalawan`).

| Field | Value |
|---|---|
| Position | x -5185.9, y 925.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | groombridge_34, innes_40, rasalhague, rotanev |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `chalawan_star` | Chalawan Star | sun (K2V) | -- | -- | none | 2026-11-17 00:00 UTC | `get_system`, own ship |
| `chalawan_haze` | Chalawan Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 48, 8041 of 50000 left; argon_gas: richness 33, 50000 of 50000 left; xenon_gas: richness 25, 838 of 10000 left; nebula_gas: richness 15, 6305 of 10000 left; neon_gas: richness 39, 50000 of 50000 left; chlorine_gas: richness 32, 833 of 10000 left | none | 2026-11-17 00:00 UTC | `get_poi`, own ship |
| `b5fcfaac265fff3e6f29f3a90e614b82` | Quiet Seam Range | station | `8270dbf054635545ed83944a43f09fcd` | -- | none | 2026-11-17 00:00 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Quiet Seam Range (`8270dbf054635545ed83944a43f09fcd`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 00:00 UTC | `get_system`, own ship |

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
| 2026-11-17 00:00 UTC | own ship | Read Chalawan Haze: 116,017 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
