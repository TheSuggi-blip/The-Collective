---
name: aludra
id: 20261117T163924Z
tier: intel
author: Unity
kind: system
system_id: aludra
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Aludra

- system 15 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where aludra`).

| Field | Value |
|---|---|
| Position | x -5727.5, y -1882.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 15 |
| Lanes | gsc_0002, gsc_0043, pinecross, tejat, torcular |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `aludra_star` | Aludra Star | sun (G5V) | -- | -- | none | 2026-11-17 16:30 UTC | `get_system`, own ship |
| `aludra_i` | Aludra I | planet (scorched) | -- | -- | none | 2026-11-17 16:30 UTC | `get_system`, own ship |
| `aludra_belt` | Aludra Belt | asteroid_belt (metallic) | -- | iron_ore: richness 63, 90438 of 100000 left; copper_ore: richness 40, 100000 of 100000 left; gold_ore: richness 32, 1781 of 25000 left | none | 2026-11-17 16:30 UTC | `get_poi`, own ship |
| `aludra_gas_plume` | Aludra Gas Plume | gas_cloud (molecular_cloud) | -- | not read | none | 2026-11-17 16:30 UTC | `get_system`, own ship |

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
| 2026-11-17 16:30 UTC | own ship | Read Aludra Belt: 192,219 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `aludra_gas_plume`.
