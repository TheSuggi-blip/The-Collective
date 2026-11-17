---
name: lacaille_9352
id: 20261117T000628Z
tier: intel
author: Unity
kind: system
system_id: lacaille_9352
standing: neutral
standing_since: 2026-11-16
threat: unknown
empire: solarian
police_level: 55
updated: 2026-11-16
---

# Lacaille 9352

Solarian system 9 jumps from home, police level 55. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where lacaille_9352`).

| Field | Value |
|---|---|
| Position | x -766.1, y -128.1 (Galactic Units) |
| Empire | solarian |
| Jumps from home | 9 |
| Lanes | grumium, nova_terra, sirius |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `theta_proxima_star` | Theta Proxima Star | sun (M1V) | -- | -- | none | 2026-11-16 23:41 UTC | `get_system`, own ship |
| `theta_proxima_i` | Theta Proxima I | planet (glacial) | -- | -- | none | 2026-11-16 23:41 UTC | `get_system`, own ship |
| `theta_proxima_ii` | Theta Proxima II | planet (ice_world) | -- | -- | none | 2026-11-16 23:41 UTC | `get_system`, own ship |
| `theta_proxima_belt` | Theta Proxima Belt | asteroid_belt (mixed) | -- | not read | none | 2026-11-16 23:41 UTC | `get_system`, own ship |
| `lacaille_9352_deep_vein` | Lacaille 9352 Deep Vein | asteroid_belt | -- | not read | none | 2026-11-16 23:41 UTC | `get_system`, own ship |

## Stations

None on the chart.

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-16 | None seen on one pass. Police level 55: Low Security (slow police response) | `get_system`, own ship |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-16 | neutral | Unity | Not judged; filed from a scouting read |

## Visits

Append-only, newest last.

| When | By | What was done or seen | Source |
|---|---|---|---|
| 2026-11-16 23:41 UTC | own ship | Passed through and listed the points of interest | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `theta_proxima_belt`, `lacaille_9352_deep_vein`.
