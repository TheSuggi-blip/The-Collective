---
name: lilii_borea
id: 20261117T163938Z
tier: intel
author: Unity
kind: system
system_id: lilii_borea
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Lilii Borea

- system 16 jumps from home, police level 0. Station: Echo Protocol Hub.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where lilii_borea`).

| Field | Value |
|---|---|
| Position | x 1928.6, y 5227.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | alpheratz, crosshaven, gsc_0010, gsc_0034, saiph |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `lilii_borea_star` | Lilii Borea Star | sun (M2V) | -- | -- | none | 2026-11-17 15:41 UTC | `get_system`, own ship |
| `lilii_borea_i` | Lilii Borea I | planet (scorched) | -- | -- | none | 2026-11-17 15:41 UTC | `get_system`, own ship |
| `lilii_borea_ii` | Lilii Borea II | planet (arid) | -- | -- | none | 2026-11-17 15:41 UTC | `get_system`, own ship |
| `lilii_borea_gas_cloud` | Lilii Borea Gas Cloud | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 40, 48150 of 50000 left; argon_gas: richness 46, 47997 of 50000 left; xenon_gas: richness 19, 9622 of 10000 left; nebula_gas: richness 18, 9633 of 10000 left; neon_gas: richness 36, 48187 of 50000 left; ion_gas: richness 32, 9623 of 10000 left | none | 2026-11-17 15:41 UTC | `get_poi`, own ship |
| `56da4dcca499808b0e76ab482fdfa71c` | Echo Protocol Hub | station | `d545d6ddb6c9ceab72fafc527a5e04b5` | -- | none | 2026-11-17 15:41 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Echo Protocol Hub (`d545d6ddb6c9ceab72fafc527a5e04b5`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 15:41 UTC | `get_system`, own ship |

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
| 2026-11-17 15:41 UTC | own ship | Read Lilii Borea Gas Cloud: 173,212 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
