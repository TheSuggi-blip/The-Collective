---
name: garnet
id: 20261115T215319Z
tier: intel
author: Unity
kind: system
system_id: garnet
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Garnet

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where garnet`).

| Field | Value |
|---|---|
| Position | x -2477.6, y 1335.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | achernar, atlas, cedarhold, hd_40307, ruchbah |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `garnet_star` | Garnet Star | sun (M4V) | -- | -- | none | 2026-11-15 21:23 UTC | `get_system`, own ship |
| `garnet_i` | Garnet I | planet (scorched) | -- | -- | none | 2026-11-15 21:23 UTC | `get_system`, own ship |
| `garnet_ii` | Garnet II | planet (arid) | -- | -- | none | 2026-11-15 21:23 UTC | `get_system`, own ship |
| `garnet_iii` | Garnet III | planet (terran) | -- | -- | none | 2026-11-15 21:23 UTC | `get_system`, own ship |
| `garnet_belt` | Garnet Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 100000 of 100000 left; copper_ore: richness 22, 100000 of 100000 left; gold_ore: richness 38, 10 of 25000 left | none | 2026-11-15 21:23 UTC | `get_poi`, own ship |
| `garnet_dim_lattice` | Garnet Dim Lattice | nebula | -- | -- | none | 2026-11-15 21:23 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 21:23 UTC | own ship | Read Garnet Belt: 200,010 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
