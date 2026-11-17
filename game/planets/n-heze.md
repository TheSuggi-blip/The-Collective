---
name: heze
id: 20261117T123147Z
tier: intel
author: Unity
kind: system
system_id: heze
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Heze

- system 26 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where heze`).

| Field | Value |
|---|---|
| Position | x 3457.4, y -5937.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 26 |
| Lanes | fafnir, gsc_0032, moonshadow |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `heze_star` | Heze Star | sun (K2V) | -- | -- | none | 2026-11-17 12:04 UTC | `get_system`, own ship |
| `heze_i` | Heze I | planet (scorched) | -- | -- | none | 2026-11-17 12:04 UTC | `get_system`, own ship |
| `heze_belt` | Heze Belt | asteroid_belt (metallic) | -- | iron_ore: richness 44, 72397 of 100000 left; copper_ore: richness 41, 99999 of 100000 left; aluminum_ore: richness 42, 2232 of 30000 left; chromium_ore: richness 18, 651 of 9000 left | none | 2026-11-17 12:04 UTC | `get_poi`, own ship |
| `palmglass_field` | Palmglass Field | asteroid_belt | -- | iron_ore: richness 39, 100000 of 100000 left; copper_ore: richness 29, 100000 of 100000 left; trade_crystal: richness 21, 55 of 2900 left | none | 2026-11-17 12:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:04 UTC | own ship | Read Heze Belt: 175,279 units left in all | `get_poi`, own ship |
| 2026-11-17 12:04 UTC | own ship | Read Palmglass Field: 200,055 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
