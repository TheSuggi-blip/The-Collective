---
name: izar
id: 20261117T123148Z
tier: intel
author: Unity
kind: system
system_id: izar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Izar

- system 13 jumps from home, police level 0. Station: Prospector Post.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where izar`).

| Field | Value |
|---|---|
| Position | x -3146.7, y -1936.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | alathfar, aldhibah, sabik, tidewater |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `izar_star` | Izar Star | sun (M2V) | -- | -- | none | 2026-11-17 11:29 UTC | `get_system`, own ship |
| `izar_belt` | Izar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 33, 96578 of 100000 left; copper_ore: richness 30, 100000 of 100000 left; zinc_ore: richness 25, 1782 of 21000 left | none | 2026-11-17 11:29 UTC | `get_poi`, own ship |
| `izar_gas_cloud` | Izar Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 50, 671 of 50000 left; argon_gas: richness 54, 49064 of 50000 left; xenon_gas: richness 21, 9625 of 10000 left; nebula_gas: richness 24, 9485 of 10000 left | none | 2026-11-17 11:29 UTC | `get_poi`, own ship |
| `tall_tale_nebula` | Tall Tale Nebula | nebula | -- | -- | none | 2026-11-17 11:29 UTC | `get_system`, own ship |
| `wh_entrance_1f2d4734` | Collapsed Wormhole | wormhole_collapsed | -- | -- | none | 2026-11-17 11:29 UTC | `get_system`, own ship |
| `9943653fd87ed268ac7ff8f9846fca92` | Prospector Post | station | `7aecb1ebb6297e861c0fa7433d7477fd` | -- | none | 2026-11-17 11:29 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Prospector Post (`7aecb1ebb6297e861c0fa7433d7477fd`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 11:29 UTC | `get_system`, own ship |

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
| 2026-11-17 11:29 UTC | own ship | Read Izar Belt: 198,360 units left in all | `get_poi`, own ship |
| 2026-11-17 11:29 UTC | own ship | Read Izar Gas Cloud: 68,845 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
