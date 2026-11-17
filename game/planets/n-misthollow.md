---
name: misthollow
id: 20261117T092734Z
tier: intel
author: Unity
kind: system
system_id: misthollow
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Misthollow

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where misthollow`).

| Field | Value |
|---|---|
| Position | x 629.3, y 1893.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | adhafera, deneb, harborlight, kapteyn_5 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `misthollow_star` | Misthollow Star | sun (F8V) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `misthollow_i` | Misthollow I | planet (scorched) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `misthollow_ii` | Misthollow II | planet (arid) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `misthollow_iii` | Misthollow III | planet (terran) | -- | -- | none | 2026-11-17 08:44 UTC | `get_system`, own ship |
| `misthollow_belt` | Misthollow Belt | asteroid_belt (metallic) | -- | iron_ore: richness 59, 4506 of 100000 left; copper_ore: richness 39, 44693 of 100000 left | none | 2026-11-17 08:44 UTC | `get_poi`, own ship |
| `misthollow_gas_pocket` | Misthollow Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 55, 541 of 50000 left; argon_gas: richness 32, 49527 of 50000 left; plasma_gas: richness 22, 8079 of 10000 left; nebula_gas: richness 14, 9965 of 10000 left; neon_gas: richness 39, 49422 of 50000 left; chlorine_gas: richness 24, 565 of 10000 left; ion_gas: richness 23, 7266 of 10000 left; fluorine_gas: richness 23, 555 of 5000 left | none | 2026-11-17 08:44 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:44 UTC | own ship | Read Misthollow Belt: 49,199 units left in all | `get_poi`, own ship |
| 2026-11-17 08:44 UTC | own ship | Read Misthollow Gas Pocket: 125,920 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
