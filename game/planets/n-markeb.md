---
name: markeb
id: 20261117T184409Z
tier: intel
author: Unity
kind: system
system_id: markeb
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: outerrim
police_level: 30
updated: 2026-11-17
---

# Markeb

Outerrim system 19 jumps from home, police level 30. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where markeb`).

| Field | Value |
|---|---|
| Position | x -1956.7, y -3444.8 (Galactic Units) |
| Empire | outerrim |
| Jumps from home | 19 |
| Lanes | beid, first_step, ironpeak, void_gate |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `markeb_star` | Markeb Star | sun (B2IV) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_i` | Markeb I | planet (scorched) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_ii` | Markeb II | planet (scorched) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_iii` | Markeb III | planet (scorched) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_iv` | Markeb IV | planet (jovian) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_v` | Markeb V | planet (scorched) | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |
| `markeb_belt` | Markeb Belt | asteroid_belt (mixed) | -- | carbon_ore: richness 51, 27 of 30000 left; uranium_ore: richness 15, 38 of 5000 left; lead_ore: richness 16, 23 of 20000 left; radium_ore: richness 6, 59 of 2000 left; aluminum_ore: richness 62, 25 of 30000 left | none | 2026-11-17 18:09 UTC | `get_poi`, own ship |
| `markeb_quantum_eddy` | Markeb Quantum Eddy | nebula | -- | -- | none | 2026-11-17 18:09 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-17 | None seen on one pass. Police level 30: Frontier (minimal police presence) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-17 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-17 18:09 UTC | own ship | Read Markeb Belt: 172 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
