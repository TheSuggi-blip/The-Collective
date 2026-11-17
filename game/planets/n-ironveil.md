---
name: ironveil
id: 20261117T153741Z
tier: intel
author: Unity
kind: system
system_id: ironveil
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ironveil

- system 28 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ironveil`).

| Field | Value |
|---|---|
| Position | x 5373.3, y -3535.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 28 |
| Lanes | alcyone, altair, foxglove, inquill, quartzfield, sadr |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ironveil_star` | Ironveil Star | sun (K6V) | -- | -- | none | 2026-11-17 14:40 UTC | `get_system`, own ship |
| `ironveil_i` | Ironveil I | planet (scorched) | -- | -- | none | 2026-11-17 14:40 UTC | `get_system`, own ship |
| `ironveil_ii` | Ironveil II | planet (arid) | -- | -- | none | 2026-11-17 14:40 UTC | `get_system`, own ship |
| `the_iron_curtain` | The Iron Curtain | asteroid_belt (metallic) | -- | iron_ore: richness 85, 179999 of 180000 left | none | 2026-11-17 14:40 UTC | `get_poi`, own ship |
| `loose_company_belt` | Loose Company Belt | asteroid_belt | -- | nickel_ore: richness 26, 2066 of 20000 left | none | 2026-11-17 14:40 UTC | `get_poi`, own ship |

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
| 2026-11-17 14:40 UTC | own ship | Read The Iron Curtain: 179,999 units left in all | `get_poi`, own ship |
| 2026-11-17 14:40 UTC | own ship | Read Loose Company Belt: 2,066 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
