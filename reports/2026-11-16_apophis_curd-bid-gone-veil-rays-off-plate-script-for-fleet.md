---
name: curd-bid-gone-veil-rays-off-plate-script-for-fleet
id: 20261116T092936Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, market, crafting, fill-gate]
links:
  - reports/2026-11-16_apophis_chain-and-cracking-the-shell-open-yield-tests-spent.md
  - reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md
  - game/routes/guidebook/military.md
---

# Military -- The Curd Bid Left Every Station, the Veil-Ray Hunts Are Off, and Carapace Becomes Plate by Script

## Situation

Period: from my report of 2026-11-16 05:27 UTC
(`reports/2026-11-16_apophis_chain-and-cracking-the-shell-open-yield-tests-spent.md`)
to 09:30 UTC, the scheduled turn of 09:00 UTC. Orders in force: `orders.log`
ENT-013 (in force from 06:55 UTC), the block APOPHIS and the three things for
every division: the Node Beta chain, Signal Fragments at the head of every plan,
and F21. The plan for my division is in Unity's report of 06:59 UTC
(`reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md`):
waiting drones as the reserve for once missions, carapace into armor plate, no new
drones.

```
Ships: 30/30 active, grounded: 0, lost: 0
Credits: start 1,247,951, end 1,643,933, net +395,982
Output: 384,813 cr paid once in the four hours to 09:29 UTC; steady -866 cr
Source: hive.py fleet (05:31 and 09:29 UTC); hive.py standing (09:29 UTC);
        data/fleet/ships/drone-*.json (09:29 UTC, no hull below 75)
```

In one unit (orders F19), the four hours to 09:29 UTC (`hive.py standing`): -7
credits per ship-hour over all 30 drones on the clock, -16 per ship-hour flown
(54.9 ship-hours flown), and 384,813 cr paid once beside it. At 09:10 UTC the tool
fleet with view tasks read 38 credits per ship-hour over all drones and 85 flown;
the two reads stand 19 minutes of window apart, and which runs moved the figure is
not traced. The scale of that hour: the fleet's best repeating
route is our own `hunt-test-achernar-cinder-sylph`, 6,423 credits per ship-hour over
four hours (view tasks, 09:10 UTC); a ship without work earns 0.

The fill gate's last line, 09:34 UTC: "PASS: 20 ships of drone wait, and nothing
that pays and no test is open to them"; after my session entry it had halted once
more on `hunt-dimming-pocket-veil-ray`, a veil-ray route in no plan, set off at
09:32:55 UTC (commit time) on the same record as the seven. No drone is held by hand (`grep "hand
Apophis" data/fleet/orders/*` printed nothing at 09:29 UTC). Levels (`hive.py
levels`, 09:10 UTC): Piloting 3, 4 and 6 (lowest, median, highest), 89 XP an hour
on average since birth, 141 hours to Piloting 10 at that rate.

## Activities

**Once missions (orders ENT-013, every division).** At 09:02 UTC Signal
Fragments and Network Expansion went to the head of the drone plan (commits
b65e990, 5ad86fe). By 09:29 UTC four drones had handed in Signal Fragments
(+27,584 cr in four runs) and seven drones Network Expansion (+10,150 cr). The Node Beta chain is flown: 29 of 30 drones in 29 runs
from 05:30 UTC, +315,369 cr in sum (`data/routes/runs.jsonl`). First Hunt at the two
home herds handed in 3 times each in 5 drone runs from 05:30 UTC.

**Hunting.** From 05:30 to 09:10 UTC the drone hunts flew 1,052 hunter-minutes for
+20,307 cr, 1,158 cr per hunter-hour (`hunt_figures.py`). The cinder-sylph herd at
Achernar Gas Pocket paid 6,340 cr per hunter-hour over three runs (4 kills, 6 ember
glands) and is the fleet's best repeating route. The seven veil-ray hunts paid until
07:05 UTC and lost from then on (Problems).

**Plan (orders F8).** At 09:05 UTC (2ea9189) the seven veil-ray hunts and First
Hunt at Achernar and Schedar left the plan; at 09:12 UTC the seven veil-ray route
files were set `status: off` with the reason and the condition that brings them
back (f8a4fe3); at 09:16 UTC First Hunt at Schedar the same (c375820), since no plan
holds it; at 09:19 UTC Cracking the Shell (central) left the drone plan (57ec2f2).
Both First Hunt route files store everything aboard at their last stop, as
Logistics asked (queue.log ENT-092).

**Carapace into armor plate (APOPHIS (6), F21).** Once by hand: one drone made 2
plates of 12 carapace at the Central Nexus workshop at 09:06 UTC and sold them into
a bid of 373 cr x 4, +746 cr, no fuel. Then by script: `game/fleet/plate.py`
(c14eb11), Apollo's script from his skill brought into `game/fleet/` for every
division, with many pilots in one call and the bid read again for each pilot. Its
test failed before the script existed; every gate of `fleet-build.sh` passed. Run
over all drones twice: 2 plates made, 1 sold at 373 cr (+373 cr); most drones were
busy on once runs and were skipped.

**Holds.** `stash.py` on nine drones in the background: two stored, seven busy.

**S6 sites (sight records from 05:17 UTC):** Achernar 53 reads, a pilot not ours in
13, no pirate; Alnair 20 and 10, no pirate; Wolf 1061 26 and 12, no pirate
(`data/intel/sightings.jsonl`). No fight against a ship of ours is on record.

## Problems

**The veil-ray hunts flew at a loss for two hours.** The verdigris curd bid (330
cr x 50) left all seven stations of our books between 07:08 and 07:51 UTC and none
stood at 09:02 UTC (`data/market/history.jsonl`). From 07:05 UTC the seven drone
veil-ray hunts ran 23 times, 18 looted curd, none sold anything: -2,056 cr
(`data/routes/runs.jsonl`, read 09:20 UTC). Our runs had sold 128 curd from 03:00 to
08:00 UTC against about 350 bid; whether others sold the rest or the stations
withdrew their bids is not in our record. Cause: no check ties a hunt route to the
bid for its drop; the loss stop judges six-hour sums, which still held the sales
before 07:00 UTC. Done: routes off; requests.log ENT-125.

**The fill gate asked for losing routes back.** It judges a route by all its runs:
twice between 09:05 and 09:16 UTC it called the Faintlight veil-ray hunt (1,300 by
all runs) and then First Hunt at Schedar (+20 cr a run) paying work. Done: `status: off` on each,
with its record, and on the Dimming Pocket veil-ray route (80 by all runs) when the
gate asked for it after 09:30 UTC. The gate's PASS rests on that judgment.

**First Hunt at Achernar Belt:** 19 drone runs from 05:30 UTC, 0 hand-ins, -1,474
cr; a ship not ours at the place in every run from 06:49 UTC. Schedar: 1 hand-in
in 17 runs from 03:13 UTC. I kept Schedar last in the plan at 05:20 UTC on the
gate's figure: the same class as Acubens, repeated.

**Cracking the Shell (central):** I moved its hunt to Alnair Ice Fields at 05:17
UTC on one read; Alnair held no pressblister at 09:07 UTC; 5 runs of the fleet from
05:43 UTC failed, -871 cr. requests.log ENT-126.

**Two errors of my own:** requests.log ENT-126 names 09:25 UTC for a commit of
09:19:30 UTC (errors.log ENT-049); three lessons went to the shared memory bank by
the wrong tool, the duplicates retired (errors.log ENT-050).

## Plans

Inside orders ENT-013, the choices mine:

- **The standing plan** (`game/routes/plans/drone.json`, committed 09:19 UTC):
  Network Expansion, Signal Fragments, Precedence, the Node Beta chain, First Hunt
  at the two home herds, Cracking the Shell at Achernar, the other once routes, the
  two cinder-sylph hunts, `census-guard-ice`, `census-frontier`, park. Expected: the
  once rewards (about 6,900 cr for each drone with navigation 3 not yet paid;
  1,450 for each with First Steps), 1,500 to 5,400 cr per ship-hour at the
  cinder-sylph herds, about -610 cr per ship-hour for each guard census ship.
- **Every turn first:** `loot_bids.py` (new in my skill military-turn) prints the
  bid for every hunt's drop; a plan route whose drop has no bid goes off, an off
  route whose bid is back returns. The seven veil-ray hunts come back the turn a
  curd bid of 100 cr or more reads again.
- **Carapace:** `plate.py` over all drones at the start and again late in every
  turn, no plate past a bid's depth. About 617 carapace lie in drone storage; how
  many plates the pools take in four hours is not measured: my next turns measure it.
- **First Hunt at Achernar and Schedar** come back when a census reads their belt
  without a ship not ours twice in a row.
- **Capacity (F18):** hunting carries one or two hunters today (the Achernar
  cinder-sylph herd read 4 at 08:49 UTC; every other cinder-sylph herd 1 to 3);
  of the 14 herds with a route measured above zero (view capacity), the veil-ray
  herds carry no hunter while the curd has no buyer; First Hunt has 2 herds for 19 drones without it. How fast a
  herd regrows is not measured. 19 drones wait: the division needs no new drone.
- **Ships (F17):** no purchase. Every hunt is bounded by its herd and its bid, not
  by the weapon.
- **Guard:** `census-guard-ice` stays until the guard route kind exists
  (requests.log ENT-070, accepted).

## Suggestions

- **`requires.bid` on hunt routes** (requests.log ENT-125, Unity's to build): the
  dispatcher closes a hunt whose drop has no bid and reopens it when the bid is
  back. It would have stopped the veil-ray loss at the first empty read, 07:08 to
  07:51 UTC, instead of two hours later. Cost: one condition beside the
  `requires.bid` already accepted for circuits (ENT-072).
- **The fill gate counts recent runs.** A route whose last N runs lost money, or
  whose last runs all left for a ship not ours, is no paying work for the gate. It
  would have spared two of today's three HALTs. Unity's to decide; cost: a window
  in fill.py's figure.
- **Pirate Bounty** (2,000 cr once, kill one pirate) stands on the boards of
  Central Nexus, Node Gamma and Synchrony Hub (`data/missions/`, 09:20 UTC); pirates
  stood at Gliese 876 and Felis (queue.log ENT-090). Orders F2 forbid firing first
  at an NPC ship, so it is not flown. Suggi's to weigh: 2,000 cr a pilot, 292,000 cr for
  146 pilots if it pays once each (not known), against a posture that starts no fight. My recommendation: no change
  until a hull and a test show a starter can win such a fight.

## Learnings

From this turn's learning capture.

**A herd pays only while its drop has a buyer, and the buyer can leave every
station at once.** The curd bid left seven stations in 43 minutes, and the routes'
figures over all their runs still read 900 to 3,020 cr per ship-hour afterwards
(`data/market/history.jsonl`; the route files). My division now reads the bid for
every hunt's drop at the start of every turn and sets a route without it off. For
the fleet: any route that sells one good, ice and gas too, is safe only with a
check tied to that good's bid that fires without a turn. Kept in
`knowledge/hunting-herds.md` (updated).

**Carapace has value as plate, and the plate bids are the limit.** 12 carapace made
+746 cr at no fuel; the drones hold about 100 plates' worth against pools of 3 to 6.
`plate.py` now serves every division. Kept in `knowledge/hunting-herds.md`.

**The fill gate's PASS is only as true as the route files.** It judges by all-time
figures, so a route whose bid or herd is gone must say `status: off`, with the
condition that turns it back on. Kept in my skill military-turn.

**A time or a hash goes into an entry only after the action** (errors.log ENT-049),
and the shared bank takes only rules another member needs (ENT-050). Both a
repeat of a class the fleet had named today: a rule in another member's skill does
not protect mine.

Open: how many plates the pools take in four hours; whether the curd bid returns.

Skill: military-turn changed -- loot_bids.py, plate step, five pitfalls (fill gate, shared routes, entry times, fill tool refusal, two banks)

## Cross-links

- `reports/2026-11-16_apophis_chain-and-cracking-the-shell-open-yield-tests-spent.md` -- my previous report, 05:27 UTC.
- `reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/military.md` -- the Standing Plan and the figures of this turn.
- `game/fleet/plate.py`, `scripts/tests/test_fleet_plate.py` -- carapace into plate for every division.
- `communications/orders.log` ENT-013; `communications/requests.log` ENT-125, ENT-126; `communications/queue.log` ENT-093; `communications/errors.log` ENT-049, ENT-050.
