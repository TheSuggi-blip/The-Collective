---
name: errai
id: 20261117T123138Z
tier: intel
author: Unity
kind: system
system_id: errai
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Errai

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where errai`).

| Field | Value |
|---|---|
| Position | x -4516.1, y -2243.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | alsciaukat, brightfall, fang, gsc_0046, tarazed, wezen |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `errai_star` | Errai Star | sun (K6V) | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |
| `errai_i` | Errai I | planet (scorched) | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |
| `errai_belt` | Errai Belt | asteroid_belt (metallic) | -- | iron_ore: richness 57, 99968 of 100000 left; copper_ore: richness 27, 99999 of 100000 left; silver_ore: richness 30, 284 of 25000 left | none | 2026-11-17 12:13 UTC | `get_poi`, own ship |
| `errai_gas_plume` | Errai Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 59, 10115 of 50000 left; argon_gas: richness 35, 49999 of 50000 left; nebula_gas: richness 27, 10000 of 10000 left; neon_gas: richness 48, 50000 of 50000 left; ion_gas: richness 34, 6971 of 10000 left | none | 2026-11-17 12:13 UTC | `get_poi`, own ship |
| `errai_faint_entanglement` | Errai Faint Entanglement | nebula | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |

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
| 2026-11-17 12:13 UTC | own ship | Read Errai Belt: 200,251 units left in all | `get_poi`, own ship |
| 2026-11-17 12:13 UTC | own ship | Read Errai Gas Plume: 127,085 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
