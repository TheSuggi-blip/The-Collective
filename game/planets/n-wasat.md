---
name: wasat
id: 20261117T123214Z
tier: intel
author: Unity
kind: system
system_id: wasat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Wasat

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wasat`).

| Field | Value |
|---|---|
| Position | x 2008.2, y 4160.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | 40_eridani, angetenar, bd20_2457, westmark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `wasat_star` | Wasat Star | sun (G2V) | -- | -- | none | 2026-11-17 11:35 UTC | `get_system`, own ship |
| `wasat_gas_cloud` | Wasat Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 55, 2703 of 50000 left; argon_gas: richness 33, 49999 of 50000 left; xenon_gas: richness 29, 10000 of 10000 left; nebula_gas: richness 16, 10000 of 10000 left; neon_gas: richness 46, 50000 of 50000 left; chlorine_gas: richness 27, 983 of 10000 left | none | 2026-11-17 11:35 UTC | `get_poi`, own ship |
| `wasat_cryobelt` | Wasat Cryobelt | ice_field (kuiper) | -- | water_ice: richness 54, 44191 of 50000 left; nitrogen_ice: richness 41, 50000 of 50000 left; deuterium_ice: richness 18, 4949 of 5000 left | none | 2026-11-17 11:35 UTC | `get_poi`, own ship |
| `wasat_cold_forge_seam` | Wasat Cold Forge Seam | asteroid_belt | -- | iron_ore: richness 42, 34589 of 100000 left; copper_ore: richness 30, 98843 of 100000 left; darksteel_ore: richness 5, 284 of 284 left | none | 2026-11-17 11:35 UTC | `get_poi`, own ship |
| `glazeknot_cluster` | Glazeknot Cluster | asteroid_belt | -- | iron_ore: richness 28, 100000 of 100000 left; copper_ore: richness 25, 100000 of 100000 left; plasma_residue: richness 9, 846 of 846 left | none | 2026-11-17 11:35 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:35 UTC | own ship | Read Wasat Gas Cloud: 123,685 units left in all | `get_poi`, own ship |
| 2026-11-17 11:35 UTC | own ship | Read Wasat Cryobelt: 99,140 units left in all | `get_poi`, own ship |
| 2026-11-17 11:35 UTC | own ship | Read Wasat Cold Forge Seam: 133,716 units left in all | `get_poi`, own ship |
| 2026-11-17 11:35 UTC | own ship | Read Glazeknot Cluster: 200,846 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
