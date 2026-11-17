---
name: vindemiatrix
id: 20261117T153759Z
tier: intel
author: Unity
kind: system
system_id: vindemiatrix
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Vindemiatrix

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where vindemiatrix`).

| Field | Value |
|---|---|
| Position | x 5873.9, y -1102.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | northwick, vega, zubeneschamali |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `vindemiatrix_star` | Vindemiatrix Star | sun (K2V) | -- | -- | none | 2026-11-17 15:02 UTC | `get_system`, own ship |
| `vindemiatrix_i` | Vindemiatrix I | planet (scorched) | -- | -- | none | 2026-11-17 15:02 UTC | `get_system`, own ship |
| `vindemiatrix_belt` | Vindemiatrix Belt | asteroid_belt (metallic) | -- | iron_ore: richness 65, 100000 of 100000 left; copper_ore: richness 24, 100000 of 100000 left | none | 2026-11-17 15:02 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:02 UTC | own ship | Read Vindemiatrix Belt: 200,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
