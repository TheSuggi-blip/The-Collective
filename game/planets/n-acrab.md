---
name: acrab
id: 20261116T050015Z
tier: intel
author: Unity
kind: system
system_id: acrab
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: -
police_level: 0
updated: 2026-11-16
---

# Acrab

- system 6 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where acrab`).

| Field | Value |
|---|---|
| Position | x -5944.8, y 2389.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 6 |
| Lanes | atria, duskfield, gsc_0049, marfik, nightveil |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `acrab_star` | Acrab Star | sun (K6V) | -- | -- | none | 2026-11-16 04:38 UTC | `get_system`, own ship |
| `acrab_belt` | Acrab Belt | asteroid_belt (metallic) | -- | iron_ore: richness 62, 98916 of 100000 left; copper_ore: richness 26, 99999 of 100000 left | none | 2026-11-16 04:38 UTC | `get_poi`, own ship |
| `thinspace_rubble` | Thinspace Rubble | asteroid_belt | -- | iron_ore: richness 28, 100000 of 100000 left; copper_ore: richness 26, 100000 of 100000 left; null_matter: richness 10, 594 of 594 left | none | 2026-11-16 04:38 UTC | `get_poi`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 0: Lawless (no police protection) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 04:38 UTC | own ship | Read Acrab Belt: 198,915 units left in all | `get_poi`, own ship |
| 2026-11-16 04:38 UTC | own ship | Read Thinspace Rubble: 200,594 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
