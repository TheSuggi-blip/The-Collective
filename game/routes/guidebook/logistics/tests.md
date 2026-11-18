# Logistics guidebook -- Tests (tests.md)

### Open Tests
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/logistics.md section 10.

- Open (2026-11-18 00:12 UTC): `supply-bunker-gsc-0044`, the first run of the runner's `bunker` step (section 15.3);
  `buy-flex-ironlight-to-node-beta`, the first loads into the faction store at Node Beta; the probe of which faction
  facilities an outpost takes, run at the end of the bunker run by a catch row (`facility types` category faction).
- Done 2026-11-18: the runner steps `bunker`, `burn_cells` and `refuel: false` (route_run.py, commit 85b14c83, queue.log
  ENT-187); the Atria kit route written, off until the Fleet Admiral's allocation (section 15.6).
- Done this turn: the Recruitment Desk stands (section 15.5); the outpost's storage and bunker used by a run of
  ours (section 15.3); `store_faction` in the runner (commit 6d69c52).
- Done 2026-11-17 16:36 UTC: the outpost founded (section 15.3); the Hiring Board stands (active, cap 50).
- `craft-boards-node-beta`: first RESULT line 2026-11-17 04:47 UTC, 45 boards from 30 silicon in
  20 minutes, -770 cr (the carbon, booked once). `craft-boards-silicon-central-nexus`: 65 boards,
  09:58 UTC (section 1.2).
- The Lockbox at The Experiment stands (section 15.2).
- The three any-role steel routes (2026-11-17 03:58 UTC): which divisions' ships fly them once
  the Fleet Admiral puts them in every plan's list Then.
- The gas routes of `gas-harvest`, one ship each.
- A Prayer bought and flown by one hauler (section 5). `refine_steel` was flown once
  (section 1.2); its use waits on the Fleet Admiral's word.
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`; the
  stations' list: section 13.
