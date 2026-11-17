---
name: chara
id: 20261117T112926Z
tier: intel
author: Unity
kind: system
system_id: chara
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Chara

- system 13 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where chara`).

| Field | Value |
|---|---|
| Position | x 1261.6, y 4315.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 13 |
| Lanes | algorab, alshain, angetenar, phecda, tureis, yed_prior |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `chara_star` | Chara Star | sun (G2V) | -- | -- | none | 2026-11-17 11:06 UTC | `get_system`, own ship |
| `chara_i` | Chara I | planet (scorched) | -- | -- | none | 2026-11-17 11:06 UTC | `get_system`, own ship |
| `chara_belt` | Chara Belt | asteroid_belt (metallic) | -- | iron_ore: richness 30, 99999 of 100000 left; copper_ore: richness 37, 36477 of 100000 left; gold_ore: richness 27, 698 of 25000 left | none | 2026-11-17 11:06 UTC | `get_poi`, own ship |
| `chara_gas_plume` | Chara Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 57, 11947 of 50000 left; argon_gas: richness 35, 49999 of 50000 left; plasma_gas: richness 28, 3582 of 10000 left; chlorine_gas: richness 24, 5669 of 10000 left; krypton_gas: richness 49, 85 of 5000 left | none | 2026-11-17 11:06 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:06 UTC | own ship | Read Chara Belt: 137,174 units left in all | `get_poi`, own ship |
| 2026-11-17 11:06 UTC | own ship | Read Chara Gas Plume: 71,282 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
