---
name: alnilam
id: 20261117T082524Z
tier: intel
author: Unity
kind: system
system_id: alnilam
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alnilam

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alnilam`).

| Field | Value |
|---|---|
| Position | x -476.0, y 5351.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | alderamin, jishui, silverbend |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alnilam_star` | Alnilam Star | sun (K4V) | -- | -- | none | 2026-11-17 08:09 UTC | `get_system`, own ship |
| `alnilam_i` | Alnilam I | planet (scorched) | -- | -- | none | 2026-11-17 08:09 UTC | `get_system`, own ship |
| `alnilam_belt` | Alnilam Belt | asteroid_belt (metallic) | -- | iron_ore: richness 42, 3439 of 100000 left; copper_ore: richness 25, 99999 of 100000 left | none | 2026-11-17 08:09 UTC | `get_poi`, own ship |
| `alnilam_gas_pocket` | Alnilam Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 45, 8043 of 50000 left; argon_gas: richness 44, 49360 of 50000 left; xenon_gas: richness 28, 10000 of 10000 left; neon_gas: richness 42, 49998 of 50000 left; krypton_gas: richness 22, 1881 of 5000 left | none | 2026-11-17 08:09 UTC | `get_poi`, own ship |
| `alnilam_frozen_drift` | Alnilam Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 50, 46421 of 50000 left; nitrogen_ice: richness 43, 50000 of 50000 left; helium_ice: richness 19, 5000 of 5000 left | none | 2026-11-17 08:09 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:09 UTC | own ship | Read Alnilam Belt: 103,438 units left in all | `get_poi`, own ship |
| 2026-11-17 08:09 UTC | own ship | Read Alnilam Gas Pocket: 119,282 units left in all | `get_poi`, own ship |
| 2026-11-17 08:09 UTC | own ship | Read Alnilam Frozen Drift: 101,421 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
