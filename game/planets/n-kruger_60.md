---
name: kruger_60
id: 20261117T184410Z
tier: intel
author: Unity
kind: system
system_id: kruger_60
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kruger 60

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kruger_60`).

| Field | Value |
|---|---|
| Position | x 2585.9, y -934.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | alnitak, bramblewood, ross_248, struve_1321, zenithfall |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kruger_60_star` | Kruger 60 Star | sun (M4V) | -- | -- | none | 2026-11-17 18:02 UTC | `get_system`, own ship |
| `kruger_60_i` | Kruger 60 I | planet (scorched) | -- | -- | none | 2026-11-17 18:02 UTC | `get_system`, own ship |
| `kruger_60_ii` | Kruger 60 II | planet (arid) | -- | -- | none | 2026-11-17 18:02 UTC | `get_system`, own ship |
| `kruger_60_belt` | Kruger 60 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 46, 99326 of 100000 left; copper_ore: richness 46, 99731 of 100000 left; silver_ore: richness 28, 25 of 25000 left | none | 2026-11-17 18:02 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:02 UTC | own ship | Read Kruger 60 Belt: 199,082 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
