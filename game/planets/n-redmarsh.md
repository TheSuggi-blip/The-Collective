---
name: redmarsh
id: 20261117T133358Z
tier: intel
author: Unity
kind: system
system_id: redmarsh
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Redmarsh

- system 26 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where redmarsh`).

| Field | Value |
|---|---|
| Position | x 6686.1, y -1001.1 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 26 |
| Lanes | gsc_0007, netherwick, sceptrum |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `redmarsh_belt_a` | Redmarsh Belt A | asteroid_belt (metallic) | -- | iron_ore: richness 31, 99999 of 100000 left; copper_ore: richness 36, 99999 of 100000 left; aluminum_ore: richness 59, 29233 of 30000 left; lithium_ore: richness 43, 5699 of 25000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |
| `redmarsh_belt_b` | Redmarsh Belt B | asteroid_belt (metallic) | -- | iron_ore: richness 43, 100000 of 100000 left; copper_ore: richness 21, 100000 of 100000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |
| `redmarsh_gas_pocket` | Redmarsh Gas Pocket | gas_cloud (molecular_cloud) | -- | hydrogen_gas: richness 51, 20873 of 50000 left; argon_gas: richness 53, 49999 of 50000 left; neon_gas: richness 41, 50000 of 50000 left | none | 2026-11-17 12:50 UTC | `get_poi`, own ship |

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
| 2026-11-17 12:50 UTC | own ship | Read Redmarsh Belt A: 234,930 units left in all | `get_poi`, own ship |
| 2026-11-17 12:50 UTC | own ship | Read Redmarsh Belt B: 200,000 units left in all | `get_poi`, own ship |
| 2026-11-17 12:50 UTC | own ship | Read Redmarsh Gas Pocket: 120,872 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
