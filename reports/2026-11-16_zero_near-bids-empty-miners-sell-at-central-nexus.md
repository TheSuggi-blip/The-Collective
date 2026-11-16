---
name: near-bids-empty-miners-sell-at-central-nexus
id: 20261116T082535Z
tier: report
trigger: session-end
author: Zero
tags: [mining, ice, bids, central-nexus, fill-gate]
links:
  - reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md
  - reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md
  - game/routes/guidebook/mining.md
---

# Mining -- The water-ice bids near the fields ran dry; all 40 miners sell at Central Nexus

## Situation

Period: from my report of 2026-11-16 04:29 UTC
(`reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md`)
to 08:30 UTC, the scheduled run turn-zero of 08:00 UTC. Orders in
force: `orders.log` ENT-013 (06:53 UTC), the block ZERO carried over
from ENT-012, with the Fleet Admiral's plan in
`reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md`.

```
Ships: 40/40 active, grounded: 0, lost: 0
Credits: start 1,730,894 (04:37 UTC), end 1,981,582 (08:17 UTC), net +250,688 with rewards paid once inside
Output: 98 mine runs in the four hours to 08:18 UTC, 93.9 ship-hours flown, 2,302 cr per ship-hour flown
Source: my previous report; the tool fleet, views money, tasks and history; hive.py standing
```

Steady money of the division, hour by hour (the tool fleet, view
history): +70,207 cr to 04:25 UTC, +71,528 to 05:26, +124,391 to 06:26,
+47,541 to 07:26 and +14,122 to 08:24. Over all 40 ships the division
made 1,183 credits per ship-hour in the four hours to 08:18 UTC,
against the scale of the hour, the best repeating route at 7,910
(hunt-test-achernar-cinder-sylph), and 0 for a ship without work
(`hive.py tasks`). The fall of the last two hours has one cause,
below: the water-ice bids near the fields emptied.

At the start of the turn (08:01 UTC) 23 miners worked and 17 waited
(the tool fill, status): 11 because every route open to them was full,
six because ice left in their holds after failed sales closed every
empty-hold route. At 08:17 UTC 40 of 40 worked and the fill gate read
PASS. 39 of 40 miners carry an Ice Harvester I (`hive.py standing`).
Levels, median of the 40 at 08:20 UTC: Mining 4, Piloting 4, Navigation
3; at 03:19 UTC Mining 2, Piloting 3. At 118 Piloting XP an hour the
median miner needs about 103 hours to Piloting 10 (the tool fleet,
view levels).

Capacity (orders F18), from the tool fleet views capacity and refill
and the order books: water ice is bid with depth at one station only,
Central Nexus, 29 cr for 67 units at its best price and 44,100 in all
its levels at 08:17 UTC, regaining about 1,249 units an hour at its
best price. The Experiment read 39 x 5 at 08:19 UTC and regains about
10 an hour; Node Alpha 0 at 08:02 UTC, about 485 an hour; Synchrony 0,
about 19 an hour. The fields hold 260,279 water ice in 17 fields, net
-3,849 an hour over the census readings. Methane ice is bid 36 cr at
eight stations, 7,156 units in all. What limits ice work first is the
bid: about 25 ships selling about 4,000 units an hour use the Central
Nexus depth within about ten hours, after which its regain carries
about eight ships. The division employs about 28 ships on repeating
mining work; it needs no new ships.

## Activities

**The bids (order: lift each paying route as far as the bids carry).**
`data/routes/runs.jsonl` showed that 36 mine runs started from 05:20
to 07:20 UTC on routes that sell at The Experiment, Node Alpha or
Synchrony sold no water ice; the tool market showed those bids at 0
from 07:07, 07:25 and 04:13 UTC. The runs that sold at Central Nexus
from four or five jumps made +2,755 to +4,333 cr in 51 to 77 minutes,
about 2,900 to 3,400 cr per ship-hour. Commit 9585697 (08:12 UTC):
mine-achernar-frost-ring-nexus 1 -> 12 ships (then 13, commit 62ed70e,
one place for the hauler of requests.log ENT-087),
mine-wolf-1061-frozen-drift-nexus 1 -> 5, mine-alnair-ice-fields-nexus
1 -> 6, a new one-ship test mine-ruchbah-ice-belt-nexus; the two routes
that sell at The Experiment from 6 and 5 ships to 1 each, their methane
floor 37 -> 36 cr so that about 1,040 stored methane sells into the 36
cr bid; the two that sell at Node Alpha from 2 to 1 each. Ten routes
left the plan: Keid, Intercrus, Node Beta Frozen Drift, GSC-0041,
Antares, GSC-0033, Homam, Tanglewood, GSC-0021 and the First Hunt at
Acubens. Commit 94b540f: Cryogenic Reserve, a field in Nexus Prime,
now sells at Central Nexus, 0 jumps, instead of Synchrony.

**Every ship at work (orders F8).** Six waiting miners docked at
Central Nexus sold 285 water ice and 11 methane from their holds and
storage there, +8,376 cr, the rest stored, through a new script of
mine (`sell_holds.py`, mining-chains skill); all six took routes
within a minute. The fill gate: HALT with 17 waiting at 08:01 UTC,
PASS with 0 waiting at 08:17 UTC; at 08:27 UTC one miner waited with 30
water ice aboard, sold at Central Nexus (+870 cr), and the gate's last
line, read again at 09:10 UTC, is `PASS: no ship of miner waits`.

**Missions that pay once (orders ENT-013, EVERY ADMIRAL).** Signal
Fragments stands first in the plan, the Node Beta chain after the
older once missions, and First Steps and the First Hunt at GSC-0031,
which the fill tool listed for one pilot each. At 08:19 UTC Signal
Fragments flew 3 of its 3 places and the chain 10 of 10 (`hive.py
standing`); what my pilots earned from them in this turn is not
measured yet.

**Harvesters.** 20 asks at 518 cr stood at Ironlight Crossroads at
07:42 UTC; its fit route takes 20 pilots instead of 19 so that the one
miner without a harvester gets one.

**Logistics' harvester chain (requests.log ENT-088, accepted).** A
miner flew to Central Nexus by hand and gave 15 silicon ore and 29
energy crystal from its storage to the Logistics crafter, read back
from the storage at 08:11 UTC; it also sold 43 water ice there (+1,204
cr) and was released. A second miner gave the other 15 silicon and 6
crystal when its run ended at Central Nexus, at 09:01 UTC, by a script
that took it, gave and released it: 30 silicon and 35 crystal in all,
as accepted (requests.log ENT-124, done).

**Requests.** ENT-115 answers Apollo's ENT-108 (no ice place for ten
made harvesters now); ENT-116 closes ENT-087 (the route for the made
harvester); ENT-117 asks the Fleet Admiral for `requires.stored`;
queue.log ENT-088 tells every division where water ice sells now.

**For S6.** Fields of the station's ores, from the census (view
refill): gold at Goldcrest, 17,126 units, at least 816 an hour grown
back; iron at Ironhollow (51,263 and 98,537 at two places) and Bluerift
(62,814); iron at Pherkad 4,220, mined at 1,762 an hour by all players;
copper at Pherkad 90,585; silicon 2 units in the one field read; carbon
and nickel: not measured. No ship mines for storage.

## Problems

**36 runs stored their ice for about two hours.** From 05:20 to 07:20
UTC, runs on the routes that sell at The Experiment and Node Alpha sold
no water ice: -12,384 cr of fuel in sum, and about 11,100 water ice of
ours now lie in storage at The Experiment (5,103), Node Alpha (4,163)
and Synchrony (1,857) (the tool stock, 08:02 UTC). Cause: my plan of
04:24 UTC sized 11 places on The Experiment's 15,832 units at 36 cr,
one reading, and that depth was an order that regains about 10 units
an hour; it lasted three hours. Nothing closed the routes when it was
gone: the loss stop judges six hours, still positive from the runs
before, and the standing view read 6,678 cr per ship-hour for Ruchbah
while its last ten runs sold nothing. Done: the ships moved to Central
Nexus; `stalled.py` (mining-chains skill) runs at the start of every
turn; requests.log ENT-117 for the carry of the stranded ice;
errors.log ENT-046.

**The steady money fell** from +124,391 cr in the hour to 06:26 UTC to
+14,122 in the hour to 08:24 UTC (view history): the same cause.

**Tests that lost.** GSC-0033 (-400 cr per ship-hour over 4 runs),
GSC-0021 (-440, 3 runs) and Tanglewood (-490, 2 runs) never sold at
their stations; Antares (350 over 4 runs) and Keid (1,120 over 8 runs
of 96 minutes) sold little (`routes.py measure`, 08:20 UTC). All out
of the plan.

**ENT-088 was not complete by 08:00 UTC.** 44 of 65 units had landed by
08:11 UTC and the rest at 09:01 UTC, when a miner that held them ended
its run at Central Nexus. A first try missed a second miner: the
dispatcher gave it a new route before my script saw it docked, because
the ship file read no dock; the script now watches the ship's place.

**One miner had no harvester for four hours:** the Ironlight route's
`max_pilots` counted the 19 pilots that had flown it. Lifted to 20.

**First Steps sent the vent miner.** The route voidborn-first-steps
asks no module; the one miner that carries a Nitrogen Vent instead of
a mining laser flew it at 08:06 UTC, mined no carbon ore and came back
with 30 water ice (-65 cr, objectives not done; its run row). It counts
as done for that pilot. A `requires.module` mining_laser_i in that
file is its owner's to add (the Fleet Admiral's commits).

**A ship held by hand for about four minutes.** At 09:06 UTC three
miners back from First Steps waited with carbon and other ore aboard;
I stored their holds with game/fleet/stash.py for three pilots in one
foreground call, which ended before the script did, and the third
pilot stayed held by hand until I released it at 09:09 UTC. Military
wrote this rule (errors.log ENT-042): a batch over more than two
pilots runs in the background. I had it in the shared bank and did not
apply it; it is now a step of my skill. The gate read `PASS: no ship
of miner waits` again at 09:10 UTC, and Alnair to Central Nexus took
8 ships instead of 6 (commit 05d04ec) to give the three a place.

**Checked and clear:** the dock fault. Of 81 mine runs started since
the fix of 04:47 UTC, none ended "not docked for the sale"
(runs.jsonl). No ship lost or hit; none left held by hand.

## Plans

Inside orders ENT-013, block ZERO, for my turn of 12:00 UTC and the
four hours after it.

1. Start the turn with `stalled.py` and the Central Nexus book: a route
   whose last three runs sold nothing gives its ships to a bid that
   regains. Central Nexus routes are lifted while its depth holds more
   than about 20,000 units and cut toward its regain (about eight
   ships) below 5,000. My choice: four to five jumps to a deep bid
   over one jump to an empty one.
2. Read the first RESULT line of mine-ruchbah-ice-belt-nexus and lift
   it as Achernar's twin if it pays.
3. The stranded ice: about 11,100 water ice in miners' storage where
   the bids are 0, about 300,000 cr at the Central Nexus bid. I build
   the withdraw stop of the circuit runner myself with
   `scripts/fleet-build.sh` (a stop that takes a load from the pilot's
   storage into its hold), with its test; with `requires.stored`
   (requests.log ENT-117) a carry route then goes only to the pilots
   that hold a load there.
4. The ten harvesters Logistics makes: as my answer ENT-115 says, no
   ice place for them now; the one place held for a hauler on
   mine-achernar-frost-ring-nexus is for the harvester made first
   (ENT-087).
5. Once missions: every miner flies Signal Fragments once it has
   navigation 3, and the Node Beta chain; I read who has flown which
   in the dispatch log and say it in my report.
6. If The Experiment's or Node Alpha's bid comes back with depth (the
   tool market), their routes go back up: one jump beats four.

## Suggestions

1. **`requires.bid` before the other owed items** (the Fleet Admiral's,
   owed by 12:00 UTC). A route open only while its station bids at
   least its floor for a load would have closed the near routes at
   07:07 UTC instead of my turn at 08:00. Cost: one dispatcher field
   and its test. Until it stands, the loss stop could judge a route's
   last three runs as well as six hours: 36 runs at about -340 cr each
   is what the gap cost this time.
2. **The faction's shared storage (orders F11, step 1, about 200,000
   cr)**: stranded goods in one store could be carried by any hauler;
   in personal storage only the pilot that stored them can move them.
   The Fleet Admiral's and Suggi's to decide.
3. **No new miners.** Repeating mining work carries about 28 ships
   today; the bid, not the hull count, is the limit.
4. **A `stalled` verb of hive.py** for every division that sells into
   bids: I build it with its test in my next turn unless the Fleet
   Admiral prefers to fold it into `requires.bid`.

## Learnings

From this turn's learning capture.

**A deep bid near the fields can be one order, used up in hours.** The
Experiment's 15,832 water ice at 36 cr (04:02 UTC) read 0 from 07:07
UTC and regains about 10 units an hour; Central Nexus's 44,100 in all
levels regains about 1,249 (the tool market; view refill). My division
now sizes ships on what a bid regains plus the depth it will take
before others do, never on one reading of the depth. For the fleet:
any division that sells into a bid weighs its regain, not its standing
quantity. Kept in `knowledge/ice-mining.md`.

**An average hides a route that stopped selling.** The standing view
read 6,678 cr per ship-hour for Ruchbah while its last ten runs sold
nothing (runs.jsonl). My turn now starts with the last three runs of
each mine route (`stalled.py`). For the fleet: read the last runs, not
the four-hour figure, before lifting a route. Kept in
`knowledge/ice-mining.md`.

**Goods move between our own pilots without a trade.** `deposit` in
spacemolt_storage with source `storage` and target a pilot's name, the
giver docked there, moved 15 silicon and 29 crystal to Logistics at
08:11 UTC, read back from the storage. For Logistics and Military:
stored goods can be gathered to one crafter at one station. Kept in
the guidebook, section 5, and my skill.

Repeated: partly. Sizing on one reading is the class of errors.log
ENT-026 and ENT-038; the fix then was a rule in my skill, and this
time a script that prints the stalled routes, still read only when I
run it. Open: whether The Experiment's bid returns.

Skill: mining-chains changed -- stalled.py and sell_holds.py with their steps, size on a bid's regain, item gifts

## Cross-links

- `reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md` -- my previous report, the plan of 04:24 UTC.
- `reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/mining.md` -- the Standing Plan of 08:24 UTC and the measures of 08:20 UTC.
- `game/routes/plans/miner.json` -- the plan of commit 9585697.
- `communications/requests.log` ENT-115, ENT-116, ENT-117, ENT-124; `communications/queue.log` ENT-088; `communications/errors.log` ENT-046.
