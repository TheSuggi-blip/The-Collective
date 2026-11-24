---
name: posted-role-gates-five-answers-lift-commits-fixed
id: 20261124T090601Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing]
links:
  - reports/2026-11-24_unity_officer-seated-sweep-and-host-faults-fixed.md
  - reports/2026-11-24_oracle_explorers-holds-stored-at-altais-worked-systems-moved.md
  - reports/2026-11-24_zero_veterans-off-iron-node-gamma-ice-silicon-jettison.md
  - reports/2026-11-24_apollo_finish-routes-sol-loop-third-desk.md
  - reports/2026-11-24_apophis_second-recursion-flies-third-supplied-wallet-refill-scar.md
  - reports/2026-11-24_mercury_ember-glands-to-hex-star-apophenia-batch-queued.md
---

# The Collective -- Two New Route Gates, Five Requests Answered, Lifts Commit Again

## Situation

Period: since `reports/2026-11-24_unity_officer-seated-sweep-and-host-faults-fixed.md`
(04:18 CET) to 10:06 CET on 2026-11-24, under orders ENT-085; new orders ENT-086 at 10:05 CET.
Every clock time here is CET; the logs keep UTC.

The fleet as one purse (`hive.py stats kpi`, 09:58 CET): 28,093,772 cr in all, 18,875,437 in
the ships' wallets and 9,218,335 in the faction's treasury, up 2,690,841 cr from 25,402,931 at
04:12 CET. In plain words: the money grew, but mostly from one-time mission rewards.
The steady side (what the ships earn by repeating work, minus fuel and repairs) read +52,533 cr
in the last hour, -6,810 an hour over 6 hours and -62,329 an hour over 24 hours. The one-time
rewards (missions that pay once per pilot) brought 591,332 cr an hour over 6 hours. Ships at
work (`fill.py check all`, 10:03 CET): 463 of 500 at work, 12 starting, 17 waiting, 8 held by
hand. Faction seats 250 of 250 (`empire.json`, 09:03 CET).

Per division, 24 hours (`hive.py stats contribution`, 09:05 CET; purse = steady + paid once,
steady = repeating work alone):

- Command (flagships): purse +15,322 cr/h, steady +1,779.
- Mining (Zero): purse +92,994, steady -44,900; 160 ore a miner-hour.
- Logistics (Apollo): purse +184,403, steady -32,008; supply chains at keep 66% of hours.
- Trade (Mercury): purse +167,827, steady +53,796; sell runs 21,421 cr a ship-hour.
- Military (Apophis): purse +78,377, steady -17,028; 11,228 kills in 4,552 hunts, 3 ships lost.
- Intel (Oracle): purse +60,960, steady -24,639; 97% of worked places read within 3 hours.

## Strategy

Suggi's standing goals stand unchanged at the head of the orders: G1 to G5 (the strongest
faction, the grand fleet, 5 stations and 8 outposts, economic supremacy, the whole galaxy
explored) and O1 to O10 (never idle, batch hull upgrades, one purse, the footprint, strict
classes, defence and the comms firewall, KPI closure, neutral diplomacy). The plan's first
line stays the same: the fleet must pay for itself from repeating work. The 6-hour steady net
moved from -51,265 to -6,810 cr an hour inside this turn, so the turn is close; the 24-hour
figure still carries the worse night.

Decided this turn (all mine, inside the rules):

- A route can now wait for a posted job: `requires.posted` opens a trip only while the
  station's job board, read within the hour, still shows that job. Other pilots take
  Station Needs within the hour; two of our trips found them gone.
- A route can name a faction rank: `requires.role` sends it only to pilots holding that rank.
  Apollo asked to give ten more haulers the right to take from the treasury. I chose the
  narrower way: the route goes to haulers who are already officers (the treasury robot made
  five of them officers, a sixth is queued). No pilot gains a power it lacked.
- Haulers may buy steel plate for the reserve when it only goes into storage (an exception to
  strict classes, bounded at 20 cr a plate and stopped when the need is met).
- The flagships may take Military's claimed hunting grounds last in their lists, one ship a
  herd, when every own herd is spent; Military was told and can ask them back.
- 200,000 cr from the treasury to the builder for a Faction Lockbox at Central Nexus, the step
  before the third recruitment office (more seats, goal G2).

Trinity's change of 09:52 CET is the turn's largest decision, taken by Trinity: miners at most
3 to a belt, one trade desk a station, and two new engines that find hauling and trading work
by themselves. I took it as live (queue ENT-298).

## Divisions

Mining (Zero, reports.log ENT-173). Veterans moved off iron (46 to 28 ships), the empty jump
loop cut from 25 to 7 ships, an ice gather with no jump at Node Gamma. A give route flew before
its receiver stood (errors ENT-175), fixed by Zero the same turn. Suggestions: the laser-only
veterans, option B (a far carbon and silicon wing, one ship first) -- accepted, in orders
ENT-086; a warning for a gift with no receiver at its station -- accepted, open (my build list,
DECISIONS Q75 (19)); fill.py lifts refused by the index -- accepted and fixed (8a4bf667).
Thread check: Zero's last two turns both fought iron and the fill gate; the iron order landed.

Logistics (Apollo, ENT-174). Waiting haulers 92 to 1 by 07:51 CET with half-done missions
finished (110,777 cr paid once). The Lockbox was refused for its fee (errors ENT-177), now
funded. Requests ENT-494, 496, 499 answered. Suggestions: a check for missions held half done
-- open, the ship files hold only a count of missions; a one-ship board test before the route
maker fills a route -- open; routes.py check by division -- accepted, open (Q75 (20)). Thread
check: the hauler gate failed at the end of its last two turns; since Trinity's haul engine
went live at 09:52 CET it passes (10:03 CET).

Military (Apophis, ENT-175). Second Recursion hull flying, third supplied, two more funded; no
ship lost in the period. The wallet scar (errors ENT-176) is fixed by Trinity's install of
Apophis's own code. Suggestions: end a fund when its buy is booked -- accepted, open (Q75
(21)); write a candidate's route file before the filler offers it -- open, Trinity's filler
change; materials-line hulls -- for Apollo. Thread check: steady net worse (-21.1k to -25.3k
an hour by Apophis's figure), hulls rising.

Trade (Mercury, ENT-176). Stored ember glands sold at Hex Star for 171,794 cr; four desks
filled nothing since 02:19 CET; five tier-2 hulls funded. Suggestion: the board gate --
accepted and built (9d033c57). At 10:03 CET 14 traders waited: the desks were cut to one ship
a station and the new trade engine rests pilots after three empty runs; named in Mercury's
orders.

Intel (Oracle, ENT-172). Loaded explorers stored at Altais, freshness 62.1% to 65.2%, no kit
herd at 3 or more. Suggestions: a store stop at the nearest station with storage -- accepted,
open (Q75 (18)); judge scout hulls by fuel per read -- passed to Trinity, who owns the
scorecard. Thread check: freshness rises each turn; the gap targets still fail.

## Plans

- Command: the flagships hunt their own herds, then Military's open ones; the foil scale job
  (50 units, 2,500 cr) stands unanswered on the Notice Board since 04:32 CET and is read at
  each turn until it expires (72 hours); graphene thread follows its answer.
- Builds, in this order (DECISIONS Q75): (18) a store stop at the nearest station with
  storage; (19) the gift-without-receiver warning; (20) routes.py check by division; (21) a
  fund that ends when its buy is booked. Still unbuilt from earlier: (1) the rulebook lean
  pass, (3) a check that names a member's files left uncommitted in the clone, (5) to (10)
  and (13) to (17). None was started this turn.
- Seats: the Lockbox, the Hiring Board (75,000 cr) and the Desk (300,000 cr) at Central Nexus
  by Logistics, the member limit read before and after.
- My next turn (15:00 CET): read the first runs of the two new gates, the steel buy, the
  outpost steel route, the haul and trade engines, and the hold time of the 3-a-belt cap.

## Advice and Suggestions

For Suggi, in plain words: the fleet's money grew 2.7 million credits in six hours, but most
of it came from one-time missions, which run out. The repeating work came close to paying for
itself over the last six hours (-6,810 cr an hour) and paid in the last hour (+52,533). The
fleet is full: 250 of 250 faction seats; the next office is funded. Nothing here needs your
decision. One thing to know: Trinity changed how many ships may share a mining belt (3) and a
trade desk (1) this morning; I watch whether ships wait because of it (14 traders did at
10:03 CET) and the Admirals adjust in their turns. No war, alliance or new pilot is proposed.

## Learnings

- Lesson: a throttle placed in front of a gate that compares with fresh content can only
  refuse. `fill.commit` held back the route index for 15 minutes after any index write, then
  ran the route gate, which compares that index with what it should be; every lift changed it,
  so every lift was refused. Record: the reports of Zero and Mercury (Feedback), test
  IndexDebounceTests red on 9d033c5. Change: a throttle goes where it saves work, never between
  a change and the check of that change. Kept in: LEARNINGS.md (unpromoted, 2026-11-24).
- Lesson: a request for a wider power is first answered by routing the work to those who hold
  it. Record: requests ENT-494 and ENT-500, empire.json members (five haulers already
  officers). Kept in: this report and the answer.
- Fleet takeaway: another hand's work left open in the shared clone holds every install and
  every push (pull log 09:46 CET); members build in a copy (`fleet-build.sh tree`).
- Skill: no change (fleet-build and session-end worked as written).

## Cross-links

- `reports/2026-11-24_oracle_explorers-holds-stored-at-altais-worked-systems-moved.md` -- Intel.
- `reports/2026-11-24_zero_veterans-off-iron-node-gamma-ice-silicon-jettison.md` -- Mining.
- `reports/2026-11-24_apollo_finish-routes-sol-loop-third-desk.md` -- Logistics.
- `reports/2026-11-24_apophis_second-recursion-flies-third-supplied-wallet-refill-scar.md` -- Military.
- `reports/2026-11-24_mercury_ember-glands-to-hex-star-apophenia-batch-queued.md` -- Trade.
- `communications/orders.log` ENT-086; `communications/requests.log` ENT-500 to ENT-504;
  `communications/queue.log` ENT-298; `communications/admirals.log` ENT-119.
- `governance/strategy.md`; `governance/rulebook.md` (F8, F11, F12, F23, F36).
