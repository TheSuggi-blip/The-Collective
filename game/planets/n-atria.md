---
name: atria
id: 20261117T010822Z
tier: intel
author: Unity
kind: system
system_id: atria
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Atria

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where atria`).

| Field | Value |
|---|---|
| Position | x -5649.5, y 2222.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | acrab, duskfield, marfik, regor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `atria_star` | Atria Star | sun (M4V) | -- | -- | none | 2026-11-17 00:36 UTC | `get_system`, own ship |
| `atria_i` | Atria I | planet (scorched) | -- | -- | none | 2026-11-17 00:36 UTC | `get_system`, own ship |
| `atria_ii` | Atria II | planet (arid) | -- | -- | none | 2026-11-17 00:36 UTC | `get_system`, own ship |
| `atria_belt` | Atria Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 91274 of 100000 left; copper_ore: richness 21, 100000 of 100000 left; aluminum_ore: richness 59, 1353 of 30000 left; gold_ore: richness 20, 925 of 25000 left | none | 2026-11-17 00:36 UTC | `get_poi`, own ship |
| `atria_emission_nebula` | Atria Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 47, 19204 of 50000 left; argon_gas: richness 52, 49999 of 50000 left; neon_gas: richness 49, 50000 of 50000 left | none | 2026-11-17 00:36 UTC | `get_poi`, own ship |
| `atria_ice_fields` | Atria Ice Fields | ice_field (kuiper) | -- | water_ice: richness 55, 39843 of 50000 left; nitrogen_ice: richness 35, 50000 of 50000 left; deuterium_ice: richness 15, 5000 of 5000 left | none | 2026-11-17 00:36 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:36 UTC | own ship | Read Atria Belt: 193,552 units left in all | `get_poi`, own ship |
| 2026-11-17 00:36 UTC | own ship | Read Atria Emission Nebula: 119,203 units left in all | `get_poi`, own ship |
| 2026-11-17 00:36 UTC | own ship | Read Atria Ice Fields: 94,843 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
