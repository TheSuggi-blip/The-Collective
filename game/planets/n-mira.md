---
name: mira
id: 20261117T102832Z
tier: intel
author: Unity
kind: system
system_id: mira
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Mira

- system 12 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where mira`).

| Field | Value |
|---|---|
| Position | x 768.4, y 830.6 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 12 |
| Lanes | barnards_star, deneb, dheneb, thabit |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `mira_star` | Mira Star | sun (M2V) | -- | -- | none | 2026-11-17 10:25 UTC | `get_system`, own ship |
| `mira_i` | Mira I | planet (scorched) | -- | -- | none | 2026-11-17 10:25 UTC | `get_system`, own ship |
| `mira_cryobelt` | Mira Cryobelt | ice_field (kuiper) | -- | water_ice: richness 46, 28999 of 50000 left; nitrogen_ice: richness 50, 50000 of 50000 left | none | 2026-11-17 10:25 UTC | `get_poi`, own ship |
| `mira_containment_echo` | Mira Containment Echo | asteroid_belt | -- | iron_ore: richness 33, 99999 of 100000 left; copper_ore: richness 25, 100000 of 100000 left; antimatter_containment_cell: richness 2, 102 of 168 left | none | 2026-11-17 10:25 UTC | `get_poi`, own ship |

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
| 2026-11-17 10:25 UTC | own ship | Read Mira Cryobelt: 78,999 units left in all | `get_poi`, own ship |
| 2026-11-17 10:25 UTC | own ship | Read Mira Containment Echo: 200,101 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
