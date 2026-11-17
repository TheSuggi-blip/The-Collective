---
name: ravenspire
id: 20261117T194616Z
tier: intel
author: Unity
kind: system
system_id: ravenspire
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ravenspire

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ravenspire`).

| Field | Value |
|---|---|
| Position | x 3304.2, y 204.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | alnitak, gliese_229, seginus, whitecliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ravenspire_star` | Ravenspire Star | sun (M2V) | -- | -- | none | 2026-11-17 18:54 UTC | `get_system`, own ship |
| `ravenspire_belt` | Ravenspire Belt | asteroid_belt (metallic) | -- | iron_ore: richness 49, 99999 of 100000 left; copper_ore: richness 49, 100000 of 100000 left; aluminum_ore: richness 54, 538 of 30000 left | none | 2026-11-17 18:54 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:54 UTC | own ship | Read Ravenspire Belt: 200,537 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
