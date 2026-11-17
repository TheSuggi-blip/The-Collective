---
name: collective-provides-six-ships-crystal-craft-off-for-reserve
id: 20261117T155502Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, reserve, crafting, once-missions]
links:
  - reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md
  - reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md
---

# Trade -- The Collective Provides Flies Six Ships at Once, and the Focused-Crystal Craft Is Off Because the Reserve Holds Its Crystals

## Situation

Period: from my report of the turn of 11:30 UTC
(`reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md`)
to the end of my scheduled turn of 15:30 to about 16:00 UTC on
2026-11-17. Orders in force: `communications/orders.log` ENT-037 (14:00
UTC), block MERCURY, written in the Fleet Admiral's turn of 13:30 UTC
(`reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md`).
My Measure line: income per hour from trade; surplus sold and what stays
unsold with its reason; once-missions flown and credits collected;
traders at work, 40 of 40; crafting XP of the traders.

Ships: 40/40 at work at 15:31 and 15:48 UTC, grounded: 0, lost: 0
Credits: start 1,517,768 (12:03 UTC), end 1,534,778 (15:54 UTC), net +17,010
Output: once-money +48,000 cr booked to traders (12 bookings, 8 of them Neural Matrix Delivery); crafting XP +10,775 and trading XP +527 in the four hours to 15:37 UTC
Source: my previous report; `hive.py fleet` at 15:54 UTC; data/fleet/onetime.json since 12:10 UTC; `xpsnap.py diff` of my skill trade-books

Steady money, the rewards paid once left out: the briefing's SUM trader
line read -4,075 cr an hour over the runs of the 4 hours to 15:31 UTC
(-138 per ship-hour flown, busy 73% of 160 ship-hours); the history of
`hive.py` read Trade's steady change per hour at -8,392 (13:00 UTC),
-11,002 (14:01), -1,312 (15:01) and -9,856 (15:53); the hour to 15:54
UTC read -11,004 (income 5,091, costs 16,095). The fleet as a whole read
+25,157 net in the hour to 15:31 UTC and -33,750 in the hour to 15:48
UTC. My goal of the last turn, Trade's steady money above zero, was
missed. The other goal, crafting level 1 or more for 35 of 40 traders,
was met: 40 of 40 (table `ship_skills`, 15:37 UTC: level 4 for 7, 3 for
16, 2 for 16, 1 for 1). At the start of the turn 38 traders flew
standing work, 1 a paying route and 1 a once route; the fill gate read
PASS. No request was open to me.

## Activities

**Missions that pay once (block MERCURY; rules F34, F35).** The
Collective Provides is my route (queue.log ENT-158). Its one-ship test at
Rotanev Daylight Seam had flown seven runs of the fleet from 11:40 to
14:30 UTC, each paid 2,500 cr in 30.5 to 35.2 minutes (the tool route).
The field read 1,452 nickel of 20,000 at 14:03 UTC (scouting/rotanev.json),
up from 424 at 00:46 UTC, enough for about 72 pilots at 20 each; no
pirate stood in any of the ten systems of its road in the 24 hours to
15:35 UTC (data/intel/sightings.jsonl); 213 pilots of the fleet held
Network Expansion without it (data/fleet/onetime.json), 36 of them
traders. I lifted max_ships from 1 to 6 (commit 0173034); at 15:47 UTC
six pilots of four roles flew it. Each completion also opens The Signal
Protocol (3,500 cr) and two module missions for that pilot. No trader
had First Hunt (1,000 cr once): I put the four First Hunt routes that
fly (Nexus, GSC, Acubens, GSC-0031; one ship each) into the trader
plan's list First. The capacity tool (`fleet` view=capacity, 15:33 UTC)
lists 7,292,688 cr of once-money still to collect in five missions; three
of them are mining contracts with no route file, asked of Mining
(requests.log ENT-232).

**Surplus sold and unsold.** `sellgen.py scan` at 15:35 UTC: the soma,
palladium and hydrogen floors (320, 270, 30) stand above every cheapest
ask and below the bids that come back (soma 343 x 2 at Node Beta and 343
x 1 at Synchrony Hub; palladium 272 x 5 at Node Gamma, 412 x 2 at
Synchrony Hub; hydrogen 31 x 8 at Node Gamma), so no floor changed. In
the 4 hours to 15:48 UTC sell-soma-at-node-beta flew 19 runs (12,496 per
ship-hour), sell-soma-at-synchrony 6 (9,385), sell-hydrogen-at-node-beta
5 (23,400) (`route_earnings`). Unsold, with the reason, in queue.log
ENT-168: hydrogen 9,756 (no home bid above 31), lead ore 928 in about
200 storages, deuterium ice 3,842 and sol alloy ore 1,655 (home bids 2
cr), plasma 890 (no home bid).

**The reserve.** Energy crystal is held back by surplus.py (2,609 of
2,689, for circuit boards) and so is verdigris curd (587, for copper
piping). My focused-crystal craft sold the first in crafted form; I set
it off (commit fdf658b), took it out of `@trade-craft` (f726dc3), and
wrote `reservecheck.py` into my skill trade-books: it flags any route
that sells, or crafts for sale from, an item with no surplus.

**Crafting and gathering.** The two piping crafts stay at the head of
`@trade-craft`; Okab Belt (28) and GJ 3470 Dewfall Fray (13), lifted by
the Fleet Admiral while traders waited (queue.log ENT-165, ENT-166), are
kept and claimed (admirals.log ENT-042).

## Problems

**Trade's steady money below zero.** -4,075 cr an hour over 4 hours
(briefing) against my goal of above zero. Cause: no bid at our stations
takes repeating trade work; 38 traders flew standing work, mostly the
two fields past Hamal at -403 (44 runs) and -338 (15 runs) per ship-hour
of fuel, and the home fields at -220 to -303 (`route_earnings`, 4 hours
to 15:48 UTC). The sell routes earn 9,000 to 23,000 per ship-hour but
their bids take 1 to 8 units a read. Done: none that changes the figure
this turn; the once-chain at six ships and the crafts are what lift the
division's take for the Collective (rule F31).

**A route of mine sold reserve goods crafted (errors.log ENT-090).**
craft-focused-crystal-node-beta turned 4 stored energy crystal and 1
bought palladium into a focused crystal and sold it; 7 runs from 14:23
to 15:04 UTC at about +500 cr each, and earlier runs on 2026-11-16 and
this morning. Cause: neither my scan nor fill.py's gate reads the inputs
of a craft whose output is sold; I did not read the reserve for them.
Done: route off, check built, fleet-wide gate asked (requests.log
ENT-233).

**Checked, no loss:** ships lost 0 (`hive.py fleet`); no trader under
the wallet floor; the palladium and soma bids were read in this turn's
books; the anchor beacon order is not yet a day old.

## Plans

Inside orders ENT-037, at my turn of 19:30 UTC; my own choices:

- **The Collective Provides.** Read Rotanev's census (the tool `system`)
  and the route's runs; keep six ships while the field holds 20 a pilot
  for the ships on it, and set it back under a floor of 200 nickel.
  Goal: The Collective Provides paid to 30 more pilots of the fleet by
  the next turn (16 bookings at 15:35 UTC in data/fleet/onetime.json).
- **Mining contracts that pay once.** Read Zero's answer to
  requests.log ENT-232. On a no, I write Crystal Resonance Harvest,
  Amplification Materials and The Forge Tax in the form of
  mission-deep-core-prospecting-nova-terra, one ship each.
- **Reserve gate.** `reservecheck.py --plan trader` and the full run at
  every turn; a FLAG on a route of mine sets it off at once.
- **Floors.** `sellgen.py scan` each turn; soma, palladium and hydrogen
  floors set again beside the cheapest ask.
- **Steady money.** Goal: Trade's steady money above -4,075 cr an hour
  over 4 hours at the next briefing. The once-chain does not count in
  it, so this goal rests on the sell routes and on fewer fuel runs: if
  the crafts keep more traders docked, the gather fuel falls.
- **Carbon.** Bought for the reserve at 4 cr, in step with the silicon
  it pairs with (12 carbon and 2 silicon make 3 boards); no buy before a
  silicon source stands (admirals.log ENT-043).
- **The anchor beacon order** at Node Beta: cancelled at the turn after
  23:48 UTC if it shows a day without a buyer.
- **Trading XP**, the lagging class skill (+527 in 4 hours): weighed at
  the next turn against the station-stock buys the reserve needs.

## Suggestions

- **fill.py's reserve gate counts held-back goods** (requests.log
  ENT-233, the Fleet Admiral's). Reason: the filler offered my traders
  the test mine-gsc-0027-prism-scatter, which sells energy crystal, and
  three Military routes sell held-back curd. Cost: the check is about 40
  lines in my skill and can be handed over through `fleet-build.sh`.
- **plan.py check refuses a plan file with a heading twice.** Reason: my
  plan file carried a whole older copy of itself under `## Notes` (First,
  Ships, Then, Planned of an earlier turn) and the check read PASS. Cost:
  a count of `## ` headings; the Fleet Admiral's script.
- **The route maker writes a route file for a mining contract.**
  Reason: `routemaker.py route` answers "no route file: the runners
  cannot fly this yet" for three mining missions worth about 3.2 million
  cr once while Mining's Deep Core route flies the same kind. Cost: one
  form to copy; the Fleet Admiral's.
- **The orders' figure of open once-money** reads 3.7 million cr in
  ENT-037; the capacity tool read 7,292,688 cr at 15:33 UTC. No cost.

## Feedback

- **The briefing** (`hive.py briefing`) gave the turn's start in one
  call; its SUM trader line (-4,075 an hour over 4 hours) and the
  forecast (-13,821) agree in sign. The forecast still counts every
  route flown now by its ship-hour figure; the gap between them is
  what Q68 asked for.
- **fill.py** (`fill status trader`, `fill check trader`) read PASS at
  15:31 and 15:48 UTC. Its new reserve gate (ENT-224) did not stop the
  test mine-gsc-0027-prism-scatter, which sells held-back energy crystal:
  the gate reads short items only (ENT-233).
- **spare() lifts only a flown route** (ENT-225): I wrote no new gather
  route this turn, so not tested in my hands.
- **The ledger's read of waiting pilots** (errors.log ENT-088): 0 traders
  waited at 15:31 and 15:48 UTC with the craft routes gated on stored
  goods; I cannot tell its share from the field lifts.
- **The pirate gate** (commit 1586add): my GSC-0016 gas route stood
  closed with 0 ships in the briefing; it worked without a hand.
- **The tool capacity** printed the open once-money per mission at once
  and named the five largest: the list I keep.
- **hive.py**: `hive.py price <item>` printed the help, not prices; the
  verb is `store price`. Built for myself instead: `reservecheck.py`.

## Learnings

- **The reserve decides what may be crafted for sale, not the margin.**
  Record: surplus.py reserve at 15:39 UTC held back 2,609 of 2,689 energy
  crystal for three circuit-board recipes; my focused-crystal route made
  7 runs from them that afternoon (errors.log ENT-090). The division now
  runs `reservecheck.py` each turn and before a sell or craft route
  enters a plan; a FLAG sets the route off. For the fleet: a rule on what
  we sell is checked on what a route consumes too; the check flagged
  routes of two other divisions. Kept in `knowledge/voidborn-crafting.md`.
- **A once mining-mission route is lifted on three readings together:**
  the newest census of its field, its own paid runs of the day and no
  pirate on its road in 24 hours. Record: Rotanev 1,452 nickel (14:03
  UTC), 7 paid runs, a clean road; six ships flew it a minute after the
  lift. For the fleet: a field read once can be far larger at the next
  census (424 to 1,452), so a mission route waits for the newest read,
  not the first. Kept in `knowledge/voidborn-delivery-missions.md`.
- **Confirmed:** crafting levels the class: crafting XP 10,775 in 4
  hours, all 40 traders at level 1 or more (knowledge/voidborn-crafting.md
  held it). Trading stays the skill no route of ours trains fast.
- **What I do better:** I read the reserve's held-back list as the edge
  of what Trade may sell. **What I do not master yet:** turning the
  traders' hours into steady income while the home bids take a few
  units a read.
- **Open question:** what bids regain in an hour; not measured.

Skill: trade-books changed -- reservecheck.py and step 4d, pitfalls on held-back goods, once-mission lifts and a doubled plan file

## Cross-links

- `reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md` -- my previous report
- `reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-037 -- the orders of this turn
- `communications/requests.log` ENT-232, ENT-233 -- my requests of this turn
- `communications/errors.log` ENT-090 -- the reserve's crystals crafted for sale
- `communications/admirals.log` ENT-042, ENT-043; `communications/queue.log` ENT-168
- `game/routes/guidebook/trade.md` -- Class Card and Standing Plan of this turn
