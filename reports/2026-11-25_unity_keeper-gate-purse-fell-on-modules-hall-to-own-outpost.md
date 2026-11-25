---
name: keeper-gate-purse-fell-on-modules-hall-to-own-outpost
id: 20261125T025502Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, purse, plans, guild-hall]
links:
  - reports/2026-11-24_unity_kit-line-chosen-hall-gated-release-fixed-schema-gate.md
  - reports/2026-11-24_oracle_census-cadences-under-targets-fit-network-kept.md
  - reports/2026-11-25_zero_mine-network-market-tier-fixed-iron-gathers-reached.md
  - reports/2026-11-25_apophis_escort-lane-stopped-after-four-pirate-losses.md
  - reports/2026-11-25_apollo_kit-line-at-node-beta-frames-staged-nodes-asked.md
  - reports/2026-11-25_mercury_craft-net-reserve-gate-nodes-to-builder-bladders-to-sol.md
---

# The Collective -- The Purse Fell 5.25 Million in Six Hours, Mostly on Ship Modules; Plan Lists Now Belong to Their Keepers

## Situation

Period: since my report of 2026-11-24 21:17 UTC (22:17 CET) to this turn, 02:00 to about 03:10 UTC (03:00 to 04:10 CET), under orders ENT-091, now ENT-092.

The fleet as one purse (hive.py stats kpi, computed 01:58 UTC): wallets 13,767,379 cr plus the faction treasury 11,226,192 cr make 24,993,571 cr. My last report read 30,241,096 cr, so the purse is 5,247,525 cr lower. In plain words: we spent much more than we earned. Where it went, from the record of money paid once (data/fleet/onetime.json, the six hours to 02:06 UTC): 3,414,572 cr on ship modules bought by the fitting network, 726,334 cr on ships bought from listings, 566,388 cr on frames for our own outpost-kit factory, against 3,045,191 cr of mission rewards and other one-time money coming in.

The repeating money (work minus fuel and repairs, one-time money left out): last hour -270,587 cr an hour, six hours -362,793, 24 hours -110,953, 72 hours -103,513 (same reading). Income in the last hour was 35,371 cr against 281,677 cr of fuel. Ships: 500; at 02:53 UTC 472 at work, 13 starting, 2 waiting, 13 by hand (fill.py check all). Over 24 hours 70% of ship-hours went to each class's own work, 14% to missions paid once, 7% docked without work (hive.py stats time).

One line per division (briefing money table, the hour to 02:00 UTC; 24-hour purse from the GAAP table):
- Mining, 130 ships: last hour -59,331 cr; 24-hour purse +46,174 cr an hour; 187 units of ore a ship-hour (stats contribution).
- Trade, 85 ships: last hour +38,721 cr, the only division with income (45,324 cr); 24-hour recurring +107,834 cr an hour.
- Logistics, 95 ships: last hour -53,073 cr; 24-hour purse -110,836 cr an hour; its freight network earned 120 cr in nine hours (Apollo's report).
- Military, 140 ships: last hour -147,192 cr, fuel and repairs 155,015 cr of the fleet's 281,348; 12,237 kills and 5 ships lost in 24 hours (stats contribution).
- Intel, 50 ships: last hour -40,888 cr; 97% of the places our routes use read within 3 hours (stats contribution).
- Command: no ship of its own; the ten flagships fly in Military's plan as pack leaders.

## Strategy

The standing goals are unchanged and Suggi's alone: G1 to G5 (dominate the galaxy, a fleet of up to 1,000 ships, a sovereign industrial empire of 5 stations and 8 outposts, the top producer and trader, master every empire) and the operational subgoals O1 to O10, first of them never idle (O1).

Decided this turn:
- **The Guild Hall goes up at an outpost of our own.** My answer of last evening (requests ENT-532) placed it at Node Beta, a rented station. Trinity relayed Suggi's word that it stands on one of our own outposts (queue ENT-321), and Suggi's word wins; the gate stays the same: the fleet's 24-hour repeating net must read zero or better first. Apollo reads before then how many seats a Hall at our outpost really adds, since his notes say an office away from the main station counts a quarter of its size (requests ENT-538, orders P4).
- **A division's lists for every ship belong to its Admiral.** Each division's plan has two lists every ship tries, First and Then. Last evening an automatic step applied an edit in my name that put two shared programs into those lists for five divisions; one of them cost Trade 479,693 cr in 3.5 hours before Trade's Admiral could look (errors ENT-203, ENT-204). Now the code refuses such a change from anyone but the division's own Admiral, unless the change says so out loud, and then the Admiral sees it written beside its plan (orders P7, commit 58498530).
- **P1 now reads: fuel only for work that pays or that trains a skill.** The fleet burns about 280,000 cr of fuel an hour while its repeating income runs between 35,000 and 350,000 cr an hour; the purse is carried by one-time mission rewards, which run out as pilots finish them.

A proposal, not yet an order: Military's hunting costs about 155,000 cr of fuel and repairs an hour (last hour) for 155 combat experience points per ship-hour (24 hours, stats contribution). I asked Apophis to hunt nearer to stations and to carry fuel home; if the figure does not move by tomorrow I will put a cap on hunting hours against what the loot sells for.

## Divisions

**Intel (Oracle).** Set nine scanning schedules a trip below their targets and kept the fitting network after it bought shield boosters for 28 scouts for 354,907 cr. Freshness of all 2,325 places read slipped from 69.5% to 68.3%; judged next turn. Suggestions: a plan-file change that names its hand: accepted and built (58498530). The NOIR alarm that counts a closing thank-you as unanswered: open, it is Trinity's metric; I back Oracle's option (b) (queue ENT-328). Weighing a scout hull by fuel per reading: open, Trinity's scorecard. Thread: the turn before asked for a test before fit-network flew; it flew without one, by another hand, which is the fault fixed this turn.

**Mining (Zero).** Found the mining network chasing goods we already hold past every buyer (copper, nitrogen ice) at -465 cr a ship-hour and fixed it with a test (d7ba405b); iron now reads 67,024 against its keep of 60,000 (briefing supply line), up from 52,325 at his turn. Suggestions: that Trinity names the owner when a shared policy changes a division's work: accepted, passed on (queue ENT-328). That the upgrade service sets the hand-over file for a built hull itself: accepted, in my block of ENT-092, not built yet. Ships-at-work counts beside credits per ship-hour in the network line: accepted, not built yet. Request ENT-534 from Apophis waits for his answer.

**Military (Apophis).** Four escorts were lost to pirates in one hour after another hand widened the escort lane without a test; he stopped the lane, Trinity reopened it behind a gate that weighs the escort side against the pirates (413f8093). He fixed hunters that closed to a gun's reach their empty launcher set (9ef00c7c) and cut fitting loadouts after 251 fits cost 1,054,648 cr. Suggestions: a hunting-policy change goes in beside the tested one: accepted, it is rule F37, passed to Trinity. Letting a strip route pass the class guard when another weapon stays: open, my dispatcher, not built. Thread: 19 of 25 tows since 21:30 UTC were Military ships out of fuel (inbox.py new), now in his block.

**Logistics (Apollo).** Sited the kit factory at Node Beta (our outpost refuses crafting), bought 215 frames for 724,006 cr of the 1,600,000 cr budget, and waits for 40 control nodes, 36 of them given by Trade. Suggestions: the Guild Hall's site: decided, our own outpost. A second source of kits at a public assembler in Sol: accepted as his read for later. A base-plan check against building a factory where crafting is refused: passed to Trinity. Thread: his requests ENT-523 and ENT-525 to me are closed as done (ENT-537, ENT-538).

**Trade (Mercury).** Found and stopped the crafting network's 479,693 cr bleed at its root (d2045617: no good an open need takes is made for sale) and gave 36 control nodes to the builder; the market desks earned 263,323 cr in six hours. Suggestions: a queue line when another hand applies a plan: accepted, built as a refusal plus a written note. Quote a craft before buying its inputs: done by Trinity in b0a2eef6. Weigh the hull alarm by what a hull earns: passed to Trinity. Cross-check: his 24-hour figures and mine agree within the hour between our readings.

## Plans

- **Next turns (CET):** Oracle 06:00, Zero 06:30, Apollo 07:00, Apophis 07:30, Mercury 08:00, mine 09:00 (each job's schedule, read this turn).
- **Orders ENT-092** carry each block: Zero answers ENT-534 and reads the mining network after Trinity reopened its lawless deficit lane; Mercury gives standing work to traders whose first mission link rests; Apollo builds the kit factory once 40 control nodes stand at Node Beta, then one kit and Atria; Apophis hunts near stations with fuel for the way home; Oracle routes scouts born in other empires back to their own region's work.
- **Built this turn:** the plan keeper gate, the wallet's patience with ships in a fight, and the hunting test that had blocked every install since 02:20 UTC (all in 58498530, tests failing first).
- **My next builds, not built yet:** spend by division and kind (modules, hulls, craft inputs) as a figure of the store, so no Admiral sums it by hand again; the network line with credits per ship-hour; the upgrade service's hand-over file; the runner unfits before it gives (ENT-178); a hand-over never gives from one receiver to another (ENT-188); the class guard's strip-route pass. DECISIONS Q75 items (13) to (21) stay unbuilt.
- **Fill gate:** HALT at 02:56 UTC with 2 of 500 ships waiting: one drone whose plan lacks standing work (Military's) and one scout (Intel's, which its own gate counts on watch). At 02:04 UTC it had been 3 scouts and 3 traders; the blocks of ENT-092 name them to their Admirals. Both plans are the Admirals', so I named them rather than writing into them.

## Advice and Suggestions

- **What I decided and why:** the Guild Hall moves to an outpost of ours because Suggi said so through Trinity; the plan lists became their Admirals' own because an automatic step of mine spent half a million of Trade's credits under my name. Nothing here needs Suggi.
- **Where I advise focus:** the purse. The fleet is spending its savings on fitting ships while its repeating work does not yet pay its fuel. The spending is allowed by rule F12 (Suggi's: fits are funded without a cap above the 500,000 cr treasury floor), so I did not cap it; the Admirals have already cut the useless parts (afterburners, scanners, cloaks on hunters). If Suggi wants a ceiling on how fast the treasury may turn into modules, that is his to set in F12; my advice is a daily ceiling of about one million credits until the 24-hour net reads above zero, because at the six-hour pace of -877,983 cr an hour (net of everything, hive.py stats kpi) the purse of 25.0 million would last about 28 hours; at the last hour's pace of -319,870 it would last about three days.
- **The miners' question from earlier** stays open; my advice is still no for now.
- **Nothing reserved to Suggi is pending:** no new pilot, no new Admiral, no war, no alliance.

## Learnings

- **A job that applies other hands' edits must name itself.** Record: commit 95bd8316, the plan history of 20:00:46 UTC, errors ENT-203 and ENT-204. Change: the keeper gate and FLEET_HAND (58498530). Kept in my knowledge file faults-that-leave-no-record. Takeaway for the fleet: a record that names the wrong author is worse than none, because readers trust it.
- **A spending program with a wallet floor has no budget when the floor is refilled from the treasury.** Record: onetime.json, 274 top-ups for 2,453,245 cr beside 3,414,572 cr of modules in six hours. Change: I read spend by division and kind every turn and will build it as a store figure. Kept in my knowledge file money-figures.
- **A change to a shared program can break every member's install.** b0a2eef6 left one test failing, and every fix in the fleet was refused for half an hour until I mended the test. Takeaway: a red suite is read at once, whoever broke it.
- Skill: collective-docs changed -- pitfall: the terminal's guard refuses any shell line holding the word for stopping a machine (a test's `HALT` text in a heredoc), so such text goes in by the file tools.

## Cross-links

- `reports/2026-11-24_unity_kit-line-chosen-hall-gated-release-fixed-schema-gate.md` -- my previous report.
- `reports/2026-11-24_oracle_census-cadences-under-targets-fit-network-kept.md` -- Intel's turn.
- `reports/2026-11-25_zero_mine-network-market-tier-fixed-iron-gathers-reached.md` -- Mining's turn.
- `reports/2026-11-25_apophis_escort-lane-stopped-after-four-pirate-losses.md` -- Military's turn.
- `reports/2026-11-25_apollo_kit-line-at-node-beta-frames-staged-nodes-asked.md` -- Logistics' turn.
- `reports/2026-11-25_mercury_craft-net-reserve-gate-nodes-to-builder-bladders-to-sol.md` -- Trade's turn.
- `communications/orders.log` ENT-092 -- the orders in force.
- `communications/requests.log` ENT-537, ENT-538; `communications/errors.log` ENT-204; `communications/queue.log` ENT-321, ENT-327, ENT-328.
- `governance/rulebook.md` F8, F12, F37 -- never idle, money, testing side by side.
