---
name: fuyue
id: 20261117T194622Z
tier: intel
author: Unity
kind: system
system_id: fuyue
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Fuyue

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where fuyue`).

| Field | Value |
|---|---|
| Position | x 1867.4, y -95.3 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | algieba, hr_8832, ross_248, struve_2398, taygeta |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fuyue_star` | Fuyue Star | sun (M2V) | -- | -- | none | 2026-11-17 19:39 UTC | `get_system`, own ship |
| `fuyue_i` | Fuyue I | planet (scorched) | -- | -- | none | 2026-11-17 19:39 UTC | `get_system`, own ship |
| `fuyue_emission_nebula` | Fuyue Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 65, 30267 of 50000 left; argon_gas: richness 42, 50000 of 50000 left; plasma_gas: richness 20, 6230 of 10000 left; xenon_gas: richness 24, 7035 of 10000 left | none | 2026-11-17 19:39 UTC | `get_poi`, own ship |

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
| 2026-11-17 19:39 UTC | own ship | Read Fuyue Emission Nebula: 93,532 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
