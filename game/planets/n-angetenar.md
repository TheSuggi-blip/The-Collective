---
name: angetenar
id: 20261117T112922Z
tier: intel
author: Unity
kind: system
system_id: angetenar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Angetenar

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where angetenar`).

| Field | Value |
|---|---|
| Position | x 1726.0, y 4294.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | 40_eridani, chara, tureis, wasat, westmark |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `angetenar_star` | Angetenar Star | sun (DA) | -- | -- | none | 2026-11-17 10:58 UTC | `get_system`, own ship |
| `angetenar_i` | Angetenar I | planet (scorched) | -- | -- | none | 2026-11-17 10:58 UTC | `get_system`, own ship |
| `angetenar_ii` | Angetenar II | planet (arid) | -- | -- | none | 2026-11-17 10:58 UTC | `get_system`, own ship |
| `angetenar_iii` | Angetenar III | planet (terran) | -- | -- | none | 2026-11-17 10:58 UTC | `get_system`, own ship |
| `angetenar_belt` | Angetenar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 53, 99999 of 100000 left; copper_ore: richness 31, 100000 of 100000 left | none | 2026-11-17 10:58 UTC | `get_poi`, own ship |
| `angetenar_gas_pocket` | Angetenar Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 68, 6654 of 50000 left; argon_gas: richness 44, 49064 of 50000 left; plasma_gas: richness 24, 8932 of 10000 left; xenon_gas: richness 19, 9570 of 10000 left; nebula_gas: richness 14, 10000 of 10000 left; neon_gas: richness 42, 49519 of 50000 left; chlorine_gas: richness 24, 1569 of 10000 left; ion_gas: richness 27, 7661 of 10000 left | none | 2026-11-17 10:58 UTC | `get_poi`, own ship |
| `angetenar_ice_belt` | Angetenar Ice Belt | ice_field (cometary) | -- | nitrogen_ice: richness 35, 50000 of 50000 left; deuterium_ice: richness 18, 5000 of 5000 left; helium_ice: richness 21, 5000 of 5000 left | none | 2026-11-17 10:58 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:58 UTC | own ship | Read Angetenar Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 10:58 UTC | own ship | Read Angetenar Gas Pocket: 142,969 units left in all | `get_poi`, own ship |
| 2026-11-17 10:58 UTC | own ship | Read Angetenar Ice Belt: 60,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
