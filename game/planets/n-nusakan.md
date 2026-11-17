---
name: nusakan
id: 20261117T153750Z
tier: intel
author: Unity
kind: system
system_id: nusakan
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Nusakan

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nusakan`).

| Field | Value |
|---|---|
| Position | x 1909.5, y -5897.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | azmidi, naos, pollux, sadalmelik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nusakan_star` | Nusakan Star | sun (M4V) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_i` | Nusakan I | planet (scorched) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_ii` | Nusakan II | planet (arid) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_iii` | Nusakan III | planet (terran) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_iv` | Nusakan IV | planet (tundra) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_v` | Nusakan V | planet (jovian) | -- | -- | none | 2026-11-17 14:51 UTC | `get_system`, own ship |
| `nusakan_belt` | Nusakan Belt | asteroid_belt (metallic) | -- | iron_ore: richness 42, 99999 of 100000 left; copper_ore: richness 41, 100000 of 100000 left; silver_ore: richness 32, 544 of 25000 left | none | 2026-11-17 14:51 UTC | `get_poi`, own ship |
| `nusakan_frost_ring` | Nusakan Frost Ring | ice_field (kuiper) | -- | water_ice: richness 42, 40617 of 50000 left; carbon_dioxide_ice: richness 14, 6000 of 6000 left | none | 2026-11-17 14:51 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:51 UTC | own ship | Read Nusakan Belt: 200,543 units left in all | `get_poi`, own ship |
| 2026-11-17 14:51 UTC | own ship | Read Nusakan Frost Ring: 46,617 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
