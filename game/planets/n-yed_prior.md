---
name: yed_prior
id: 20261117T133415Z
tier: intel
author: Unity
kind: system
system_id: yed_prior
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Yed Prior

- system 14 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where yed_prior`).

| Field | Value |
|---|---|
| Position | x 1198.7, y 4998.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 14 |
| Lanes | chara, skyreach, tureis |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `yed_prior_star` | Yed Prior Star | sun (M2V) | -- | -- | none | 2026-11-17 12:50 UTC | `get_system`, own ship |
| `yed_prior_i` | Yed Prior I | planet (scorched) | -- | -- | none | 2026-11-17 12:50 UTC | `get_system`, own ship |
| `yed_prior_ii` | Yed Prior II | planet (arid) | -- | -- | none | 2026-11-17 12:50 UTC | `get_system`, own ship |
| `yed_prior_iii` | Yed Prior III | planet (terran) | -- | -- | none | 2026-11-17 12:50 UTC | `get_system`, own ship |
| `yed_prior_belt` | Yed Prior Belt | asteroid_belt (metallic) | -- | iron_ore: richness 44, 64154 of 100000 left; copper_ore: richness 42, 64399 of 100000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |
| `yed_prior_emission_nebula` | Yed Prior Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 54, 874 of 50000 left; argon_gas: richness 36, 48814 of 50000 left; fluorine_gas: richness 13, 3212 of 5000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |
| `yed_prior_cryobelt` | Yed Prior Cryobelt | ice_field (kuiper) | -- | water_ice: richness 42, 47353 of 50000 left; nitrogen_ice: richness 42, 50000 of 50000 left; helium_ice: richness 18, 4579 of 5000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:50 UTC | own ship | Read Yed Prior Belt: 128,553 units left in all | `get_poi`, own ship |
| 2026-11-17 12:50 UTC | own ship | Read Yed Prior Emission Nebula: 52,900 units left in all | `get_poi`, own ship |
| 2026-11-17 12:50 UTC | own ship | Read Yed Prior Cryobelt: 101,932 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
