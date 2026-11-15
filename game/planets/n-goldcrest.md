---
name: goldcrest
id: 20261115T235517Z
tier: intel
author: Unity
kind: system
system_id: goldcrest
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Goldcrest

- system 7 jumps from home, police level 0. Station: Ironlight Verdigris Range, Ironlight Ferrous Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where goldcrest`).

| Field | Value |
|---|---|
| Position | x -612.9, y 2168.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | bluerift, deepwell, gemma, gsc_0017, gsc_0033, lhs_1140 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `goldcrest_star` | Goldcrest Star | sun (M4V) | -- | -- | none | 2026-11-15 23:35 UTC | `get_system`, own ship |
| `goldcrest_belt` | Goldcrest Belt | asteroid_belt (metallic) | -- | iron_ore: richness 36, 96597 of 100000 left; copper_ore: richness 43, 79589 of 100000 left | none | 2026-11-15 23:35 UTC | `get_poi`, own ship |
| `the_gold_crest` | The Gold Crest | asteroid_belt (metallic) | -- | gold_ore: richness 85, 13667 of 150000 left | none | 2026-11-15 23:35 UTC | `get_poi`, own ship |
| `glitterback_scatter` | Glitterback Scatter | asteroid_belt | -- | iron_ore: richness 32, 100000 of 100000 left; copper_ore: richness 32, 100000 of 100000 left; sol_alloy_ore: richness 4, 1546 of 1547 left | none | 2026-11-15 23:35 UTC | `get_poi`, own ship |
| `6502095215168cbf8b1bddf5dca2245a` | Ironlight Verdigris Range | station | `319786a992e4389bfe39b49777feb7ad` | -- | none | 2026-11-15 23:35 UTC | `get_system`, own ship |
| `b222887f5d48d77e119dd2ceafbbf08e` | Ironlight Ferrous Range | station | `17becbe9f88e6ad8efb2cc1c0785485a` | -- | none | 2026-11-15 23:35 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ironlight Verdigris Range (`319786a992e4389bfe39b49777feb7ad`) | unknown | not tried | not read | unknown | unknown | 2026-11-15 23:35 UTC | `get_system`, own ship |
| Ironlight Ferrous Range (`17becbe9f88e6ad8efb2cc1c0785485a`) | unknown | not tried | not read | unknown | unknown | 2026-11-15 23:35 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 23:35 UTC | own ship | Read Goldcrest Belt: 176,186 units left in all | `get_poi`, own ship |
| 2026-11-15 23:35 UTC | own ship | Read The Gold Crest: 13,667 units left in all | `get_poi`, own ship |
| 2026-11-15 23:35 UTC | own ship | Read Glitterback Scatter: 201,546 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
