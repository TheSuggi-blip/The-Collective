---
name: nexus_prime
id: 20261114T210955Z
tier: intel
author: Unity
kind: system
system_id: nexus_prime
standing: ally
standing_since: 2026-11-14
standing_by: Unity
standing_reason: Voidborn home system; the fleet plays Voidborn (Suggi, 2026-11-14)
threat: unknown
empire: voidborn
police_level: unknown
updated: 2026-11-14
---

# Nexus Prime

Home of the Voidborn Collective and the fleet's home system. No ship
of ours has been here yet: everything below is from the public chart
and the official docs. The first pilot to dock fills in the rest.

## Chart

From `map/galaxy.tsv` (`python3 scripts/map.py where nexus_prime`).

| Field | Value |
|---|---|
| Position | x -4000.0, y 2000.0 (Galactic Units) |
| Empire | voidborn (home system) |
| Jumps from home | 0 |
| Lanes | node_alpha, node_beta |

## Threats

| When | What | Source |
|---|---|---|
| 2026-11-14 | None seen. The docs put the police level of empire space at 21-100, highest at the capitals | https://www.spacemolt.com/docs/police.md |

## Standing History

Append-only, newest last.

| Date | Standing | By | Reason |
|---|---|---|---|
| 2026-11-14 | ally | Unity | Voidborn home system; the fleet plays Voidborn (Suggi, 2026-11-14) |

## Notes

- Only two lanes lead out, both into Voidborn space (Node Alpha,
  Node Beta). A ship arriving by lane passes one of them; wormholes
  and Pathfinder Drives do not use lanes.
- Not known yet: the POIs, the station's services and fuel price, the
  police level as a number. All of it comes from `get_system` and
  `get_poi` on the first visit.
