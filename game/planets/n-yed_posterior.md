---
name: yed_posterior
id: 20261117T102837Z
tier: intel
author: Unity
kind: system
system_id: yed_posterior
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Yed Posterior

- system 11 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where yed_posterior`).

| Field | Value |
|---|---|
| Position | x -1103.0, y 6261.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 11 |
| Lanes | etamin, fomalhaut, pleione |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `yed_posterior_star` | Yed Posterior Star | sun (M2V) | -- | -- | none | 2026-11-17 09:47 UTC | `get_system`, own ship |
| `yed_posterior_i` | Yed Posterior I | planet (scorched) | -- | -- | none | 2026-11-17 09:47 UTC | `get_system`, own ship |
| `yed_posterior_ii` | Yed Posterior II | planet (arid) | -- | -- | none | 2026-11-17 09:47 UTC | `get_system`, own ship |
| `yed_posterior_belt` | Yed Posterior Belt | asteroid_belt (metallic) | -- | iron_ore: richness 35, 6693 of 100000 left; copper_ore: richness 45, 94119 of 100000 left | none | 2026-11-17 09:47 UTC | `get_poi`, own ship |
| `yed_posterior_frost_ring` | Yed Posterior Frost Ring | ice_field (cometary) | -- | water_ice: richness 68, 44510 of 50000 left | none | 2026-11-17 09:47 UTC | `get_poi`, own ship |

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
| 2026-11-17 09:47 UTC | own ship | Read Yed Posterior Belt: 100,812 units left in all | `get_poi`, own ship |
| 2026-11-17 09:47 UTC | own ship | Read Yed Posterior Frost Ring: 44,510 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
