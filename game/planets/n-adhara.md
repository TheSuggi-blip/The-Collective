---
name: adhara
id: 20261117T082523Z
tier: intel
author: Unity
kind: system
system_id: adhara
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Adhara

- system 10 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where adhara`).

| Field | Value |
|---|---|
| Position | x 492.5, y 3248.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 10 |
| Lanes | mebsuta, pipirima, porrima |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `adhara_star` | Adhara Star | sun (K2V) | -- | -- | none | 2026-11-17 08:08 UTC | `get_system`, own ship |
| `adhara_i` | Adhara I | planet (scorched) | -- | -- | none | 2026-11-17 08:08 UTC | `get_system`, own ship |
| `adhara_ii` | Adhara II | planet (arid) | -- | -- | none | 2026-11-17 08:08 UTC | `get_system`, own ship |
| `adhara_iii` | Adhara III | planet (terran) | -- | -- | none | 2026-11-17 08:08 UTC | `get_system`, own ship |
| `adhara_belt` | Adhara Belt | asteroid_belt (metallic) | -- | iron_ore: richness 58, 578 of 100000 left; copper_ore: richness 45, 6000 of 100000 left; aluminum_ore: richness 67, 82 of 30000 left; gold_ore: richness 33, 56 of 25000 left | none | 2026-11-17 08:08 UTC | `get_poi`, own ship |

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
| 2026-11-17 08:08 UTC | own ship | Read Adhara Belt: 6,716 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
