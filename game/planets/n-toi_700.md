---
name: toi_700
id: 20261117T123211Z
tier: intel
author: Unity
kind: system
system_id: toi_700
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# TOI-700

- system 22 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where toi_700`).

| Field | Value |
|---|---|
| Position | x 5817.4, y 418.0 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 22 |
| Lanes | copperfield, duskmere, rustpoint |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `toi_700_star` | TOI-700 Star | sun (K2V) | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |
| `toi_700_i` | TOI-700 I | planet (scorched) | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |
| `toi_700_ii` | TOI-700 II | planet (arid) | -- | -- | none | 2026-11-17 12:13 UTC | `get_system`, own ship |
| `toi_700_ice_fields` | TOI-700 Ice Fields | ice_field (kuiper) | -- | nitrogen_ice: richness 48, 50000 of 50000 left; deuterium_ice: richness 19, 5000 of 5000 left; helium_ice: richness 22, 5000 of 5000 left | none | 2026-11-17 12:13 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:13 UTC | own ship | Read TOI-700 Ice Fields: 60,000 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
