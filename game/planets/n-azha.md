---
name: azha
id: 20261117T041723Z
tier: intel
author: Unity
kind: system
system_id: azha
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Azha

- system 9 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where azha`).

| Field | Value |
|---|---|
| Position | x -1298.9, y 4572.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 9 |
| Lanes | alderamin, groombridge_1618, gsc_0020, gsc_0024, hassaleh, jasmine, mirach |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `azha_star` | Azha Star | sun (K2III) | -- | -- | none | 2026-11-17 04:11 UTC | `get_system`, own ship |
| `azha_belt` | Azha Belt | asteroid_belt (metallic) | -- | iron_ore: richness 45, 1686 of 28000 left; copper_ore: richness 35, 3436 of 20000 left; nickel_ore: richness 20, 570 of 10000 left; chromium_ore: richness 18, 678 of 8000 left | none | 2026-11-17 04:11 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:11 UTC | own ship | Read Azha Belt: 6,370 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
