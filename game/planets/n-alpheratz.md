---
name: alpheratz
id: 20261117T133326Z
tier: intel
author: Unity
kind: system
system_id: alpheratz
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alpheratz

- system 15 jumps from home, police level 0. Station: Starlight Cartographer.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alpheratz`).

| Field | Value |
|---|---|
| Position | x 2307.2, y 5016.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | 40_eridani, crosshaven, diphda, gsc_0034, lilii_borea, saiph |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alpheratz_star` | Alpheratz Star | sun (B8V) | -- | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `alpheratz_vapor_fields` | Alpheratz Vapor Fields | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 13:12 UTC | `get_system`, own ship |
| `0367654caf8485adcef9a58b7122d223` | Starlight Cartographer | station | `7d1f97987d5eb46bf603b8027e1eec8c` | -- | none | 2026-11-17 13:12 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Starlight Cartographer (`7d1f97987d5eb46bf603b8027e1eec8c`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 13:12 UTC | `get_system`, own ship |

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
| 2026-11-17 13:12 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `alpheratz_vapor_fields`.
