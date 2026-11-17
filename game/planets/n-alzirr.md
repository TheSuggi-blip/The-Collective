---
name: alzirr
id: 20261117T153725Z
tier: intel
author: Unity
kind: system
system_id: alzirr
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alzirr

- system 21 jumps from home, police level 0. Station: Event Horizon Relay.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alzirr`).

| Field | Value |
|---|---|
| Position | x 5954.8, y 3027.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | blood_forge, frostfeld, muscida, windmere |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `the_maw` | The Maw | sun (BH) | -- | -- | tidal_shear, severity 4 | 2026-11-17 14:44 UTC | `get_system`, own ship |
| `alzirr_a` | Alzirr A | sun (K2III) | -- | -- | none | 2026-11-17 14:44 UTC | `get_system`, own ship |
| `the_bleeding_ring` | The Bleeding Ring | gas_cloud (emission) | -- | not read | tidal_shear, severity 1 | 2026-11-17 14:44 UTC | `get_system`, own ship |
| `alzirr_i` | Alzirr I | planet (scorched) | -- | -- | tidal_shear, severity 2 | 2026-11-17 14:44 UTC | `get_system`, own ship |
| `alzirr_belt` | Alzirr Belt | asteroid_belt (mixed) | -- | not read | none | 2026-11-17 14:44 UTC | `get_system`, own ship |
| `b6007ea0d1b905492a17dcd5d3e72286` | Event Horizon Relay | station | `2e8caabbf604606db0692b3f71751ded` | -- | none | 2026-11-17 14:44 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Event Horizon Relay (`2e8caabbf604606db0692b3f71751ded`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 14:44 UTC | `get_system`, own ship |

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
| 2026-11-17 14:44 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `the_bleeding_ring`, `alzirr_belt`.
