---
name: alshat
id: 20261117T153724Z
tier: intel
author: Unity
kind: system
system_id: alshat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alshat

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alshat`).

| Field | Value |
|---|---|
| Position | x 5169.7, y -710.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | edgewater, northwick, quarrytown, undercliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alshat_star` | Alshat Star | sun (K6V) | -- | -- | none | 2026-11-17 15:15 UTC | `get_system`, own ship |
| `alshat_i` | Alshat I | planet (scorched) | -- | -- | none | 2026-11-17 15:15 UTC | `get_system`, own ship |
| `alshat_ii` | Alshat II | planet (arid) | -- | -- | none | 2026-11-17 15:15 UTC | `get_system`, own ship |
| `alshat_emission_nebula` | Alshat Emission Nebula | gas_cloud (emission) | -- | hydrogen_gas: richness 40, 14393 of 50000 left; argon_gas: richness 37, 50000 of 50000 left; plasma_gas: richness 28, 1111 of 10000 left; nebula_gas: richness 14, 8244 of 10000 left; neon_gas: richness 53, 50000 of 50000 left | none | 2026-11-17 15:15 UTC | `get_poi`, own ship |
| `alshat_frost_ring` | Alshat Frost Ring | ice_field (kuiper) | -- | water_ice: richness 67, 4409 of 50000 left; deuterium_ice: richness 24, 1448 of 5000 left | none | 2026-11-17 15:15 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:15 UTC | own ship | Read Alshat Emission Nebula: 123,748 units left in all | `get_poi`, own ship |
| 2026-11-17 15:15 UTC | own ship | Read Alshat Frost Ring: 5,857 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
