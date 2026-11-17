---
name: dabih
id: 20261117T163929Z
tier: intel
author: Unity
kind: system
system_id: dabih
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Dabih

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where dabih`).

| Field | Value |
|---|---|
| Position | x -6592.7, y -2213.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | gsc_0002, gsc_0045, rimegate, tejat |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `dabih_star` | Dabih Star | sun (K2V) | -- | -- | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_i` | Dabih I | planet (scorched) | -- | -- | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_ii` | Dabih II | planet (arid) | -- | -- | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_iii` | Dabih III | planet (terran) | -- | -- | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_iv` | Dabih IV | planet (tundra) | -- | -- | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_belt` | Dabih Belt | asteroid_belt (metallic) | -- | iron_ore: richness 58, 99583 of 100000 left; copper_ore: richness 33, 99969 of 100000 left; aluminum_ore: richness 67, 13255 of 30000 left | none | 2026-11-17 16:21 UTC | `get_poi`, own ship |
| `dabih_gas_plume` | Dabih Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 16:21 UTC | `get_system`, own ship |
| `dabih_frost_ring` | Dabih Frost Ring | ice_field (kuiper) | -- | not read | none | 2026-11-17 16:21 UTC | `get_system`, own ship |

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
| 2026-11-17 16:21 UTC | own ship | Read Dabih Belt: 212,807 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `dabih_gas_plume`, `dabih_frost_ring`.
