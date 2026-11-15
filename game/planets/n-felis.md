---
name: felis
id: 20261115T235516Z
tier: intel
author: Unity
kind: system
system_id: felis
standing: neutral
standing_since: 2026-11-15
threat: unknown
empire: -
police_level: 0
updated: 2026-11-15
---

# Felis

- system 7 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where felis`).

| Field | Value |
|---|---|
| Position | x -2560.1, y 4632.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 7 |
| Lanes | biham, gliese_876, gsc_0016, gsc_0021, sualocin, tanglewood |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `felis_star` | Felis Star | sun (M6V) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_i` | Felis I | planet (scorched) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_ii` | Felis II | planet (arid) | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_belt_a` | Felis Belt A | asteroid_belt (metallic) | -- | not read | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_belt_b` | Felis Belt B | asteroid_belt (metallic) | -- | nothing listed | none | 2026-11-15 23:34 UTC | `get_poi`, own ship |
| `felis_frost_ring` | Felis Frost Ring | ice_field (cometary) | -- | not read | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_dim_lattice` | Felis Dim Lattice | nebula | -- | -- | none | 2026-11-15 23:34 UTC | `get_system`, own ship |
| `felis_dark_residue` | Felis Dark Residue | asteroid_belt | -- | not read | none | 2026-11-15 23:34 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-15 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-15 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-15 23:34 UTC | own ship | Read Felis Belt B: nothing left | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `felis_belt_a`, `felis_frost_ring`, `felis_dark_residue`.
