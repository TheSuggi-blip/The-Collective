---
name: whitecliff
id: 20261117T133413Z
tier: intel
author: Unity
kind: system
system_id: whitecliff
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Whitecliff

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where whitecliff`).

| Field | Value |
|---|---|
| Position | x 3417.2, y 29.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | alnitak, gliese_229, ravenspire, seginus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `whitecliff_star` | Whitecliff Star | sun (K2V) | -- | -- | none | 2026-11-17 13:04 UTC | `get_system`, own ship |
| `whitecliff_i` | Whitecliff I | planet (scorched) | -- | -- | none | 2026-11-17 13:04 UTC | `get_system`, own ship |
| `whitecliff_ii` | Whitecliff II | planet (arid) | -- | -- | none | 2026-11-17 13:04 UTC | `get_system`, own ship |
| `whitecliff_belt` | Whitecliff Belt | asteroid_belt (metallic) | -- | iron_ore: richness 65, 78195 of 100000 left; copper_ore: richness 48, 100000 of 100000 left; aluminum_ore: richness 56, 1693 of 30000 left; manganese_ore: richness 20, 597 of 12000 left | none | 2026-11-17 13:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:04 UTC | own ship | Read Whitecliff Belt: 180,485 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
