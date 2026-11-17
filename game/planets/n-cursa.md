---
name: cursa
id: 20261117T163928Z
tier: intel
author: Unity
kind: system
system_id: cursa
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Cursa

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where cursa`).

| Field | Value |
|---|---|
| Position | x 3862.3, y -4401.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | alrescha, farpoint, ravensbrook, tarf |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `cursa_star` | Cursa Star | sun (K2V) | -- | -- | none | 2026-11-17 16:10 UTC | `get_system`, own ship |
| `cursa_i` | Cursa I | planet (scorched) | -- | -- | none | 2026-11-17 16:10 UTC | `get_system`, own ship |
| `cursa_belt` | Cursa Belt | asteroid_belt (metallic) | -- | iron_ore: richness 56, 99999 of 100000 left; copper_ore: richness 35, 100000 of 100000 left | none | 2026-11-17 16:10 UTC | `get_poi`, own ship |
| `cursa_ice_belt` | Cursa Ice Belt | ice_field (cometary) | -- | water_ice: richness 55, 1659 of 50000 left; nitrogen_ice: richness 43, 1654 of 50000 left; deuterium_ice: richness 17, 571 of 5000 left | none | 2026-11-17 16:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:10 UTC | own ship | Read Cursa Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 16:10 UTC | own ship | Read Cursa Ice Belt: 3,884 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
