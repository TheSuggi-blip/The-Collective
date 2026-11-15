---
name: nightveil
id: 20261115T235526Z
tier: intel
author: Unity
kind: system
system_id: nightveil
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Nightveil

- system 5 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where nightveil`).

| Field | Value |
|---|---|
| Position | x -6012.0, y 2837.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 5 |
| Lanes | acrab, brachium, denebola, gsc_0049, marfik |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `nightveil_star` | Nightveil Star | sun (M4V) | -- | -- | none | 2026-11-15 23:32 UTC | `get_system`, own ship |
| `nightveil_haze` | Nightveil Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 49, 447 of 50000 left; argon_gas: richness 37, 45745 of 50000 left; plasma_gas: richness 30, 5958 of 10000 left; neon_gas: richness 38, 44972 of 50000 left; chlorine_gas: richness 25, 324 of 10000 left; ion_gas: richness 56, 327 of 10000 left | none | 2026-11-15 23:32 UTC | `get_poi`, own ship |
| `nightveil_dark_residue` | Nightveil Dark Residue | asteroid_belt | -- | iron_ore: richness 36, 100000 of 100000 left; copper_ore: richness 27, 99999 of 100000 left; null_matter: richness 9, 594 of 607 left | none | 2026-11-15 23:32 UTC | `get_poi`, own ship |

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
| 2026-11-15 23:32 UTC | own ship | Read Nightveil Haze: 97,773 units left in all | `get_poi`, own ship |
| 2026-11-15 23:32 UTC | own ship | Read Nightveil Dark Residue: 200,593 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
