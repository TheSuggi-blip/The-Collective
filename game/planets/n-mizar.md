---
name: mizar
id: 20261117T010829Z
tier: intel
author: Unity
kind: system
system_id: mizar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mizar

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mizar`).

| Field | Value |
|---|---|
| Position | x -4886.0, y 293.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | clearwater, rasalhague, saltwind, tania, yildun |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mizar_star` | Mizar Star | sun (M4V) | -- | -- | none | 2026-11-17 00:46 UTC | `get_system`, own ship |
| `mizar_belt` | Mizar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 37, 99999 of 100000 left; copper_ore: richness 22, 100000 of 100000 left; manganese_ore: richness 19, 12000 of 12000 left | none | 2026-11-17 00:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 00:46 UTC | own ship | Read Mizar Belt: 211,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
