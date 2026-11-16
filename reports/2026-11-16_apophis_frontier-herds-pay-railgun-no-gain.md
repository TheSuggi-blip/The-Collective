---
name: frontier-herds-pay-railgun-no-gain
id: 20261116T000852Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, frontier, missions, fits, turn-t7]
links:
  - reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md
  - reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md
  - game/routes/guidebook/military.md
  - game/routes/plans/drone.json
---

# Military -- Four of six frontier veil-ray herds paid on their first run; the railgun brought no gain

## Situation

Period: from `reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md`
(2026-11-15 21:57 UTC) to 2026-11-16 00:09 UTC. This run of the scheduled
job turn-apophis started at 23:18 UTC. Orders in force: `orders.log
ENT-007`, written 23:17 UTC and in force from 23:30 UTC, read in full at
preflight; between my last report and 23:30 UTC `orders.log ENT-006`
held. My block in ENT-007: hunt, explore with the scouts, design the
ships for battle; one hunter on each veil-ray herd of our space; the five
frontier veil-ray routes of the route maker and Ruchbah again, each a
test with one ship, `alone` and an empty hold; the First Hunt routes
for every drone when their RESULT lines are read; name the hull and fit
the division flies next. The Fleet Admiral's newest report is still
`reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md`.

```
Ships: 30/30 active, grounded: 0, lost: 0; hull 75 of 75 on all 30 at 00:06 UTC
Credits: 884,890 at 2026-11-15 21:52 UTC, 1,108,529 at 2026-11-16 00:06 UTC, net +223,639
Output: 91 drone runs; 21 hunts with 52 kills; one-time rewards 180,780 cr
Source: game/fleet/board.py at 21:52 and 00:06 UTC; data/fleet/ships/drone-*.json 00:06 UTC; data/routes/runs.jsonl, drone rows started 21:52 UTC or later, read 00:08 UTC
```

The 21 hunts made +14,768 cr in 441.4 hunter-minutes, 2,007 cr per
hunter-hour, test runs included (runs.jsonl, same read). The rest of the
credits are one-time missions: Concurrent Approval 30 runs (90,000),
the mining missions 10 runs (33,000), Precedence 10 runs (40,000),
Market Participation: Selling 20 runs (17,780). The collector's rate for
Military at 00:06 UTC: 5,568 cr per hour without one-time money, 56,702
one-time per hour, fuel 3,830 and repair 145 cr per hour
(`data/fleet/fleet.json`, totals.rates.divisions). No contact from
another player reached our ships (`game/fleet/inbox.py show --to-us`,
23:22 UTC: 0 to us). No request addressed to me was open at preflight.

## Activities

**The plan as a standing loop (orders F8).** I rewrote
`game/routes/plans/drone.json` in six commits between 23:28 and 00:07
UTC (2287b3e to e1d0d69) and wrote the routes' measures once (cd7baa3). It now holds, in order: the one-time
missions Precedence, First Hunt (four herds), Selling, Concurrent,
Substrate, missions-1 and the mining missions; the two home veil-ray
herds; six frontier veil-ray herds; one yield test; the frontier census;
park. The dispatcher started 12 hunts and tests within two minutes of
the first commit; 13 drones were hunting at 23:30 UTC (board).

**One-time missions.** Precedence (4,000 cr once) and Selling (1,000 cr
for the pilots that hold the starter mission) entered the plan when the
command group's first RESULT lines were read: 10 and 20 drone runs by
00:02 UTC, +38,968 and +17,311 cr. The three First Hunt routes with the
runner's new hunt step paid the command group +974, +934 and +945 cr in
19 to 28 minutes; they head the plan, and I wrote a fourth herd beyond
the border, `voidborn-first-hunt-schedar` (20 belt-grazers at 21:14 UTC,
`alone`, empty hold), a test with one ship.

**The railgun test ended.** Three runs at `hunt-gsc-veil-ray` with the
Piercing Railgun I: 4, 4 and 0 kills; the two full trips took 21.4 and
24.0 minutes, the eight pulse-laser trips with four kills there 21.7 to
26.8 (runs.jsonl). Its eight slug cases ran out in the third run, which
fled after one fight (-65 cr). No gain: both home herds take every
pulse drone again and no hunt takes a railgun ship
(`requires.without_module`).

**Frontier veil-ray tests, one ship each, `alone`, empty hold.** Seven
runs from 23:29 UTC: Achird +2,189 cr, Ruchbah +1,243, Keid +1,199,
Cedarhold +561, all four kills and full hull; Garnet, Okab and a second
Ruchbah run left at once with a ship not of ours at the place (-99, -99,
-77). Together +4,917 cr in 145.3 minutes, 2,030 cr per hunter-hour.

**Yield tests in our space.** Five species no run of ours had looted,
one run each: bell-jellies, rime-grazers with pressblisters and
deuteron-slugs dropped nothing bid over 2 cr; kiln-snails gave no kill;
patina-grazers were left (a foreign ship). Six runs, -98 cr in all;
four tests are off.

**Hull and fit.** The game's `commission_quote` (read only) prices a
Vigil at 106,208 cr or 15,040 cr with materials, a Paradox at 82,690 or
12,368; their materials at our best asks with depth cost 39,187 and
27,688 cr (books of 23:59 to 00:01 UTC). The division flies the
Threshold with a Pulse Laser I next; what a tier-1 hull earns is not
measured.

**Levels.** Piloting 3 on 20 drones, 4 on 8, 5 on 2 (ship files, 23:35
UTC); the guidebook's read of 21:17 UTC showed 3 and 4 only.

## Problems

**Hull lost in a test, no ship lost.** The kiln-snail yield test at
Eltanin Prime Belt ran 32.8 minutes with no kill and drove the drone
from 75 to 46 hull (lowest 68% in the battle table), -167 cr. Cause:
prey of 100 hull, the top of what orders F9 allow, hits a starter
without a defence module hard. Done: the route is off and out of the
plan (e1d0d69); the ship was repaired at dock and read 75 of 75 at
00:06 UTC.

**The railgun ship ran dry.** It fled its third run with no ammunition
and has sat out of the hunts since. Cause: the dispatcher checks a
fitted module, not the ammunition in the hold, and eight cases lasted
about two and a half runs. Done: no hunt route takes it until it
carries ammunition.

**Shared herds.** Four runs met a ship not of ours and left (-335 cr in
all). The Hamal home herd read 16 at 21:59 and 0 at 23:41 UTC with
other pilots at the place; our run there from 23:25 UTC made 2 kills and
lost 91 cr. Cause: other players hunt the same herds. Nothing to fix;
the route rests while the herd is under four.

**A test flew twice.** The node-gamma ice-belt test started a second run
at 23:46 UTC, ten minutes before I took it out (-60 cr). Cause: the
dispatcher starts a route between my reading and my commit.

**A tool wrote other divisions' files.** `routes.py measure --write`
wrote the measured block of 24 route files, 15 of them not Military's. I
reverted those before my commit (cd7baa3); a pitfall in my skill now
says how.

No ship was lost, no pilot fired on us, and no hand hold is left (the
grep for a hand order printed nothing).

## Plans

Inside orders.log ENT-007, my own choices unless named:

1. **Ships at work for the next four hours.** The one-time routes hold
   every drone that has not booked them: Precedence (10 drones had it
   by 00:02 UTC, 11 more were on it at 00:06), First Hunt for all 30 across four herds, one
   hunter each (the command group flies the same three home herds), and
   Selling for the few drones that still hold it. After them the
   hunts hold at most nine drones at once, one per herd; the frontier
   census takes up to twelve ships of the whole fleet; the rest park.
   At 00:06 UTC 18 of 30 drones were flying.
2. **Frontier herds.** After three runs per herd: `routes.py measure
   --write` (Military files only), lift nothing (a herd takes one
   hunter), take out a herd where a foreign ship stood twice. Garnet
   and Okab are the first candidates.
3. **The railgun ship.** A Pulse Laser I lies in our storage at Central
   Nexus (`ledger.py show`, 23:25 UTC); refit it by hand with one
   `install_mod`, or craft Ferrous Slug Cases from stored iron; then it
   rejoins the hunts.
4. **Next hull.** Weigh one Vigil for prey of 100 hull and for guard
   work: the quote's materials for its default loadout include two
   Pulse Laser I and two Shield Booster I; about 54,227 cr in all. Inside F12 (25% of
   the division's credits for weapons and hulls); a drone's wallet held
   34,349 to 47,721 cr (ship files, 00:10 UTC), so it needs Unity's word on moving credits between our
   own pilots. Not before the frontier figures hold.
5. **Guard.** When a guard step exists (requests.log, this turn), one
   drone at each frontier field our miners work.

## Suggestions

1. **`routes.py measure --write` for one division** (a `--mine` or
   `--role drone` option). Reason: today it writes every route file of
   the fleet, so an Admiral who follows fleet-play step 6 either commits
   other divisions' files or reverts them by hand. Cost: one filter.
   Unity's script.
2. **An ammunition check in the dispatcher.** A hunt is not given to a
   ship whose weapon takes ammunition and whose hold has none. Reason:
   the railgun ship fled a run with an empty magazine (-65 cr) and the
   only guard now is a route-by-route exclusion. Cost: one condition
   beside `requires.module`. Unity's script.
3. **More herds for First Hunt.** Three herds of one hunter each serve
   the 144 pilots that had it open (route maker, 23:12 UTC); a fourth
   beyond the border is under test. A run takes 19 to 28 minutes, so a
   herd serves at most about nine pilots in four hours. Cost: none; every Admiral can add the Schedar route when its
   first RESULT line holds.
4. **A word on the first hull.** Whether Military may move credits
   between its own pilots to build one Vigil. Suggi's or Unity's to
   decide; the figure it should move is credits per hunter-hour on prey
   the starter cannot take.

## Learnings

**A hunter is bounded by its herd, not by its weapon.** Two railgun
trips at GSC-0027 took 21.4 and 24.0 minutes against 21.7 to 26.8 for
eight laser trips, and a 60-damage hit left 60-hull prey at 4 and 8 hull
(runs.jsonl, the hunt log of 22:49 UTC). My division keeps the starter
fit and buys a weapon only for a measured gain at the same herd. Kept
in `knowledge/weapons-fits-and-hulls.md`; the unpromoted entry on
catalog damage is now covered there and removed.

**Herds are shared, at home and beyond the border.** Of seven frontier
runs, four paid 561 to 2,189 cr and three met a foreign ship and left
for 77 to 99 cr; the Hamal herd fell to 0 with other pilots there. The
`alone` rule costs little where it fires. Kept in
`knowledge/hunting-herds.md`.

**Only veil-rays pay among the prey tested.** Four new species dropped
goods bid at 1 to 2 cr or nothing, and a 100-hull kiln-snail cost 29
hull without a kill. A yield test is one run and leaves at once. Kept in
`knowledge/hunting-herds.md` and `weapons-fits-and-hulls.md`.

**For the fleet:** a hull is priced without an order (`commission_quote`)
and its materials option halves the cost; steel plate and copper wiring
are what our stored ore makes. Confirmed: First Hunt pays once per pilot
as a route (the open entry in LEARNINGS.md stays until a knowledge file
on one-time missions holds it). Open question: what a kill gives in
Piloting XP.

## Cross-links

- `reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md` -- my previous report
- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- the Fleet Admiral's newest report
- `communications/orders.log` -- ENT-007, the orders in force
- `game/routes/plans/drone.json` -- the drone plan of this turn
- `game/routes/guidebook/military.md` -- every figure of this report by route
- `game/routes/index.md` -- every route with its measure
