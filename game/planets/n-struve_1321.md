---
name: struve_1321
id: 20261117T184403Z
tier: intel
author: Unity
kind: system
system_id: struve_1321
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Struve 1321

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where struve_1321`).

| Field | Value |
|---|---|
| Position | x 2616.9, y -1154.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | bramblewood, gsc_0039, kruger_60, zenithfall |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `struve_1321_star` | Struve 1321 Star | sun (K6V) | -- | -- | none | 2026-11-17 17:56 UTC | `get_system`, own ship |
| `struve_1321_i` | Struve 1321 I | planet (scorched) | -- | -- | none | 2026-11-17 17:56 UTC | `get_system`, own ship |
| `struve_1321_ii` | Struve 1321 II | planet (arid) | -- | -- | none | 2026-11-17 17:56 UTC | `get_system`, own ship |
| `struve_1321_iii` | Struve 1321 III | planet (terran) | -- | -- | none | 2026-11-17 17:56 UTC | `get_system`, own ship |
| `struve_1321_gas_plume` | Struve 1321 Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 58, 1600 of 50000 left; argon_gas: richness 46, 1597 of 50000 left; plasma_gas: richness 19, 599 of 10000 left; xenon_gas: richness 25, 597 of 10000 left; nebula_gas: richness 26, 596 of 10000 left; ion_gas: richness 34, 593 of 10000 left | none | 2026-11-17 17:56 UTC | `get_poi`, own ship |
| `struve_1321_cryobelt` | Struve 1321 Cryobelt | ice_field (kuiper) | -- | water_ice: richness 63, 293 of 50000 left; nitrogen_ice: richness 38, 344 of 50000 left; deuterium_ice: richness 15, 574 of 5000 left | none | 2026-11-17 17:56 UTC | `get_poi`, own ship |
| `wanderers_veil` | Wanderer's Veil | nebula | -- | -- | none | 2026-11-17 17:56 UTC | `get_system`, own ship |

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
| 2026-11-17 17:56 UTC | own ship | Read Struve 1321 Gas Plume: 5,582 units left in all | `get_poi`, own ship |
| 2026-11-17 17:56 UTC | own ship | Read Struve 1321 Cryobelt: 1,211 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
