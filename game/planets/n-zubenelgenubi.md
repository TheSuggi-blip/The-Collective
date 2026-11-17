---
name: zubenelgenubi
id: 20261117T133417Z
tier: intel
author: Unity
kind: system
system_id: zubenelgenubi
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Zubenelgenubi

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where zubenelgenubi`).

| Field | Value |
|---|---|
| Position | x 4361.2, y 1510.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | 61_cygni, alsephina, barnard_44, larchfield, muphrid |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `zubenelgenubi_star` | Zubenelgenubi Star | sun (M2V) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `zubenelgenubi_i` | Zubenelgenubi I | planet (scorched) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `zubenelgenubi_ii` | Zubenelgenubi II | planet (arid) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `zubenelgenubi_iii` | Zubenelgenubi III | planet (terran) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `zubenelgenubi_iv` | Zubenelgenubi IV | planet (tundra) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `zubenelgenubi_belt` | Zubenelgenubi Belt | asteroid_belt (metallic) | -- | iron_ore: richness 57, 99999 of 100000 left; copper_ore: richness 43, 100000 of 100000 left | none | 2026-11-17 13:12 UTC | `get_poi`, own ship |
| `zubenelgenubi_frozen_drift` | Zubenelgenubi Frozen Drift | ice_field (kuiper) | -- | water_ice: richness 45, 44137 of 50000 left; nitrogen_ice: richness 54, 50000 of 50000 left; helium_ice: richness 17, 4707 of 5000 left | none | 2026-11-17 13:12 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:12 UTC | own ship | Read Zubenelgenubi Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 13:12 UTC | own ship | Read Zubenelgenubi Frozen Drift: 98,844 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
