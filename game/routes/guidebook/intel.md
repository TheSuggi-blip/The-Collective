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

What the scouts fly between two turns: the intel plan file, applied in
the Intel turn of 2026-11-17 that began 03:15 UTC (`plan.py check`
PASS at 03:24 UTC), checked against `fill.py check scout` (PASS, 03:44
UTC) and `hive.py forecast Oracle` (03:44 UTC). Thirty ships. A free ship
takes the first route open to it of the list First, its own routes, the
list Then.

| Order | Routes | Ships | Cap | Expected, credits per ship-hour (dated reading) | Why |
|---|---|---|---|---|---|
| First | store-hold-central-nexus (Mining's standing route, `requires.hold`) | a scout with more than five units aboard | 40 for the fleet | 0; a one-minute stop | A gather run leaves ore aboard and every census beyond the border wants an empty hold: 25 scouts carried goods at 03:18 UTC |
| First | the once line (Central Nexus board, Signal Fragments, the mining and trading missions, Conductive Lattice, First Hunt, Cracking the Shell, Ghosts in the Cloud) | every scout that holds one | each route's own | paid once per pilot | Orders ENT-027, EVERY ADMIRAL: the missions that pay once come first |
| First | census-voidborn | any | 4 | -567 over 61 scout runs, 2026-11-16 23:15 to 2026-11-17 03:15 UTC (`data/routes/runs.jsonl`) | The ten home systems and the six books we sell to, every 30 minutes; 62 gaps in 4 hours, median 36 minutes, longest 48 (03:18 UTC) |
| Own | hunt-amberfall-chlorophage-sac | 1 | 1 | below zero on the books: it sells nothing (the test that sold its sacs made +723 over 7 runs) | Caustic sac for the reserve (428 short), stored at Node Beta (rule F24) |
| Own | hunt-garnet-dim-lattice-veil-ray; hunt-atlas-gas-pocket with mine-gliese-876-belt; hunt-test-homam-frost-moth | 3 ships, one route each, then @reader | 1 each | Atlas -585 (1 run: a ship not ours at the place); Gliese 876 belt -642 (1 run) | Scouts hunt on the way (rule F16); each place is shared with others |
| Own | census-roads-chain | 1 explorer, then @explorer | 1 | not measured: the one-ship test of the chain (census.py 9ceae23) | Up to three systems of census-roads in one trip instead of one |
| Own | @explorer: census-roads, census-frontier | 10 (the youngest) | 10, 12 | census-roads -626 over 31 runs (4 h to 03:15 UTC) | Orders P4 a: the south and east regions first (18 systems never read), then the north again every 480 minutes |
| Own | @reader: census-worked, census-frontier, census-roads | 20 | 6, 12, 10 | census-worked -686 over 32 runs; census-frontier -671 over 5 scout runs | The 22 systems beyond home our routes use, opened every 90 minutes so that each is read twice a turn; the 31 others of the frontier every 200 (since 03:54 UTC: at 03:53 UTC only 9 of the 22 had been read twice in 4 hours, the oldest worked read was 145 minutes and the oldest frontier read 275) |
| Then | gather-gsc-0027-prism-scatter, gather-hamal-crystal-bloom, mine-pherkad-rift, gather-gsc-0027-spacetime-seep, census-frontier, park | the rest, while nothing is due | shared by the fleet | -179 (Hamal, 60 scout runs), -180 (Pherkad, the briefing's 4 hours) | The fallback: ore into storage for the reserve (Unity put Pherkad and the spacetime seep here at 03:13 UTC, requests.log ENT-188) |

The forecast's SUM line: -4,483 credits an hour at the briefing (03:15
UTC), -9,884 an hour after the plan (03:44 UTC), with more ships on the
census and the sac hunt selling nothing. What would change it: the chain
test's first rows (one trip for up to three systems); a read that becomes
a paying route of another division; a field that holds silicon ore; the
herd at Amberfall falling under two.

## 1. Route Guides

How each kind of route of this division is flown. A credits figure here
is a dated reading, never a verdict: what a route earns now is in the
fleet's database with its age (rule F22; the tool `routes`, the view
`route_earnings`).

| Kind | How it is flown | Fit and skills | Dated reading |
|---|---|---|---|
| Census (census-voidborn, census-worked, census-frontier, census-roads, census-roads-chain) | `census.py`: fly to the system, `get_poi` at every field, `get_nearby` for creatures, pilots and pirates (each pirate with name, tier, hull and shield since commit 9ceae23), dock at each station and save its book and board; ends docked at the last station read, else at Central Nexus. A route with `chain` N reads up to N more due systems of its list within `chain_jumps` lanes before it turns home (one-ship test from 2026-11-17). A system opens when its scouting file is `every_minutes` old; never-read systems first, in list order (`dispatch.py`, stalest_system) | The starter Threshold; an empty hold (`requires.empty_hold`, five units at most) for every route beyond the border. Trains piloting, navigation by its jumps and exploration a little | census-frontier -528 per ship-hour over 92 runs, census-voidborn -550 over 47, census-guard-ice -668 over 9 (4 hours to 23:28 UTC); a frontier read takes a median of 14.4 minutes over 165 runs |
| Hunt (one hunter per herd, rule F9) | `hunt.py`: fly to the place, kill up to `kills` grazers of the route's species while the herd holds `min_creatures`, loot, sell at `sell_at` what a fresh bid of `min_bid` takes, store the rest; `alone` leaves when a ship not ours is at the place | Mining laser and pulse laser of the starter; flees under 60% hull (F2). Trains weapons and xenobiology | hunt-atlas-gas-pocket +1,406 per ship-hour over 4 runs (4 h) and +2,237 over 13 runs (24 h); hunt-test-homam-frost-moth -586 over 2 (4 h), +1,168 over 9 (24 h): the place was shared in most runs |
| Mine beside a hunt (mine-gliese-876-belt) | `mine.py`: the engine's mining loop for its minutes, then sell at the station named | Mining laser; trains mining | +2,880 per ship-hour over 2 runs (12 h); its nickel bid at Nova Terra Central stood at 0 depth at 23:19 UTC (`fill.py status`) |
| Gather (standing work, the fallback) | `mine.py` without a sale: ore into storage at Node Beta; `min_left` is the field's floor | Mining laser; trains mining and deep core mining, not a scout's skills | -146 and -178 per ship-hour (4 h) |
| Once missions | the route's circuit: accept on the board, do the steps, hand in | as the route says; Signal Fragments asks navigation 3 | paid once per pilot; listed in section 3 |

## 2. Route Templates

A kind of work is a named list of routes: a template, kept in
`game/routes/templates/intel.json` and listed in
`game/routes/templates-intel.md`. A ship's row in the plan file names it
as `@<name>`, alone or after routes of its own.

| Template | Routes, in the order a ship tries them | Trains | For |
|---|---|---|---|
| @explorer | census-roads, census-frontier | navigation, exploration, piloting | about ten scouts: the roads to the station sites and the systems beside them, then the frontier (rule F26) |
| @reader | census-worked, census-frontier, census-roads | exploration, navigation, piloting | about twenty scouts where the fleet works: every place our routes use twice a turn, then the frontier, then the roads |

| Task | How |
|---|---|
| See the templates and the ships on each | `plan.py templates` (the tool `plan`, `action=templates`) |
| Make or change one | `plan.py template <name> <routes> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>`; a hunter keeps its hunt first: `plan.py set <ship> <hunt route>,@reader` |
| Take one away | `plan.py template <name> none`, once no ship names it |

This guidebook keeps no list of routes that did not pay (rule F22). The
list it held until 2026-11-16 is in the file's history.

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
| voidborn-first-hunt-nexus (and -gsc, -acubens, one hunter per herd) | the command group's run of 23:20 UTC: +974 cr in 18.9 minutes, 1,000 cr once | 2026-11-15 23:42 UTC to 2026-11-16 03:11 UTC: out when the herds ran empty (the list in this file's history) |

## 4. Levelling Guide

Which skills a scout levels and on which work (rule F23): a scout scans
and explores; gathering ore is the fallback when nothing is due. The
readings are from `hive.py levels` and `data/fleet/ships/`.

| Kind of scout | Skill that matters | What raises it | What the next level opens | Template |
|---|---|---|---|---|
| Explorer | navigation, then piloting | jumps: a road read is 14 to 30 jumps out and back, a home read 2 to 6 | navigation 3 opens Signal Fragments (7,000 cr once, list First); piloting 10 opens the tier 2 hulls | @explorer |
| Reader | exploration, navigation, piloting | every census: places surveyed, jumps flown | piloting 10, 20, 30 and 50 open hull tiers 2 to 5 | @reader |
| Hunter | weapons, xenobiology | kills of grazers (rule F9) | not measured for a scout yet | own hunt route, then @reader |

Readings:

- 2026-11-17 03:23 UTC (`fleet` view=levels): 30 scouts, 32 hours played
  (median); piloting 3, 6 and 7 (lowest, median, highest), 141 piloting
  XP an hour since birth, 70 hours to piloting 10; median deep core
  mining 6 (139 XP an hour), mining 5 (73), navigation 3 (49), trading 2
  (9), exploration 2 (12). The division's strongest skill is still the
  fallback's (deep core mining), not a scout's: the scout runs that
  started from 2026-11-16 23:15 to 2026-11-17 03:20 UTC flew 49 hours of
  gathering (Hamal 43.7, the prism scatter 5.5) and 32 of census
  (`data/routes/runs.jsonl`).
- 2026-11-16 23:28 UTC (`hive.py levels`): 30 scouts, 28 hours played
  (median); piloting 2, 5 and 7 (lowest, median, highest), 137 piloting
  XP an hour since birth, 78 hours to piloting 10 at that rate; median
  navigation 3 (45 XP an hour), exploration 2 (12 XP an hour), mining 4
  (69), deep core mining 6 (126). Deep core mining and mining lead
  because gathering was the work most scouts flew; exploration rises
  slowest.
- The same hour (`data/fleet/ships/`): the ten scouts born on
  2026-11-16 stand at navigation 2 and piloting 2 or 3; of the twenty
  older ones, ten stand at navigation 4 or 5 and ten at 3.
- 2026-11-16 12:22 UTC: piloting 3, 5 and 5; 91 piloting XP an hour;
  131 hours to piloting 10. 2026-11-15 23:44 UTC: in ten minutes twenty
  scouts gained 55 exploration XP, 235 navigation XP and 456 piloting
  XP on census reads.
- First Hunt gives 50 weapons, 15 xenobiology and 20 piloting XP once.

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

- Species tests from 2026-11-16 03:11 UTC, one scout each: what each
  kill dropped is in its run row (`data/routes/runs.jsonl`); a drop
  without a bid of 50 cr is stored, so the row shows it. Military tests
  other species (`guidebook/military.md`).
- Caustic sac (428 short in the reserve, `surplus.py reserve` 2026-11-17
  03:23 UTC): answered. hunt-test-amberfall-chlorophage flew 8 runs from
  2026-11-16 23:45 to 2026-11-17 03:08 UTC: 15 kills, 6 sacs dropped (0.4
  a kill), 7 sold at 420 cr into the Node Beta bid (`data/routes/runs.jsonl`).
  From 03:24 UTC hunt-amberfall-chlorophage-sac stores every drop at Node
  Beta and sells nothing (rule F24). The herd read 2 or 3 chlorophages
  in every census since 2026-11-16 02:06 UTC: one hunter, about two sacs
  an hour if the herd holds. Another herd of chlorophages: not read.
- The regions of the base sites (orders P4), read by the census
  (`data/scouting/`, 2026-11-16 23:50 to 2026-11-17 01:56 UTC); none holds a
  station, so a place in any of them can take an outpost:
  - North: Hawthorne holds one belt with iron and copper ore at 100,000
    of 100,000 each, 9 belt-grazers, 4 patina grazers, 4 slag tortoises;
    Aldebaran one ice field (nitrogen ice 50,000) and no belt; Alchiba an
    ice field (water ice 27,529, nitrogen 50,000); Yildun two belts mined
    down (copper 29,501 of 30,000, iron 27,712 of 35,000, carbon 66 of
    30,000, aluminum 102 of 20,000) and one pilot not ours. Hawthorne is
    the north's richest read.
  - South: Felis holds three belts at 100,000 iron and 100,000 copper each,
    an ice field, a nebula with deuterium ice 4,355 and null matter 361,
    and the largest herds we read (45 belt-grazers, 21 patina grazers, 20
    slag tortoises); one pirate at its frost ring (Flinch, 85 hull and 30
    shield in Military's test). Biham and the nine systems around it are
    on census-roads since 03:24 UTC.
  - East: Intercrus holds three belts at 100,000 iron and copper each, an
    ice field, sol alloy ore 1,401 and null matter 427; 50 belt-grazers
    and 3 crusher mantises (predators); four pilots not ours at its read.
    Diadem and seven systems around it are on census-roads since 03:24 UTC.
- The census chain (census.py 9ceae23): census-roads-chain tests it with
  one explorer from 03:30 UTC; its rows (one per system) are compared
  with census-roads per system read.
- Game 0.722.0 (changelog, read 2026-11-17 03:39 UTC): "calibration defects
  in recently sold survey scanners" were fixed and "frontier explorers
  should recheck their survey data". Our census reads `get_poi` and fits
  no survey scanner (survey_scanner_i, base value 4,400): whether a survey
  shows resources `get_poi` does not (silicon ore among them) is not
  tested.
- Silicon ore (53,222 short in the reserve; 34 held): no field of the 63
  systems read holds it (data/scouting/, 2026-11-16 23:20 UTC). Asked at
  Central Nexus at 420 cr (424 at the best price, 16,189 over all
  levels), at Ironlight Crossroads (LHS 1140) at 561 cr for 200, at
  Synchrony at 376 cr for 4. The explorers' 28 road systems are the
  search for a field.
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
- The game stood at 0.723.1 at 2026-11-17 03:39 UTC (https://spacemolt.com/changelog,
  1,886 releases); `game/rules/15-patch-notes.md` names 0.719.3.
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
