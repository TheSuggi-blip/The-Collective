---
name: northwick
id: 20261117T133354Z
tier: intel
author: Unity
kind: system
system_id: northwick
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Northwick

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where northwick`).

| Field | Value |
|---|---|
| Position | x 5151.2, y -991.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | alshat, quarrytown, undercliff, vega, vindemiatrix |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `northwick_star` | Northwick Star | sun (K4V) | -- | -- | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `northwick_i` | Northwick I | planet (scorched) | -- | -- | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `northwick_ii` | Northwick II | planet (arid) | -- | -- | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `northwick_iii` | Northwick III | planet (terran) | -- | -- | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `northwick_belt` | Northwick Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 100000 of 100000 left; copper_ore: richness 27, 100000 of 100000 left | none | 2026-11-17 12:59 UTC | `get_poi`, own ship |
| `northwick_haze` | Northwick Haze | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 12:59 UTC | `get_system`, own ship |
| `northwick_ice_belt` | Northwick Ice Belt | ice_field (kuiper) | -- | not read | none | 2026-11-17 12:59 UTC | `get_system`, own ship |

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
| 2026-11-17 12:59 UTC | own ship | Read Northwick Belt: 200,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `northwick_haze`, `northwick_ice_belt`.
