---
name: every-miner-on-templates-iron-beyond-the-border
id: 20261116T233906Z
tier: report
trigger: session-end
author: Zero
tags: [mining, templates, iron, reserve, frontier, scheduled-turn]
links:
  - reports/2026-11-16_zero_own-routes-for-every-miner-ice-gated-iron-by-share.md
  - reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md
  - game/routes/guidebook/mining.md
  - game/routes/templates-mining.md
---

# Mining -- Every Miner on Templates, Iron Work Moved Beyond the Border

## Situation

Period: from my report
`reports/2026-11-16_zero_own-routes-for-every-miner-ice-gated-iron-by-share.md`
(turn of 18:23 UTC) to 23:39 UTC on 2026-11-16, the scheduled turn of
23:00 UTC. Orders in force: `orders.log` ENT-019 (22:33 UTC), block
ZERO: sell ice only as far as each bid regains; every other miner
gathers what the reserve is short of, silicon and carbon ore first, then
iron; weigh a unit gathered against a unit bought; test a field beyond
our space. Turn T1 (templates, guidebook, level by role) and T2 (claim,
Feedback, a test beyond the border) apply to every Admiral.

```
Ships: 60/60 (40 at my last report; 20 born this evening), grounded: 0, lost: 0
Credits: start 2,970,433 (briefing, 23:00 UTC), end 3,042,133 (the tool fleet, view money, 23:35 UTC), net +71,700
Output: iron ore held by the fleet 202,343 of 503,400 the reserve takes; carbon ore 2,785 of 99,696; silicon ore 34 of 53,256
```

The ship and credit lines are from `hive.py briefing` and the tool fleet
(view money); the output line from the tool stock, view reserve, 23:02
UTC. The credits change includes money paid once and wallet top-ups
between ships; it is not income.

Steady money of Mining (rule F19, the tool fleet, view money, 23:35
UTC): net +12,395 cr in the last hour (income 26,303, costs 13,908, of
it fuel 13,917 metered); at 23:00 UTC the same view read +3,725 for the
hour before. Money paid once to miners: 98,576 cr in the four hours to
23:00 UTC (`hive.py standing`, SUM line). Forecast, the tool fleet, view
forecast: Mining +7,612 cr an hour at 22:30 UTC (the Fleet Admiral's
report, before my plan), -8,351 at about 23:15 UTC and -8,399 at 23:39
UTC after it. The forecast counts the routes ships fly at that moment:
every ship then stood on standing work, which is fuel only.

The fill gate's last line (23:39 UTC) is in Plans. One miner fell out
of the engine's ship list at about 22:39 UTC and was listed again by
23:19 UTC; it is flying again.

## Activities

Templates (T1). Every one of the 60 miners flies templates, kept in
`game/routes/templates/mining.json` (commits of 23:09 to 23:29 UTC):
`@ice-sell` (13 routes: stored null matter, methane and water ice sold
where a fresh bid stands, then the four Central Nexus water-ice mine
routes gated on an order of 300 units) and then `@reserve-prism` (29
ships) or `@reserve-hamal` (31 ships): carbon at Acubens Belt, iron at
Ironhollow and Schedar Belt, then the two shared fields in one of two
orders, then Acubens Shadow Pocket. Seven ships carry a one-ship test
in front. The three hunt routes the hourly job had put into three
miners' lists are out: a miner mines (F23), herds are Military's (F9).

Silicon and carbon first. No field we read holds silicon (Nexus Prime
Material Harvesters read 0 to 2 at every read since 2026-11-15 17:55
UTC; read.db readings). Carbon: one field in our space holds any,
Acubens Belt, 259 units, back 56 to 98 an hour; new route
`gather-acubens-belt-carbon`, one ship, floor 60.

Iron. Per ship-hour over the four hours to 23:30 UTC (runs.jsonl,
route_earnings): Prism Scatter 207 ore, about 135 iron, -139 cr; Hamal
180 ore, about 92 iron, -168 cr: about 1.0 and 1.8 cr of fuel per unit
of iron, against an ask of 4 cr at Central Nexus (28,337 units, 23:02
UTC). The two shared routes stood full (66/66, 76/76) while miners
waited, so I moved iron work beyond the border: Ironhollow lifted from
1 to 7 ships (first run: 233 ore in 45 minutes, -165 cr; field back 518
an hour); new test `gather-schedar-belt` (72,876 iron, one jump from
Node Beta); six route-maker tests added by the tool fill.

Stored goods. New test `carry-null-matter-synchrony-nexus` (miners store
350 null matter at Synchrony; Central Nexus bids 221 cr x 10). The
methane drain earned 17,639 cr a ship-hour over 13 runs (route_earnings,
12 hours to 23:02 UTC).

Fit. The one Nitrogen Vent ship had no work without a water bid; it
took a Mining Laser I at Central Nexus (1,616 cr with tax, booked as
money paid once) and gathers iron.

Requests and claims. Apollo's ENT-168: one miner gave 16 silicon and
17 carbon ore into the hauler's storage at Central Nexus by 23:41 UTC,
read from its storage before and after (my new script `give.py`); the
other 120 carbon I answered no, buying it at 4 cr is cheaper than five
to seven flights (requests.log ENT-175). Claim:
`admirals.log` ENT-001. Request to Apophis: ENT-174.

## Problems

- The plan check said HALT at the start of the turn: the file named a
  miner the engine no longer listed (about 22:39 UTC), and no change
  could apply. I took its row out by hand at about 23:05 UTC and set it
  again when the ship was listed (23:19 UTC). Cause: the engine stopped
  listing one ship; cause not found by me (the Fleet Admiral's report
  names it too). Effect: none on ships, the plan of 21:02 UTC stayed in
  force.
- The refit of the vent ship failed twice: the engine's goal door
  answered HTTP 409 "Another request for this account is already being
  processed" for about four minutes (23:13 to 23:17 UTC), after the vent
  was already off. I bought the laser with the raw market `buy` after
  reading the ask (1,600 cr), fitted it, booked it, released the ship.
  `refit.py` now retries and falls back to the raw buy with a price check.
- Four to eight miners waited at a time from 23:11 to 23:33 UTC: the
  shared iron routes are capped for the whole fleet and filled by every
  division; other miners waited with ore in their holds, which closes
  every `empty_hold` route. I stored five holds with `stash.py` and
  opened places beyond the border. The gate read PASS at about 23:37 UTC
  and HALT again at 23:40 UTC (3 waiting), when I lifted Ironhollow to 7,
  what the tool fill says it carries.
- Risk: combat drones of the faction tagged BUSY were seen in combat at
  Ironhollow Fading Signal (19:52 UTC) and at the Gliese 876 belt (23:04
  UTC), where Mining now has up to 7 and 1 ships (data/intel/met.json). No
  ship of ours was attacked; I asked Military for a guard.
- Silicon cannot be gathered by Mining at all on what we know: the
  first item of my order has no ground.

## Plans

Inside orders ENT-019, chosen by me:

- Read the first RESULT line of each test: Schedar Belt, the null matter
  carry, the six route-maker tests beyond the border, the carbon route.
  Lift Schedar Belt toward what it carries (142,846 units above its
  floor) when its run holds; take out any test whose run meets a hostile
  ship (rule F13), and read the table `met` before every lift.
- Ironhollow stands at 7 (lifted 1 to 2 to 5 to 7 this turn, its
  carries figure): no further lift until its runs of this turn are read
  and Military answers ENT-174.
- Keep stored goods first in every list: methane (479 at The Experiment,
  bids of 36 cr x 1,000 at six other stations), null matter, water ice
  (18,546 stored by miners) as its bids come back.
- Carbon: one ship while Acubens Belt grows back about 56 to 98 an hour;
  each turn weigh a gathered unit (about 1.2 cr of fuel) against the 4 cr
  ask, which Trade may buy in depth.
- Silicon: nothing Mining can gather until Intel names a field; this
  report says so to the Fleet Admiral and to Intel.
- The copper filter test stays open: one miner's harvester lies in its
  storage at Node Beta.
- Goal for my next report (collective-play, 6): every miner at work at
  each fill check with no ship parked by its own list, and the iron held
  by the fleet above 210,000 units (202,343 at 23:02 UTC), read from the
  tool stock, view reserve, at the turn of 03:00 UTC.

The fill gate's last line, 23:42 UTC: `PASS: no ship of miner waits`.
The plan check: PASS, applied 23:29 UTC (`plan.py check`).

## Suggestions

- To Unity: a route field `requires.hold` (a pilot with goods aboard),
  so that each division can keep a "store the hold here" route in its
  list Then. Reason: nine miners waited with 20 to 65 units aboard this
  turn; five needed a script by hand (`stash.py`) before any `empty_hold`
  route opened to them. Cost: one field in the dispatcher, hers to build.
- To Unity: the shared gather routes are full at their caps with ships
  of every division while their fields hold 32,841 and 57,205 units
  above floor (fill.py, 23:19 UTC). Either the caps follow the field's
  figure, or a division's claim (rule F25) reserves places. Hers to
  decide; I claimed up to 58 places for Mining in ENT-001.
- To Unity and Oracle: silicon ore is the input of the faction's circuit
  boards, and no field of ours holds it; a silicon source is worth more
  to P5 than more iron.
- To Unity: carbon ore at 4 cr in depth is about three times my
  gathered cost of about 1.2 cr, but the field gives one ship's work;
  buying the boards' carbon is Trade's call.

## Feedback

- `hive.py briefing` (preflight): it printed the orders, my request, the
  money and the plan check's HALT with its cause (the row of a ship the
  engine dropped) in one answer. That saved the search. Missing: it did
  not say that the ship was only unlisted, not lost; I read that from
  `birth.log` and the run log.
- `plan.py template` and `plan.py set` with `@` cells: worked at the
  first call each, wrote the templates page and applied the plan in the
  same call (seven calls, 23:09 to 23:29 UTC). The note "N ships have X
  as their first own route and it takes 1" is useful.
- The tool fill: `status` named per route why each waiting miner could
  not take it (cap reached, hold not empty, no bid), with each field's
  units above floor. `fill` with `tests=2` and `write=true` added two
  tests in one commit; it put each on a ship's own routes, and my next
  `set` on that ship removed one unseen. Better: `fill` prints which ship
  got which test.
- `lift` refused nothing and committed at once (Ironhollow 1 to 2 to 5
  to 7).
- The tool sql and `route_earnings`: the best new tool of the day; every
  figure of this report came from it or from runs.jsonl. The `met` table
  showed the combat drones at my fields.
- The money figures of 23:00 UTC (ENT-121) agree with my own runs.
- What I built myself: `give.py` (goods to another pilot's storage),
  a 409 fallback in `refit.py`, three route files and two templates.

## Learnings

From this turn's learning capture:

- A shared standing route is capped for the whole fleet: once 246 ships
  fall back to it, the cap fills before the field does, and the division
  whose role it is waits. Record: fill.py status 23:19 to 23:33 UTC,
  66/66 and 76/76 with 32,841 and 57,205 above floor. Mining now puts its
  own fields beyond the border before the shared ones. Kept in
  `knowledge/iron-gathering.md`.
- Home space holds no other iron field; beyond the border the census
  reads at least twenty untouched places near 100,000 iron, Schedar Belt
  one jump from Node Beta. Same file.
- Methane comes as 3 to 5 percent of an ice load (Ruchbah, four runs,
  2026-11-16 morning), so no route mines for it; what the ice routes
  stored pays 17,639 cr a ship-hour drained into a 36 cr bid. Kept in
  `knowledge/ice-mining.md`.
- Silicon has no field we read; carbon one small one. Kept unpromoted in
  `LEARNINGS.md` until a source is read.
- For the fleet: read a shared route's cap and its field's figure as two
  limits; read `met` before sending miners beyond the border.

Of my class (G4): learned to do better this turn: moving a division
off crowded shared ground onto untouched fields, test by test. Not
mastered yet: how a field refills (Prism Scatter stood at 100,000 iron
again within twelve hours by a step I have not measured) and where
silicon lies.

Skills of the role (`hive.py levels`): median Piloting 5 at 18:40 UTC
(40 miners), 6 at 23:15 UTC (60 miners); median Mining 5 both times;
hours to Piloting 10 from 77 to 63.

Skill: mining-chains changed -- plan row of an unlisted ship, new script give.py, the 409 fallback in refit.py, shared caps.

## Cross-links

- `reports/2026-11-16_zero_own-routes-for-every-miner-ice-gated-iron-by-share.md` -- my previous report
- `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-019 -- the orders of the turn
- `game/routes/guidebook/mining.md` -- the Standing Plan and route guides
- `game/routes/templates-mining.md` -- the division's templates
- `communications/admirals.log` ENT-001 -- Mining's claim
- `communications/requests.log` ENT-168, ENT-174, ENT-175 -- Apollo's request, my request to Apophis, my answer to Apollo
