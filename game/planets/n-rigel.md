---
name: rigel
id: 20261117T184408Z
tier: intel
author: Unity
kind: system
system_id: rigel
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Rigel

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where rigel`).

| Field | Value |
|---|---|
| Position | x 2670.0, y 3567.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | bd20_2457, fumalsamakah, nashira, rasalgethi |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `rigel_star` | Rigel Star | sun (M4V) | -- | -- | none | 2026-11-17 18:01 UTC | `get_system`, own ship |
| `rigel_i` | Rigel I | planet (scorched) | -- | -- | none | 2026-11-17 18:01 UTC | `get_system`, own ship |
| `rigel_gas_plume` | Rigel Gas Plume | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 67, 1709 of 50000 left; argon_gas: richness 52, 33587 of 50000 left; plasma_gas: richness 21, 7649 of 10000 left; xenon_gas: richness 19, 8944 of 10000 left; neon_gas: richness 53, 32863 of 50000 left; chlorine_gas: richness 24, 583 of 10000 left | none | 2026-11-17 18:01 UTC | `get_poi`, own ship |
| `rigel_cold_forge_seam` | Rigel Cold Forge Seam | asteroid_belt | -- | iron_ore: richness 37, 96319 of 100000 left; copper_ore: richness 30, 99982 of 100000 left; darksteel_ore: richness 5, 214 of 311 left | none | 2026-11-17 18:01 UTC | `get_poi`, own ship |
| `last_sigh_vent` | Last Sigh Vent | asteroid_belt | -- | iron_ore: richness 43, 24175 of 100000 left; copper_ore: richness 20, 100000 of 100000 left; plasma_residue: richness 10, 272 of 1008 left | none | 2026-11-17 18:01 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:01 UTC | own ship | Read Rigel Gas Plume: 85,335 units left in all | `get_poi`, own ship |
| 2026-11-17 18:01 UTC | own ship | Read Rigel Cold Forge Seam: 196,515 units left in all | `get_poi`, own ship |
| 2026-11-17 18:01 UTC | own ship | Read Last Sigh Vent: 124,447 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
