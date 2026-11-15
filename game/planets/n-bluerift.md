---
name: bluerift
id: 20261115T235514Z
tier: intel
author: Unity
kind: system
system_id: bluerift
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Bluerift

- system 7 jumps from home, police level 0. Station: Ironlight Rime Range.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where bluerift`).

| Field | Value |
|---|---|
| Position | x -919.4, y 1674.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | deepwell, goldcrest, gsc_0033, homam, nihal |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `bluerift_star` | Bluerift Star | sun (G5V) | -- | -- | none | 2026-11-15 23:48 UTC | `get_system`, own ship |
| `bluerift_frost_ring` | Bluerift Frost Ring | ice_field (kuiper) | -- | nitrogen_ice: richness 49, 50000 of 50000 left | none | 2026-11-15 23:48 UTC | `get_poi`, own ship |
| `bluerift_fading_signal` | Bluerift Fading Signal | asteroid_belt | -- | iron_ore: richness 29, 5187 of 100000 left; copper_ore: richness 28, 20059 of 100000 left; antimatter_containment_cell: richness 2, 7 of 157 left | none | 2026-11-15 23:48 UTC | `get_poi`, own ship |
| `gaugewatch_belt` | Gaugewatch Belt | asteroid_belt | -- | iron_ore: richness 27, 61725 of 100000 left; copper_ore: richness 33, 100000 of 100000 left; null_matter: richness 12, 559 of 641 left | none | 2026-11-15 23:48 UTC | `get_poi`, own ship |
| `sys_0141_poi_0` | Arcturus Prime | sun | -- | -- | none | 2026-11-15 23:48 UTC | `get_system`, own ship |
| `6a887f744385ce938f601778c5b3ae61` | Ironlight Rime Range | station | `a5705e223b88926b9f55c18ee0f44e6e` | -- | none | 2026-11-15 23:48 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Ironlight Rime Range (`a5705e223b88926b9f55c18ee0f44e6e`) | unknown | not tried | not read | unknown | unknown | 2026-11-15 23:48 UTC | `get_system`, own ship |

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
| 2026-11-15 23:48 UTC | own ship | Read Bluerift Frost Ring: 50,000 units left in all | `get_poi`, own ship |
| 2026-11-15 23:48 UTC | own ship | Read Bluerift Fading Signal: 25,253 units left in all | `get_poi`, own ship |
| 2026-11-15 23:48 UTC | own ship | Read Gaugewatch Belt: 162,284 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
