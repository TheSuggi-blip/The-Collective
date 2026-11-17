---
name: cervantes
id: 20261117T082526Z
tier: intel
author: Unity
kind: system
system_id: cervantes
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Cervantes

- system 10 jumps from home, police level 0. Station: OBKT Cervantes.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where cervantes`).

| Field | Value |
|---|---|
| Position | x -1482.7, y -1145.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | hatysa, miaplacidus, nembus, ridgecrest |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `cervantes_star` | Cervantes Star | sun (G5V) | -- | -- | none | 2026-11-17 08:10 UTC | `get_system`, own ship |
| `cervantes_belt` | Cervantes Belt | asteroid_belt (metallic) | -- | iron_ore: richness 55, 99996 of 100000 left; copper_ore: richness 46, 99996 of 100000 left; aluminum_ore: richness 56, 721 of 30000 left; chromium_ore: richness 19, 51 of 10000 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |
| `cervantes_vapor_fields` | Cervantes Vapor Fields | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 56, 2862 of 50000 left; argon_gas: richness 48, 6520 of 50000 left; plasma_gas: richness 18, 3154 of 10000 left; xenon_gas: richness 24, 10000 of 10000 left; neon_gas: richness 48, 6383 of 50000 left; chlorine_gas: richness 31, 1017 of 10000 left; ion_gas: richness 28, 9015 of 10000 left; krypton_gas: richness 17, 3967 of 5000 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |
| `cervantes_fading_signal` | Cervantes Fading Signal | asteroid_belt | -- | iron_ore: richness 28, 100000 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; antimatter_containment_cell: richness 2, 157 of 157 left | none | 2026-11-17 08:10 UTC | `get_poi`, own ship |
| `251902d8c7f6d4032511897e08f7d4ca` | OBKT Cervantes | station | `3c3c72f649c98b35609bb708e917cc1c` | -- | none | 2026-11-17 08:10 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| OBKT Cervantes (`3c3c72f649c98b35609bb708e917cc1c`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 08:10 UTC | `get_system`, own ship |

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
| 2026-11-17 08:10 UTC | own ship | Read Cervantes Belt: 200,764 units left in all | `get_poi`, own ship |
| 2026-11-17 08:10 UTC | own ship | Read Cervantes Vapor Fields: 42,918 units left in all | `get_poi`, own ship |
| 2026-11-17 08:10 UTC | own ship | Read Cervantes Fading Signal: 200,157 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
