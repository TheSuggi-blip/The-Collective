---
name: frontier
id: 20261117T174209Z
tier: intel
author: Unity
kind: system
system_id: frontier
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 100
updated: 2026-11-17
---

# Frontier

Outerrim system 18 jumps from home, police level 100. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where frontier`).

| Field | Value |
|---|---|
| Position | x -3000.0, y -3500.0 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 18 |
| Lanes | altais, deep_range, horizon |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `frontier_star` | Frontier Star | sun (K5V) | -- | -- | none | 2026-11-17 16:50 UTC | `get_system`, own ship |
| `old_survey_station` | Old Survey Station | relic (megastructure) | -- | -- | none | 2026-11-17 16:50 UTC | `get_system`, own ship |
| `veil_nebula` | Veil Nebula | nebula (stellar_nursery) | -- | -- | none | 2026-11-17 16:50 UTC | `get_system`, own ship |
| `drifters_haze` | Drifter's Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 75, 6535 of 50000 left; argon_gas: richness 55, 47777 of 50000 left | none | 2026-11-17 16:50 UTC | `get_poi`, own ship |
| `icecap_drift` | Icecap Drift | ice_field (cometary) | -- | water_ice: richness 75, 9115 of 50000 left; nitrogen_ice: richness 60, 41128 of 50000 left; carbon_dioxide_ice: richness 15, 6734 of 7000 left | none | 2026-11-17 16:50 UTC | `get_poi`, own ship |
| `pioneer_fields` | Pioneer Fields | asteroid_belt (metallic) | -- | iron_ore: richness 80, 4361 of 100000 left; copper_ore: richness 70, 7543 of 100000 left; nickel_ore: richness 60, 699 of 20000 left; titanium_ore: richness 30, 731 of 25000 left | none | 2026-11-17 16:50 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 100: Maximum Security (empire capital) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 16:50 UTC | own ship | Read Drifter's Haze: 54,312 units left in all | `get_poi`, own ship |
| 2026-11-17 16:50 UTC | own ship | Read Icecap Drift: 56,977 units left in all | `get_poi`, own ship |
| 2026-11-17 16:50 UTC | own ship | Read Pioneer Fields: 13,334 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
