---
name: groombridge_34
id: 20261117T000624Z
tier: intel
author: Unity
kind: system
system_id: groombridge_34
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Groombridge 34

- system 8 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where groombridge_34`).

| Field | Value |
|---|---|
| Position | x -5077.3, y 1579.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 8 |
| Lanes | chalawan, innes_40, regor |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `groombridge_34_star` | Groombridge 34 Star | sun (K6V) | -- | -- | none | 2026-11-16 23:40 UTC | `get_system`, own ship |
| `groombridge_34_i` | Groombridge 34 I | planet (scorched) | -- | -- | none | 2026-11-16 23:40 UTC | `get_system`, own ship |
| `groombridge_34_belt` | Groombridge 34 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 32, 99999 of 100000 left; copper_ore: richness 34, 100000 of 100000 left | none | 2026-11-16 23:40 UTC | `get_poi`, own ship |
| `groombridge_34_ice_fields` | Groombridge 34 Ice Fields | ice_field (cometary) | -- | water_ice: richness 52, 42817 of 50000 left; nitrogen_ice: richness 47, 50000 of 50000 left; deuterium_ice: richness 13, 5000 of 5000 left; helium_ice: richness 23, 3855 of 5000 left | none | 2026-11-16 23:40 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:40 UTC | own ship | Read Groombridge 34 Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-16 23:40 UTC | own ship | Read Groombridge 34 Ice Fields: 101,672 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
