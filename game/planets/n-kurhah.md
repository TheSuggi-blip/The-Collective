---
name: kurhah
id: 20261117T133348Z
tier: intel
author: Unity
kind: system
system_id: kurhah
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Kurhah

- system 17 jumps from home, police level 0. Station: Lantern Facet Post.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where kurhah`).

| Field | Value |
|---|---|
| Position | x -66.3, y -3661.9 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 17 |
| Lanes | frostpeak, maia, wazn, zibal |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `kurhah_star` | Kurhah Star | sun (M6V) | -- | -- | none | 2026-11-17 12:36 UTC | `get_system`, own ship |
| `kurhah_belt` | Kurhah Belt | asteroid_belt (metallic) | -- | not read | none | 2026-11-17 12:36 UTC | `get_system`, own ship |
| `kurhah_frozen_drift` | Kurhah Frozen Drift | ice_field (cometary) | -- | not read | none | 2026-11-17 12:36 UTC | `get_system`, own ship |
| `kurhah_wild_facets` | Kurhah Wild Facets | asteroid_belt | -- | iron_ore: richness 28, 100000 of 100000 left; copper_ore: richness 34, 100000 of 100000 left; trade_crystal: richness 18, 27 of 2800 left | none | 2026-11-17 12:36 UTC | `get_poi`, own ship |
| `b78e7212e21a90dc977a6fc751e8f97d` | Lantern Facet Post | station | `44ef660b02963348a35f18fe1e1410f8` | -- | none | 2026-11-17 12:36 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| Lantern Facet Post (`44ef660b02963348a35f18fe1e1410f8`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 12:36 UTC | `get_system`, own ship |

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
| 2026-11-17 12:36 UTC | own ship | Read Kurhah Wild Facets: 200,027 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `kurhah_belt`, `kurhah_frozen_drift`.
