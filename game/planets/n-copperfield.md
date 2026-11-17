---
name: copperfield
id: 20261117T123135Z
tier: intel
author: Unity
kind: system
system_id: copperfield
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Copperfield

- system 23 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where copperfield`).

| Field | Value |
|---|---|
| Position | x 6373.4, y 624.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 23 |
| Lanes | praecipua, rustpoint, taiyi, toi_700 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `copperfield_star` | Copperfield Star | sun (M2V) | -- | -- | none | 2026-11-17 12:09 UTC | `get_system`, own ship |
| `copperfield_i` | Copperfield I | planet (scorched) | -- | -- | none | 2026-11-17 12:09 UTC | `get_system`, own ship |
| `copperfield_ii` | Copperfield II | planet (arid) | -- | -- | none | 2026-11-17 12:09 UTC | `get_system`, own ship |
| `copperfield_emission_nebula` | Copperfield Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 69, 40425 of 50000 left; argon_gas: richness 31, 50000 of 50000 left; plasma_gas: richness 34, 7175 of 10000 left; neon_gas: richness 52, 46088 of 50000 left | none | 2026-11-17 12:09 UTC | `get_poi`, own ship |
| `copperfield_ice_belt` | Copperfield Ice Belt | ice_field (kuiper) | -- | water_ice: richness 63, 44446 of 50000 left; nitrogen_ice: richness 53, 50000 of 50000 left; deuterium_ice: richness 22, 5000 of 5000 left | none | 2026-11-17 12:09 UTC | `get_poi`, own ship |
| `copperfield_veins` | Copperfield Veins | asteroid_belt (metallic) | -- | copper_ore: richness 90, 199978 of 200000 left | none | 2026-11-17 12:09 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:09 UTC | own ship | Read Copperfield Emission Nebula: 143,688 units left in all | `get_poi`, own ship |
| 2026-11-17 12:09 UTC | own ship | Read Copperfield Ice Belt: 99,446 units left in all | `get_poi`, own ship |
| 2026-11-17 12:09 UTC | own ship | Read Copperfield Veins: 199,978 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
