---
name: tidewater
id: 20261117T133409Z
tier: intel
author: Unity
kind: system
system_id: tidewater
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tidewater

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tidewater`).

| Field | Value |
|---|---|
| Position | x -3592.9, y -2144.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | fang, gsc_0046, izar, last_light, sabik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tidewater_star` | Tidewater Star | sun (M4V) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `tidewater_i` | Tidewater I | planet (scorched) | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |
| `tidewater_belt` | Tidewater Belt | asteroid_belt (metallic) | -- | iron_ore: richness 50, 12309 of 100000 left; copper_ore: richness 47, 99999 of 100000 left | none | 2026-11-17 12:46 UTC | `get_poi`, own ship |
| `tidewater_emission_nebula` | Tidewater Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 67, 1169 of 50000 left; nebula_gas: richness 19, 9127 of 10000 left; neon_gas: richness 38, 47633 of 50000 left; chlorine_gas: richness 58, 649 of 10000 left | none | 2026-11-17 12:46 UTC | `get_poi`, own ship |
| `thin_breath_haze` | Thin Breath Haze | nebula | -- | -- | none | 2026-11-17 12:46 UTC | `get_system`, own ship |

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
| 2026-11-17 12:46 UTC | own ship | Read Tidewater Belt: 112,308 units left in all | `get_poi`, own ship |
| 2026-11-17 12:46 UTC | own ship | Read Tidewater Emission Nebula: 58,578 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
