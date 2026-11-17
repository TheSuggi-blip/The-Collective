---
name: ogma
id: 20261117T174152Z
tier: intel
author: Unity
kind: system
system_id: ogma
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: nebula
police_level: 30
updated: 2026-11-17
---

# Ogma

Nebula system 21 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ogma`).

| Field | Value |
|---|---|
| Position | x 961.9, y -4861.7 (Galactic Units) |
| Empire | nebula |
| Jumps from home | 21 |
| Lanes | caph, gliese_436, the_levy, traders_rest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ogma_star` | Ogma Star | sun (K3V) | -- | -- | none | 2026-11-17 17:39 UTC | `get_system`, own ship |
| `ogma_i` | Ogma I | planet (arid) | -- | -- | none | 2026-11-17 17:39 UTC | `get_system`, own ship |
| `ogma_ii` | Ogma II | planet (tundra) | -- | -- | none | 2026-11-17 17:39 UTC | `get_system`, own ship |
| `ogma_belt` | Ogma Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 58, 336 of 30000 left; vanadium_ore: richness 43, 185 of 25000 left; tungsten_ore: richness 31, 204 of 25000 left; aluminum_ore: richness 54, 350 of 30000 left; prismatic_nebulite: richness 5, 250 of 250 left | none | 2026-11-17 17:39 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 17:39 UTC | own ship | Read Ogma Belt: 1,325 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
