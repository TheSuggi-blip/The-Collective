---
name: harborlight
id: 20261117T092727Z
tier: intel
author: Unity
kind: system
system_id: harborlight
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Harborlight

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where harborlight`).

| Field | Value |
|---|---|
| Position | x 406.9, y 1271.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | adhafera, deneb, kapteyn_5, markab, misthollow |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `harborlight_star` | Harborlight Star | sun (M6V) | -- | -- | none | 2026-11-17 08:37 UTC | `get_system`, own ship |
| `harborlight_gas_cloud` | Harborlight Gas Cloud | gas_cloud (molecular_cloud) | -- | argon_gas: richness 49, 50000 of 50000 left; nebula_gas: richness 17, 10000 of 10000 left; neon_gas: richness 49, 50000 of 50000 left; chlorine_gas: richness 35, 1762 of 10000 left | none | 2026-11-17 08:37 UTC | `get_poi`, own ship |
| `harborlight_ice_shelf` | Harborlight Ice Shelf | ice_field (kuiper) | -- | water_ice: richness 69, 47879 of 50000 left; nitrogen_ice: richness 35, 50000 of 50000 left | none | 2026-11-17 08:37 UTC | `get_poi`, own ship |
| `harborlight_prospectors_leavings` | Harborlight Prospector's Leavings | asteroid_belt | -- | iron_ore: richness 35, 99999 of 100000 left; copper_ore: richness 22, 100000 of 100000 left; sol_alloy_ore: richness 6, 1399 of 1399 left | none | 2026-11-17 08:37 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:37 UTC | own ship | Read Harborlight Gas Cloud: 111,762 units left in all | `get_poi`, own ship |
| 2026-11-17 08:37 UTC | own ship | Read Harborlight Ice Shelf: 97,879 units left in all | `get_poi`, own ship |
| 2026-11-17 08:37 UTC | own ship | Read Harborlight Prospector's Leavings: 201,398 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
