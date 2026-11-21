# Logistics guidebook -- Tests (tests.md)

### Open Tests
Status: test. Updated: 2026-11-21. Evidence: the tests of 2026-11-17 and 2026-11-18 (route_run.py commits 85b14c83 and 6d69c52, queue.log ENT-187); requests.log ENT-281; faction_owned and the storage view 2026-11-21 19:50 UTC.

- Open (2026-11-21): `supply-repair-gsc-0044-plate` (3 loads of 60) and `-boards` (60): whether the outpost rebuilds its damaged bunker and Lockbox by itself from the faction's storage there, and what get_base's repairs block asks (topic-bases.md); `train-jumps-hauler`: its cost a loop (`hive.py route train-jumps-hauler`) and the piloting it brings; `supply-bunker-gsc-0044` on `requires.reserve` below 4,000 (ENT-281) in place of `once` and `max_pilots` 3, closed while the gate is off; `buy-flex-ironlight-to-node-beta`, the loads into the faction store at Node Beta; which faction facilities an outpost takes (`facility types` category faction).
- Open: a Prayer bought and flown by one hauler (ships.md). `craft-steel-refine-node-beta` (refine_steel) was flown once; its use waits on the Fleet Admiral's word (requests.log ENT-200).
- Open: the any-role steel routes of 2026-11-17 03:58 UTC (requests.log ENT-190): which divisions' ships fly them once they stand in every plan's list Then.
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`; a station's inputs: topic-station.md.

### Tests done
Status: proven. Updated: 2026-11-21. Evidence: RESULT lines and the tables faction_facilities and faction, 2026-11-17 to 18; topic-bases.md.

- 2026-11-18: the runner steps `bunker`, `burn_cells` and `refuel: false`; the Atria kit route written, off until the Fleet Admiral's allocation.
- 2026-11-17: the Lockbox at The Experiment, the Hiring Board, the outpost CLTV Outpost GSC-0044 (16:36 UTC) and the Recruitment Desk stand; the outpost's storage and bunker used by a run of ours; `store_faction` in the runner.
- `craft-boards-node-beta`: first RESULT line 2026-11-17 04:47 UTC, 45 boards from 30 silicon in 20 minutes; `craft-boards-silicon-central-nexus` 65 boards (09:58 UTC).
- The gas routes of the template `gas-harvest`: ended, haulers no longer gather (rule F23).
