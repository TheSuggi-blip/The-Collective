---
name: larawag
id: 20261117T133349Z
tier: intel
author: Unity
kind: system
system_id: larawag
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Larawag

- system 19 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where larawag`).

| Field | Value |
|---|---|
| Position | x 4357.5, y -141.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 19 |
| Lanes | atik, dusthaven, seginus, undercliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `larawag_star` | Larawag Star | sun (G2V) | -- | -- | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `larawag_i` | Larawag I | planet (scorched) | -- | -- | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `larawag_ii` | Larawag II | planet (arid) | -- | -- | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `larawag_belt_a` | Larawag Belt A | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `larawag_belt_b` | Larawag Belt B | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 13:03 UTC | `get_system`, own ship |
| `larawag_ice_belt` | Larawag Ice Belt | ice_field (kuiper) | -- | water_ice: richness 53, 40954 of 50000 left; nitrogen_ice: richness 47, 50000 of 50000 left; helium_ice: richness 10, 5000 of 5000 left | none | 2026-11-17 13:03 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:03 UTC | own ship | Read Larawag Ice Belt: 95,954 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `larawag_belt_a`, `larawag_belt_b`.
