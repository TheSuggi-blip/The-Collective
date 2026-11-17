---
name: ashmark
id: 20261117T133330Z
tier: intel
author: Unity
kind: system
system_id: ashmark
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ashmark

- system 29 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ashmark`).

| Field | Value |
|---|---|
| Position | x 5151.8, y -4925.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 29 |
| Lanes | castula, luyten_789, mekbuda |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ashmark_star` | Ashmark Star | sun (K6V) | -- | -- | none | 2026-11-17 13:20 UTC | `get_system`, own ship |
| `ashmark_i` | Ashmark I | planet (scorched) | -- | -- | none | 2026-11-17 13:20 UTC | `get_system`, own ship |
| `ashmark_ii` | Ashmark II | planet (arid) | -- | -- | none | 2026-11-17 13:20 UTC | `get_system`, own ship |
| `ashmark_iron_ti_reef` | Ashmark Iron-Ti Reef | asteroid_belt | -- | iron_ore: richness 36, 99615 of 100000 left; copper_ore: richness 23, 99923 of 100000 left; titanium_ore: richness 40, 9 of 25000 left; chromium_ore: richness 16, 932 of 7000 left | none | 2026-11-17 13:20 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:20 UTC | own ship | Read Ashmark Iron-Ti Reef: 200,479 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
