---
name: miaplacidus
id: 20261117T102830Z
tier: intel
author: Unity
kind: system
system_id: miaplacidus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Miaplacidus

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where miaplacidus`).

| Field | Value |
|---|---|
| Position | x -1061.6, y -1570.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | cervantes, maplevale, mimosa |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `miaplacidus_star` | Miaplacidus Star | sun (K2V) | -- | -- | none | 2026-11-17 09:32 UTC | `get_system`, own ship |
| `miaplacidus_i` | Miaplacidus I | planet (scorched) | -- | -- | none | 2026-11-17 09:32 UTC | `get_system`, own ship |
| `miaplacidus_ii` | Miaplacidus II | planet (arid) | -- | -- | none | 2026-11-17 09:32 UTC | `get_system`, own ship |
| `miaplacidus_iii` | Miaplacidus III | planet (terran) | -- | -- | none | 2026-11-17 09:32 UTC | `get_system`, own ship |
| `miaplacidus_frost_ring` | Miaplacidus Frost Ring | ice_field (kuiper) | -- | water_ice: richness 40, 37171 of 50000 left; nitrogen_ice: richness 54, 50000 of 50000 left | none | 2026-11-17 09:32 UTC | `get_poi`, own ship |
| `miaplacidus_alloy_remnants` | Miaplacidus Alloy Remnants | asteroid_belt | -- | iron_ore: richness 39, 99885 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; sol_alloy_ore: richness 5, 601 of 1642 left | none | 2026-11-17 09:32 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:32 UTC | own ship | Read Miaplacidus Frost Ring: 87,171 units left in all | `get_poi`, own ship |
| 2026-11-17 09:32 UTC | own ship | Read Miaplacidus Alloy Remnants: 200,486 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
