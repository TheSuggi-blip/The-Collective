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
(commit c82bd8d, 2026-11-16 04:57 UTC), checked against `hive.py standing`
at 04:48 UTC and again after the commit. Twenty ships; a free ship takes the first route open to it,
in this order.

| # | Route | Ships | Expected, credits per ship-hour | Why |
|---|---|---|---|---|
| 1 | census-voidborn | at most 3, only when a home system is 30 minutes old; about 2.3 on average | -550 (measured) | Every Voidborn system read within the hour: 65 gaps in the four hours to 04:17 UTC, median 36 minutes, longest 43 |
| 2 | voidborn-precedence, -selling, -concurrent, -substrate, -missions-1, -mining-missions | 0: every scout holds these booked or done | one-time | A pilot born later flies them first |
| 3 | voidborn-first-steps | 2 at a time, the fleet's limit (Logistics' route) | 935 cr once a run in about 10 minutes, 2 scout runs this turn | 11 scouts held First Steps in the Void at 04:44 UTC; the route skips a pilot that does not hold it, and two holders count as done from skipped runs of 2026-11-15 (one is flown by hand) |
| 4 | voidborn-conductive-lattice | up to 6 at a time and 30 pilots in all, Mercury's limits | +10,893 cr once per pilot in about 32 minutes (six trader runs before 01:09 UTC); no scout run measured yet | The runner fault that crashed every run since 01:09 UTC is fixed since 04:49 UTC (requests.log ENT-098); orders.log ENT-012 puts the chain in every plan. Seven scouts hold Conductive Lattice and go on at the buy stop |
| 5 | hunt-atlas-gas-pocket | 1, when 4 halo-drifters and cinder-sylphs stand together | 2 runs at the place: +1,259 and +839 cr in 18.7 minutes each, about 3,360 per ship-hour | Noble condensate 690 cr and ember glands 480 cr, bid about 50 deep at all six stations |
| 6 | hunt-test-homam-frost-moth | 1 | first run left, -132 cr: two pilots not ours at the place | Frost-moths are the one untested grazer of 100 hull or less with a herd of four or more |
| 7 | census-frontier | up to 12; about 3 on average with 51 systems | -620 (measured, 77 runs) | 51 lawless systems since 04:31 UTC, each again after 240 minutes (orders F13) |
| 8 | park | the rest | 0 | A docked ship costs nothing |

The chain was out of the plan from 04:44 to 04:57 UTC: every run of it
from 01:09 UTC had crashed at the silver buy (errors.log ENT-039,
ENT-040); it came back when the fix was written done (requests.log
ENT-098, ENT-099). Its first scout RESULT line after the fix is the
check of the next turn.

Expected for the four hours: about five ships read, one or two hunt, the
First Steps holders take two places at a time until all have flown it
(about an hour), and the chain takes up to six scouts at a time for about
32 minutes each as far as the silver at Ironlight Crossroads carries
(Trade's ten traders take the 200 units of this hour, queue.log ENT-074).
The rest wait docked: no repeating paying work stands open to a scout
beyond these (the veil-ray
and cinder-sylph herds are Military's, one hunter each; ice and gas need
harvesters and the Admiral's word). Steady money -107 credits per
ship-hour over all twenty ships (the four hours to 04:48 UTC, -8,586 cr
over 80 ship-hours, `hive.py standing`), with 6,000 cr paid once, against
the scale of 9,073 (mine-ruchbah-ice-belt, `hive.py tasks`). What would
change it: the chain's first runs after the fix (seven held chains and
up to thirteen more scouts, +10,893 cr each, while the silver ask
carries them); a paying herd found in the new frontier ring; a free place on another division's paying
route with its Admiral's word and the tool it needs.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| hunt-atlas-gas-pocket (halo-drifters and cinder-sylphs) | 2 runs at the place, 18.7 minutes each: +1,259 cr (2 halo-drifters, 2 noble condensate at 690 cr, 03:11 UTC, as the test hunt-test-atlas-halo-drifter) and +839 cr (2 cinder-sylphs, 2 ember glands at 480 cr, 04:24 UTC); about 3,360 per ship-hour (`data/routes/runs.jsonl`) | 2026-11-16 | One hunter, no hunt below 4 animals of the two species together; the place read 2 halo-drifters and 3 cinder-sylphs at 03:25 UTC. Apophis gave the herd to Intel (queue.log ENT-065) |
| -- | -- | -- | Before it, none of Intel's own. Reading earns nothing by itself; Intel is measured by the age of the picture and by the leads others turn into income. From the next turn the scouts also hunt between reads (orders.log ENT-008, F16) |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| census-voidborn | 93 runs, 8 minutes and -70 cr per run, -550 cr per ship-hour (`routes.py measure`, 23:45 UTC) | 2026-11-15 | Fuel only. Kept: it is the picture every division plans from. With `every_minutes` 30 and `max_ships` 3, 61 gaps between two reads of one system in the four hours to 23:20 UTC were 33 to 48 minutes, median 38, none over the hour (`data/routes/runs.jsonl`) |
| census-frontier, read again | 35 reads from 2026-11-15 23:00 to 2026-11-16 03:04 UTC with both wallets read: mean -158 cr, median -156, -77 to -260, 14.5 minutes (`data/routes/runs.jsonl`) | 2026-11-16 | Fuel only. A refuel where it is cheap changes little: Hive Antares and Ironlight Crossroads are the only stations of the 42 systems that sell fuel, and about half of a read's 13 units (158 cr at the fleet's 11.86 cr a unit) could be bought there: about 70 cr saved on an Antares read and 30 on an LHS 1140 read, under 2% of the round's 6,600 cr (an estimate; units per read not recorded) |
| census-frontier | 35 runs, 14 minutes and -140 cr per run, -600 cr per ship-hour (`routes.py measure`, 23:45 UTC); a third-ring read 15.1 to 15.5 minutes and -156 to -169 cr; Antares by hand 18.7 minutes, -96 cr | 2026-11-15 | Fuel only. Kept on Suggi's word (orders F13). No own ship below full hull at 23:31 UTC (`data/fleet/ships/`) |
| voidborn-first-hunt-intercrus-belt, -intercrus-remnants, -gsc-0031 (First Hunt at three herds beyond the border) | 3 runs at 03:11 UTC: objectives not done, -143 to -154 cr each, 15.0 to 20.7 minutes; two pilots held the mission from a failed home run, so The Experiment did not offer it; the ships were seen at other places of the systems | 2026-11-16 | Cause not found (requests.log ENT-092). Out of the plan since b09dd88 |
| hunt-test-amberfall-sift-ray (with chlorophage), hunt-test-stormwatch-lantern-slug, hunt-test-nightveil-rivetshell | one run each: -110, -110 and +496 cr; drops of crystallized biogas (4), creature carapace (2) and creature carapace with raw xeno meat (3), bid 1 to 2 cr; the lantern-slug run left after 1 kill, a ship not ours at the place; the rivetshell run's +496 cr was a neural soma from the hold sold at 617 cr | 2026-11-16 | The drops do not sell. Out of the plan by 03:43 UTC |
| voidborn-first-hunt-nexus, -gsc, -acubens for scouts | 4 scout runs from 02:01 to 02:49 UTC, objectives not done, -26 to -55 cr each; the three herds read 1, 3 and 0 belt-grazers at 02:37 to 03:04 UTC (`data/wildlife/`) | 2026-11-16 | Too many first hunters for three home herds. Out of the scout plan since 784ac51; the three herds beyond the border that took their place failed too (row above) |
| hunt-test-homam-frost-moth | first run 04:24 UTC: left at the place, two pilots not ours there, 0 kills, -132 cr in 12.9 minutes (`data/routes/runs.jsonl`) | 2026-11-16 | No drop read yet; one more run, then the loss stop decides |
| voidborn-conductive-lattice for scouts | from 04:27 UTC every scout run ended in the circuit runner's crash at the silver buy and wrote no row; 7 scouts hold Conductive Lattice accepted (`data/routes/logs/`, `data/fleet/ships/`) | 2026-11-16 | Out since f4bad72 until the runner is fixed (requests.log ENT-096, ENT-097) |
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
  Wolf 1061 in that order; Ruchbah and Intercrus not advised.

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
  it makes wrong are in `requests.log` ENT-038.
