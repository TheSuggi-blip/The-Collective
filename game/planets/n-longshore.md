---
name: longshore
id: 20261117T143546Z
tier: intel
author: Unity
kind: system
system_id: longshore
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Longshore

- system 24 jumps from home, police level 0. Station: Atlantis.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where longshore`).

| Field | Value |
|---|---|
| Position | x -1494.6, y -6832.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | hd_10647 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `longshore_star` | Longshore Star | sun (M4V) | -- | -- | none | 2026-11-17 14:28 UTC | `get_system`, own ship |
| `longshore_i` | Longshore I | planet (scorched) | -- | -- | none | 2026-11-17 14:28 UTC | `get_system`, own ship |
| `longshore_ii` | Longshore II | planet (arid) | -- | -- | none | 2026-11-17 14:28 UTC | `get_system`, own ship |
| `longshore_gas_cloud` | Longshore Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 52, 7078 of 50000 left; argon_gas: richness 42, 40761 of 50000 left; neon_gas: richness 36, 49535 of 50000 left; chlorine_gas: richness 35, 211 of 10000 left; ion_gas: richness 30, 253 of 10000 left | none | 2026-11-17 14:28 UTC | `get_poi`, own ship |
| `39d7e19c0f183fe179ec245cab2720cd` | Atlantis | station | `5b645d54443116f33cf54ba70235e7d5` | -- | none | 2026-11-17 14:28 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Atlantis (`5b645d54443116f33cf54ba70235e7d5`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:28 UTC | `get_system`, own ship |

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
| 2026-11-17 14:28 UTC | own ship | Read Longshore Gas Cloud: 97,838 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
