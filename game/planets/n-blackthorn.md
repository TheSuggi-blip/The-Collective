---
name: blackthorn
id: 20261126T052614Z
tier: intel
author: Unity
kind: system
system_id: blackthorn
standing: neutral
standing_since: 2026-11-26
threat: unknown
empire: -
police_level: 0
updated: 2026-11-26
---

# Blackthorn

- system 23 jumps from home, police level 0. Station: Fortress Blackthorn.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where blackthorn`).

| Field | Value |
|---|---|
| Position | x -2374.6, y -4649.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | matar, sunridge |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `blackthorn_belt` | Blackthorn Belt | asteroid_belt (metallic) | -- | iron_ore: richness 59, 97661 of 100000 left; copper_ore: richness 44, 99696 of 100000 left; aluminum_ore: richness 52, 719 of 30000 left | none | 2026-11-26 04:29 UTC | `get_poi`, own ship |
| `blackthorn_ice_belt` | Blackthorn Ice Belt | ice_field (cometary) | -- | nitrogen_ice: richness 45, 50000 of 50000 left; helium_ice: richness 23, 5000 of 5000 left | none | 2026-11-26 04:29 UTC | `get_poi`, own ship |
| `9d742eadce7c211220fa20ba10093462` | Fortress Blackthorn | station | `566fbb2d3a304fa2d846147aed2aec0c` | -- | none | 2026-11-26 04:29 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Fortress Blackthorn (`566fbb2d3a304fa2d846147aed2aec0c`) | unknown | not tried | not read | unknown | unknown | 2026-11-26 04:29 UTC | `get_system`, own ship |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-26 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-26 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-26 04:29 UTC | own ship | Read Blackthorn Belt: 198,076 units left in all | `get_poi`, own ship |
| 2026-11-26 04:29 UTC | own ship | Read Blackthorn Ice Belt: 55,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
