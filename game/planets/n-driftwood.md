---
name: driftwood
id: 20261117T184416Z
tier: intel
author: Unity
kind: system
system_id: driftwood
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Driftwood

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where driftwood`).

| Field | Value |
|---|---|
| Position | x -1494.6, y -3741.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | beid, castor, cloverfield, cocibolca, ironpeak, zosma |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `driftwood_star` | Driftwood Star | sun (M2V) | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |
| `driftwood_i` | Driftwood I | planet (scorched) | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |
| `driftwood_ii` | Driftwood II | planet (arid) | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |
| `driftwood_iii` | Driftwood III | planet (terran) | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |
| `driftwood_iv` | Driftwood IV | planet (tundra) | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |
| `driftwood_frost_ring` | Driftwood Frost Ring | ice_field (cometary) | -- | water_ice: richness 54, 319 of 50000 left; nitrogen_ice: richness 41, 531 of 50000 left; helium_ice: richness 12, 499 of 5000 left | none | 2026-11-17 18:12 UTC | `get_poi`, own ship |
| `driftwood_ghost_resonance` | Driftwood Ghost Resonance | nebula | -- | -- | none | 2026-11-17 18:12 UTC | `get_system`, own ship |

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
| 2026-11-17 18:12 UTC | own ship | Read Driftwood Frost Ring: 1,349 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
