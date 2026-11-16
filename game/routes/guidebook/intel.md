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

## Standing Plan

What the scouts fly between two turns, from `game/routes/plans/scout.json`
(last changed in the Intel turn of 2026-11-16 12:15 UTC, commit 7c43485),
checked against `hive.py standing` at 12:16 UTC and `fill.py status scout`
at 12:16 and 12:20 UTC. Twenty ships; a free ship takes the first route
open to it, in this order.

| # | Route | Ships | Expected, credits per ship-hour | Why |
|---|---|---|---|---|
| 1 | voidborn-first-steps-board | 3 at a time for the whole fleet (Trade's limit, Acubens carbon) | about 920 cr once a run in about 12 minutes (Trade's runs, queue.log ENT-095) | Orders ENT-014, EVERY ADMIRAL (c): the once line of the Central Nexus board heads every plan. 5 scouts wait for it at 12:20 UTC |
| 2 | voidborn-network-expansion | up to 20 for the fleet; 11 flew it at 12:20 UTC | 1,440 measured (fill.py status), 1,500 cr once in about 8 minutes | The link after First Steps |
| 3 | voidborn-collective-provides | 2 for the fleet (GSC-0049 nickel) | +2,188 cr in 48 minutes, 2,500 cr once (Trade's test) | Empty hold; opens the next links |
| 4 | voidborn-signal-protocol | up to 20 | +3,409 cr in 14 minutes, 3,500 cr once (Trade's test) | Asks The Collective Provides booked |
| 5 | voidborn-signal-fragments | up to 10 for the fleet; navigation 3 only | 12 scout runs from 08:15 UTC, +82,646 cr in 203 minutes with 84,000 paid once (`data/routes/runs.jsonl`) | Every scout with navigation 3 holds it booked; the nine with navigation 2 fly it when they reach 3 |
| 6 | census-voidborn | at most 3, only when a home system is 30 minutes old | -525 (65 scout runs, 08:15 to 12:21 UTC) | Every Voidborn system read within the hour: 67 gaps in four hours, median 36 minutes, longest 44 |
| 7 | voidborn-first-hunt-intercrus-belt | 1, herd floor 3 | 3 of 7 runs paid +816 to +841 cr with 1,000 once, in 35 to 53 minutes; 4 left at once, a ship not ours at the place (09:12 to 12:00 UTC) | 11 scouts hold First Hunt unfinished; the belt read 13 belt-grazers at 12:10 UTC |
| 8 | voidborn-first-hunt-intercrus-sootfall | 1, a test, herd floor 3 | not measured; written 12:18 UTC | Sootfall Belt read 16 belt-grazers and no pilot not ours at 11:48 UTC |
| 9 | mission-cracking-the-shell-central | 1 (Unity's place at GSC-0041 Frost Ring, herd floor 3) | 1,500 cr once; 1 of 4 scout runs paid since 08:15 UTC | Three scouts hold it unfinished |
| 10 | voidborn-precedence, -selling, -concurrent, -substrate, -missions-1, -mining-missions | 0: every scout holds these booked or done | one-time | A pilot born later flies them first |
| 11 | voidborn-conductive-lattice | 10 at a time for the fleet, Trade's limit | 8 scout runs from 08:15 UTC: +86,966 cr with 88,776 paid once | Every scout has it booked at 12:20 UTC |
| 12 | hunt-atlas-gas-pocket | 1, when 4 halo-drifters and cinder-sylphs stand together | 2 runs from 08:15 UTC: +514 cr in 20 minutes, 1,519 per ship-hour; about 3,600 over its first four runs | A ship not ours left two of its last three runs early |
| 13 | hunt-test-homam-frost-moth | 1, herd floor 4 | 2 runs from 08:15 UTC: +2,147 cr in 31 minutes, 4,142 per ship-hour | Superfluid vials at 600 cr; a ship not ours at the place in both runs |
| 14 | census-frontier | up to 12 for the fleet; 4 flew at 12:16 UTC | -640 (11 scout runs from 08:15 UTC) | 51 lawless systems, each again after 240 minutes (orders F13) |
| 15 | park | the rest | 0 | A docked ship costs nothing |

Expected for the four hours: the once line carries most scouts (about
8,000 cr once a pilot from First Steps to The Signal Protocol, by
Trade's tests), two to three read home, about one reads the frontier,
two fly First Hunt, one hunts at Atlas or Homam when the herd and the
place allow. Once the line is flown, about 15 scouts wait docked: no
repeating work that pays stands open to a scout beyond the two hunts
(the cinder-sylph and veil-ray herds are Military's, one hunter each;
ice needs a harvester and Mining holds the places). Steady money -127
credits per ship-hour over all twenty ships in the four hours to 12:16
UTC (-10,123 cr over 80 ship-hours, `hive.py standing`), with 178,276
cr paid once, against the scale of 6,578 (mine-wolf-1061-vent, `hive.py
tasks`). What would change it: a herd of a species whose drop sells,
read with no ship not ours at it; a free place on another division's
paying route with its Admiral's word and the tool it needs; a deposit
of uranium, thorium, seam glass or palladium (bid at every station we
read, section 7).

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| hunt-atlas-gas-pocket (halo-drifters and cinder-sylphs) | 4 runs at the place, 71 minutes in all: +1,259 cr (2 halo-drifters, 03:11 UTC, as the test), +839 cr (2 cinder-sylphs, 04:24 UTC), +1,799 cr (2 kills, 4 ember glands at 480 cr, 06:03 UTC), +370 cr (1 kill, left: a ship not ours at the place, 07:47 UTC); about 3,600 per ship-hour (`data/routes/runs.jsonl`) | 2026-11-16 | One hunter, no hunt below 4 animals of the two species together. Apophis gave the herd to Intel (queue.log ENT-065) |
| hunt-test-homam-frost-moth | 3 runs, 42 minutes in all: -132 cr (04:24 UTC), +1,079 cr (1 kill, 2 superfluid vials sold at 600 cr, 05:07 UTC), -132 cr (06:47 UTC); about 1,160 per ship-hour (`data/routes/runs.jsonl`) | 2026-11-16 | A ship not ours stood at the place in all three runs and each left early: the herd pays when the place is free. Stays one ship |
| -- | -- | -- | Before it, none of Intel's own. Reading earns nothing by itself; Intel is measured by the age of the picture and by the leads others turn into income. From the next turn the scouts also hunt between reads (orders.log ENT-008, F16) |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| census-voidborn | 93 runs, 8 minutes and -70 cr per run, -550 cr per ship-hour (`routes.py measure`, 23:45 UTC) | 2026-11-15 | Fuel only. Kept: it is the picture every division plans from. With `every_minutes` 30 and `max_ships` 3, 61 gaps between two reads of one system in the four hours to 23:20 UTC were 33 to 48 minutes, median 38, none over the hour (`data/routes/runs.jsonl`) |
| census-frontier, read again | 35 reads from 2026-11-15 23:00 to 2026-11-16 03:04 UTC with both wallets read: mean -158 cr, median -156, -77 to -260, 14.5 minutes (`data/routes/runs.jsonl`) | 2026-11-16 | Fuel only. A refuel where it is cheap changes little: Hive Antares and Ironlight Crossroads are the only stations of the 42 systems that sell fuel, and about half of a read's 13 units (158 cr at the fleet's 11.86 cr a unit) could be bought there: about 70 cr saved on an Antares read and 30 on an LHS 1140 read, under 2% of the round's 6,600 cr (an estimate; units per read not recorded) |
| census-frontier | 35 runs, 14 minutes and -140 cr per run, -600 cr per ship-hour (`routes.py measure`, 23:45 UTC); a third-ring read 15.1 to 15.5 minutes and -156 to -169 cr; Antares by hand 18.7 minutes, -96 cr | 2026-11-15 | Fuel only. Kept on Suggi's word (orders F13). No own ship below full hull at 23:31 UTC (`data/fleet/ships/`) |
| voidborn-first-hunt-intercrus-belt, -intercrus-remnants, -gsc-0031 (First Hunt at three herds beyond the border) | 3 runs at 03:11 UTC: objectives not done, -143 to -154 cr each, 15.0 to 20.7 minutes; two pilots held the mission from a failed home run, so The Experiment did not offer it; the ships were seen at other places of the systems | 2026-11-16 | Cause not found (requests.log ENT-092, ENT-113: the rows hold no cause). Out of the plan since b09dd88; voidborn-first-hunt-gsc-0031 paid 5 of its 7 later runs (section 3) and is back since bf627b0, -intercrus-belt back as a re-test since 61d5518 |
| hunt-test-amberfall-sift-ray (with chlorophage), hunt-test-stormwatch-lantern-slug, hunt-test-nightveil-rivetshell | one run each: -110, -110 and +496 cr; drops of crystallized biogas (4), creature carapace (2) and creature carapace with raw xeno meat (3), bid 1 to 2 cr; the lantern-slug run left after 1 kill, a ship not ours at the place; the rivetshell run's +496 cr was a neural soma from the hold sold at 617 cr | 2026-11-16 | The drops do not sell. Out of the plan by 03:43 UTC |
| voidborn-first-hunt-nexus, -gsc, -acubens for scouts | 4 scout runs from 02:01 to 02:49 UTC, objectives not done, -26 to -55 cr each; the three herds read 1, 3 and 0 belt-grazers at 02:37 to 03:04 UTC (`data/wildlife/`) | 2026-11-16 | Too many first hunters for three home herds. Out of the scout plan since 784ac51; the three herds beyond the border that took their place failed too (row above) |
| voidborn-first-hunt-gsc-0031 | 13 scout runs from 08:15 to 11:36 UTC, 1 paid (+857 cr, 10:11 UTC), 12 ended "kills 0 in 0 min", -1,892 cr steady with 1,000 paid once (`data/routes/runs.jsonl`); GSC-0031 Belt read 0 belt-grazers and 4 patina-grazers at 11:45 UTC (`data/wildlife/gsc_0031.json`) | 2026-11-16 | The herd was spent by First Hunts of four plans, and the route had no herd floor. Out of the plan since 7c43485; the hunt step names `min_creatures` 3, which closes it while the place's census is under 90 minutes old |
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
| voidborn-first-steps | two scouts, 04:32 and 04:35 UTC: +935 cr each in 8.7 and 9.8 minutes, 1,000 cr once; 12 of 20 scouts held the mission and the scout plan had not carried the route since it was switched on again | 2026-11-16 04:23 UTC |
| voidborn-conductive-lattice | 11 scout runs after the runner fix of 04:49 UTC: +119,394 cr in 404 minutes, 122,067 cr of it paid once (11,097 per pilot), so +10,854 cr a pilot in about 37 minutes; from 04:27 to 04:49 UTC every scout run had crashed at the silver buy without a row (errors.log ENT-039, ENT-040) | 2026-11-16 04:57 UTC |
| voidborn-signal-fragments | none by a scout by 08:27 UTC; five runs of other plans, 07:13 to 07:55 UTC: +6,792 to +6,883 cr in 18.0 to 26.1 minutes, 7,000 cr once; offered only from navigation 3 (`requires.skills`) | 2026-11-16 08:16 UTC |
| voidborn-first-hunt-gsc-0031 | 8 runs from 03:11 UTC: one scout run failed (03:11 UTC), 5 of the 7 later runs paid +846 cr in about 31 minutes, each by a pilot that already held the mission | 2026-11-16 08:24 UTC |
| voidborn-network-expansion, -first-steps-board, -collective-provides, -signal-protocol (Trade's once line of the Central Nexus board) | Trade's tests, queue.log ENT-091, ENT-095, ENT-096: +922 to +3,409 cr each; 11 scouts on Network Expansion within two minutes of the commit (fill.py status, 12:20 UTC) | 2026-11-16 12:18 UTC |
| voidborn-first-hunt-nexus (and -gsc, -acubens, one hunter per herd) | the command group's run of 23:20 UTC: +974 cr in 18.9 minutes, 1,000 cr once | 2026-11-15 23:42 UTC to 2026-11-16 03:11 UTC: out when the herds ran empty (section 2) |

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

Read 2026-11-16 between 03:02 and 03:16 UTC (`hive.py levels`): Piloting 3, 4 and 5 (lowest,
median, highest; it was 3 and 4 at 23:34 UTC), 121 Piloting XP an hour
per pilot on average since birth, so 102 hours to Piloting 10 at that
rate. First Hunt gives 50 Weapons, 15 Xenobiology and 20 Piloting XP
once; the species tests train Weapons and Xenobiology.

Read 2026-11-16 08:16 to 08:30 UTC (`data/fleet/ships/`, `hive.py levels`):
Piloting 3, 5 and 5 (lowest, median, highest), 100 Piloting XP an hour
per pilot on average since birth, 121 hours to Piloting 10 at that rate.
Navigation 3 or 4 for eleven scouts and 2 for nine: navigation 3 opens
Signal Fragments (7,000 cr once), so the nine with navigation 2 are sent
the census first; what one census read adds to navigation is not
measured.

Read 2026-11-16 12:22 UTC (`hive.py levels`): Piloting 3, 5 and 5
(lowest, median, highest), 91 Piloting XP an hour per pilot on average
since birth, 131 hours to Piloting 10 at that rate (121 at 08:30 UTC:
the once missions of the period are short and train little Piloting);
median navigation 3, exploration 2 (1 at 2026-11-15 23:34 UTC), mining
2, deep core mining 3.

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

- Species tests from 2026-11-16 03:11 UTC, one scout each: halo-drifter
  pays (noble condensate, section 1); sift-ray, chlorophage,
  lantern-slug and rivetshell do not (section 2). A drop without a
  bid of 50 cr is stored, so the run row shows it. Military tests five
  other species at the same time (`guidebook/military.md`).
- Leads no field we read holds (`data/scouting/`, read 2026-11-16 between 03:02 and 03:16 UTC):
  tritium ice (bid 400 cr for 2,000 at each of five stations of ours and
  973 at Ironlight Crossroads), caustic sac (420 cr, 50 at seven), void-
  charged ichor (1,142 cr, 517), control nodes and quantum silk. Uranium,
  thorium and tungsten ore stand at 0 in the home belts that held them.
- Solarian law (get_empire_info, read 2026-11-16 by one scout): foreigners
  pay 3% sales tax and a fuel surcharge of 6 cr a unit; eight goods are
  contraband (fine 2x their value); an attack in policed space carries a
  500 cr bounty. Nova Terra Central was read by one scout with an empty
  hold at 03:22 UTC (requests.log ENT-073): 517 items, 16 price gaps with
  our books, the deepest 73 units; 304 cr for the round trip of about 25
  minutes (`game/planets/n-nova_terra.md`).
- Base sites beside the best ice (queue.log ENT-067): Achernar, Alnair,
  Wolf 1061 in that order; Ruchbah and Intercrus not advised. The same
  three as station sites for S6 (queue.log ENT-090, 2026-11-16 08:30
  UTC): Achernar first as the only one with belt, gas and ice (iron and
  copper ore 99,997 of 100,000 each); each system's file in
  `game/planets/` holds its line "Station site (S6)".
- Crimson law (get_empire_info, read 2026-11-16 08:18 UTC, queue.log
  ENT-089): a Voidborn visitor pays 4% sales tax on what it buys and a
  fuel surcharge of 4 cr a unit; income and property tax fall on
  citizens; the contraband list is the Solarian one. The Rampart
  Checkpoint lies 17 jumps out and Blood Forge 20, behind 13 lawless
  systems of which 9 are unread.
- Ores bid everywhere and sold nowhere at the bid (station/market.json and
  our books, 2026-11-16 12:16 UTC): uranium ore 300 cr (5,871 units at
  the best price over our eight books; asked only by Nebula at 500 and
  the Outer Rim), thorium ore 240 cr (6,246), seam glass 1,200 cr (333 at
  each of our seven books, base value 600, made into annealed seam
  glass), palladium ore 358 cr (43,450 at four). Every uranium and
  thorium deposit we read stands at 0 of 5,000 (Acubens Belt, Bellatrix
  Major Belt at Node Gamma, Nova Terra Industrial Belt); no field we read
  holds seam glass. The capacity tool names the tool for uranium and
  thorium as `rad`, carried by none of ours. A deposit of either beyond
  the frontier is the largest lead of the picture.
- The game stood at 0.719.0 at 12:24 UTC (https://spacemolt.com/changelog,
  1,875 releases): no release since the turn of 08:15 UTC.
- Pirates in the fourth ring: one at Gliese 876 (Stillwork Belt) and one
  at Felis (Felis Dim Lattice), census of 04:40 UTC (`data/wildlife/`).

- The frontier (orders F13): 51 systems on the list since 2026-11-16
  04:31 UTC: rings 1 to 3 of our border, Atlas, Intercrus, LHS 1140,
  Goldcrest, Bluerift, and the next ring (Marfik, Acrab, Acrux, Botein,
  Deepwell, Felis, Gliese 876, HD 147513, Rastaban), 6 or 7 jumps from
  home; all lawless, none a pirate stronghold (Gliese 581 stays off).
  All nine new systems were taken by ships of three plans within two
  minutes of the commit. The base-site
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
  it makes wrong are in `requests.log` ENT-038. At 0.719.0 on
  2026-11-16 08:17 UTC: starter ships pay no property tax (0.717.1),
  five prestige hulls (0.718.0), a faction board of pirates destroyed
  (0.719.0); the lines they make wrong are in `requests.log` ENT-119.
