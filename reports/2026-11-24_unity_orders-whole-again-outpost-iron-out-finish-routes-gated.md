---
name: orders-whole-again-outpost-iron-out-finish-routes-gated
id: 20261124T150318Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, orders, supply, gates]
links:
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
  - communications/orders.log
  - communications/requests.log
---

# The Collective -- Orders Whole Again, Locked Outpost Iron Counted Out, Finish Routes Opened Only to Their Holders

## Situation

Period: from my report of 09:09 UTC (10:09 CET) to 15:03 UTC (16:03 CET), 2026-11-24. Orders in force: `orders.log` ENT-090 (written this turn; ENT-089 restored the orders whole at 14:31 UTC).

The fleet as one purse (`hive.py fleet`, 15:03 UTC): 28,946,996 cr in all, 18,834,592 in the pilots' wallets and 10,112,404 in the faction treasury. At my last report (`hive.py stats kpi`, 08:58 UTC) it was 28,093,772, so the purse grew by about 853,000 cr in six hours, nearly all of it rewards paid once.

Steady money (repeating work minus fuel and repairs; one-time rewards left out), same reading: +19,945 cr an hour over the last hour, -468,390 over 6 hours, -191,764 over 24 hours. Paid once in the last hour: 781,399 cr. The 6-hour figure is bent by two things that are not burnt money: at 09:00 and 10:00 UTC the costs read 1,906,917 and 1,344,564 cr against fuel of 247,620 and 436,348 (`stats_money_hour`, Fleet rows), which is mostly buy orders posted on station markets (money parked in an order, about 1.51 million cr at 10:37 UTC by Trade's count, mostly back since); at 11:00 UTC hull purchases were booked as fuel and repairs (Mining 889,340 cr of costs, Military 296,686 cr of repairs; Trinity's fix 6f78a871 stops it from 12:26 UTC on, the old hour stays in the window until it ages out).

Ships (`fill.py check all`, 15:04 UTC): 500; 461 at work, 25 held by hand or by a service, 14 waiting (4 miners during Mining's extra turn, 1 hauler, 9 scouts docked on watch, which rule F8 counts as working). The fill gate reads HALT for miners and haulers; both are their Admirals' plans, named below.

Per division (`hive.py stats contribution`, 13:57 UTC; purse = steady plus one-time per hour, 24 h; recurring = matched steady cash per hour, 24 h):
- Command: purse +2,070 an hour, recurring -12,627.
- Mining: purse +90,198, recurring -73,598; 174 units of ore per ship-hour.
- Trade: purse +119,280, recurring +25,539; selling earns 19,335 cr a ship-hour.
- Logistics: purse +141,159, recurring -23,997; 3 of 4 supply chains at keep.
- Military: purse +77,671, recurring -33,417; 11,597 kills in 24 h, 1 ship lost.
- Intel: purse +66,223, recurring -20,229; 96% of the places our routes use read within 3 hours.

## Strategy

Suggi's standing goals G1 to G5 and his operating rules O1 to O10 stand word for word as ENT-087 carried them (his update of 11:52 UTC through Trinity: manufacturing, trade and extraction are mandatory engines; hulls of any empire may be flown by job).

Decided this turn, and why, in plain words:
- The orders are one complete page again. Trinity's ENT-088 at 13:32 UTC carried only what changed (two smart networks and regional hubs), and every member's start-of-turn summary then showed the goals, the plan and all six task blocks as gone. ENT-089 puts them back whole with Trinity's additions inside; ENT-090 adds one line for the haulers. From now on the logging tool itself refuses an orders entry that lacks the goals, the plan or any member's block (commit f41916e0), so this cannot happen again by accident.
- Iron stored at our outpost no longer counts as iron we have. The game does not let any pilot take goods out of the outpost's shared storage, so its 100,000 iron was a number on paper. Counting it kept the iron-gathering routes shut because the fleet looked full. Now the usable iron reads 49,691 against a floor of 60,000 (`pull.py levels`, 14:29 UTC), so miners gather iron again.
- A route that finishes a half-done mission now only opens to a pilot that actually holds that mission. In the six hours before, such routes were flown 494 times and 397 of those runs earned nothing (-147,389 cr, Military's count in requests ENT-514); at 14:16 UTC three of my own flagships were among them, and I stopped four such flagship runs by hand this turn (`stop_pilot.py`).

Proposals, not decided: stations as one core at home plus a hub in each of the four other empires stand in Trinity's `governance/strategy.md` and in the PLAN as written by him; where exactly is still my call with Intel's readings.

## Divisions

Every Admiral turn since my last report was read (`reports.log` ENT-178 to ENT-187: two turns each). Judgments of their suggestions follow, one line each.

Intel (Oracle). Kit herds read and passed to Military, scout lasers handed to Mining, eleven leaders hailed. Suggestions: a warning when one stop both unfits and gives the same item -- accepted, open (I chose the runner's order fix instead, in my build list); `judged()` treating an unfit like a fit -- done by Trinity (11f1b38e); NOIR's contact and status -- done: Friday added as NOIR's envoy at 14:16 UTC and the hail text given (requests ENT-521); scouts' hull alarm judged by fuel per reading -- open, with Trinity (scorecard); board RUNS lines without treasury sweeps -- open, mine; Military gating kit hunts on fresh reads -- Military's call, not mine.

Mining (Zero). Put field floors on 27 mine routes after 44 miners flew nearly empty belts (errors ENT-179), gated the outpost's faction gathers (ENT-185). Suggestions: the route maker writes a floor and the route check warns without one -- Trinity set a 15% default floor in the strategy (f9e5d28e), whether the route maker writes it is not verified; the warning is open, mine; booking hull purchases as one-time -- done by Trinity (6f78a871); a warning for a faction gather without a reserve gate -- open, mine; a docked exception for miners whose only work brings goods above max -- put to Suggi below.

Logistics (Apollo). Found the outpost iron locked by a one-unit test, bought carbon at home at 4 cr a unit (710 units in 10 runs), built the Central Nexus desk row (seats 250 to 275). Suggestions: haul engine claims by sell bid on fresh books -- done by Trinity (3bbb0fbb); a one-ship gate for a new kind of route -- accepted as orders P7, a code gate open; a hand-over that never gives from one receiver to another -- accepted, open, mine; stored buys of the haul engine counted as stock -- open, Trinity.

Military (Apophis). Bought listed hulls far under commission prices (a Recursion for 224,430 cr against about 310,000 commissioned), took the finish routes out of his list and asked for the mission gate. Suggestions: read the market's listed ships before any commission -- done by Trinity (82ca53d3); listed hull buys shown as repairs -- done by Trinity (6f78a871); buy ammunition with an armed hull -- open, Trinity's upgrade script.

Trade (Mercury). Stopped a buy lane that had parked 1,510,265 cr in unfilled orders (errors ENT-183) and unwound it to 407,385 cr by 13:06 UTC; bought listed hulls. Suggestions: a fleet-wide cap before any buy lane returns -- done by Trinity (3bbb0fbb); a lock on the hull queue file -- done by Trinity (bbe943d0); a fund paid out where the pilot is, not only at a Lockbox -- accepted, open, mine (the health check of 13:21 and 13:37 UTC reported the wallet service's `no_storage` refusal of two funds).

Thread audit against my last report: of what I said I would read, the officer gate (`requires.role`) worked within a minute but met a game limit at the outpost (ENT-513); the board-posting gate went onto four Trade routes; the new hauling engine lost 239,167 cr in its first hour on stale price data and its trading lane was removed; the 3-ships-per-belt cap is in force with floors added. Figures in the Admirals' entries match the store where I checked them (requests ENT-513's 100,000 iron: `holdings`, pilot Faction, 14:07 UTC). Two Admirals' own corrections stand in the logs (errors ENT-180, queue ENT-305), and one of mine (queue ENT-306: the envoy time).

## Plans

Next fleet steps, as the orders say (ENT-090): pay for itself (steady 24-hour net above zero), lean supply with the outpost's iron out of the count, the Atria outpost kit then Yildun, seats and the next office on a rent-free base, strict classes, newborns home first, and every smart network read by its owner each turn with one ship and three runs before a new lane grows.

Builds named and not yet done (each stays visible until built): the runner takes a module off before it gives it away (errors ENT-178); a hand-over never gives from one receiver to another (ENT-188); the route check warns on a mine route without a floor and on a faction gather without a reserve gate (ENT-179, ENT-185); a store stop at the nearest station with storage (Oracle); a gift-served fund for far pilots (Mercury); board RUNS lines without treasury sweeps (Oracle); buy escrow booked as a move, not a cost (put to Trinity in queue ENT-306); the older list in `DECISIONS.md` Q75 (13) to (21) apart from what was built. The cap of the new five-capitals finish route stays 2 for its three holders until the route folder is clean of other members' work in flight (my lift was refused while it was not); the third holder takes it when one of the two is done.

Upcoming turns (CET): Zero 18:30, Apollo 19:00, Mercury 20:00, the other Admirals by their schedules, mine 21:00. Six haulers waited at 14:56 UTC with the haul engine at its cap; ENT-090 names it for Apollo.

Empire skill levels by role (rule F35, `hive.py briefing`): Mastery 1 or more on 225 of 500 pilots, all Voidborn (225 of 246); none yet among Solarian (71), Nebula (99), Crimson (41) or Outer Rim (43) pilots.

## Advice and Suggestions

For Suggi, plainly: the fleet is richer by about 853,000 cr since this morning, but mostly from one-time mission rewards; the repeating work still costs more than it earns over a day (-191,764 cr an hour). Three leaks found this turn are now shut by code rather than by memory: empty mission-finishing trips, iron that could not be used being counted as stock, and an orders page that was not whole.

One question is his, raised by Mining (reports.log ENT-184): should a miner whose only work would bring goods the fleet already has too much of be allowed to stay docked instead of working? That changes rule F8 (never idle), which is Suggi's. My recommendation: not now. This turn's iron fix reopened the iron routes, and the new mining network spreads ships over more belts; I would measure a day first. Default fleet action if he says nothing: miners keep working under F8.

Nothing else needs his decision. No new pilot, no new Admiral, no war or alliance is proposed. NOIR's leader asked for a gift in person in return for "market wisdom"; we decline gifts to outsiders (rule F39) and answer only through the contact he named.

## Learnings

1. A gate that checks only size passes an incomplete record. Record: `orders.log` ENT-088 passed `comms.py check`, and every briefing read the orders as gone for about an hour. Change: an orders append now refuses an entry without the goals, PLAN and all six blocks (f41916e0, test red first). Kept in `knowledge/faults-that-leave-no-record.md`. Fleet takeaway: when a rule says "complete", the gate checks for the parts, not the length.
2. A stock figure counts only what can be taken out. Record: requests ENT-513; `pull.py levels` 14:29 UTC. Change: goods at our outposts leave the reserve's held, the pull levels, the surplus and the fleet supply chains (2b596fcb). Kept in `knowledge/money-figures.md`. Fleet takeaway: before a store counts toward a reserve, one unit is taken out of it.
3. The whole test suite now takes 809 seconds; two timing tests failed under that load and passed alone. Change: the skill says to start the suite in the background and rerun a failed timing test alone before calling it a fault.

Skill: collective-docs changed -- a pitfall on the slow suite and timed tests under load.

## Cross-links

- `reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md` -- my previous report.
- `reports/2026-11-24_oracle_five-kit-herds-belts-gate-laser-strip-eleven-hails.md` -- Intel, first turn of the period.
- `reports/2026-11-24_oracle_kit-herds-contested-sarin-read-lasers-flow-qualia-back.md` -- Intel, second turn.
- `reports/2026-11-24_zero_floors-on-every-belt-sarin-carbon-test-three-t2-hulls.md` -- Mining, first turn.
- `reports/2026-11-24_zero_faction-gathers-gated-silicon-waits-on-pirates.md` -- Mining, second turn.
- `reports/2026-11-24_apollo_haul-arbitrage-out-officer-steel-desk-row.md` -- Logistics, first turn.
- `reports/2026-11-24_apollo_outpost-iron-locked-carbon-at-home-nebula-first-links.md` -- Logistics, second turn.
- `reports/2026-11-24_apophis_listed-hulls-cheaper-than-commissions-tier2-fuel-measured.md` -- Military, first turn.
- `reports/2026-11-24_apophis_finish-routes-leak-closed-listed-hulls-need-ammo.md` -- Military, second turn.
- `reports/2026-11-24_mercury_bursar-buy-lane-off-station-needs-gated-listed-apophenia.md` -- Trade, first turn.
- `reports/2026-11-24_mercury_listed-hulls-bought-duplicate-commission-cancelled.md` -- Trade, second turn.
- `governance/strategy.md` -- Suggi's strategy, v2.5 and the regional hubs.
- `communications/orders.log` -- ENT-088, ENT-089, ENT-090.
- `communications/requests.log` -- ENT-513, ENT-514, ENT-516 to ENT-521.
