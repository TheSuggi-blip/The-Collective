---
name: fafnir
id: 20261117T123139Z
tier: intel
author: Unity
kind: system
system_id: fafnir
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Fafnir

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where fafnir`).

| Field | Value |
|---|---|
| Position | x 3082.8, y -5680.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | gsc_0032, heze, moonshadow, ross_128 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `fafnir_star` | Fafnir Star | sun (K4V) | -- | -- | none | 2026-11-17 11:59 UTC | `get_system`, own ship |
| `fafnir_i` | Fafnir I | planet (scorched) | -- | -- | none | 2026-11-17 11:59 UTC | `get_system`, own ship |
| `fafnir_ii` | Fafnir II | planet (arid) | -- | -- | none | 2026-11-17 11:59 UTC | `get_system`, own ship |
| `fafnir_frozen_drift` | Fafnir Frozen Drift | ice_field (cometary) | -- | water_ice: richness 57, 2057 of 50000 left; nitrogen_ice: richness 49, 2059 of 50000 left; deuterium_ice: richness 14, 652 of 5000 left | none | 2026-11-17 11:59 UTC | `get_poi`, own ship |

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
| 2026-11-17 11:59 UTC | own ship | Read Fafnir Frozen Drift: 4,768 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
