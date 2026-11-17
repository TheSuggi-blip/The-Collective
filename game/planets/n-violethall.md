---
name: violethall
id: 20261117T133412Z
tier: intel
author: Unity
kind: system
system_id: violethall
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Violethall

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where violethall`).

| Field | Value |
|---|---|
| Position | x 1439.5, y 6185.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | flintrock, gsc_0010 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `violethall_star` | Violethall Star | sun (M2V) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `violethall_i` | Violethall I | planet (scorched) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `violethall_ii` | Violethall II | planet (arid) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `violethall_belt` | Violethall Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 55332 of 100000 left; copper_ore: richness 28, 68861 of 100000 left | none | 2026-11-17 13:16 UTC | `get_poi`, own ship |
| `the_door` | The Door | relic (derelict) | -- | -- | none | 2026-11-17 13:16 UTC | `get_system`, own ship |
| `violethall_gas_plume` | Violethall Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 66, 18619 of 50000 left; argon_gas: richness 49, 48541 of 50000 left; plasma_gas: richness 24, 9837 of 10000 left; xenon_gas: richness 20, 9933 of 10000 left; nebula_gas: richness 19, 9855 of 10000 left; ion_gas: richness 33, 2760 of 10000 left | none | 2026-11-17 13:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:16 UTC | own ship | Read Violethall Belt: 124,193 units left in all | `get_poi`, own ship |
| 2026-11-17 13:16 UTC | own ship | Read Violethall Gas Plume: 99,545 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
