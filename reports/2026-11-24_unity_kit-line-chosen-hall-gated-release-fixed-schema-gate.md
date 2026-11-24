---
name: kit-line-chosen-hall-gated-release-fixed-schema-gate
id: 20261124T211743Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, capital, gates, flagships]
links:
  - reports/2026-11-24_unity_orders-whole-again-outpost-iron-out-finish-routes-gated.md
  - communications/orders.log
  - communications/requests.log
---

# The Collective -- Our Own Outpost-Kit Line Chosen, the Guild Hall Waits for a Paying Day, Hand Scripts Fixed, a Schema Gate Added

## Situation

Period: from my report of 15:07 UTC to this turn, 20:01 to about 21:20 UTC on 2026-11-24 (22:20 CET). Orders at the start: ENT-090.

- **The purse.** Wallets 18,565,941 cr plus treasury 11,675,155 cr = 30,241,096 cr (stats kpi, 20:00 UTC), against 28,946,996 cr in my last report: about +1.29 million in five hours. In plain words: the fleet's money keeps growing, mostly from mission rewards that pay each pilot only once (540,531 cr an hour over 24 hours). The repeating work, after fuel and repairs, earned +118,625 cr in the last hour and +89,729 an hour over 6 hours, but still -140,855 an hour over 24 hours (stats kpi). Two bad hours of this morning (09:00 and 10:00 UTC, -1.58 and -1.15 million, table stats_money_hour) leave the 24-hour window around 10:00 UTC tomorrow.
- **One figure is not right yet.** In the last hour the money view read costs of -69,176 cr against 135,651 cr of fuel and repairs the meters saw, and 209,718 cr an hour the game's own counters do not explain (fleet.json, 20:13 UTC). Four withdrawals from the treasury for hulls (171,315 cr) fell in that hour; whether they cause it is not proven.
- **Ships.** 500 ships, 458 at work, 28 starting, 0 waiting, 14 held by hand scripts; fill gate PASS (fill status, 20:11 UTC). At 21:13 UTC one hauler waited (the Builder, at Node Gamma, outside the two home systems its own watch route allows) and the gate read HALT for haulers; the scouts docked on watch pass by rule F8's exception. The command group itself has no ship now: the ten flagships fly in Military's plan since 17:41 UTC (see Strategy).
- **Divisions, 24-hour purse an hour (contribution, 20:00 UTC):** Trade +137,217 (repeating +76,197, the only division whose repeating work pays); Mining +96,332 (repeating -71,608); Logistics +69,812 (repeating -23,909); Military +50,482 (repeating -34,717; 12,035 kills, no ship lost); Intel +44,531 (repeating -20,362; 95% of the places our routes use read within 3 hours); Command +1,302.
- **Seats** 275 of 275, 225 ships outside the faction; own-empire Mastery: 225 of 246 Voidborn pilots at level 1 or more, 0 of the 254 pilots of the other four empires (briefing).

## Strategy

Suggi's goals stand as written (G1 to G5, O1 to O10). What I decided this turn, as the player who holds the purse:

- **The Atria outpost kit comes from our own kit line (decided, requests ENT-531).** Simple version: an outpost needs a kit, and a kit can only be made in a factory called an outpost frame assembler, which we do not own. Buying one finished kit costs about 1.1 million and must be flown 16 jumps through lawless space; building the factory costs about 1.5 million for the first kit and about 257,000 for each one after. Suggi's goal is eight outposts, so the factory pays from the second kit, and it gives our idle haulers carrying work at home. Budget up to 1.6 million from the treasury; first a check that the factory may stand at our outpost (rent-free) or at Node Beta.
- **The Guild Hall waits (decided, ENT-532).** It would lift our seats past 275, but costs about 8.7 million, three quarters of the treasury, and would stop the automatic hull buys. It is built once the 24-hour repeating net reads zero or better; Apollo checks that gate at each turn and builds without asking again.
- **The flagships lead Military's packs (taken from Trinity's design).** Trinity moved the ten flagships into Military's plan at 17:41 UTC (queue ENT-310, ENT-314), so they lead hunting packs and level Leadership and Tactics. Ownership stays with me under rule F10; diplomacy, the faction leader's errands and the purse stay with the command group. I cleared their rows from my plan file, which had failed its check since then.
- **New orders ENT-091** carry these, and P7 now follows the new rule F37 (test variants side by side instead of one ship at a time).
- **Proposed, not decided:** nothing new for Suggi this turn; the miners' question of my last report stays open (Advice).

## Divisions

All nine Admiral reports of the period read in full (Apollo two, Mercury two, Zero two, Apophis two, Oracle one).

- **Logistics (Apollo).** Took the arbitrage lane out of haul-network as ordered; since then up to 94 haulers wait docked for freight that never comes: haul-network earned 0 cr in the hours 15 to 17 UTC (Apollo's second report). The fill gate counts that as work, which hides it. The kit line answer gives them home work. Suggestions: stall rule spares a docked buy-and-store run -- **open** (built when next in line; Apollo's three-cycle runs work around it); the needs tool names a facility we lack -- **accepted**, in my builds (orders); longer rest for an empty freight board -- **accepted for Trinity** (haul.py, server courtesy); count a 0-cr watch as idle -- **accepted**, open build; Guild Hall over an outpost Center -- **accepted** (ENT-532); kit line -- **accepted** (ENT-531).
- **Trade (Mercury).** Best division by repeating money: melt sold at Hex Star (+301,160 cr in one run), caustic sacs (+81,972), three stuck hull orders finished by their owners with 208,029 cr refunded. Suggestions: a trading desk's empty utility slot counts as filled -- **open** (scorecard); gate.release clears the want -- **done** (1ec2361a); stale building rows in the upgrade queue -- **accepted**, open; craft output priced at the local bid -- **for Trinity**.
- **Mining (Zero).** Fixed mine-network (it had mined nothing for 100 minutes), opened nine far iron fields and three one-ship tests, two new Resonance Miners switched in by hand. Suggestions: a live-schema test for network runners -- **done this turn** (sqlcheck); install restores the clone when its caller dies -- **declined**, already there (Zero's own feedback: RECOVERED); upgrade service polls built hulls first -- **done by Trinity** (ca694b9e); craft demand net of what we hold -- **done by Trinity** (same commit); utility slots in the miners' slot count -- **open**; the miners' question to Suggi -- see Advice.
- **Military (Apophis).** Fixed hunt-network (it was blind for two hours), found why the listed Cleavers never killed (an empty long-range launcher kept them out of their guns' reach), no ship lost in 24 hours. Suggestions: tug.py reads a hull's own fuel burn -- **accepted**, open; live-schema tests -- **done** (sqlcheck); kills a run in the upgrade view and rungs on kills -- **accepted**, open (the store holds the figure: hunts of the last 24 hours read 2.7 kills a run for Recursions, 1.78 for Cleavers, 1.88 for Broadaxes, 2.22 for Thresholds, table runs joined to ships); hunt.py closes to the shortest reach that can fire -- **accepted, Apophis's** through fleet-build (his runner); routes.py check refuses a stop off the map -- **accepted**, in my builds.
- **Intel (Oracle).** Answered NOIR in Phase 2 (their secretary passes our proposal up; no gift asked), fixed fit_net before any fit, widened the north road census. Suggestions: fit-network only after one clean run per hull class -- **each Admiral's call**, see the fit-network note in Plans; scouts docked on watch count as working in the scorecard -- **accepted**, open.
- **Thread audit.** My last turn's two fixes held: usable iron stays short of 60,000 (47,957 at 15:00, 46,803 at 20:00 UTC, stats_supply_hour), so iron gathering continues; finish routes since the mission gate: 19 of 21 runs paid once (109,000 cr), against 112 of 679 before (table runs). Two faults of this period came from one commit by another hand (9396c21c: gate.release); both Admirals who hit it filed it correctly.

## Plans

- **Next turns (CET):** Oracle 00:00, Zero 00:15, Apollo 00:30, Apophis 00:45, Mercury 01:00, mine 02:30.
- **The fill gate is not closed for one ship:** the Builder waits at Node Gamma; it is Apollo's plan, so the orders name it (APOLLO: standing class work for every hauler, the Builder too wherever it stands) instead of my hand moving it.
- **Apollo:** where the kit factory may stand, one reinforced frame bought and read, then the fee and the kit (ENT-531). The Guild Hall at its gate (ENT-532).
- **Fit-network:** at about 20:00 UTC the route fit-network was added to the end of the first list of five division plans, matching Trinity's queue ENT-310; the hand that wrote it is not in the record. By 20:41 UTC 75 ships had flown it for -483,351 cr of modules (table runs), 31 of them Military's, whose Admiral had decided to keep it out until its loadout is tuned. The orders leave each Admiral to tune its fit policy; I did not undo the change.
- **My builds, in order (orders ENT-091):** runner unfits before it gives (ENT-178); a hand-over never gives from one receiver to another (ENT-188); routes.py check warns on a mine route without a floor, a faction gather without a reserve gate and a stop off the map; the needs tool names a facility we lack. Open and unbuilt (DECISIONS Q75): (13) to (21) as before, (22) a 0-cr watch counted as idle, (23) the slot KPI for desks, miners and scouts on watch, (24) stale upgrade rows and kills a run, (25) tug.py's own burn, (26) the stall rule, (27) the money view's unexplained last hour.

## Advice and Suggestions

- **For Suggi, one open question (unchanged):** Mining asks whether miners may stay docked when their only work would gather goods we already hold too much of. My advice stays no for now: iron is short again (46,803 of 60,000), so every miner has iron to gather; the question returns when iron reaches its maximum. Default: miners keep gathering what the reserve lacks, then work further out.
- **Diplomacy:** NOIR's secretary acknowledged our proposal and will pass it up; nothing is owed until their office writes. No gift (rule F39). Default: wait.
- **No new pilot, no war, no alliance** is asked for this turn.

## Learnings

- **A query on a column the store lacks, inside one broad `except`, makes a runner read an empty world.** Record: errors.log ENT-194, queue ENT-307 (mine_net and hunt_net blind for 100 and 117 minutes). Change: sqlcheck.py prepares every literal query of our scripts against the store's own schema; on the old runners it names all four bad queries, on today's code it found one more dead read (rivals.py). Takeaway: a check that reads the code beats waiting for a reader. Kept in knowledge/faults-that-leave-no-record.md.
- **A cleanup line added after a working step, with no test that calls it, broke every member's hand scripts for two and a half hours.** Record: errors.log ENT-199, requests ENT-526/527, commit 9396c21c. Change: gate.release has its test (1ec2361a). Kept in the same file.
- **A failed install that deletes its own log costs a second suite run.** Record: this turn's install of 20:26 UTC (1,258 tests, 2 failures, names not kept). Change: repo_install.sh keeps the failing suite's output and prints the failing test names.
- Skill: collective-docs changed -- repo_install.sh keeps a failed suite's log and prints FAIL lines.

## Cross-links

- `reports/2026-11-24_apollo_arbitrage-out-atria-kit-needs-a-facility.md`
- `reports/2026-11-24_apollo_freight-watch-at-zero-builder-watch-guild-hall-asked.md`
- `reports/2026-11-24_mercury_melt-to-hex-star-plasma-test-listed-apophenia.md`
- `reports/2026-11-24_mercury_stuck-apophenias-supplied-sacs-to-hex-star-listed-t2-ladder.md`
- `reports/2026-11-24_zero_yards-fed-mine-network-fixed-far-iron-opened.md`
- `reports/2026-11-24_zero_mine-network-to-iron-new-hulls-switched.md`
- `reports/2026-11-24_apophis_hunt-network-was-blind-tier2-hulls-to-packs.md`
- `reports/2026-11-24_apophis_armed-listed-hulls-could-not-fight-pack-lane-retuned.md`
- `reports/2026-11-24_oracle_noir-answered-fit-net-fixed-north-road-widened.md`
- `communications/requests.log` ENT-528 to ENT-532; `communications/queue.log` ENT-309, ENT-310, ENT-314, ENT-317
- `governance/rulebook.md` F10, F17, F37; `governance/strategy.md`
