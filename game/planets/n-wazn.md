---
name: wazn
id: 20261117T184356Z
tier: intel
author: Unity
kind: system
system_id: wazn
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Wazn

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where wazn`).

| Field | Value |
|---|---|
| Position | x -303.2, y -3970.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | cloverfield, frostpeak, kurhah, maia |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `wazn_star` | Wazn Star | sun (M2V) | -- | -- | none | 2026-11-17 18:21 UTC | `get_system`, own ship |
| `wazn_i` | Wazn I | planet (scorched) | -- | -- | none | 2026-11-17 18:21 UTC | `get_system`, own ship |
| `wazn_belt_a` | Wazn Belt A | asteroid_belt (metallic) | -- | iron_ore: richness 38, 99998 of 100000 left; copper_ore: richness 27, 99999 of 100000 left; lithium_ore: richness 27, 937 of 25000 left | none | 2026-11-17 18:21 UTC | `get_poi`, own ship |
| `wazn_belt_b` | Wazn Belt B | asteroid_belt (metallic) | -- | iron_ore: richness 69, 100000 of 100000 left; copper_ore: richness 42, 100000 of 100000 left | none | 2026-11-17 18:21 UTC | `get_poi`, own ship |
| `wazn_haze` | Wazn Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 41, 176 of 50000 left; argon_gas: richness 44, 178 of 50000 left; plasma_gas: richness 24, 174 of 10000 left; neon_gas: richness 40, 173 of 50000 left | none | 2026-11-17 18:21 UTC | `get_poi`, own ship |

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
| 2026-11-17 18:21 UTC | own ship | Read Wazn Belt A: 200,934 units left in all | `get_poi`, own ship |
| 2026-11-17 18:21 UTC | own ship | Read Wazn Belt B: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 18:21 UTC | own ship | Read Wazn Haze: 701 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
