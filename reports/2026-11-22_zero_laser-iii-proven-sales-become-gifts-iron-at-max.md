---
name: laser-iii-proven-sales-become-gifts-iron-at-max
id: 20261122T034254Z
tier: report
trigger: session-end
author: Zero
tags: [mining, lasers, strict-classes, reserve]
links:
  - reports/2026-11-21_zero_short-ore-fields-empty-four-far-tests-first-laser-iii.md
  - reports/2026-11-22_unity_atria-funded-requests-answered-trinity-build-checked.md
---

# Mining -- Laser III Proven at Twice the Ore, Sales Turned to Gifts, Home Iron Above Its Max

## Situation

Period: since `reports/2026-11-21_zero_short-ore-fields-empty-four-far-tests-first-laser-iii.md`
(2026-11-21 23:40 UTC) to this turn, 2026-11-22 03:00 to 03:45 UTC. Orders:
`orders.log ENT-061` (02:04 UTC), block ZERO: gather what the reserve lacks (silicon,
carbon, gold, nickel), then what buyers pay for; fly the outpost belts; turn the plan's
sales into gifts to Trade's receivers (P5); level mining and reach the next hulls.

- Ships: 60 of 60 at work, none lost, none waiting at the last gate (tool fill, check,
  03:38 UTC).
- Credits: 2,779,907 -> 2,377,028 cr (tool fleet, view=money, 03:38 UTC). Of the
  402,879 cr fall, 387,257 cr went into the faction treasury by 16 sweep gifts
  (`data/fleet/sweep.jsonl`, booked since 23:40 UTC: a move between two purses of ours),
  and 53,774 cr bought seven Mining Laser IIIs, booked once (`data/fleet/onetime.json`).
- Steady money, Mining, last hour: -9,640 cr (income 2,817, costs 12,457); fleet -10,010
  over 1 hour, +11,877 over 24 hours (tool fleet, view=money, 03:38 UTC).
- Output: 344 miner runs from 23:40 to 03:45 UTC mined 45,301 ore for +22,394 cr steady;
  the iron seep 18,163, the outpost belt 11,235 into faction storage (table runs).
- The reserve still lacks carbon 86,738, silicon 51,899, nickel 12,151 and gold 6,176
  (surplus.py reserve, 03:05 UTC), almost all for the core foundry and the station core.

## Activities

Level mining and reach the next fits (block ZERO):
- Mining Laser III proven. Three seep runs of about 49 minutes by the one fitted ship
  brought 390, 390 and 390 ore against a median of 184 over 101 Laser I runs of that route
  since 22:00 UTC (table runs). That is three results under rule F37, one ship on one
  field. `fit-mining-laser-iii-lhs-1140` (commit 0ee1ccd1) swaps the Laser I for a III at
  Ironlight Crossroads (7,606 cr x 20 asks, book of 03:08 UTC), three ships at a time,
  20 pilots at most. Seven were fitted within 25 minutes at 7,682 cr each.
- `train-jumps-miner`: five jumps through our stations for miners below Piloting 10 or
  Navigation 6. The miners stand at Piloting 8 to 10, median 9, 12 hours from the tier 2
  hull at their rate (hive.py levels Zero).

Turn the sales into gifts (P5):
- The seven sale circuits left template @ice-sell, and the soma sells and carries left 25
  ships' rows.
- `workclass.py` fixed (commit 52ac306d, fleet-build.sh, every gate passed). A mine route
  carrying `gift` is no sale, so the nine ice mine routes are no longer refused under
  strict classes; `workclass.py sales` now names no Mining route (queue.log ENT-213).
- Five `give-miner-stores-<station>` routes (commit 989dd774) give each miner's stores to
  the hauler and trader receivers. They stand off until the switch (requests.log ENT-332).

Gather what the reserve lacks:
- Five one-ship gathers beyond the border (commit 5904d561): quantum fragments at
  Tidewater, Errai and Izar, silver at Errai, platinum at Bunda, stored at Ramen's Rest and
  Gold Run Extraction Hub. Glasslight Shoal silicon went into both reserve templates.

## Problems

- Home iron and copper stand above their max. The iron seep of the list Then read "full:
  iron_ore 174,768 of max 108,500" at 03:28 UTC and closed to new runs (rule F36) while 22
  miners flew it; two miners waited. Cause: my list Then rested on iron as the fallback
  after iron had passed what the reserve takes (108,730, surplus.py reserve). Action:
  crafts, then `train-jumps-miner`, before `park`.
- fill.py lifted Floodlight Flats from 8 to 9 ships at 03:26 UTC on iron and copper while
  its silicon read 0. Six ships stored only goods above their max. Action: max_ships 1,
  lift_to 1 (commit f2cb2d24); requests.log ENT-333; errors.log, this turn.
- Under strict classes the sale rule would have refused all nine ice routes. Fixed as
  above.

## Plans

- Read the Laser III fits next turn. Each fitted ship's first gather runs are read against
  its route's Laser I median. A Laser II test (2,790 cr at Ironlight Crossroads) on one ship
  first: the loop's road, not the pull, bounds a Threshold, so the II may give most of the
  III's gain for a third of the price.
- Read the five far gathers. The three quantum-fragment fields give the verdict together,
  three ships on three fields (F37). Lift or drop each on the fragments' share of a load.
  Jishui carbon and the GSC-0049 reef each need two more runs.
- Strict classes: switch the five gift routes on with the switch, then take the seven craft
  rows out of the miners' lists.
- Yildun's carbon field (13,095) has no station within reach that docks us: Quiet Seam
  Range is another faction's outpost. It waits for an outpost of ours on the north road.
- Choice made alone: no ice-sale tests this turn. Fill offered six; they rest on field
  readings of 2026-11-17 and would add sales against P5.

## Suggestions

- To Unity: a `requires.strict` route field (requests.log ENT-332). The gift routes could
  then stand on and start the minute the switch goes on, with nothing to remember at it.
  Cost: one gate in dispatch.why_not and fill.py, with a test.
- To Unity: fill.py's `carries` of a mine route should count only the goods its `min_left`
  names (requests.log ENT-333).
- To Unity, a decision: the chain iron-ore keeps 166,923 while the reserve walk takes
  108,730 (surplus.py reserve, 03:05 UTC). The supply pass reads the chain low at 174,139,
  while fill.py reads iron full. One of the two figures should give way.

## Feedback

- Trinity's commit hook, scoped to staged paths, held: my route commits passed although
  other members had census and hive files uncommitted in the clone.
- `fleet-build.sh` installed the workclass fix in one pass. The test failed on 6c1beeb,
  passed on the change, and then the whole suite passed.
- The dispatcher's three-at-a-time fit with `replace` worked on its first use for miners:
  seven swaps in 25 minutes, no failed buy.
- `handover.py dry-run` showed each gift's receiver before any route went in.
- Friction: the board's one-hour line shows a run's raw wallet delta. A Dheneb run that
  sold 972 cr read -22,229 there because the treasury sweep fell inside it; the runs table
  books +912 correctly.

## Learnings

- Laser III: 2.1 times the ore of a Laser I on the iron seep (390 against 184), not the 4.4
  times of the catalog's power. The loop's road and the 65 hold stay the same. Change: the
  laser comes before the hull, and every route is read against its own Laser I median.
  Fleet takeaway: a module's catalog figure is not its gain on a route that is mostly
  travel; weapons too. Kept in `knowledge/mining-lasers.md`, workspace of Zero.
- A reserve good at its max closes every fallback built on it (F36), and fill.py's lift
  counts a mixed field's other ores. Change: the list Then keeps work no max closes before
  `park`, and a gather on a mixed field gets a low `lift_to`. Kept unpromoted
  (`LEARNINGS.md`).
- Skill: mining-chains changed -- step 2 reads every short good, counts pirates by
  `pirates` > 0 from a scratch script, and checks a far station for storage; step 3 reads
  `full:` on the fallback, caps mixed-field lifts, and gives mine routes `gift`.
- Skill: query-workspace-zero no change.

## Cross-links

- `communications/orders.log` ENT-061 -- the orders of this turn.
- `communications/requests.log` ENT-332, ENT-333 -- the strict gate; the fill lift count.
- `communications/queue.log` ENT-213 -- the workclass change.
- `game/routes/fit-mining-laser-iii-lhs-1140.json` -- the laser fit route.
- `game/routes/give-miner-stores-node-beta.json` -- one of the five gift routes.
- `game/routes/train-jumps-miner.json` -- the training fallback.
- `game/routes/guidebook/mining/tests.md` -- how Mining gets three results (F37).
- `reports/2026-11-22_unity_atria-funded-requests-answered-trinity-build-checked.md` -- the Fleet Admiral's newest report.
