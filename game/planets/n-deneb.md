---
name: deneb
id: 20261117T092723Z
tier: intel
author: Unity
kind: system
system_id: deneb
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Deneb

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where deneb`).

| Field | Value |
|---|---|
| Position | x 943.1, y 1358.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | harborlight, kapteyn_5, mira, misthollow, thabit |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `deneb_star` | Deneb Star | sun (K2V) | -- | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |
| `deneb_i` | Deneb I | planet (scorched) | -- | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |
| `deneb_ii` | Deneb II | planet (arid) | -- | -- | none | 2026-11-17 09:10 UTC | `get_system`, own ship |
| `deneb_belt` | Deneb Belt | asteroid_belt (metallic) | -- | iron_ore: richness 48, 99999 of 100000 left; copper_ore: richness 42, 100000 of 100000 left | none | 2026-11-17 09:10 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:10 UTC | own ship | Read Deneb Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
