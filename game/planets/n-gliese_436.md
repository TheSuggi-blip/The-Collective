---
name: gliese_436
id: 20261117T153735Z
tier: intel
author: Unity
kind: system
system_id: gliese_436
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 55
updated: 2026-11-17
---

# Gliese 436

Nebula system 21 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where gliese_436`).

| Field | Value |
|---|---|
| Position | x 1089.0, y -5151.2 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 21 |
| Lanes | caph, khambalia, ogma, the_levy, traders_rest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `gliese_436_star` | Gliese 436 Star | sun (M2V) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `gliese_436_i` | Gliese 436 I | planet (scorched) | -- | -- | none | 2026-11-17 14:41 UTC | `get_system`, own ship |
| `gliese_436_belt` | Gliese 436 Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 42, 89 of 30000 left; platinum_ore: richness 19, 24 of 8000 left; iridium_ore: richness 18, 1 of 5000 left; thorium_ore: richness 19, 0 of 5000 left; gold_ore: richness 29, 24 of 25000 left; osmium_ore: richness 12, 42 of 3500 left | none | 2026-11-17 14:41 UTC | `get_poi`, own ship |
| `gliese_436_gas_cloud` | Gliese 436 Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 41, 523 of 50000 left; argon_gas: richness 47, 524 of 50000 left; xenon_gas: richness 21, 344 of 10000 left | none | 2026-11-17 14:41 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 14:41 UTC | own ship | Read Gliese 436 Belt: 180 units left in all | `get_poi`, own ship |
| 2026-11-17 14:41 UTC | own ship | Read Gliese 436 Gas Cloud: 1,391 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
