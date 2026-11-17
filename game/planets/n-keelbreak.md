---
name: keelbreak
id: 20261117T143544Z
tier: intel
author: Unity
kind: system
system_id: keelbreak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Keelbreak

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where keelbreak`).

| Field | Value |
|---|---|
| Position | x 962.8, y -3239.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | copernicus, gsc_0030, xihe, zibal |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `keelbreak_star` | Keelbreak Star | sun (K2III) | -- | -- | none | 2026-11-17 14:01 UTC | `get_system`, own ship |
| `keelbreak_i` | Keelbreak I | planet (scorched) | -- | -- | none | 2026-11-17 14:01 UTC | `get_system`, own ship |
| `unassessed_seam` | Unassessed Seam | asteroid_belt | -- | iron_ore: richness 45, 72008 of 100000 left; copper_ore: richness 24, 100000 of 100000 left; trade_crystal: richness 18, 25 of 2400 left | none | 2026-11-17 14:01 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:01 UTC | own ship | Read Unassessed Seam: 172,033 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
