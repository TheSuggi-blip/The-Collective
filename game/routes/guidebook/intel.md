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
| -- | -- | -- | None of Intel's own. Reading earns nothing by itself; Intel is measured by the age of the picture and by the leads others turn into income. From the next turn the scouts also hunt between reads (orders.log ENT-008, F16) |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| census-voidborn | 93 runs, 8 minutes and -70 cr per run, -550 cr per ship-hour (`routes.py measure`, 23:45 UTC) | 2026-11-15 | Fuel only. Kept: it is the picture every division plans from. With `every_minutes` 30 and `max_ships` 3, 61 gaps between two reads of one system in the four hours to 23:20 UTC were 33 to 48 minutes, median 38, none over the hour (`data/routes/runs.jsonl`) |
| census-frontier | 35 runs, 14 minutes and -140 cr per run, -600 cr per ship-hour (`routes.py measure`, 23:45 UTC); a third-ring read 15.1 to 15.5 minutes and -156 to -169 cr; Antares by hand 18.7 minutes, -96 cr | 2026-11-15 | Fuel only. Kept on Suggi's word (orders F13). No own ship below full hull at 23:31 UTC (`data/fleet/ships/`) |
| Mining for skill (mine-acubens, mine-gsc-seep, mine-pherkad-rift) | scouts: -148 to -179 cr per ship-hour over 60 runs in the four hours to 21:17 UTC (`board.py all`) | 2026-11-15 | The ore had no buyer. Out of the plan since the handover (orders F8) |

## 3. Missions That Pay Once

The `once` routes stand right after the home census in the plan: every
pilot flies them first, and a route that holds nothing for a pilot
passes it. Before the handover scouts flew voidborn-substrate and
voidborn-missions-1 (one-time +37,280 and +52,580 cr in the four hours
to 21:17 UTC, `board.py all`); ten scouts flew voidborn-mining-missions
from 21:21 UTC and all twenty voidborn-concurrent (3,000 cr each).

| Route | First RESULT lines | In the scout plan since |
|---|---|---|
| voidborn-selling | nine scouts that held Market Participation: Selling, 23:32 UTC: +865 to +876 cr in 3.8 to 5.0 minutes each; ten of twenty held it | 2026-11-15 23:27 UTC |
| voidborn-precedence | the command group's run of 23:20 UTC: +3,896 cr in 15.0 minutes, 4,000 cr once | 2026-11-15 23:42 UTC |
| voidborn-first-hunt-nexus (and -gsc, -acubens, one hunter per herd) | the command group's run of 23:20 UTC: +974 cr in 18.9 minutes, 1,000 cr once | 2026-11-15 23:42 UTC |

## 4. Levelling

Read 2026-11-15 23:34 UTC (`data/fleet/ships/`): piloting 3 for ten
scouts and 4 for ten; navigation 2 for fifteen and 3 for five;
exploration 1 for all twenty; deep core mining 2 to 5 and mining 2 to 4
from the mining of the first day. In the ten minutes to 23:44 UTC the
twenty scouts gained 55 exploration XP, 235 navigation XP (one of them
reached navigation 3 on a third-ring read), 456 piloting XP and 160
trading XP (voidborn-selling): a census read trains piloting and
navigation by its jumps and exploration a little. Piloting 10, 20, 30
and 50 open hull tiers 2 to 5 (shared skill `fleet-play`, levelling);
at today's rate that is not measured yet.

## 5. Ships and Fits

The scouts fly the starter Threshold with its mining laser and pulse
laser. Read 2026-11-15 21:21 UTC (`data/fleet/ships/`): cargo 65 (the
Voidborn cargo bonus left the game with 0.715.3), fuel 95, hull 75.
Fuel: one unit per jump; two scouts read 95 to 90 after five jumps,
and a round trip to a system six jumps out used 15 units (21:39 and
21:50 UTC). The tank holds every frontier system on the list with room
to spare. Fuel beyond the border is cheaper than at home: Hive Antares
2 cr a unit (23:29 UTC), Ironlight Crossroads 7 cr (23:18 UTC), the
fleet's meter at home 12.29 cr. Ironlight Crossroads sells modules a
scout could carry (ship scanner I 1,854 cr, afterburner I 1,768 cr,
23:21 UTC); which fit a scout needs to hunt and to get away is the
next turn's test (orders.log ENT-008, F17): `not measured`.

## 6. How the Census Is Dispatched

- A system opens for a read when its scouting file is `every_minutes`
  old; the first free pilot whose plan holds the census takes the
  oldest. The threshold is the floor of the gap, never its ceiling:
  30 minutes gave gaps of 33 to 71 minutes on 2026-11-15.
- `max_ships` of a census route counts only the census orders of its
  own systems since `game/fleet/dispatch.py` commit fa17b9c
  (2026-11-15 21:32 UTC). Before it, four frontier ships held every
  scout off the home census for eleven minutes.
- In the scouts' plan the home census stands first: it takes at most
  three ships and only when a home system is due, so the missions that
  pay once never hold the hour back (since 23:42 UTC).
- census-frontier carries `requires.empty_hold` since 23:27 UTC (orders
  F13): a ship with more than five units of goods aboard is not sent.
- A list that grows is read at once: twelve systems added at 23:27 UTC
  had eleven ships of the fleet on their way at 23:27:01 UTC (the
  orders files), the route's limit of twelve with the Antares read.
- A census by hand: `python3 -I -B game/fleet/census.py <pilot>
  <system> --route census-frontier` from the clone; it docks at every
  station it finds and saves the book with the depth at the best price
  (`best_buy_qty`, Ironlight Crossroads 23:21 UTC).

## 7. Open Tests

- The frontier (orders F13): 42 systems on the list since 23:27 UTC,
  rings 1 to 3 of our border, Atlas, Intercrus, LHS 1140, Goldcrest
  and Bluerift; all lawless, none a pirate stronghold. The base-site
  line of each read system is in its file in `game/planets/`.
- Order books beyond the border: Ironlight Crossroads (LHS 1140) read,
  no trade with depth to ours (queue.log ENT-046); Hive Antares has no
  market; the Ironlight bases at Goldcrest and Bluerift are outposts
  without services (queue.log ENT-049). The next markets: Korr
  Fortress Station in the pirate stronghold Gliese 581, the Solarian
  stations that F3 keeps us out of (requests.log ENT-067), then The
  Crescent Moon (MOON) eight jumps past the border
  (`data/station/stations.json`).
- Predators beyond the border: rainbow leviathans at Atlas, crusher
  mantises at Intercrus (census of 2026-11-15); what they do to a
  starter is Military's to test.
- BUSY pilots hunt herds in our space and beyond and fight pirates: one
  destroyed a pirate at Thornhaven at 23:07 UTC (`data/station/battles.json`);
  none has fired on a ship of ours (`game/factions/n-busy.md`).
- The game stood at 0.717.0 at 23:33 UTC; the lines of `game/rules/`
  it makes wrong are in `requests.log` ENT-038.
