# Logistics guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: rule F37 (queue.log ENT-203); `hive.py route <id>` of each route named; requests.log ENT-281, ENT-332; faction_owned 2026-11-22 03:49 UTC.

- Three results (rule F37): a hauler test decides on three runs. A route whose runs share no buyer, field or herd (a craft from each pilot's own store) gets `max_ships` 3; one whose runs share a book, a bunker or a board (a buy, a supply route) gets `max_ships` 1 and three runs in a row; a test that buys goods starts with one unit (F12) and two runs follow. A stop for loss is a rest (F22), never the verdict.
- Open (2026-11-22): `supply-bunker-gsc-0044-own-cells` (our own cells from Node Beta into the bunker under 5,000; one ship, three runs); `buy-flex-central-nexus-to-node-beta` (three loads at most); `craft-cells-hydrogen-node-beta` (cells from hydrogen no bid takes; it needs plate in the same pilot's store); `train-jumps-hauler` (its cost against the piloting it brings).
- Off until strict classes are on: `give-hauler-stores-*` (P5: Trade's goods to Trade's receivers).
- Open: a Prayer bought and flown by one hauler (ships.md); `craft-steel-refine-node-beta` waits on the Fleet Admiral's word (requests.log ENT-200).

### Carrying for pay: freight and passengers
Status: test. Updated: 2026-11-22. Evidence: the game's guides packages and passenger-lines (read 2026-11-22); list_station_passengers 2026-11-21 23:52 UTC; needs passenger-cabin-test, transit-lounge.

- Freight contracts (`shipping` list_all, accept, deliver; the game's packages guide: 400 cr + 200 a hop, probationary carriers up to 5,000 cr a package): the hauler's paid carrying beyond our borders, read first from one docked hauler.
- Passenger lines (the game's passenger-lines guide): a Threshold has no berth; an Economy Passenger Cabin (12 seats, a utility slot) or a Fugue (Voidborn courier, 1 business seat, speed 4) first, on one ship. Boards of 2026-11-22: 0 to 2 waiting a Voidborn station, fares 3,125 and 5,500 to far stations (need passenger-cabin-test).
- Why: the haulers outnumber the hauls at home (orders ENT-059); both pay for carrying itself, which is the hauler's class, and both reach beyond our borders.

### Tests done
Status: proven. Updated: 2026-11-21. Evidence: RESULT lines and the tables faction_facilities and faction, 2026-11-17 to 18; topic-bases.md.

- 2026-11-18: the runner steps `bunker`, `burn_cells` and `refuel: false`; the Atria kit route written, off until the Fleet Admiral's allocation.
- 2026-11-17: the Lockbox at The Experiment, the Hiring Board, the outpost CLTV Outpost GSC-0044 (16:36 UTC) and the Recruitment Desk stand; the outpost's storage and bunker used by a run of ours; `store_faction` in the runner.
- `craft-boards-node-beta`: first RESULT line 2026-11-17 04:47 UTC, 45 boards from 30 silicon in 20 minutes; `craft-boards-silicon-central-nexus` 65 boards (09:58 UTC).
- The gas routes of the template `gas-harvest`: ended, haulers no longer gather (rule F23).
