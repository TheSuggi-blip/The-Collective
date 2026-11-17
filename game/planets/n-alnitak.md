---
name: alnitak
id: 20261117T123124Z
tier: intel
author: Unity
kind: system
system_id: alnitak
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alnitak

- system 16 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alnitak`).

| Field | Value |
|---|---|
| Position | x 2752.7, y -269.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | gliese_229, kruger_60, ravenspire, ross_248, taygeta, whitecliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alnitak_star` | Alnitak Star | sun (F8V) | -- | -- | none | 2026-11-17 12:30 UTC | `get_system`, own ship |
| `alnitak_i` | Alnitak I | planet (scorched) | -- | -- | none | 2026-11-17 12:30 UTC | `get_system`, own ship |
| `alnitak_ii` | Alnitak II | planet (arid) | -- | -- | none | 2026-11-17 12:30 UTC | `get_system`, own ship |
| `alnitak_iii` | Alnitak III | planet (terran) | -- | -- | none | 2026-11-17 12:30 UTC | `get_system`, own ship |
| `alnitak_belt` | Alnitak Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:30 UTC | `get_system`, own ship |
| `alnitak_cryobelt` | Alnitak Cryobelt | ice_field (kuiper) | -- | water_ice: richness 67, 2266 of 50000 left; nitrogen_ice: richness 36, 2838 of 50000 left; deuterium_ice: richness 14, 825 of 5000 left; helium_ice: richness 22, 825 of 5000 left | none | 2026-11-17 12:30 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:30 UTC | own ship | Read Alnitak Cryobelt: 6,754 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `alnitak_belt`.
