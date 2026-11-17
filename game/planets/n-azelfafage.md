---
name: azelfafage
id: 20261117T174216Z
tier: intel
author: Unity
kind: system
system_id: azelfafage
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Azelfafage

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where azelfafage`).

| Field | Value |
|---|---|
| Position | x -613.9, y -4949.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | 36_ophiuchi, acamar, gsc_0001, gsc_0005, highcrest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `azelfafage_star` | Azelfafage Star | sun (M2V) | -- | -- | none | 2026-11-17 16:41 UTC | `get_system`, own ship |
| `azelfafage_i` | Azelfafage I | planet (scorched) | -- | -- | none | 2026-11-17 16:41 UTC | `get_system`, own ship |
| `azelfafage_far_seam` | Azelfafage Far Seam | asteroid_belt (metallic) | -- | iron_ore: richness 40, 4270 of 30000 left; copper_ore: richness 20, 11088 of 15000 left; titanium_ore: richness 25, 21 of 15000 left | none | 2026-11-17 16:41 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:41 UTC | own ship | Read Azelfafage Far Seam: 15,379 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
