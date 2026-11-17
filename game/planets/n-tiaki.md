---
name: tiaki
id: 20261117T143555Z
tier: intel
author: Unity
kind: system
system_id: tiaki
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tiaki

- system 17 jumps from home, police level 0. Station: Stellar Leap Station, To The Dark Moon.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tiaki`).

| Field | Value |
|---|---|
| Position | x 2809.1, y 5717.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | crosshaven, diphda, gsc_0034 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tiaki_star` | Tiaki Star | sun (M6V) | -- | -- | none | 2026-11-17 14:19 UTC | `get_system`, own ship |
| `tiaki_i` | Tiaki I | planet (scorched) | -- | -- | none | 2026-11-17 14:19 UTC | `get_system`, own ship |
| `worldsend_field` | Worldsend Field | asteroid_belt | -- | nickel_ore: richness 30, 2074 of 20000 left | none | 2026-11-17 14:19 UTC | `get_poi`, own ship |
| `1e2d6bd532e06724b80851cff3d68e2e` | Stellar Leap Station | station | `1c20ebffce4818219cde45fc5c71e43b` | -- | none | 2026-11-17 14:19 UTC | `get_system`, own ship |
| `c80c08eda08aa613d88736d4132b093c` | To The Dark Moon | station | `c6f5ab8fec8ed6d82e8f6b7ae3b65356` | -- | none | 2026-11-17 14:19 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Stellar Leap Station (`1c20ebffce4818219cde45fc5c71e43b`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:19 UTC | `get_system`, own ship |
| To The Dark Moon (`c6f5ab8fec8ed6d82e8f6b7ae3b65356`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:19 UTC | `get_system`, own ship |

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
| 2026-11-17 14:19 UTC | own ship | Read Worldsend Field: 2,074 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
