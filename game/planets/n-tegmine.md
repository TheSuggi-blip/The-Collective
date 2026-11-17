---
name: tegmine
id: 20261117T143553Z
tier: intel
author: Unity
kind: system
system_id: tegmine
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Tegmine

- system 25 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where tegmine`).

| Field | Value |
|---|---|
| Position | x 6200.3, y -2232.5 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 25 |
| Lanes | alsuhail, edasich, gacrux, paikauhale |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `tegmine_star` | Tegmine Star | sun (K2V) | -- | -- | none | 2026-11-17 13:39 UTC | `get_system`, own ship |
| `tegmine_belt` | Tegmine Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 13:39 UTC | `get_system`, own ship |
| `tegmine_emission_nebula` | Tegmine Emission Nebula | gas_cloud (emission) | -- | not read | none | 2026-11-17 13:39 UTC | `get_system`, own ship |
| `tegmine_frost_ring` | Tegmine Frost Ring | ice_field (kuiper) | -- | not read | none | 2026-11-17 13:39 UTC | `get_system`, own ship |
| `tegmine_armored_shelf` | Tegmine Armored Shelf | asteroid_belt | -- | iron_ore: richness 37, 99685 of 100000 left; copper_ore: richness 33, 99985 of 100000 left; titanium_ore: richness 37, 20 of 25000 left | none | 2026-11-17 13:39 UTC | `get_poi`, own ship |

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
| 2026-11-17 13:39 UTC | own ship | Read Tegmine Armored Shelf: 199,690 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `tegmine_belt`, `tegmine_emission_nebula`, `tegmine_frost_ring`.
