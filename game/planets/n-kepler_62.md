---
name: kepler_62
id: 20261117T153742Z
tier: intel
author: Unity
kind: system
system_id: kepler_62
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kepler-62

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kepler_62`).

| Field | Value |
|---|---|
| Position | x 4334.8, y -1216.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | cebalrai, gsc_0011, quarrytown, upsilon_andromedae |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kepler_62_star` | Kepler-62 Star | sun (K2V) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `kepler_62_i` | Kepler-62 I | planet (scorched) | -- | -- | none | 2026-11-17 15:18 UTC | `get_system`, own ship |
| `kepler_62_gas_pocket` | Kepler-62 Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 47, 1619 of 50000 left; argon_gas: richness 39, 1621 of 50000 left; plasma_gas: richness 22, 563 of 10000 left; xenon_gas: richness 21, 561 of 10000 left; neon_gas: richness 46, 1622 of 50000 left; chlorine_gas: richness 32, 563 of 10000 left | none | 2026-11-17 15:18 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:18 UTC | own ship | Read Kepler-62 Gas Pocket: 6,549 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
