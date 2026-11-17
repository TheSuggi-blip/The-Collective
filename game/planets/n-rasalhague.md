---
name: rasalhague
id: 20261117T000629Z
tier: intel
author: Unity
kind: system
system_id: rasalhague
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rasalhague

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rasalhague`).

| Field | Value |
|---|---|
| Position | x -5108.6, y 304.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | chalawan, mizar, saltwind, tania, yildun |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rasalhague_star` | Rasalhague Star | sun (M4V) | -- | -- | none | 2026-11-17 00:02 UTC | `get_system`, own ship |
| `rasalhague_haze` | Rasalhague Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 57, 13875 of 50000 left; argon_gas: richness 42, 50000 of 50000 left; nebula_gas: richness 18, 7187 of 10000 left; neon_gas: richness 43, 50000 of 50000 left; krypton_gas: richness 15, 3957 of 5000 left | none | 2026-11-17 00:02 UTC | `get_poi`, own ship |
| `rasalhague_ice_fields` | Rasalhague Ice Fields | ice_field (cometary) | -- | water_ice: richness 48, 50000 of 50000 left; nitrogen_ice: richness 36, 50000 of 50000 left | none | 2026-11-17 00:02 UTC | `get_poi`, own ship |

## Stations

None on the chart.

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
| 2026-11-17 00:02 UTC | own ship | Read Rasalhague Haze: 125,019 units left in all | `get_poi`, own ship |
| 2026-11-17 00:02 UTC | own ship | Read Rasalhague Ice Fields: 100,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
