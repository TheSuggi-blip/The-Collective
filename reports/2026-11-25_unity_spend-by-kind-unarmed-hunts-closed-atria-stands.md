---
name: spend-by-kind-unarmed-hunts-closed-atria-stands
id: 20261125T084736Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, purse, spend, outposts]
links:
  - reports/2026-11-25_unity_keeper-gate-purse-fell-on-modules-hall-to-own-outpost.md
  - reports/2026-11-25_oracle_afterburners-off-scouts-census-refuels-on-the-way.md
  - reports/2026-11-25_zero_pirate-gate-joined-booster-spend-stopped-deposits-ours.md
  - reports/2026-11-25_apollo_kit-assembler-built-kit-row-running-hall-seats-read.md
  - reports/2026-11-25_apophis_afterburners-stripped-pack-fuel-guard-flagships-lead-packs.md
  - reports/2026-11-25_mercury_melt-to-hex-star-carries-freighter-desks-hulls-held.md
---

# The Collective -- Module Spending Fell by Four Fifths, Our Second Outpost Stands, Unarmed Ships Hunt No More

## Situation

Period: since my report of 2026-11-25 02:59 UTC (03:59 CET) to this turn, 08:00 to about 09:00 UTC (09:00 to 10:00 CET), under orders ENT-092, now ENT-093.

The fleet as one purse (hive.py stats kpi, computed 08:41 UTC): wallets 13,455,235 cr plus the faction treasury 10,733,460 cr make 24,188,695 cr, which is 804,876 cr less than at my last report. Most of that fall was building: the kit factory at Node Beta cost 600,000 cr and founding the outpost at Atria 100,000 cr, both from the treasury (Apollo's report, build.py and found.py results).

Repeating money (work minus fuel and repairs, one-time money left out), by whole hours from the store: the last six hours -95,887 cr an hour, which is 73% better than the six hours before (-348,984); the last 24 hours -213,443. The last single hour read +286,071. One-time money (mission rewards minus one-time buys) added 67,906 cr an hour over six hours. Ship modules bought in the six hours to 08:15 UTC: 599,780 cr, against 3,414,572 cr in the six hours before my last report (hive.py spend, new this turn).

Ships: 500; at 08:49 UTC 475 at work, 12 starting, 4 waiting and 9 by hand, gate PASS (fill.py check all). Over 24 hours 78% of ship-hours went to each class's own work, 10% to missions paid once (stats time).

One line per division (hive.py fleet, the last hour to 08:41 UTC; 24-hour purse from its division table):
- Mining, 130 ships: last hour -66,710 cr; 24-hour purse -79,316 cr an hour; 243 units of ore a ship-hour (stats contribution).
- Trade, 85 ships: last hour +363,065 cr; 24-hour purse +162,956 cr an hour; stored crystal melt sold at a deep bid at Hex Star.
- Logistics, 95 ships: last hour -8,022 cr; 24-hour purse -59,221 cr an hour; outposts of ours 2 of 8.
- Military, 140 ships: last hour -60,031 cr, of it 57,737 cr fuel and repairs, against 155,015 at my last report; 13,139 kills and 5 ships lost in 24 hours, none lost after 02:00 UTC (stats contribution, Apophis's report).
- Intel, 50 ships: last hour -27,170 cr; 98% of the places our routes use read within 3 hours (stats contribution).
- Command: no ship of its own; the flagships lead Military's hunting packs.

## Strategy

The standing goals are Suggi's and unchanged: G1 to G5 (dominate the galaxy, a fleet of up to 1,000 ships, a sovereign industrial empire of 5 stations and 8 outposts, the top producer and trader, master every empire) and the operational subgoals O1 to O10, first of them never idle (O1).

Decided this turn (orders ENT-093):
- **A module or a hull is bought only when its measured gain pays it back within a week of work** (P1). In plain words: before buying an upgrade, show that it earns its price in about 168 working hours. Trade measured a tier-2 freighter desk at 669 cr an hour against 636 for the old hull: 33 cr an hour more for about 100,000 cr, which would take months to repay. So the scorecard's hull alarm is a signal, not an order to buy.
- **A division's part of a shared program setting belongs to that division's Admiral** (P7). The fitting program reads one settings file with a part per division. Shared changes of yesterday evening put afterburners (speed modules that more than double the fuel of each jump) on scouts and hunters and shield boosters on miners; each Admiral found it in his own turn after the money was spent. The rule is now in the orders; a check in code is not built yet.
- **Roads:** Atria, the north road's first outpost, stands since 06:47 UTC. Felis on the south road is next, built from our own stock once it reads no pirate for 24 hours; then Yildun. Felis was once listed for after Oakridge; Oakridge is a station whose core costs about 13 million cr to buy (rival sedcards, the Arneb ask), which P1 rules out for now, so the three inner outposts come first, as rule F33 lays out the roads.
- **The Guild Hall** (a faction office that raises our seat limit) goes to an outpost of ours, as Suggi said, and by Apollo's reading of the seat rule to GSC-0044: first a Center, then a Hall, for 225 more seats at about 10 million cr in fees. It waits until the 24-hour repeating net reads zero and the treasury keeps 3 million cr after the fees.

A proposal, not an order: when the store keeps the record of one-time money whole, I will move the orders' P1 figure to the 24-hour whole-hours net and stop quoting the money view's 24-hour window, which moves with what its source file still holds.

## Divisions

**Intel (Oracle).** Found why six scouts were towed and 389 scanning trips refused: afterburners fitted by the shared fitting program. Stripped them (45d42408) and let a long trip refuel on the way (53bc129c); refused trips fell from 40 of 93 runs (05:00 to 05:20 UTC) to 10 of 35 (05:20 to 05:36 UTC). Suggestions: no hunt for a ship without a weapon: accepted and built (850aee18, answered ENT-541). Fuel per jump in the fitting program's own choice: passed to Trinity, open. Apophis to read his hunters' fuel: done by Apophis. Thread: the three scouts born in other empires, far from their region's work, are not in his report; they stay in his block.

**Mining (Zero).** Joined the mining network to the dispatcher's one pirate list (it saw 4 of 21 pirate systems; 04cbb69a, test first), stopped the shield-booster buys that cost 477,066 cr (0916d551), and stopped storing iron where no route of ours can take it out (3ef7d3cb). Suggestions: a shared policy change goes in as a variant beside the tested one, named with its owner: accepted, now orders P7; a code check is open (DECISIONS Q75 (34)). Every network runner takes the dispatcher's pirate set: passed to Trinity, open. The network line with credits per ship-hour: accepted, still unbuilt. Thread: ENT-534 answered (ENT-540), as ordered.

**Logistics (Apollo).** Built our own outpost-kit factory at Node Beta, made the first kit in 1.4 minutes, and founded CLTV Outpost Atria at 06:47:59 UTC: 1,425,267 cr spent of the 1,600,000 cr I set. A failed treasury read had held the factory for four hours (errors ENT-207). Suggestions: the Guild Hall ladder at GSC-0044: accepted as the site, gated (P4); every gate that turns a failed read into 0 or -1 stops as `not read`: accepted, Q75 (37), unbuilt. Atria's fuel bunker and a supply-chain row: yes, with me next turn. Thread: P3 landed in full.

**Military (Apophis).** Measured that starter hunters with an afterburner lost -1,529 cr a ship-hour against -746 without, stripped them (390773f1), and made a hunting pack weigh its fuel before it flies (92c66d1f). Tows: 19 of Military's ships between 02:00 and 07:10 UTC, none from 07:10 to 08:34 UTC (messages record). Suggestions: a fit names its measured gain and the briefing shows fit spend per division: accepted; the spend line is built (b28f7b0d) and the payback rule is P1. A shared test reads the division's own loadout: passed to Trinity, open. Thread: his fuel order of ENT-092 landed: the division's fuel and repairs fell from 155,015 to 57,737 cr an hour (last hour).

**Trade (Mercury).** Sent 285 stored crystal melt to a 3,158 cr bid at Hex Star (three sales for 142,598 cr) and moved two big-hold traders from empty training jumps onto a market desk. Suggestions: whether the hull alarm should be closed at about 100,000 cr a hull: declined; no buy without a measured payback within a week (P1). The surplus view naming the deepest bid: passed to Trinity, open. Cross-check: his 24-hour Trade purse (+199,597 cr an hour at 07:16 UTC) and mine (+162,956 at 08:41 UTC) differ by the hour between our reads.

## Plans

- **Next turns (CET):** Oracle 12:00, Zero 12:30, Apollo 13:00, Apophis 13:30, Mercury 14:00, mine 15:00 (each job's schedule).
- **Orders ENT-093** set each block: Zero reads iron stored at market hubs and gives it where a receiver stands; Mercury reads the first results of the melt, sac and phase carries; Apollo keeps Atria fuelled and prepares Felis from our own stock; Apophis reads fuel per hunter-hour after the strip; Oracle drops unarmed hunts from the scout plan and keeps Felis read, since P3 waits on its pirates.
- **Built this turn:** no hunt for an unarmed ship (850aee18) and the spend figure by division and kind (b28f7b0d), both with tests that failed first; one treasury deposit booked from its own proof.
- **My next builds, not built yet:** the store keeps the record of one-time money whole (Q75 (33)); a code check for a division's part of a shared policy file (34); `fleet-build.sh test` running every module named (35); the sweep proving a deposit by its own answer (36); `not read` instead of 0 or -1 in every gate (37); the network line with credits per ship-hour (30); the upgrade service's hand-over file (31); the class guard's strip-route pass (32); items (13) to (26) and (28) of Q75 stay unbuilt.
- **Fill gate:** PASS at 08:49 UTC for all 500 ships (4 scouts docked on watch count as working under rule F8).

## Advice and Suggestions

- **What I decided and why, in plain words:** upgrades must pay for themselves within a week, because the fleet's savings were turning into equipment faster than its work earned; each division now owns its part of the shared fitting settings, because three divisions paid for changes they never asked for; unarmed scouts are no longer sent to hunt, because one was sent alone into lawless space with no gun.
- **Where I advise focus:** the repeating money. In the six hours before 02:00 UTC the fleet lost about 349,000 cr an hour on repeating work; in the last six about 96,000 (whole hours, stats kpi). Fuel was the lever: Military's hourly fuel fell by almost two thirds once afterburners came off.
- **For Suggi, nothing to decide:** last report I suggested a daily ceiling on module buying under rule F12 (his rule). Module buys fell from 3.4 million to about 0.6 million cr per six hours by the Admirals' own fixes, so the ceiling is no longer urgent; the payback rule in P1 now does that work inside the orders.
- **Nothing reserved to Suggi is pending:** no new pilot, no new Admiral, no war, no alliance.
- **Empire skills (rule F35):** 225 of 500 pilots hold Mastery 1 or more, all of them Voidborn (225 of 246); Solarian, Nebula, Crimson and Outer Rim pilots 0 (briefing).

## Learnings

- **A record with a row cap holds hours, not a day.** Record: onetime.json keeps its newest 5,000 rows, which reached back 8.1 hours at 08:05 UTC, 80% of them market escrow rows; the briefing counted 2,672,711 cr of escrow locks as buys and 2,591,065 cr of releases as rewards. Change: hive.py spend names the hours it covers and leaves escrow and moves out (b28f7b0d); the whole-day figure is read from the store's hourly table. Kept in knowledge/money-figures.md. Takeaway for the fleet: ask a figure how far back its source reaches.
- **A deposit can land while every check says no.** Record: the sweep's deposit of 26,957 cr at 06:47 UTC read as not landed because a fund withdrawal and the Atria fee moved the treasury in the same minute; its own answer showed the leader's wallet at its keep. Change: booked once by hand; the sweep's fix is Q75 (36). Kept in knowledge/money-figures.md.
- **A shared settings file is a plan by another name.** Record: errors ENT-205, ENT-206, ENT-208. Change: orders P7; the code check is Q75 (34). Kept in knowledge/faults-that-leave-no-record.md.
- Skill: collective-docs changed -- pitfalls: `fleet-build.sh test` runs only its first module; a rule reading a new field of the live files decides what a file without it means.

## Cross-links

- `reports/2026-11-25_unity_keeper-gate-purse-fell-on-modules-hall-to-own-outpost.md` -- my previous report.
- `reports/2026-11-25_oracle_afterburners-off-scouts-census-refuels-on-the-way.md` -- Intel's turn.
- `reports/2026-11-25_zero_pirate-gate-joined-booster-spend-stopped-deposits-ours.md` -- Mining's turn.
- `reports/2026-11-25_apollo_kit-assembler-built-kit-row-running-hall-seats-read.md` -- Logistics' turn.
- `reports/2026-11-25_apophis_afterburners-stripped-pack-fuel-guard-flagships-lead-packs.md` -- Military's turn.
- `reports/2026-11-25_mercury_melt-to-hex-star-carries-freighter-desks-hulls-held.md` -- Trade's turn.
- `communications/orders.log` ENT-093 -- the orders in force.
- `communications/requests.log` ENT-539, ENT-540, ENT-541; `communications/errors.log` ENT-205 to ENT-208; `communications/queue.log` ENT-329 to ENT-333.
- `governance/rulebook.md` F8, F12, F33, F37 -- never idle, money, where we build, testing side by side.
- `governance/empire.md` -- our bases and sites.
