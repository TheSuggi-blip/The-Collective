# Logistics guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: rule F37 (queue.log ENT-203); `hive.py route <id>` of each route named; table holdings 2026-11-22 19:34 to 19:54 UTC; faction_owned 2026-11-22 19:56 UTC.

- Three results (rule F37): a hauler test decides on three runs. A route whose runs share no buyer, field or herd (a craft from each pilot's own store) gets `max_ships` 3; one whose runs share a book, a bunker or a board (a buy, a supply route) gets `max_ships` 1 and three runs in a row; a test that buys goods starts with one unit (F12) and two runs follow. A stop for loss is a rest (F22), never the verdict.
- Open (2026-11-22): `craft-boards-crescent-moon` (a player workshop beyond the border crafts for us: 615 boards in the receiver's storage after two runs; a third run decides); `supply-bunker-gsc-0044-own-cells` (our own cells into the bunker under 5,000); `craft-cells-hydrogen-node-beta` (it needs plate in the same pilot's store); `train-jumps-hauler` (its cost against the piloting it brings). Decided: `craft-boards-stored-node-beta` works (2,314 boards in one receiver's storage, table holdings 19:34 UTC).
- Open: a Prayer bought and flown by one hauler (ships.md); `craft-steel-refine-node-beta` waits on the Fleet Admiral's word (requests.log ENT-200).

### Carrying for pay: freight and passengers
Status: test. Updated: 2026-11-24. Evidence: the game's guides packages and passenger-lines (read 2026-11-22); shipping.py list 2026-11-24 01:47 UTC; shipping list_all and profile, list_station_passengers 2026-11-22 08:01 UTC (a docked hauler); table stations; needs passenger-cabin-test, transit-lounge.

- Freight contracts (`shipping` list_all, accept, deliver; the game's packages guide: 400 cr + 200 a hop, probationary carriers up to 5,000 cr a package): the hauler's paid carrying beyond our borders. Read 2026-11-22 08:01 UTC: 161 contracts; the twenty best all bound for pirate strongholds 11 to 30 jumps out (Kael Arsenal, Crix, Dross Citadel), the best from our stations 2,242 to 13,264 cr; a new carrier is probationary (liability 50,000 cr, a package up to 25,000; licensed after 5 deliveries). Not work for an unarmed Threshold; read again when Military escorts or a contract ends at a policed station. The board is a command for gate.py: read it in a catch.py row (requests.log ENT-344).
- Read again 2026-11-24 01:47 UTC from a Prospect (110 cargo) docked at Krynn (shipping.py list): 20 contracts, 1,200 to 5,846 cr over 16 to 41 jumps, all to pirate strongholds or inside Ironlight's own station; the runner's `shipping` stop (commit 8a4efabf) takes only a contract to a charted policed station, so none fits yet.
- Passenger lines (the game's passenger-lines guide): a Threshold has no berth; an Economy Passenger Cabin (12 seats, a utility slot) or a Fugue (Voidborn courier, 1 business seat, speed 4) first, on one ship. Boards of 2026-11-22: 0 to 2 waiting a Voidborn station, fares 3,125 and 5,500 to far stations (need passenger-cabin-test).
- Why: the haulers outnumber the hauls at home (orders ENT-059); both pay for carrying itself, which is the hauler's class, and both reach beyond our borders.

### Station procurements (Shipyard Supply)
Status: test. Updated: 2026-11-23. Evidence: table missions (deep_range_outpost, read 03:53 and 04:15 UTC); table books 03:51 to 04:00 UTC; data/routes/runs.jsonl 04:16 to 04:33 UTC; route_run commit 9a65d1dd; game/map/galaxy.tsv.

- A shipyard station posts its own procurements: Deep Range Outpost (Outer Rim) posted Shipyard Supply copies of fuel tanks (14 for 9,515 cr), engine cores (12 for 18,988) and titanium alloy (25 for 26,133), dozens of each, every copy a new mission_id and no template. Delivered on docking. It is the hauler's carrying work where the Rim newborns were born: bought within 1 to 3 jumps (Unknown Edge, Frontier, Ramen's Rest), sold to the board at a margin of about 1,100 to 2,600 cr a load.
- An `accept` entry names such a mission by `title` (route_run 9a65d1dd): the first copy on the board is taken.
- Pitfall: a newborn's hold is full of starter leftovers (fuel cells, probes, rods: 73 of 75 used). The buy stop first stores the hold and withdraws the mission's goods (`store: all`, `withdraw`), else the buy takes one load short and the delivery is refused for goods missing.
- First result: titanium alloy +2,297 cr in 7 minutes (04:18 UTC). Open: the three routes `mission-shipyard-*-deep-range` at one ship each until three results; whether the board posts new copies when they are taken is not known; asks are thin for titanium and engine cores (one or two loads), deep for fuel tanks (about 3,000 units within 3 jumps).

### Tests done
Status: proven. Updated: 2026-11-21. Evidence: RESULT lines and the tables faction_facilities and faction, 2026-11-17 to 18; topic-bases.md.

- 2026-11-18: the runner steps `bunker`, `burn_cells` and `refuel: false`; the Atria kit route written, off until the Fleet Admiral's allocation.
- 2026-11-17: the Lockbox at The Experiment, the Hiring Board, the outpost CLTV Outpost GSC-0044 (16:36 UTC) and the Recruitment Desk stand; the outpost's storage and bunker used by a run of ours; `store_faction` in the runner.
- `craft-boards-node-beta`: first RESULT line 2026-11-17 04:47 UTC, 45 boards from 30 silicon in 20 minutes; `craft-boards-silicon-central-nexus` 65 boards (09:58 UTC).
- The gas routes of the template `gas-harvest`: ended, haulers no longer gather (rule F23).
