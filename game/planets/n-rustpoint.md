---
name: rustpoint
id: 20261117T123159Z
tier: intel
author: Unity
kind: system
system_id: rustpoint
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rustpoint

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rustpoint`).

| Field | Value |
|---|---|
| Position | x 6526.6, y 478.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | copperfield, toi_700 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rustpoint_star` | Rustpoint Star | sun (M4V) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rustpoint_i` | Rustpoint I | planet (scorched) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rustpoint_ii` | Rustpoint II | planet (arid) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rustpoint_iii` | Rustpoint III | planet (terran) | -- | -- | none | 2026-11-17 12:12 UTC | `get_system`, own ship |
| `rustpoint_belt` | Rustpoint Belt | asteroid_belt (metallic) | -- | iron_ore: richness 55, 99999 of 100000 left; copper_ore: richness 40, 100000 of 100000 left | none | 2026-11-17 12:12 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:12 UTC | own ship | Read Rustpoint Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
