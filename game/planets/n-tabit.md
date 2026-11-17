---
name: tabit
id: 20261117T153755Z
tier: intel
author: Unity
kind: system
system_id: tabit
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tabit

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tabit`).

| Field | Value |
|---|---|
| Position | x -5374.4, y -3653.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | ashenmoor, emberglow, willowgate, winterhold |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tabit_star` | Tabit Star | sun (F8V) | -- | -- | none | 2026-11-17 14:59 UTC | `get_system`, own ship |
| `tabit_i` | Tabit I | planet (scorched) | -- | -- | none | 2026-11-17 14:59 UTC | `get_system`, own ship |
| `tabit_ii` | Tabit II | planet (arid) | -- | -- | none | 2026-11-17 14:59 UTC | `get_system`, own ship |
| `tabit_iii` | Tabit III | planet (terran) | -- | -- | none | 2026-11-17 14:59 UTC | `get_system`, own ship |
| `tabit_cryobelt` | Tabit Cryobelt | ice_field (kuiper) | -- | nitrogen_ice: richness 48, 50000 of 50000 left | none | 2026-11-17 14:59 UTC | `get_poi`, own ship |
| `tabit_cobalt_shelf` | Tabit Cobalt Shelf | asteroid_belt | -- | iron_ore: richness 36, 98792 of 100000 left; copper_ore: richness 20, 99772 of 100000 left; cobalt_ore: richness 46, 270 of 25000 left | none | 2026-11-17 14:59 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:59 UTC | own ship | Read Tabit Cryobelt: 50,000 units left in all | `get_poi`, own ship |
| 2026-11-17 14:59 UTC | own ship | Read Tabit Cobalt Shelf: 198,834 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
