---
name: beid
id: 20261117T184421Z
tier: intel
author: Unity
kind: system
system_id: beid
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Beid

- system 20 jumps from home, police level 0. Station: Jim Bob's Backwater Shack.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where beid`).

| Field | Value |
|---|---|
| Position | x -1756.4, y -3619.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | castor, cocibolca, driftwood, ironpeak, markeb |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `beid_star` | Beid Star | sun (K6V) | -- | -- | none | 2026-11-17 18:31 UTC | `get_system`, own ship |
| `beid_i` | Beid I | planet (scorched) | -- | -- | none | 2026-11-17 18:31 UTC | `get_system`, own ship |
| `beid_ii` | Beid II | planet (arid) | -- | -- | none | 2026-11-17 18:31 UTC | `get_system`, own ship |
| `beid_belt` | Beid Belt | asteroid_belt (metallic) | -- | iron_ore: richness 54, 83047 of 100000 left; copper_ore: richness 28, 100000 of 100000 left | none | 2026-11-17 18:31 UTC | `get_poi`, own ship |
| `beid_vapor_fields` | Beid Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 55, 483 of 50000 left; argon_gas: richness 36, 573 of 50000 left; plasma_gas: richness 21, 570 of 10000 left; xenon_gas: richness 27, 469 of 10000 left; neon_gas: richness 42, 476 of 50000 left | none | 2026-11-17 18:31 UTC | `get_poi`, own ship |
| `4650c48e3b6787e6cbeb69ebb3c61933` | Jim Bob's Backwater Shack | station | `b7ecd9b1ce7c2689d73d4f15f30dd134` | -- | none | 2026-11-17 18:31 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Jim Bob's Backwater Shack (`b7ecd9b1ce7c2689d73d4f15f30dd134`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 18:31 UTC | `get_system`, own ship |

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
| 2026-11-17 18:31 UTC | own ship | Read Beid Belt: 183,047 units left in all | `get_poi`, own ship |
| 2026-11-17 18:31 UTC | own ship | Read Beid Vapor Fields: 2,571 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
