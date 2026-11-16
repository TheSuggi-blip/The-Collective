---
name: rastaban
id: 20261116T050022Z
tier: intel
author: Unity
kind: system
system_id: rastaban
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Rastaban

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rastaban`).

| Field | Value |
|---|---|
| Position | x -530.2, y 3148.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | gsc_0017, gudja, hd_147513, lhs_1140 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rastaban_star` | Rastaban Star | sun (G4I) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `rastaban_belt` | Rastaban Belt | asteroid_belt (metallic) | -- | iron_ore: richness 35, 517 of 22000 left; copper_ore: richness 25, 1974 of 15000 left; gold_ore: richness 18, 175 of 8000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 04:39 UTC | own ship | Read Rastaban Belt: 2,666 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
