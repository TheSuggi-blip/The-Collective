---
name: larchfield
id: 20261117T153743Z
tier: intel
author: Unity
kind: system
system_id: larchfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Larchfield

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where larchfield`).

| Field | Value |
|---|---|
| Position | x 3695.6, y 1170.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | 61_cygni, sargas, zubenelgenubi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `larchfield_star` | Larchfield Star | sun (G8V) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `larchfield_i` | Larchfield I | planet (scorched) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `larchfield_ii` | Larchfield II | planet (arid) | -- | -- | none | 2026-11-17 14:46 UTC | `get_system`, own ship |
| `larchfield_belt` | Larchfield Belt | asteroid_belt (metallic) | -- | iron_ore: richness 57, 99999 of 100000 left; copper_ore: richness 33, 100000 of 100000 left | none | 2026-11-17 14:46 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:46 UTC | own ship | Read Larchfield Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
