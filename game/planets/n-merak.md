---
name: merak
id: 20261117T102828Z
tier: intel
author: Unity
kind: system
system_id: merak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Merak

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where merak`).

| Field | Value |
|---|---|
| Position | x -3945.3, y -1256.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | alathfar, alsciaukat, hollowcrest, merope, sheliak, titawin, zubenelhakrabi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `merak_star` | Merak Star | sun (M2V) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `merak_i` | Merak I | planet (scorched) | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |
| `merak_belt_a` | Merak Belt A | asteroid_belt (metallic) | -- | iron_ore: richness 49, 99998 of 100000 left; copper_ore: richness 36, 99999 of 100000 left | none | 2026-11-17 10:14 UTC | `get_poi`, own ship |
| `merak_belt_b` | Merak Belt B | asteroid_belt (metallic) | -- | iron_ore: richness 53, 100000 of 100000 left; copper_ore: richness 46, 100000 of 100000 left | none | 2026-11-17 10:14 UTC | `get_poi`, own ship |
| `merak_ice_belt` | Merak Ice Belt | ice_field (kuiper) | -- | water_ice: richness 57, 26621 of 50000 left; nitrogen_ice: richness 37, 50000 of 50000 left | none | 2026-11-17 10:14 UTC | `get_poi`, own ship |
| `merak_dim_phase_pocket` | Merak Dim Phase Pocket | nebula | -- | -- | none | 2026-11-17 10:14 UTC | `get_system`, own ship |

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
| 2026-11-17 10:14 UTC | own ship | Read Merak Belt A: 199,997 units left in all | `get_poi`, own ship |
| 2026-11-17 10:14 UTC | own ship | Read Merak Belt B: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 10:14 UTC | own ship | Read Merak Ice Belt: 76,621 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
