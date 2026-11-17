---
name: veritate
id: 20261117T163953Z
tier: intel
author: Unity
kind: system
system_id: veritate
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Veritate

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where veritate`).

| Field | Value |
|---|---|
| Position | x -6106.8, y -3192.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | betelgeuse, gsc_0037, rimegate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `veritate_belt` | Veritate Belt | asteroid_belt (metallic) | -- | iron_ore: richness 69, 99999 of 100000 left; copper_ore: richness 21, 100000 of 100000 left | none | 2026-11-17 16:16 UTC | `get_poi`, own ship |
| `veritate_emission_nebula` | Veritate Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 41, 49423 of 50000 left; argon_gas: richness 31, 49999 of 50000 left; xenon_gas: richness 25, 9730 of 10000 left; nebula_gas: richness 27, 8950 of 10000 left; neon_gas: richness 48, 50000 of 50000 left; chlorine_gas: richness 34, 1976 of 10000 left | none | 2026-11-17 16:16 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:16 UTC | own ship | Read Veritate Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 16:16 UTC | own ship | Read Veritate Emission Nebula: 170,078 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
