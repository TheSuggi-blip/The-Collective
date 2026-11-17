---
name: inquill
id: 20261117T133346Z
tier: intel
author: Unity
kind: system
system_id: inquill
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Inquill

- system 27 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where inquill`).

| Field | Value |
|---|---|
| Position | x 5466.0, y -2835.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 27 |
| Lanes | foxglove, ironveil, paikauhale, sadr |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `inquill_star` | Inquill Star | sun (M6V) | -- | -- | none | 2026-11-17 12:49 UTC | `get_system`, own ship |
| `inquill_i` | Inquill I | planet (scorched) | -- | -- | none | 2026-11-17 12:49 UTC | `get_system`, own ship |
| `inquill_ii` | Inquill II | planet (arid) | -- | -- | none | 2026-11-17 12:49 UTC | `get_system`, own ship |
| `inquill_iii` | Inquill III | planet (terran) | -- | -- | none | 2026-11-17 12:49 UTC | `get_system`, own ship |
| `inquill_belt` | Inquill Belt | asteroid_belt (metallic) | -- | iron_ore: richness 37, 100000 of 100000 left; copper_ore: richness 23, 100000 of 100000 left | none | 2026-11-17 12:49 UTC | `get_poi`, own ship |
| `inquill_gas_pocket` | Inquill Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 63, 7076 of 50000 left; argon_gas: richness 39, 50000 of 50000 left; neon_gas: richness 45, 50000 of 50000 left; chlorine_gas: richness 27, 3858 of 10000 left | none | 2026-11-17 12:49 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:49 UTC | own ship | Read Inquill Belt: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 12:49 UTC | own ship | Read Inquill Gas Pocket: 110,934 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
