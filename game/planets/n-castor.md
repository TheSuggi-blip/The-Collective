---
name: castor
id: 20261117T174215Z
tier: intel
author: Unity
kind: system
system_id: castor
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Castor

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where castor`).

| Field | Value |
|---|---|
| Position | x -1498.5, y -3350.7 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | beid, cocibolca, driftwood, gsc_0023, haedus, ironpeak |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `castor_star` | Castor Star | sun (K2V) | -- | -- | none | 2026-11-17 17:18 UTC | `get_system`, own ship |
| `castor_i` | Castor I | planet (scorched) | -- | -- | none | 2026-11-17 17:18 UTC | `get_system`, own ship |
| `castor_ii` | Castor II | planet (arid) | -- | -- | none | 2026-11-17 17:18 UTC | `get_system`, own ship |
| `castor_iii` | Castor III | planet (terran) | -- | -- | none | 2026-11-17 17:18 UTC | `get_system`, own ship |
| `castor_belt` | Castor Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 17762 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; manganese_ore: richness 23, 3051 of 17000 left | none | 2026-11-17 17:18 UTC | `get_poi`, own ship |
| `castor_emission_nebula` | Castor Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 63, 179 of 50000 left; plasma_gas: richness 17, 175 of 10000 left; neon_gas: richness 51, 175 of 50000 left; ion_gas: richness 27, 174 of 10000 left | none | 2026-11-17 17:18 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:18 UTC | own ship | Read Castor Belt: 120,813 units left in all | `get_poi`, own ship |
| 2026-11-17 17:18 UTC | own ship | Read Castor Emission Nebula: 703 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
