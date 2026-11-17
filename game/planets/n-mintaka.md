---
name: mintaka
id: 20261117T143549Z
tier: intel
author: Unity
kind: system
system_id: mintaka
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mintaka

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mintaka`).

| Field | Value |
|---|---|
| Position | x -547.6, y -5683.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | acamar, albali, gsc_0001, gsc_0048, kepler_186, nunki, regulus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mintaka_star` | Mintaka Star | sun (G2V) | -- | -- | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_i` | Mintaka I | planet (scorched) | -- | -- | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_ii` | Mintaka II | planet (arid) | -- | -- | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_iii` | Mintaka III | planet (terran) | -- | -- | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_iv` | Mintaka IV | planet (jovian) | -- | -- | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_belt` | Mintaka Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 13:40 UTC | `get_system`, own ship |
| `mintaka_gas_pocket` | Mintaka Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 64, 240 of 50000 left; argon_gas: richness 51, 5221 of 50000 left; nebula_gas: richness 22, 3693 of 10000 left; neon_gas: richness 51, 8822 of 50000 left; ion_gas: richness 35, 240 of 10000 left | none | 2026-11-17 13:40 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:40 UTC | own ship | Read Mintaka Gas Pocket: 18,216 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `mintaka_belt`.
