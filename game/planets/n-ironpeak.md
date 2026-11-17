---
name: ironpeak
id: 20261117T184411Z
tier: intel
author: Unity
kind: system
system_id: ironpeak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ironpeak

- system 20 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ironpeak`).

| Field | Value |
|---|---|
| Position | x -1881.4, y -3867.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 20 |
| Lanes | beid, castor, driftwood, markeb |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ironpeak_star` | Ironpeak Star | sun (NS) | -- | -- | none | 2026-11-17 18:33 UTC | `get_system`, own ship |
| `ironpeak_i` | Ironpeak I | planet (scorched) | -- | -- | none | 2026-11-17 18:33 UTC | `get_system`, own ship |
| `ironpeak_belt` | Ironpeak Belt | asteroid_belt (metallic) | -- | iron_ore: richness 64, 85096 of 100000 left; copper_ore: richness 44, 100000 of 100000 left; gold_ore: richness 36, 265 of 25000 left | none | 2026-11-17 18:33 UTC | `get_poi`, own ship |
| `ironpeak_weak_superposition` | Ironpeak Weak Superposition | nebula | -- | -- | none | 2026-11-17 18:33 UTC | `get_system`, own ship |

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
| 2026-11-17 18:33 UTC | own ship | Read Ironpeak Belt: 185,361 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
