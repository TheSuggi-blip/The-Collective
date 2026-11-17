---
name: segin
id: 20261117T184405Z
tier: intel
author: Unity
kind: system
system_id: segin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Segin

- system 21 jumps from home, police level 0. Station: Hive Segin.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where segin`).

| Field | Value |
|---|---|
| Position | x 2634.3, y -2580.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | gsc_0051, nekkar, tau_bootis |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `segin_star` | Segin Star | sun (G5V) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_i` | Segin I | planet (scorched) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_ii` | Segin II | planet (arid) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_iii` | Segin III | planet (terran) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_iv` | Segin IV | planet (tundra) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_v` | Segin V | planet (jovian) | -- | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |
| `segin_emission_nebula` | Segin Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 66, 585 of 50000 left; argon_gas: richness 42, 24874 of 50000 left; plasma_gas: richness 22, 5261 of 10000 left; nebula_gas: richness 15, 5748 of 10000 left; chlorine_gas: richness 32, 562 of 10000 left; ion_gas: richness 37, 4301 of 10000 left | none | 2026-11-17 18:16 UTC | `get_poi`, own ship |
| `b558150dff77744769dac6485cd87a54` | Hive Segin | station | `92fd0bb3c5232a0d9a337afe5f883116` | -- | none | 2026-11-17 18:16 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Hive Segin (`92fd0bb3c5232a0d9a337afe5f883116`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:16 UTC | `get_system`, own ship |

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
| 2026-11-17 18:16 UTC | own ship | Read Segin Emission Nebula: 41,331 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
