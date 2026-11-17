---
name: iron-met-make-before-gather-acrab-chosen
id: 20261117T220509Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, reserve, orders, dispatcher, store, sites, faction]
links:
  - reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md
  - reports/2026-11-17_zero_deep-core-eleven-paid-liminal-building-three-tests.md
  - reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md
  - reports/2026-11-17_mercury_node-beta-chain-reopened-null-matter-wiring-crafting.md
  - reports/2026-11-17_apollo_desk-built-outpost-bunker-filled-from-cells.md
  - reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md
---

# The Collective -- The Iron Is Met, Ships Make Before They Gather, Acrab Is the North Outpost

## Situation

Period: from my report `reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md` (turn of 17:30
UTC) to the end of my scheduled turn of 21:30 to about 22:20 UTC on 2026-11-17. Times here are UTC; Suggi's are
CET, one hour later. All five Admirals reported in their turns of 19:00 to 21:15 UTC, and every job's last run
reads `ok` (`hermes cron list`, read 21:53 UTC).

Where the fleet stands, in plain words. Every ship has work: the fill gate (the check that no ship sits idle) read
PASS for all seven roles at 22:01 UTC, 231 ships at work, 3 starting, 0 waiting and 12 held by my own script that
gives out faction seats. The ships' wallets hold 10,691,802 cr and the faction's shared purse, the treasury,
147,817 cr (`hive.py fleet`, 21:55 UTC). The steady money, which repeats and leaves out the rewards the game pays
once per pilot, is still below zero: -3,132 cr an hour over 6 hours and -8,084 over 24 hours; the last hour read
-31,864. Rewards paid once brought 164,722 cr an hour over 6 hours, so the net of everything (steady plus paid
once) is about +161,600 cr an hour over 6 hours: the wallets grow on one-time money while the work that repeats
still costs more fuel than it brings.

| Division (Admiral) | Ships | At work 21:55 | Steady net, last hour | Steady income per hour, runs of 4 h | Paid once per hour, 4 h |
|---|---|---|---|---|---|
| Command (Unity) | 6 | 6 | -964 | +2,484 | 4,125 |
| Mining (Zero) | 60 | 60 | -7,672 | -285 | 53,309 |
| Logistics (Apollo) | 40 | 39 | -9,903 | -5,881 | 17,952 |
| Trade (Mercury) | 40 | 39 | -7,079 | -2,827 | 48,803 |
| Military (Apophis) | 70 | 69 | +9,196 | +15,663 | 51,987 |
| Intel (Oracle) | 30 | 29 | -15,443 | -11,006 | 10,088 |
| Fleet | 246 | 242 | -31,864 | -1,852 | 186,264 |

Sources: `hive.py fleet` (wallets per division, the last hour) and `hive.py tasks` (the runs of 4 hours). The last
hour moved 43,698 cr of gifts and 53,340 cr of deposits into the treasury between our own purses; both are left
out of every figure above.

The routes that earned most per hour flown in the last 4 hours (`route_earnings`, 21:40 UTC):

| Route | Credits per ship-hour flown | Runs | Ships on it now / its limit |
|---|---|---|---|
| carry-null-matter-beta-to-nexus | 30,972 | 7 | 0 of 1 |
| carry-null-matter-synchrony-nexus | 20,047 | 8 | 0 of 1 |
| sell-hydrogen-at-node-beta | 19,726 | 5 | 0 of 1 |
| sell-soma-at-synchrony | 9,937 | 10 | 0 of 1 |
| sell-soma-at-node-beta | 7,910 | 13 | 0 of 2 |
| craft-wiring-synchrony-hub | 456 | 65 | 8 of 8 |
| gather-garnet-belt | -80 | 108 | 13 of 29 |
| gather-ironhollow-echo-ejecta | -214 | 138 | 18 of 35 |
| gather-okab-belt | -395 | 166 | 5 of 42 |

The scale `hive.py tasks` prints, the best repeating route with two runs or more, is a hunt at 5,559 cr per
ship-hour. The first five routes sell goods we hold in storage: they pay well and they end when the stores are
sold. The three gather routes are standing work that costs fuel.

## Strategy

What Suggi decided stands as it was: his four standing orders and goals G1 to G4 head orders ENT-047 unchanged;
the fleet is in phase 1 of `governance/strategy.md` (income), and its bottleneck is still the same one: work that
repeats and pays, for 246 ships.

What I decided this turn, as the player he left these choices to, and why:

1. **Make before gather.** Our reserve (the stock of goods kept back for bases and upgrades, rule F24) is met
   in iron: 349,546 iron ore held against 334,550 it takes, and copper ore 462,391 against 13,608 (`surplus.py
   reserve`, 21:53 UTC). Until now every ship without paying work gathered ore, mostly iron and copper, at about
   -200 to -400 cr an hour of fuel each. That work now feeds nothing. From orders ENT-047 such a ship first makes
   things from what is stored (iron into steel plate, of which the reserve still lacks 33,455; copper into piping
   and wiring), then gathers only what the reserve lacks (silicon, carbon, gold and nickel ore), and docks last. A
   docked ship costs nothing; the fill gate will name it, and its Admiral says why in the report.
2. **Acrab is the north outpost.** Intel read a chain north of us: Acrab, then GSC-0006, then Oxbow, each 3 or 4
   jumps apart, each with fields of about 200,000 iron and copper, with no pirate on our record within two jumps.
   Acrab lies 4 systems beyond our border, 6 jumps from home (`map.py where`), which is rule F33's distance.
   GSC-0006, two jumps from Aldebaran in the region Suggi named, is the candidate for a station later. Logistics
   builds Acrab once our first outpost, GSC-0044, is kept running by routes rather than by hand.
3. **No fuel depot at Node Beta now.** Logistics proposed a Faction Fuel Bunker there (800,000 cr, about 24,100 cr
   a day of rent) filled from fuel cells sold at 100 cr. Those cells are a stock, not a flow: Central Nexus held
   20,863 on 2026-11-15 and 1,856 tonight, about 16 hours of the fleet's fuel in all with The Experiment's. A rent
   that runs every day on a stock that may be gone in one is not a saving. It comes back when a restock is read.

What I recommend and did not decide: nothing new needs Suggi's word this turn (Advice and Suggestions).

## Divisions

Each Admiral's last reports read as one thread, and every suggestion is answered below.

**Mining (Zero),** `reports/2026-11-17_zero_deep-core-eleven-paid-liminal-building-three-tests.md`. Planned at
15:00 UTC: Deep Core Prospecting for as many miners as Markab's platinum carries, the Liminal hull, the fields
around the outpost. Done: 11 pilots paid 5,000 cr each, the Liminal built (the shipyard's message to its pilot,
20:01 UTC), the outpost's fields waiting for seats. The thread holds, and the money agrees with the fleet's data
(-7,672 cr steady in the last hour). Answers: selling surplus copper ore, accepted, it is Trade's to sell where a
bid stands; the stop file that did not free a miner, accepted, open build Q73 (2) (the run host takes away the
stop file of a run it does not fly); a commission's state in the ship files, open, Q73 (13); the seats of requests
ENT-245, given in part (Plans). The five Deep Core pilots whose field ran short are open to the mission again:
the dispatcher counts such a run as no try now (commit 9582453).

**Intel (Oracle),** `reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md`. Planned: the north
and south lists and the hourly outpost watch. Done: the lists and the site chain; the watch is still not hourly
(gaps of 43 to 72 minutes, now 4 ships every 35 minutes). Answers: the north chain, accepted (Acrab chosen); a plan
check for a heading carried twice, open, Q73 (8); one pass of the filler's kept-goods gate over every plan, open,
Q73 (12); the Violethall hunt, done (out of the command plan; a heavy pirate pack now closes its system 24 hours).
Its request ENT-246 (the store's figures) is done: the cause was mine (errors.log ENT-102).

**Trade (Mercury),** `reports/2026-11-17_mercury_node-beta-chain-reopened-null-matter-wiring-crafting.md`. Its goal
had two parts: 30 more pilots paid The Collective Provides (met: 35) and its steady money above -4,075 cr an hour
(missed: -8,178). Its report says both plainly; the thread holds. A once route stood still 20 hours on a pilot cap
sized for 146 ships: found and fixed by Mercury itself. Answers: the fallback once iron is full, accepted, it is
the order of this turn (requests ENT-256); caps that grow with the fleet, open, Q73 (3); null matter for the
Apophenia, declined for now: that hull also takes processed null matter, void nanites and a neural gel made only in
facilities we do not own, and raw null matter is our best-paying sale tonight (30,972 cr per ship-hour), so Trade
keeps selling it.

**Logistics (Apollo),** `reports/2026-11-17_apollo_desk-built-outpost-bunker-filled-from-cells.md`. Planned: the
Recruitment Desk and the first use of the outpost. Done: the Desk stands (treasury 363,931 -> 63,931 cr, cap 50 ->
100) and 1,292 fuel went into the outpost's bunker. Two errors of its own, both written down and fixed. Answers:
the bunker at Node Beta, declined (Strategy); the burning of carried cells in the runner, accepted as Apollo's own
build through `fleet-build.sh`, one ship first; the recount, done. Its note that its haulers fill places on
Trade's claimed gather fields through the Then list is settled between the two in `admirals.log`; with iron met
those fields lose most of their purpose anyway.

**Military (Apophis),** `reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md`. Planned:
one group of three drones on a pilot whale, the escort's first flight. Done: the group flew (no kill: the members
joined but did not fire without their own target), the escort flew at the first try. The thread holds; Military is
the one division with steady money above zero (+9,196 cr in the last hour). Answers: the dispatcher's `group: N`,
accepted, after its second flight, Q73 (1); the filler's guard check, open, Q73 (11); a claim check of plan rows,
open, Q73 (8); the pirate gate, built (24 hours for a pack of 1,000 hull and shield or more).

Where two reports meet: Zero, Oracle and Apollo each found the gather figures bent by the sweep's gifts, and
Mercury and Apollo each asked what ships do once iron is full. Both are answered this turn.

## Plans

What each division does until its next turn (orders ENT-047), and why.

- **Every division:** a ship without paying work makes before it gathers: smelts its stored iron into steel plate,
  turns its stored copper into piping or wiring, gathers only silicon, carbon, gold or nickel ore where a field
  holds them, docks last. Why: the reserve's iron is met and gathering more costs fuel for nothing.
- **Mining (Zero):** the miners seated in the faction take the belts around GSC-0044 with mine routes that store
  into faction storage (`"deposit": "faction"`, one ship first: the step is built and tested, not flown); the
  Liminal's pilot switches in and its gather runs are read against the old hull; Deep Core opens again to the five
  pilots its field cut short while a field holds platinum.
- **Logistics (Apollo):** keeps the outpost's bunker filled by a route, not by hand; plans Acrab's kit and road;
  reads the fuel cell stocks at Central Nexus and The Experiment each turn; makes plate and piping from stores.
- **Trade (Mercury):** sells what we hold beyond the reserve (null matter, soma, hydrogen, copper ore where a bid
  stands) and makes from its own stores before it gathers.
- **Military (Apophis):** a second group flight with each member's own target; hunts one hunter a herd; no guard
  in the first ring. No drone holds level 1 of Voidborn Mastery yet: its report names what stands still.
- **Intel (Oracle):** keeps Acrab, GSC-0006 and their neighbours read; names the east and south candidates.
- **Mine (Unity):** the open builds of Q73 at my next turn; the faction's seats finished (the script running from
  my chat seats miners, then ten each of traders, scouts and drones; 69 members of 100 at 21:52 UTC, the ten
  miners whose invites fell into the engine's restart of 21:22 UTC follow); the treasury filled by the five-minute
  sweep.

What would change this plan: a bid that returns for ice or ore (then ships sell before they make), a reserve item
that falls short again (then it is gathered), a restock of the fuel cells (then the bunker comes back).

## Advice and Suggestions

For Suggi, informing, asking nothing:

- **The money in one line.** The wallets grow by about 160,000 cr an hour on rewards the game pays once per pilot,
  and those end when every pilot has done its missions. The work that repeats still loses a few thousand cr an
  hour. Tonight's change (make before gather) stops the largest part of that loss, about 11,000 cr an hour of fuel
  on gather routes that fed nothing, by Trade's estimate. I will read the steady line at my next turn and say
  whether it moved.
- **What is his alone:** nothing new this turn. No new pilot, no word to another player, no war. The pirate packs
  we avoid are game characters, not players; Military judges them by rule F9.
- **What to look at on the station:** the faction's member count, which should climb toward 100 tonight as seats
  are given.
- **An improvement I propose to myself and will build:** the fallback of every division should read the reserve
  by itself, so that a met item leaves the gather routes without an order (Q73 (5)).

## Learnings

What this period taught me about leading the fleet, from the learning capture:

- **A fix in a file is not a fix in a process.** The fix of a misleading figure reached its file at 17:58 UTC, and
  I asked the store service to count again one minute later, but the store still ran its old code and counted
  nothing new. Three Admirals planned on a wrong figure (-3,438 cr per ship-hour for a route that loses -214) for
  two hours. Record: requests ENT-246 and ENT-253, errors.log ENT-102, the store's log. What I do now: after any
  install that changes code a service uses, the service is restarted and its start time read before it is asked
  anything; the store now notices its own code changed and counts again by itself (commit 9582453). Kept in
  `knowledge/faults-that-leave-no-record.md`; the skill collective-docs names the step. For the Admirals: a
  figure that looks absurd is asked about at once, as Intel did.
- **Work that fills a store ends when the store is full, and the plan does not see it.** Mining warned at 19:18 UTC
  that iron would be met within five hours; by my turn it was, while 412 gather runs in 4 hours still brought
  iron and copper. Record: `surplus.py reserve` and `route_earnings`, 21:53 UTC; admirals.log ENT-049. What I do
  now: every fallback that serves a target carries its end beside it, read each turn against the reserve's gauge.
  Kept in `knowledge/fleet-employment.md`; the automatic version is open build Q73 (5). For Suggi: this is why a
  fleet with every ship busy can still lose money each hour.
- Open questions: why three Deep Core hand-ins were not paid (Zero, cause not found); whether the 100 cr fuel cells
  restock.

Skill: collective-docs changed -- a service restarted and its start read after an install that changes its code

## Cross-links

- `reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md` -- my previous report
- `reports/2026-11-17_zero_deep-core-eleven-paid-liminal-building-three-tests.md` -- Mining
- `reports/2026-11-17_oracle_north-south-lists-site-chain-reserve-check.md` -- Intel
- `reports/2026-11-17_mercury_node-beta-chain-reopened-null-matter-wiring-crafting.md` -- Trade
- `reports/2026-11-17_apollo_desk-built-outpost-bunker-filled-from-cells.md` -- Logistics
- `reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md` -- Military
- `communications/orders.log` ENT-047 -- the orders of this turn
- `communications/requests.log` ENT-253 to ENT-257 -- my answers
- `communications/queue.log` ENT-184 -- what changed for every division
- `communications/errors.log` ENT-102 -- the store's recount on old code
- `governance/strategy.md` -- phase 1, income
