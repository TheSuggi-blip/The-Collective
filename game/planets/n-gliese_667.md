---
name: gliese_667
id: 20261117T143534Z
tier: intel
author: Unity
kind: system
system_id: gliese_667
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Gliese 667

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gliese_667`).

| Field | Value |
|---|---|
| Position | x 455.4, y -6743.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | gsc_0025, menkalinan, poerava, sadalbari |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gliese_667_star` | Gliese 667 Star | sun (M2V) | -- | -- | none | 2026-11-17 14:02 UTC | `get_system`, own ship |
| `gliese_667_i` | Gliese 667 I | planet (scorched) | -- | -- | none | 2026-11-17 14:02 UTC | `get_system`, own ship |
| `gliese_667_rutile_shoal` | Gliese 667 Rutile Shoal | asteroid_belt (metallic) | -- | iron_ore: richness 40, 6928 of 30000 left; copper_ore: richness 20, 12923 of 15000 left; titanium_ore: richness 25, 60 of 15000 left | none | 2026-11-17 14:02 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:02 UTC | own ship | Read Gliese 667 Rutile Shoal: 19,911 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
