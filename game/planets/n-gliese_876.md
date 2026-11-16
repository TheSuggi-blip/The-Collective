---
name: gliese_876
id: 20261116T050019Z
tier: intel
author: Unity
kind: system
system_id: gliese_876
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Gliese 876

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gliese_876`).

| Field | Value |
|---|---|
| Position | x -2221.0, y 4464.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | biham, felis, gsc_0021, gsc_0024, gsc_0035, jasmine |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gliese_876_star` | Gliese 876 Star | sun (M4V) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `gliese_876_d` | Gliese 876 d | planet (scorched) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `gliese_876_bc` | Gliese 876 b/c | planet (jovian) | -- | -- | none | 2026-11-16 04:39 UTC | `get_system`, own ship |
| `gliese_876_belt` | Gliese 876 Belt | asteroid_belt (mixed) | -- | iron_ore: richness 45, 3197 of 30000 left; carbon_ore: richness 30, 2830 of 18000 left; nickel_ore: richness 20, 618 of 12000 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |
| `stillwork_belt` | Stillwork Belt | asteroid_belt | -- | iron_ore: richness 37, 100000 of 100000 left; copper_ore: richness 20, 100000 of 100000 left; null_matter: richness 13, 606 of 606 left | none | 2026-11-16 04:39 UTC | `get_poi`, own ship |

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
| 2026-11-16 04:39 UTC | own ship | Read Gliese 876 Belt: 6,645 units left in all | `get_poi`, own ship |
| 2026-11-16 04:39 UTC | own ship | Read Stillwork Belt: 200,606 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
