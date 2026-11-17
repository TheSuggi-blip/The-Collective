---
name: seginus
id: 20261117T123203Z
tier: intel
author: Unity
kind: system
system_id: seginus
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Seginus

- system 18 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where seginus`).

| Field | Value |
|---|---|
| Position | x 3828.2, y -145.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 18 |
| Lanes | cebalrai, larawag, ravenspire, whitecliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `seginus_belt` | Seginus Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:18 UTC | `get_system`, own ship |
| `seginus_haze` | Seginus Haze | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 59, 4015 of 50000 left; argon_gas: richness 33, 44188 of 50000 left; plasma_gas: richness 15, 8941 of 10000 left; xenon_gas: richness 26, 1043 of 10000 left; neon_gas: richness 39, 40596 of 50000 left; fluorine_gas: richness 20, 1091 of 5000 left | none | 2026-11-17 12:18 UTC | `get_poi`, own ship |
| `seginus_ice_fields` | Seginus Ice Fields | ice_field (kuiper) | -- | not read | none | 2026-11-17 12:18 UTC | `get_system`, own ship |

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
| 2026-11-17 12:18 UTC | own ship | Read Seginus Haze: 99,874 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `seginus_belt`, `seginus_ice_fields`.
