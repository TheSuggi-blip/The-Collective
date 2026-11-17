---
name: kepler_186
id: 20261117T163937Z
tier: intel
author: Unity
kind: system
system_id: kepler_186
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kepler-186

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kepler_186`).

| Field | Value |
|---|---|
| Position | x -443.4, y -6178.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | gsc_0048, luyten_726, mintaka, regulus |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kepler_186_star` | Kepler-186 Star | sun (K4V) | -- | -- | none | 2026-11-17 15:40 UTC | `get_system`, own ship |
| `kepler_186_i` | Kepler-186 I | planet (scorched) | -- | -- | none | 2026-11-17 15:40 UTC | `get_system`, own ship |
| `kepler_186_belt` | Kepler-186 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 34, 99999 of 100000 left; copper_ore: richness 26, 100000 of 100000 left | none | 2026-11-17 15:40 UTC | `get_poi`, own ship |
| `kepler_186_ice_fields` | Kepler-186 Ice Fields | ice_field (kuiper) | -- | water_ice: richness 60, 2540 of 50000 left; nitrogen_ice: richness 32, 4179 of 50000 left; deuterium_ice: richness 10, 1304 of 5000 left | none | 2026-11-17 15:40 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:40 UTC | own ship | Read Kepler-186 Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 15:40 UTC | own ship | Read Kepler-186 Ice Fields: 8,023 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
