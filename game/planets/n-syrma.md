---
name: syrma
id: 20261117T133407Z
tier: intel
author: Unity
kind: system
system_id: syrma
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Syrma

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where syrma`).

| Field | Value |
|---|---|
| Position | x 2262.1, y 799.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | ascella, hr_8832, propus, spica |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `syrma_star` | Syrma Star | sun (M2V) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `syrma_i` | Syrma I | planet (scorched) | -- | -- | none | 2026-11-17 12:41 UTC | `get_system`, own ship |
| `syrma_belt` | Syrma Belt | asteroid_belt (metallic) | -- | iron_ore: richness 51, 43158 of 100000 left; copper_ore: richness 33, 100000 of 100000 left | none | 2026-11-17 12:41 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:41 UTC | own ship | Read Syrma Belt: 143,158 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
