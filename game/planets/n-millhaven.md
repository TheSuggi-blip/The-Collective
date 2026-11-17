---
name: millhaven
id: 20261117T133350Z
tier: intel
author: Unity
kind: system
system_id: millhaven
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Millhaven

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where millhaven`).

| Field | Value |
|---|---|
| Position | x 741.4, y 5624.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | flintrock, skyreach, talitha |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `millhaven_star` | Millhaven Star | sun (M2V) | -- | -- | none | 2026-11-17 13:19 UTC | `get_system`, own ship |
| `millhaven_belt` | Millhaven Belt | asteroid_belt (metallic) | -- | iron_ore: richness 66, 20827 of 100000 left; copper_ore: richness 36, 20824 of 100000 left | none | 2026-11-17 13:19 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:19 UTC | own ship | Read Millhaven Belt: 41,651 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
