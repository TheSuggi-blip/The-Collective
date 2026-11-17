---
name: alrescha
id: 20261117T163923Z
tier: intel
author: Unity
kind: system
system_id: alrescha
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alrescha

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alrescha`).

| Field | Value |
|---|---|
| Position | x 3375.8, y -4685.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | ashford, cursa, farpoint, ravensbrook |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alrescha_star` | Alrescha Star | sun (M4V) | -- | -- | none | 2026-11-17 16:20 UTC | `get_system`, own ship |
| `alrescha_i` | Alrescha I | planet (scorched) | -- | -- | none | 2026-11-17 16:20 UTC | `get_system`, own ship |
| `alrescha_ii` | Alrescha II | planet (arid) | -- | -- | none | 2026-11-17 16:20 UTC | `get_system`, own ship |
| `alrescha_emission_nebula` | Alrescha Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 64, 2574 of 50000 left; argon_gas: richness 39, 2585 of 50000 left; plasma_gas: richness 18, 793 of 10000 left; neon_gas: richness 37, 2588 of 50000 left; chlorine_gas: richness 22, 756 of 10000 left; ion_gas: richness 33, 753 of 10000 left | none | 2026-11-17 16:20 UTC | `get_poi`, own ship |
| `alrescha_ice_fields` | Alrescha Ice Fields | ice_field (kuiper) | -- | water_ice: richness 62, 38113 of 50000 left; nitrogen_ice: richness 38, 50000 of 50000 left; helium_ice: richness 13, 5000 of 5000 left | none | 2026-11-17 16:20 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:20 UTC | own ship | Read Alrescha Emission Nebula: 10,049 units left in all | `get_poi`, own ship |
| 2026-11-17 16:20 UTC | own ship | Read Alrescha Ice Fields: 93,113 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
