---
name: grumium
id: 20261117T051922Z
tier: intel
author: Unity
kind: system
system_id: grumium
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: solarian
police_level: 30
updated: 2026-11-17
---

# Grumium

Solarian system 9 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where grumium`).

| Field | Value |
|---|---|
| Position | x -1206.1, y -380.2 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | celaeno, lacaille_9352, lanternwick, ridgecrest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `grumium_star` | Grumium Star | sun (K2III) | -- | -- | none | 2026-11-17 04:33 UTC | `get_system`, own ship |
| `grumium_i` | Grumium I | planet (scorched) | -- | -- | none | 2026-11-17 04:33 UTC | `get_system`, own ship |
| `grumium_ii` | Grumium II | planet (arid) | -- | -- | none | 2026-11-17 04:33 UTC | `get_system`, own ship |
| `grumium_iii` | Grumium III | planet (tundra) | -- | -- | none | 2026-11-17 04:33 UTC | `get_system`, own ship |
| `grumium_belt` | Grumium Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 51, 464 of 30000 left; tungsten_ore: richness 27, 346 of 25000 left; palladium_ore: richness 15, 208 of 5000 left; aluminum_ore: richness 58, 488 of 30000 left; legacy_ore: richness 4, 250 of 250 left | none | 2026-11-17 04:33 UTC | `get_poi`, own ship |

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
| 2026-11-17 04:33 UTC | own ship | Read Grumium Belt: 1,756 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
