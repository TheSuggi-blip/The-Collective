---
name: avior
id: 20261117T010823Z
tier: intel
author: Unity
kind: system
system_id: avior
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Avior

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where avior`).

| Field | Value |
|---|---|
| Position | x -5842.2, y -450.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | gsc_0042, hawthorne, springdale, yildun |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `avior_star` | Avior Star | sun (K4V) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `avior_i` | Avior I | planet (scorched) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `avior_ii` | Avior II | planet (arid) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `avior_belt` | Avior Belt | asteroid_belt (metallic) | -- | iron_ore: richness 54, 99998 of 100000 left; copper_ore: richness 43, 100000 of 100000 left; silver_ore: richness 36, 1 of 25000 left | none | 2026-11-17 00:46 UTC | `get_poi`, own ship |
| `avior_gas_pocket` | Avior Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 62, 16475 of 50000 left; argon_gas: richness 47, 50000 of 50000 left; xenon_gas: richness 15, 10000 of 10000 left; nebula_gas: richness 12, 10000 of 10000 left; chlorine_gas: richness 28, 2985 of 10000 left; ion_gas: richness 56, 8914 of 10000 left | none | 2026-11-17 00:46 UTC | `get_poi`, own ship |
| `avior_cryobelt` | Avior Cryobelt | ice_field (kuiper) | -- | water_ice: richness 59, 47259 of 50000 left; nitrogen_ice: richness 32, 50000 of 50000 left | none | 2026-11-17 00:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:46 UTC | own ship | Read Avior Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 00:46 UTC | own ship | Read Avior Gas Pocket: 98,374 units left in all | `get_poi`, own ship |
| 2026-11-17 00:46 UTC | own ship | Read Avior Cryobelt: 97,259 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
