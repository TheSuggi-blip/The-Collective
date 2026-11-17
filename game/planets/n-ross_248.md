---
name: ross_248
id: 20261117T184407Z
tier: intel
author: Unity
kind: system
system_id: ross_248
standing: neutral
standing_since: 2026-11-17
threat: unknown
empire: -
police_level: 0
updated: 2026-11-17
---

# Ross 248

- system 16 jumps from home, police level 0. Station: The Half Moon.

## Chart

From `game/map/galaxy.tsv` (`python3 scripts/map.py where ross_248`).

| Field | Value |
|---|---|
| Position | x 2275.9, y -408.4 (Galactic Units) |
| Empire | lawless |
| Jumps from home | 16 |
| Lanes | algieba, alnitak, fuyue, kruger_60, struve_2398, taygeta |

## Points of Interest

| POI id | Name | Type | Base and services | Resources | Hazard | When | Source |
|---|---|---|---|---|---|---|---|
| `ross_248_star` | Ross 248 Star | sun (G2V) | -- | -- | none | 2026-11-17 17:51 UTC | `get_system`, own ship |
| `ross_248_i` | Ross 248 I | planet (scorched) | -- | -- | none | 2026-11-17 17:51 UTC | `get_system`, own ship |
| `ross_248_ii` | Ross 248 II | planet (arid) | -- | -- | none | 2026-11-17 17:51 UTC | `get_system`, own ship |
| `ross_248_belt` | Ross 248 Belt | asteroid_belt (metallic) | -- | iron_ore: richness 30, 99999 of 100000 left; copper_ore: richness 42, 100000 of 100000 left | none | 2026-11-17 17:51 UTC | `get_poi`, own ship |
| `ross_248_cryobelt` | Ross 248 Cryobelt | ice_field (kuiper) | -- | not read | none | 2026-11-17 17:51 UTC | `get_system`, own ship |
| `d2efa9771ab643a7c7d4dec20cd3ea34` | The Half Moon | station | `428b353757ef4100317abd39cbdb79bf` | -- | none | 2026-11-17 17:51 UTC | `get_system`, own ship |

## Stations

| Base | Owner | Docking | Services | Fuel price | Market fee | When | Source |
|---|---|---|---|---|---|---|---|
| The Half Moon (`428b353757ef4100317abd39cbdb79bf`) | unknown | not tried | not read | unknown | unknown | 2026-11-17 17:51 UTC | `get_system`, own ship |

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
| 2026-11-17 17:51 UTC | own ship | Read Ross 248 Belt: 199,999 units left in all | `get_poi`, own ship |

## Notes

- Filed by `scripts/intel-planets.py` from one scouting read. Deposits are shared and change by the hour: read again before sending ships.
- Not read yet: `ross_248_cryobelt`.
