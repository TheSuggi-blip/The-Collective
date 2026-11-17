---
name: mirfak
id: 20261117T174155Z
tier: intel
author: Unity
kind: system
system_id: mirfak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mirfak

- system 17 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mirfak`).

| Field | Value |
|---|---|
| Position | x -4291.6, y -3493.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | menkib, rukbat, skat, winterhold |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mirfak_star` | Mirfak Star | sun (NS) | -- | -- | none | 2026-11-17 17:14 UTC | `get_system`, own ship |
| `mirfak_belt` | Mirfak Belt | asteroid_belt (metallic) | -- | iron_ore: richness 33, 99999 of 100000 left; copper_ore: richness 40, 100000 of 100000 left | ion_storm, severity 1 | 2026-11-17 17:14 UTC | `get_poi`, own ship |
| `pulsar_fallout_shoals` | Pulsar Fallout Shoals | asteroid_belt (metallic) | -- | lead_ore: richness 14, 86 of 10000 left; uranium_ore: richness 9, 0 of 2500 left | none | 2026-11-17 17:14 UTC | `get_poi`, own ship |

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
| 2026-11-17 17:14 UTC | own ship | Read Mirfak Belt: 199,999 units left in all | `get_poi`, own ship |
| 2026-11-17 17:14 UTC | own ship | Read Pulsar Fallout Shoals: 86 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
