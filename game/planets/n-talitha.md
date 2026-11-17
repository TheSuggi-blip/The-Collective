---
name: talitha
id: 20261117T174147Z
tier: intel
author: Unity
kind: system
system_id: talitha
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Talitha

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where talitha`).

| Field | Value |
|---|---|
| Position | x 451.5, y 5122.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | millhaven, skyreach |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `talitha_star` | Talitha Star | sun (G5III) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `talitha_i` | Talitha I | planet (scorched) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `talitha_ii` | Talitha II | planet (arid) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `the_nailed_map` | The Nailed Map | relic (derelict) | -- | -- | none | 2026-11-17 17:13 UTC | `get_system`, own ship |
| `talitha_cryobelt` | Talitha Cryobelt | ice_field (kuiper) | -- | water_ice: richness 60, 39373 of 50000 left; nitrogen_ice: richness 53, 50000 of 50000 left; carbon_dioxide_ice: richness 13, 5000 of 5000 left | none | 2026-11-17 17:13 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:13 UTC | own ship | Read Talitha Cryobelt: 94,373 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
