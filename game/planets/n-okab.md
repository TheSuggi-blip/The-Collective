---
name: okab
id: 20261115T215326Z
tier: intel
author: Unity
kind: system
system_id: okab
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Okab

- system 4 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where okab`).

| Field | Value |
|---|---|
| Position | x -3935.8, y 4009.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 4 |
| Lanes | coldwater, hamal, keid, megrez, thornhaven |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `okab_star` | Okab Star | sun (M2V) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `okab_i` | Okab I | planet (scorched) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `okab_ii` | Okab II | planet (arid) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `okab_iii` | Okab III | planet (terran) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `okab_iv` | Okab IV | planet (jovian) | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |
| `okab_belt` | Okab Belt | asteroid_belt (metallic) | -- | iron_ore: richness 43, 99999 of 100000 left; copper_ore: richness 45, 99999 of 100000 left | none | 2026-11-15 21:49 UTC | `get_poi`, own ship |
| `okab_haze` | Okab Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 56, 49999 of 50000 left; argon_gas: richness 39, 49999 of 50000 left; nebula_gas: richness 26, 10000 of 10000 left; neon_gas: richness 44, 50000 of 50000 left | none | 2026-11-15 21:49 UTC | `get_poi`, own ship |
| `low_charge_glint` | Low Charge Glint | nebula | -- | -- | none | 2026-11-15 21:49 UTC | `get_system`, own ship |

## Stations

None on the chart.

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
| 2026-11-15 21:49 UTC | own ship | Read Okab Belt: 199,998 units left in all | `get_poi`, own ship |
| 2026-11-15 21:49 UTC | own ship | Read Okab Haze: 159,998 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
