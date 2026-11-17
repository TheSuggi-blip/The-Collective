---
name: alsuhail
id: 20261117T133327Z
tier: intel
author: Unity
kind: system
system_id: alsuhail
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Alsuhail

- system 24 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where alsuhail`).

| Field | Value |
|---|---|
| Position | x 6317.1, y -1830.2 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 24 |
| Lanes | edasich, gacrux, gsc_0047, netherwick, tegmine, zubeneschamali |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `alsuhail_star` | Alsuhail Star | sun (K2V) | -- | -- | none | 2026-11-17 12:42 UTC | `get_system`, own ship |
| `alsuhail_i` | Alsuhail I | planet (scorched) | -- | -- | none | 2026-11-17 12:42 UTC | `get_system`, own ship |
| `alsuhail_ii` | Alsuhail II | planet (arid) | -- | -- | none | 2026-11-17 12:42 UTC | `get_system`, own ship |
| `alsuhail_iii` | Alsuhail III | planet (terran) | -- | -- | none | 2026-11-17 12:42 UTC | `get_system`, own ship |
| `alsuhail_belt` | Alsuhail Belt | asteroid_belt (metallic) | -- | iron_ore: richness 50, 99548 of 100000 left; copper_ore: richness 27, 100000 of 100000 left; aluminum_ore: richness 63, 864 of 30000 left; chromium_ore: richness 22, 424 of 13000 left | none | 2026-11-17 12:42 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:42 UTC | own ship | Read Alsuhail Belt: 200,836 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
