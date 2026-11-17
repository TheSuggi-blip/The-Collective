---
name: acamar
id: 20261117T174222Z
tier: intel
author: Unity
kind: system
system_id: acamar
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Acamar

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where acamar`).

| Field | Value |
|---|---|
| Position | x -790.9, y -5282.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | albali, azelfafage, gsc_0001, gsc_0005, mintaka, nunki |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `acamar_star` | Acamar Star | sun (M2V) | -- | -- | none | 2026-11-17 16:39 UTC | `get_system`, own ship |
| `acamar_i` | Acamar I | planet (scorched) | -- | -- | none | 2026-11-17 16:39 UTC | `get_system`, own ship |
| `acamar_ii` | Acamar II | planet (arid) | -- | -- | none | 2026-11-17 16:39 UTC | `get_system`, own ship |
| `acamar_iii` | Acamar III | planet (terran) | -- | -- | none | 2026-11-17 16:39 UTC | `get_system`, own ship |
| `acamar_iv` | Acamar IV | planet (tundra) | -- | -- | none | 2026-11-17 16:39 UTC | `get_system`, own ship |
| `acamar_belt` | Acamar Belt | asteroid_belt (metallic) | -- | iron_ore: richness 54, 99999 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; manganese_ore: richness 24, 18000 of 18000 left | none | 2026-11-17 16:39 UTC | `get_poi`, own ship |

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
| 2026-11-17 16:39 UTC | own ship | Read Acamar Belt: 217,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
