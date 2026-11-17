---
name: undercliff
id: 20261117T133411Z
tier: intel
author: Unity
kind: system
system_id: undercliff
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Undercliff

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where undercliff`).

| Field | Value |
|---|---|
| Position | x 4825.2, y -423.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | alshat, dusthaven, edgewater, larawag, northwick, quarrytown |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `undercliff_star` | Undercliff Star | sun (K2III) | -- | -- | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `undercliff_i` | Undercliff I | planet (scorched) | -- | -- | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `undercliff_ii` | Undercliff II | planet (arid) | -- | -- | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `undercliff_belt` | Undercliff Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `undercliff_gas_plume` | Undercliff Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:34 UTC | `get_system`, own ship |
| `undercliff_frost_ring` | Undercliff Frost Ring | ice_field (cometary) | -- | water_ice: richness 41, 30805 of 50000 left; nitrogen_ice: richness 50, 50000 of 50000 left; helium_ice: richness 12, 3166 of 5000 left | none | 2026-11-17 12:34 UTC | `get_poi`, own ship |
| `cut_anchor_cache` | Cut Anchor Cache | asteroid_belt | -- | not read | none | 2026-11-17 12:34 UTC | `get_system`, own ship |

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
| 2026-11-17 12:34 UTC | own ship | Read Undercliff Frost Ring: 83,971 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `undercliff_belt`, `undercliff_gas_plume`, `cut_anchor_cache`.
