# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section Standing Plan.

What the scouts fly between two turns: the intel plan file, applied in
the Intel turn of 2026-11-17 that began 23:15 UTC (`plan.py check` PASS
at 23:33 UTC, `fill.py check scout` PASS at 23:27 and 23:30 UTC). Thirty
ships. A free ship takes the first route open to it of the list First,
its own routes, the list Then. From this turn the three roads of orders
ENT-052 (P4 b, D4) are census lists of their own, and both templates
name them before census-roads: the north road from Atria (the north
outpost) to Yildun (the station candidate), the east road beyond
GSC-0044 and Intercrus, the southeast road beyond Biham.

| Order | Routes | Ships | Cap | Expected, credits per ship-hour (route_earnings, 4 h to 23:31 UTC) | Why |
|---|---|---|---|---|---|
| First | store-hold-central-nexus (Mining's, `requires.hold`) | a scout with more than five units aboard | 40 for the fleet | -971 over 67 runs | Every census beyond the border wants an empty hold |
| First | the once line (Central Nexus board, the Voidborn chain, Signal Fragments, First Hunt, Cracking the Shell, Selling, Ghosts in the Cloud and the rest) | every scout that holds one | each route's own | paid once per pilot | Missions that pay once and the empire chain come first (rules F34, F35) |
| First | census-voidborn | any | 4 | -613 over 66 runs | The ten home systems and the books we sell to every 30 minutes; 76 gaps in 4 hours, median 35, longest 52 (23:17 UTC) |
| Own, @explorer, @reader | census-north | five explorers and the scanner scout first; readers after the frontier | 6 | -712 over 20 | 31 systems: the Atria-Yildun road (Atria, Regor, Groombridge 34, Chalawan, Rasalhague, Yildun), its neighbours, Aldebaran, Hawthorne, Alchiba and theirs; every 150 minutes, `chain` 3, so each is read under three hours (at 180 the ages reached 209) |
| Own, @explorer, @reader | census-east (new) | three explorers first | 3 | not flown yet | 17 systems beyond GSC-0044 and Intercrus, west of the Dross pirate group: the east station and outpost candidates (Nembus, Cervantes, Oakridge, Miaplacidus, Aldhibah, Tidewater, Ross 154); every 150 minutes, `chain` 3 |
| Own, @explorer, @reader | census-south | three explorers first | 4 | -655 over 16 | 19 systems: Biham and the nine around it, and beyond them Alnilam, Silverbend, Groombridge 1618, Jishui, Pleione, Etamin, Greenvale, Yed Posterior, Fomalhaut; every 150 minutes, `chain` 3 |
| Own | census-far-1 to census-far-5 | each explorer's second list, one it has not flown | 3, 2, 2, 2, 2 | -476 to -907 over 4 to 22 runs | Exploration XP is the pilot's own first visit: a far list it has not flown trains it; every 480 minutes |
| Own | the hunts and mines of one ship each (Intercrus, Alnilam, GSC-0021, Achernar, Pleione ice fields and drifts; Atlas gas pocket; Titawin and Amberfall chlorophages, storing; Homam frost moths, storing; Garnet veil rays; Birchwood cinder sylphs; carry-soma-synchrony-to-alpha, sell-soma-at-node-beta, sell-soma-at-synchrony (added by fill.py at 23:46 UTC); mine-flicker-fray, mine-nightveil-dark-residue, mine-gliese-876-belt) | one ship each, then @reader | 1 each | sell-soma-at-node-beta +5,433 over 13, carry-soma +5,642 over 4; 12 h: Titawin +6,554 over 3, mine-flicker-fray +4,958 over 5, Atlas +3,724 over 9, Birchwood +2,064 over 3, mine-nightveil +1,664 over 5 | Scouts hunt on the way (D8, F9), one hunter a herd; hunt.py stores every good the reserve keeps (d93c033); the dispatcher closes a place where a pirate was seen within 6 hours, 24 for a pack of 1,000 hull and shield |
| Own | fit-survey-scanner-central-nexus | three readers | 1 | buys nothing while Central Nexus asks 11,000 (max_price 5,000) | Scanning rises only by surveys |
| Own | @reader: census-watch-gsc-0044, census-worked, census-frontier, census-north, census-east, census-south, census-roads | 19 | 4, 6, 12, then the roads' caps, 10 | watch -674 over 35, worked -757 over 38, frontier -664 over 36, roads -777 over 25 | The outpost and its six neighbours every 35 minutes (WATCH: longest gap or age 58 minutes, 23:17 UTC); the 21 systems our routes use every 90 (Rotanev added for The Collective Provides); the frontier every 170 (oldest 168); then the three roads; census-roads every 480 |
| Then | gather-gsc-0027-prism-scatter, gather-hamal-crystal-bloom, mine-pherkad-rift, gather-gsc-0027-spacetime-seep, gather-schedar-belt, gather-ironhollow-echo-ejecta, the three craft-steel routes, census-frontier, park | the rest, while nothing is due | shared | gather-schedar-belt -102 over 69, gather-ironhollow-echo-ejecta -235 over 111 runs of the fleet | The fallback: make before gather (orders P2) |

The forecast's SUM line at the briefing (23:15 UTC): -10,513 credits an
hour; Intel's steady net in the last hour -20,137 (income 333, costs
20,470), its runs of 4 hours -16,282 an hour steady and 90,538 paid once
(`hive.py briefing`). What would change the plan: the first census-east
rows (reads an hour, pirates met beside the Dross group); a pirate on the
north road; a probe step that resolves a faint signature; a visit-mission
route that pays its 6,500 cr after fuel. Not taken: the test hunt-merope-gas-plume-cinder-sylph the
fill tool offered at 23:46 UTC; Merope lies in the Dross group, one jump from the eleven Dross at
Merak (21:36 UTC), with a pirate line of its own at 10:19 UTC.

### Route Guides
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section 1.

How each kind of route of this division is flown. A credits figure here
is a dated reading, never a verdict: what a route earns now is in the
fleet's database with its age (rule F22; the tool `routes`, the view
`route_earnings`).

| Kind | How it is flown | Fit and skills | Dated reading |
|---|---|---|---|
| Census (census-voidborn, census-worked, census-frontier, census-roads, census-roads-chain) | `census.py`: fly to the system, `get_poi` at every field, `get_nearby` for creatures, pilots and pirates (each pirate with name, tier, hull and shield since commit 9ceae23), dock at each station and save its book and board; ends docked at the last station read, else at Central Nexus. A route with `chain` N reads up to N more due systems of its list within `chain_jumps` lanes before it turns home (97 first reads on the five far routes in under four hours, 2026-11-17). A ship with a survey scanner runs `survey_system` on arrival in each system, before `get_system` (census.py 7540393). A system opens when its scouting file is `every_minutes` old; never-read systems first, in list order (`dispatch.py`, stalest_system) | The starter Threshold; an empty hold (`requires.empty_hold`, five units at most) for every route beyond the border. Trains piloting, navigation by its jumps and exploration a little | census-frontier -528 per ship-hour over 92 runs, census-voidborn -550 over 47, census-guard-ice -668 over 9 (4 hours to 23:28 UTC); a frontier read takes a median of 14.4 minutes over 165 runs |
| Hunt (one hunter per herd, rule F9) | `hunt.py`: fly to the place, kill up to `kills` grazers of the route's species while the herd holds `min_creatures`, loot, sell at `sell_at` what a fresh bid of `min_bid` takes, store the rest; `alone` leaves when a ship not ours is at the place | Mining laser and pulse laser of the starter; flees under 60% hull (F2). Trains weapons and xenobiology | hunt-atlas-gas-pocket +1,406 per ship-hour over 4 runs (4 h) and +2,237 over 13 runs (24 h); hunt-test-homam-frost-moth -586 over 2 (4 h), +1,168 over 9 (24 h): the place was shared in most runs |
| Mine beside a hunt (mine-gliese-876-belt) | `mine.py`: the engine's mining loop for its minutes, then sell at the station named | Mining laser; trains mining | +2,880 per ship-hour over 2 runs (12 h); its nickel bid at Nova Terra Central stood at 0 depth at 23:19 UTC (`fill.py status`) |
| Gather (standing work, the fallback) | `mine.py` without a sale: ore into storage at Node Beta; `min_left` is the field's floor | Mining laser; trains mining and deep core mining, not a scout's skills | -146 and -178 per ship-hour (4 h) |
| Once missions | the route's circuit: accept on the board, do the steps, hand in | as the route says; Signal Fragments asks navigation 3 | paid once per pilot; listed in section 3 |

### Route Templates
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/intel.md section 2.

A kind of work is a named list of routes: a template, kept in
`game/routes/templates/intel.json` and listed in
`game/routes/templates-intel.md`. A ship's row in the plan file names it
as `@<name>`, alone or after routes of its own.

| Template | Routes, in the order a ship tries them | Trains | For |
|---|---|---|---|
| @explorer | census-north, census-east, census-south, census-roads, census-frontier | navigation, exploration, piloting | about ten scouts, after their own lists (a road list first, a far list it has not flown second): the three roads of orders D4, the roads, then the frontier (rule F26) |
| @reader | census-watch-gsc-0044, census-worked, census-frontier, census-north, census-east, census-south, census-roads | navigation, exploration, piloting, scanning | about twenty scouts where the fleet works: the outpost site and its neighbours, every place our routes use twice a turn, the frontier, then the three roads and the roads |

| Task | How |
|---|---|
| See the templates and the ships on each | `plan.py templates` (the tool `plan`, `action=templates`) |
| Make or change one | `plan.py template <name> <routes> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py use <ships> <name>`; a hunter keeps its hunt first: `plan.py set <ship> <hunt route>,@reader` |
| Take one away | `plan.py template <name> none`, once no ship names it |

This guidebook keeps no list of routes that did not pay (rule F22). The
list it held until 2026-11-16 is in the file's history.

### Missions That Pay Once
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/intel.md section 3.

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
