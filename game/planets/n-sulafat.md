---
name: sulafat
id: 20261117T194612Z
tier: intel
author: Unity
kind: system
system_id: sulafat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Sulafat

- system 19 jumps from home, police level 0. Station: Hive Sulafat.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where sulafat`).

| Field | Value |
|---|---|
| Position | x -1646.5, y -2780.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | gsc_0023, haedus, kochab, starfall, void_gate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `sulafat_star` | Sulafat Star | sun (M4V) | -- | -- | none | 2026-11-17 19:27 UTC | `get_system`, own ship |
| `sulafat_belt` | Sulafat Belt | asteroid_belt (metallic) | -- | iron_ore: richness 30, 0 of 100000 left; copper_ore: richness 35, 0 of 100000 left | none | 2026-11-17 19:27 UTC | `get_poi`, own ship |
| `sulafat_haze` | Sulafat Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 54, 7075 of 50000 left; argon_gas: richness 45, 49999 of 50000 left; neon_gas: richness 46, 50000 of 50000 left; chlorine_gas: richness 40, 1616 of 10000 left | none | 2026-11-17 19:27 UTC | `get_poi`, own ship |
| `07bf78755682cf3e8ef049f3fa560049` | Hive Sulafat | station | `9b1e70b700b5de06e6f9e5ecf9e43df1` | -- | none | 2026-11-17 19:27 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Hive Sulafat (`9b1e70b700b5de06e6f9e5ecf9e43df1`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 19:27 UTC | `get_system`, own ship |

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
| 2026-11-17 19:27 UTC | own ship | Read Sulafat Belt: nothing left | `get_poi`, own ship |
| 2026-11-17 19:27 UTC | own ship | Read Sulafat Haze: 108,690 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
