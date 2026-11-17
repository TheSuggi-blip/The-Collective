---
name: etamin
id: 20261117T082529Z
tier: intel
author: Unity
kind: system
system_id: etamin
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Etamin

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where etamin`).

| Field | Value |
|---|---|
| Position | x -1527.5, y 5806.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | coppervale, greenvale, pleione, yed_posterior |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `etamin_star` | Etamin Star | sun (M4V) | -- | -- | none | 2026-11-17 08:17 UTC | `get_system`, own ship |
| `etamin_i` | Etamin I | planet (scorched) | -- | -- | none | 2026-11-17 08:17 UTC | `get_system`, own ship |
| `etamin_belt` | Etamin Belt | asteroid_belt (metallic) | -- | iron_ore: richness 51, 13776 of 100000 left; copper_ore: richness 35, 99999 of 100000 left | none | 2026-11-17 08:17 UTC | `get_poi`, own ship |
| `etamin_haze` | Etamin Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 53, 5501 of 50000 left; argon_gas: richness 30, 49845 of 50000 left; plasma_gas: richness 27, 9929 of 10000 left; chlorine_gas: richness 23, 1677 of 10000 left | none | 2026-11-17 08:17 UTC | `get_poi`, own ship |
| `monitoring_blind` | Monitoring Blind | relic (derelict) | -- | -- | none | 2026-11-17 08:17 UTC | `get_system`, own ship |

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
| 2026-11-17 08:17 UTC | own ship | Read Etamin Belt: 113,775 units left in all | `get_poi`, own ship |
| 2026-11-17 08:17 UTC | own ship | Read Etamin Haze: 66,952 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
