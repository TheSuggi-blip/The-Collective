---
name: netherwick
id: 20261117T133353Z
tier: intel
author: Unity
kind: system
system_id: netherwick
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Netherwick

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where netherwick`).

| Field | Value |
|---|---|
| Position | x 6728.4, y -1544.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alsuhail, edasich, gacrux, redmarsh |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `netherwick_star` | Netherwick Star | sun (K2III) | -- | -- | none | 2026-11-17 12:54 UTC | `get_system`, own ship |
| `netherwick_i` | Netherwick I | planet (scorched) | -- | -- | none | 2026-11-17 12:54 UTC | `get_system`, own ship |
| `netherwick_belt` | Netherwick Belt | asteroid_belt (metallic) | -- | iron_ore: richness 65, 71058 of 100000 left; copper_ore: richness 30, 100000 of 100000 left; gold_ore: richness 23, 2080 of 25000 left | none | 2026-11-17 12:54 UTC | `get_poi`, own ship |
| `netherwick_gas_pocket` | Netherwick Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 69, 17518 of 50000 left; argon_gas: richness 49, 45935 of 50000 left; plasma_gas: richness 25, 8742 of 10000 left; xenon_gas: richness 18, 9806 of 10000 left; nebula_gas: richness 24, 9278 of 10000 left; neon_gas: richness 45, 47717 of 50000 left; chlorine_gas: richness 24, 9197 of 10000 left; krypton_gas: richness 15, 5000 of 5000 left; fluorine_gas: richness 45, 775 of 5000 left | none | 2026-11-17 12:54 UTC | `get_poi`, own ship |
| `netherwick_glass_reef` | Netherwick Glass Reef | asteroid_belt | -- | iron_ore: richness 37, 100000 of 100000 left; copper_ore: richness 34, 98066 of 100000 left; silicon_ore: richness 47, 3052 of 20000 left | none | 2026-11-17 12:54 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:54 UTC | own ship | Read Netherwick Belt: 173,138 units left in all | `get_poi`, own ship |
| 2026-11-17 12:54 UTC | own ship | Read Netherwick Gas Pocket: 153,968 units left in all | `get_poi`, own ship |
| 2026-11-17 12:54 UTC | own ship | Read Netherwick Glass Reef: 201,118 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
