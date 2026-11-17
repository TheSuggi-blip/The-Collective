---
name: quarrytown
id: 20261117T153753Z
tier: intel
author: Unity
kind: system
system_id: quarrytown
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Quarrytown

- system 21 jumps from home, police level 0. No station on the chart.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where quarrytown`).

| Field | Value |
|---|---|
| Position | x 4736.4, y -723.8 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 21 |
| Lanes | alshat, edgewater, kepler_62, northwick, undercliff |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `quarrytown_belt` | Quarrytown Belt | asteroid_belt (metallic) | -- | iron_ore: richness 53, 100000 of 100000 left; copper_ore: richness 40, 100000 of 100000 left; lithium_ore: richness 25, 25000 of 25000 left | none | 2026-11-17 15:04 UTC | `get_poi`, own ship |
| `quarrytown_cryobelt` | Quarrytown Cryobelt | ice_field (cometary) | -- | water_ice: richness 63, 1587 of 50000 left; nitrogen_ice: richness 30, 1594 of 50000 left; deuterium_ice: richness 15, 629 of 5000 left; helium_ice: richness 16, 629 of 5000 left | none | 2026-11-17 15:04 UTC | `get_poi`, own ship |

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
| 2026-11-17 15:04 UTC | own ship | Read Quarrytown Belt: 225,000 units left in all | `get_poi`, own ship |
| 2026-11-17 15:04 UTC | own ship | Read Quarrytown Cryobelt: 4,439 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
