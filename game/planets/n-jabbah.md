---
name: jabbah
id: 20261117T143543Z
tier: intel
author: Unity
kind: system
system_id: jabbah
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Jabbah

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where jabbah`).

| Field | Value |
|---|---|
| Position | x 5411.4, y -1811.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | daybreak, gsc_0047, lalande_21185, vega, zubeneschamali |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `jabbah_star` | Jabbah Star | sun (M4V) | -- | -- | none | 2026-11-17 14:06 UTC | `get_system`, own ship |
| `jabbah_i` | Jabbah I | planet (scorched) | -- | -- | none | 2026-11-17 14:06 UTC | `get_system`, own ship |
| `jabbah_belt` | Jabbah Belt | asteroid_belt (metallic) | -- | iron_ore: richness 44, 100000 of 100000 left; copper_ore: richness 24, 100000 of 100000 left | none | 2026-11-17 14:06 UTC | `get_poi`, own ship |
| `jabbah_gas_cloud` | Jabbah Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 69, 298 of 50000 left; argon_gas: richness 47, 294 of 50000 left; plasma_gas: richness 26, 298 of 10000 left; nebula_gas: richness 18, 462 of 10000 left; chlorine_gas: richness 34, 295 of 10000 left; fluorine_gas: richness 17, 516 of 5000 left | none | 2026-11-17 14:06 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:06 UTC | own ship | Read Jabbah Belt: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 14:06 UTC | own ship | Read Jabbah Gas Cloud: 2,163 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
