# Logistics guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the tests of 2026-11-17 and 2026-11-18 (route_run.py commits 85b14c83 and 6d69c52, queue.log ENT-187); requests.log ENT-281; faction_owned 2026-11-21 23:48 UTC; list_station_passengers 2026-11-21 23:52 UTC; the game's guides packages and passenger-lines (read 2026-11-22).

- Open (2026-11-22): `supply-repair-gsc-0044-boards` on `requires.reserve` below 45 boards at the outpost, and `-plate` (three more loads of 60): the repair stock kept by itself (topic-bases.md); `supply-bunker-gsc-0044` on `requires.reserve` below 4,000 (gate on since 2026-11-21 21:20 UTC); `train-jumps-hauler`: its cost a loop (`hive.py route train-jumps-hauler`) against the piloting it brings.
- Open: a Prayer bought and flown by one hauler (ships.md). `craft-steel-refine-node-beta` (refine_steel) was flown once; its use waits on the Fleet Admiral's word (requests.log ENT-200).
- Open: the any-role steel routes of 2026-11-17 03:58 UTC (requests.log ENT-190): which divisions' ships fly them once they stand in every plan's list Then.
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`; a station's inputs: topic-station.md.

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
