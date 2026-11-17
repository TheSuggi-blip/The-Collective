---
name: mimosa
id: 20261117T102831Z
tier: intel
author: Unity
kind: system
system_id: mimosa
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Mimosa

Solarian system 12 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mimosa`).

| Field | Value |
|---|---|
| Position | x -636.9, y -1065.8 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 12 |
| Lanes | electra, miaplacidus, ross_154, tau_ceti |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mimosa_star` | Mimosa Star | sun (B1III) | -- | -- | none | 2026-11-17 10:18 UTC | `get_system`, own ship |
| `mimosa_i` | Mimosa I | planet (scorched) | -- | -- | none | 2026-11-17 10:18 UTC | `get_system`, own ship |
| `mimosa_ii` | Mimosa II | planet (scorched) | -- | -- | none | 2026-11-17 10:18 UTC | `get_system`, own ship |
| `mimosa_iii` | Mimosa III | planet (scorched) | -- | -- | none | 2026-11-17 10:18 UTC | `get_system`, own ship |
| `mimosa_cryobelt` | Mimosa Cryobelt | ice_field (kuiper) | -- | water_ice: richness 60, 20 of 50000 left; nitrogen_ice: richness 34, 46771 of 50000 left | none | 2026-11-17 10:18 UTC | `get_poi`, own ship |
| `volatile_pocket` | Volatile Pocket | asteroid_belt | -- | iron_ore: richness 42, 88991 of 100000 left; copper_ore: richness 33, 99706 of 100000 left; antimatter_containment_cell: richness 3, 152 of 271 left | none | 2026-11-17 10:18 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:18 UTC | own ship | Read Mimosa Cryobelt: 46,791 units left in all | `get_poi`, own ship |
| 2026-11-17 10:18 UTC | own ship | Read Volatile Pocket: 188,849 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
