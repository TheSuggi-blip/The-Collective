---
name: guidebook-intel
id: 20261115T205808Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# intel.md -- Guidebook of the Intel Division

Kept by Oracle; read by every member. What the Intel division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Oracle writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/scout.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | None. Reading earns nothing by itself; Intel is measured by the age of the picture and by the leads others turn into income |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| census-voidborn | 64 runs, 8 minutes and -70 cr per run, -560 cr per ship-hour (`routes.py measure`, 22:00 UTC) | 2026-11-15 | Fuel only. Kept: it is the picture every division plans from. With `every_minutes` 30 and `max_ships` 3 the 40 gaps between two reads of one system from 19:20 to 21:48 UTC were 34 to 48 minutes, none over the hour (`data/routes/runs.jsonl`) |
| census-frontier | 16 runs, 12 minutes and -140 cr per run, -630 cr per ship-hour (`routes.py measure`, 22:00 UTC); single runs 8.0 to 22.6 minutes, -78 to -247 cr | 2026-11-15 | Fuel only. Kept on Suggi's word (orders F13, list of 29 systems since 21:45 UTC). No damage in my three test reads (hull 75 of 75 on return) |
| Mining for skill (mine-acubens, mine-gsc-seep, mine-pherkad-rift) | scouts: -148 to -179 cr per ship-hour over 60 runs in the four hours to 21:17 UTC (`board.py all`) | 2026-11-15 | The ore had no buyer. Out of the plan since the handover (orders F8) |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time. Scouts flew voidborn-substrate and
voidborn-missions-1 before the handover (one-time +37,280 and +52,580
cr in the four hours to 21:17 UTC, `board.py all`); ten scouts flew
voidborn-mining-missions from 21:21 UTC.

## 4. Levelling

Which skills this division's pilots need, what trains them fastest and
what it costs: `not measured`. A scout read at 21:20 UTC on 2026-11-15
held piloting 4, navigation 2, exploration 1 (`data/fleet/ships/`);
whether a census read trains exploration is not measured. Piloting 10,
20, 30 and 50 opens hull tiers 2 to 5 (shared skill `fleet-play`,
levelling).

## 5. Ships and Fits

The scouts fly the starter Threshold with its mining laser and pulse
laser. Read 2026-11-15 21:21 UTC (`data/fleet/ships/`): cargo 65 (the
Voidborn cargo bonus left the game with 0.715.3), fuel 95, hull 75.
Fuel: one unit per jump; two scouts read 95 to 90 after five jumps,
and a round trip to a system six jumps out used 15 units (21:39 and
21:50 UTC). The tank holds every frontier system on the list with room
to spare. A better hull or fit for reading: `not measured`.

## 6. How the Census Is Dispatched

- A system opens for a read when its scouting file is `every_minutes`
  old; the first free pilot whose plan holds the census takes the
  oldest. The threshold is the floor of the gap, never its ceiling:
  30 minutes gave gaps of 34 to 71 minutes on 2026-11-15.
- `max_ships` of a census route counts only the census orders of its
  own systems since `game/fleet/dispatch.py` commit fa17b9c
  (2026-11-15 21:32 UTC). Before it, four frontier ships held every
  scout off the home census for eleven minutes.
- In the scouts' plan the home census stands before the frontier
  census: a free scout takes a due home system first.
- A census by hand: `python3 -I -B game/fleet/census.py <pilot>
  <system> --route census-frontier` from the clone; it ends docked at
  Central Nexus when the system has no station.

## 7. Open Tests

- The frontier (orders F13): 29 systems on the list; none of the 18
  read by 21:58 UTC on 2026-11-15 holds a station, so no order book or
  board beyond our border is known yet. What each read found that
  another division can use: `communications/queue.log` ENT-040.
- Predators beyond the border: rainbow leviathans at Atlas, crusher
  mantises at Intercrus (census of 2026-11-15); what they do to a
  starter is Military's to test.
- Pilots of the faction BUSY at veil-ray places at home and beyond
  (`data/intel/sightings.jsonl`, 21:30 and 21:31 UTC): whether they
  hunt the herds is not seen.
- The game moved from 0.715.2 to 0.717.0 on 2026-11-15: read; the
  lines of `game/rules/` it makes wrong are in `requests.log` ENT-038.
