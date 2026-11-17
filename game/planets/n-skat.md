---
name: skat
id: 20261117T184404Z
tier: intel
author: Unity
kind: system
system_id: skat
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Skat

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where skat`).

| Field | Value |
|---|---|
| Position | x -4128.4, y -3903.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | menkib, mirfak, rukbat, wolf_359 |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `skat_star` | Skat Star | sun (A2V) | -- | -- | none | 2026-11-17 17:58 UTC | `get_system`, own ship |
| `skat_belt` | Skat Belt | asteroid_belt (metallic) | -- | iron_ore: richness 49, 99987 of 100000 left; copper_ore: richness 48, 100000 of 100000 left; aluminum_ore: richness 48, 2470 of 30000 left | none | 2026-11-17 17:58 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:58 UTC | own ship | Read Skat Belt: 202,457 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
