---
name: electra
id: 20261117T112928Z
tier: intel
author: Unity
kind: system
system_id: electra
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Electra

Solarian system 13 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where electra`).

| Field | Value |
|---|---|
| Position | x -422.9, y -973.2 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 13 |
| Lanes | mimosa, ross_154, tau_ceti, timberline |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `electra_star` | Electra Star | sun (B6III) | -- | -- | none | 2026-11-17 11:18 UTC | `get_system`, own ship |
| `electra_i` | Electra I | planet (scorched) | -- | -- | none | 2026-11-17 11:18 UTC | `get_system`, own ship |
| `electra_ii` | Electra II | planet (scorched) | -- | -- | none | 2026-11-17 11:18 UTC | `get_system`, own ship |
| `electra_iii` | Electra III | planet (scorched) | -- | -- | none | 2026-11-17 11:18 UTC | `get_system`, own ship |
| `main_belt_echo` | Main Belt Echo | asteroid_belt | -- | iron_ore: richness 35, 100000 of 100000 left; copper_ore: richness 20, 100000 of 100000 left; sol_alloy_ore: richness 7, 2224 of 2224 left | none | 2026-11-17 11:18 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 11:18 UTC | own ship | Read Main Belt Echo: 202,224 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
