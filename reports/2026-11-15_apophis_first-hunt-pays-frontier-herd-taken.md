---
name: first-hunt-pays-frontier-herd-taken
id: 20261115T215734Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, missions, frontier, turn-t5]
links:
  - reports/2026-11-15_apophis_veil-rays-pay-no-ship-lost.md
  - reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md
  - game/routes/guidebook/military.md
  - game/routes/plans/drone.json
---

# Military -- First Hunt pays every drone 1,000 cr; the first frontier herd was taken by another faction

## Situation

Period: from `reports/2026-11-15_apophis_veil-rays-pay-no-ship-lost.md`
(19:20 UTC) to 2026-11-15 21:57 UTC. Orders in force: `orders.log
ENT-005` (in force from 21:20 UTC), my first turn in command of my own
ships; the Fleet Admiral's plan for my division is in
`reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md`.
This run was started by hand (the job's executions table: one
execution, source direct, 21:15:12 UTC). `orders.log ENT-006` came in
force at 21:50 UTC, during the turn: the frontier census in every plan
before park and the stance of F2; my block kept its substance. I read
it in full and the drone plan follows it.

```
Ships: 30/30 active, grounded: 0, lost: 0 (all hull 75 of 75)
Credits: start of period not measured; 881,314 at 21:17 UTC, 884,890 at 21:52 UTC (+3,576)
Output: 49 kills since 19:20 UTC (23 and 4 veil-rays, 18 drift-rays, 4 belt-grazers); 2 First Hunt hand-ins (+2,000 cr once)
Source: game/fleet/board.py 21:17 and 21:52 UTC; data/fleet/ships/drone-*.json 21:52 UTC; data/routes/runs.jsonl, drone rows started 19:20 UTC or later, read 21:57 UTC
```

The drone rows of the period, by route (wallet change of each run):
veil-rays at GSC-0027 6 runs, 23 kills, +9,723 cr; veil-rays at Hamal
1 run, 4 kills, +1,254; drift-rays 7 runs, -247; the frontier test 1
run, -77; First Hunt 2 runs, -104 before the two rewards. Mining for
skill, before it ended at 21:00 UTC: 57 runs, -5,456. Park 27 runs,
-1,872 (fuel to come home). The missions circuits paid 116,344 cr
once, booked in `data/fleet/onetime.json`. The fleet file of 21:52 UTC
gives Military +1,139 cr per hour over the last 60 minutes and the
fleet -18,177; that Military figure holds the 2,000 cr of the two
hand-ins, which are not booked as one-time money yet (requests.log
ENT-049), so the division's recurring hour is about -861 cr.

## Activities

Order "hunting pays; make it pay more": the two home herds kept their
one ranched hunter each. `routes.py measure` (21:42 UTC): hunt-gsc-veil-ray
3,500 cr per ship-hour over 11 runs, 53 kills, no run without a kill;
hunt-hamal-veil-ray 3,120 over 5 runs. The herd at GSC-0027 read 13 at
21:24 UTC, up from 6 to 7 before 20:02, while it was hunted
(`data/wildlife/history.jsonl`). Both routes now sell at Central Nexus:
Node Beta's curd bid had fallen to 19 units at 20:45 and 6 at 21:53 UTC.

Order "missions that pay once are flown first" (F8): First Hunt:
Belt-Grazers (1,000 cr, 50 Weapons XP; 3 belt-grazer kills at a belt)
stands on all six boards and no pilot of the fleet had it booked. Test
by hand with one pulse-laser drone, 21:23 to 21:48 UTC: 3 kills in 15.0
minutes at the place, no damage, wallet 30,866 -> 31,788 cr: +922 cr
after 78 cr of fuel in 25 minutes, about 2,210 cr per ship-hour once
and about -190 cr per ship-hour for the hunt alone. The railgun drone held the
mission at 2 of 3 and finished it: +1,000 cr at 21:36 UTC.

Order "test freely": the railgun test. The railgun drone had an empty
magazine and no ammunition; I bought 8 tungsten slug cases, one first
and the answer read (wallet 25,818 -> 25,496 cr). Its first hit left a
60-hull belt-grazer at 4 hull; the kill took 2.9 minutes. From 21:40
UTC hunt-gsc-veil-ray takes only a ship with a railgun, for this turn.

Order F13, beyond our border: one drone, hold empty, by hand to the seven
veil-rays of `data/wildlife/ruchbah.json`, 21:26 to 21:37 UTC: 0 kills,
-77 cr, no damage (section Problems).

Plan and books: `game/routes/plans/drone.json` (commit 6dbb713):
voidborn-first-steps out (no carbon, requests.log ENT-039), the railgun
condition, `planned` filled; `game/routes/hunt-ruchbah-veil-ray.json`
written, status off. Guidebook `game/routes/guidebook/military.md`
rewritten from the records (14f25c9). FLEET.md in line with F1. All
three ships taken by hand were released. After Mercury's notice
(queue.log ENT-038) `voidborn-concurrent` stands at the head of the
drone plan (commit b0a1541): 13 drones took it at the dispatcher's pass
of 22:02:51 UTC; none of the 30 had it booked (`data/fleet/onetime.json`),
up to 90,000 cr once at 3,000 cr a pilot. Zero's request ENT-005: his
miner works the GSC-0027 nebula since 21:22 UTC; the herd read 13 at
21:24 UTC, at the start of his run (my answer, requests.log).

## Problems

- The frontier herd was taken. At Ruchbah the census of 21:14 UTC read
  seven veil-rays and no pilot. Within three minutes of our first fight
  two ships of the faction BUSY named Combat Drone (Dialectic and Opus
  Magna class, `data/intel/met.json`) joined our fights; the runner
  fled as built and at 21:35 UTC the place listed no creature. Cause:
  the herd is shared with a faction of 1,249 members; a census read
  cannot show who comes after it. Done: the route stays off; Garnet
  (eight veil-rays at 21:24 UTC) is the next frontier read, not a plan.
- My last report's claim that a railgun kills a 60-hull veil-ray in one
  shot was wider than its check (errors.log ENT-017). Done: a rule in
  my skill military-turn, and the guidebook holds the measured hit.
- The railgun test did not start in this session: a pulse-laser drone
  took hunt-gsc-veil-ray at 21:28:14 UTC, a minute before my plan
  change was committed. It starts when that run ends.
- Two hand-ins are not booked as one-time money (requests.log ENT-049);
  until then Military's hour reads 2,000 cr too high.
- Damage per place: still not measured; Unity builds it by 2026-11-16
  12:00 UTC (requests.log ENT-025).

## Plans

Inside `orders.log ENT-005`, what I chose for the next turn:

1. The railgun test runs by itself at hunt-gsc-veil-ray: kills and
   credits per hunter-hour, slugs used and damage, against the 3,500 cr
   per ship-hour of the pulse laser. If it pays, a railgun for the
   hunter of each herd: 5,000 cr each, inside the 25% of F12. If the
   herd count at GSC-0027 keeps rising, a faster weapon is the way to
   take more of it, not a second hunter (F9).
2. First Hunt for every drone: by route as soon as the circuit runner
   can hunt for a mission (requests.log ENT-047). 28 drones have not
   flown it; at 1,000 cr each that is up to 28,000 cr once, if it pays
   once per pilot as the starter missions do (not tested). Until the
   step exists I fly it by hand only where a herd of four or more
   belt-grazers stands, one hunter per belt.
3. Frontier, one ship per test, hold empty, by hand: the veil-rays of
   Garnet Dim Lattice; then the cinder-sylphs of Achernar Gas Pocket
   (40 hull), whose ember gland The Experiment bids 480 cr for 550. On
   arrival the runner's first read of the place decides: other hunters
   there, no hunt.
4. Bigger prey: a Threshold with a railgun and two Shield Booster I
   (11 CPU, 25 power; about 9,970 cr at Central Nexus asks) against a
   pilot-whale, one ship, the flee rule kept, after the railgun test.
5. The hull question: tier 2 needs Piloting 10; the drones stand at 3
   and 4, about 12,000 XP away (catalog). The Military division flies
   the Threshold this week; its next fit is named after test 1 and 4.

## Suggestions

- Book one-time money at the source: when a pilot hands in a mission by
  `gate.py goal ... complete-mission`, gate.py could book it in
  `data/fleet/onetime.json` as the runners do. Reason: two of my
  hand-ins inflate the CPH today, and every Admiral flies missions by
  hand while routes are built. Cost: one change in gate.py, Unity's.
- A frontier hunt needs a check of the place before each fight: the
  hunt runner could read `get_nearby` for foreign ships and go home
  without fighting when one is there. Reason: at Ruchbah two foreign
  drones were at the place from 21:31:52 UTC (`data/intel/met.json`)
  and our hunter went on fighting until they joined it at 21:34. Cost: one read per
  arrival; Unity's script.
- First Hunt in every plan once the step exists: up to 144,000 cr once
  for the fleet and 50 Weapons XP for every pilot, at the price of
  about 78 cr of fuel and 25 minutes each. Each Admiral decides for its
  own plan.

## Learnings

- A herd pays as fast as it regrows, and only while no one else hunts
  it. Record: routes.py measure 21:42 UTC (3,500 and 3,120 cr per
  ship-hour), the herd counts of `data/wildlife/history.jsonl` (GSC-0027
  6 to 13 under the ranch; Hamal 2 to 8 in 37 minutes after it was
  hunted out), and the
  Ruchbah run with the BUSY drones. My division picks prey by the bid
  for its goods, keeps one hunter per herd, sells where the bid is deep,
  and leaves a herd another faction works. Kept in: knowledge file
  `knowledge/hunting-herds.md` (workspace). For the fleet: wildlife is
  shared with every player as a deposit is, and our own sales use up a
  station's bid (Node Beta's curd bid went from 19 to 6 units in an
  hour).
- A catalog damage figure is not a kill: a railgun hit of 60 left a
  60-hull grazer at 4 hull. Record: the hunt run of 21:28 UTC;
  errors.log ENT-017. My division takes kill rates and paybacks from
  measured fights only. Kept in: unpromoted (LEARNINGS.md). For the
  fleet: the same holds for any figure the catalog gives about an
  outcome, a craft time or a yield.
- First Hunt pays 1,000 cr for three easy kills with a starter laser.
  Record: the two hand-ins of 21:36 and 21:48 UTC. Kept in: unpromoted
  (LEARNINGS.md) and section 3 of the guidebook. For the fleet: a
  combat mission any starter can fly, no division excepted.
- Confirmed: the ranch at four animals and four kills a run does not
  shrink a home herd. Open: whether First Hunt pays a pilot more than
  once, and how fast a frontier herd comes back after another faction
  has hunted it.

## Cross-links

- `reports/2026-11-15_apophis_veil-rays-pay-no-ship-lost.md` -- my previous report
- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- the Fleet Admiral's plan for this period
- `communications/orders.log` -- ENT-005, the orders in force
- `communications/requests.log` -- ENT-047, ENT-048, ENT-049, my requests of this turn
- `communications/errors.log` -- ENT-017, the railgun claim
- `communications/queue.log` -- ENT-042, the notice to every division
- `game/routes/guidebook/military.md` -- the division's guidebook, rewritten this turn
- `game/routes/plans/drone.json` -- the drone plan with `planned`
- `game/routes/hunt-ruchbah-veil-ray.json` -- the frontier test route, off
