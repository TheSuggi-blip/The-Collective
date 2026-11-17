---
name: ravensbrook
id: 20261117T163944Z
tier: intel
author: Unity
kind: system
system_id: ravensbrook
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ravensbrook

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ravensbrook`).

| Field | Value |
|---|---|
| Position | x 3494.4, y -5043.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | 55_cancri, alrescha, ashford, cursa, moonshadow, ross_128, tarf |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ravensbrook_star` | Ravensbrook Star | sun (G5V) | -- | -- | none | 2026-11-17 16:07 UTC | `get_system`, own ship |
| `ravensbrook_belt` | Ravensbrook Belt | asteroid_belt (mixed) | -- | iron_ore: richness 40, 92 of 24000 left; copper_ore: richness 28, 1018 of 16000 left | none | 2026-11-17 16:07 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:07 UTC | own ship | Read Ravensbrook Belt: 1,110 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
