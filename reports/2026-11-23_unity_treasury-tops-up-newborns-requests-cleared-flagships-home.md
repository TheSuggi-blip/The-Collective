---
name: treasury-tops-up-newborns-requests-cleared-flagships-home
id: 20261123T021223Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, wallets, newborns, requests]
links:
  - reports/2026-11-22_unity_jump-loops-capped-hunts-fuel-first-newborns-held-near.md
  - reports/2026-11-22_zero_newborn-miners-home-missions-skill-gathers-seats-asked.md
  - reports/2026-11-23_oracle_newborn-regions-read-by-newborns-census-cut-put-to-unity.md
  - reports/2026-11-23_apollo_newborn-haulers-on-home-boards-loop-kept.md
  - reports/2026-11-23_mercury_newborn-traders-on-home-tours-docked-crafts-cut-loop.md
  - reports/2026-11-23_zero_newborn-miners-empire-missions-voidborn-guard.md
  - reports/2026-11-23_apophis_recursion-commissioned-newborns-home-work-wallets-short.md
  - communications/orders.log
---

# The Collective -- The Treasury Tops Up the Newborns, Every Request Cleared, the New Flagships Sent Home

## Situation

Period: from my report of 2026-11-22 23:28 CET (reports.log ENT-128) to
this turn, 02:31 to about 03:15 CET on 2026-11-23. Orders in force at the
start: ENT-068 (Trinity wrote Suggi's goals as G1 to G5 and subgoals O1
to O9 over my plan); at the end: ENT-069, mine.

The fleet as one purse (`hive.py fleet`, 03:12 CET): 500 ships, 365 at
work, 101 docked without work, 34 adrift; wallets 10,229,084 cr plus the
treasury 1,907,123 cr, together 12,136,207 cr. In plain words: the fleet
spends more on fuel than it earns from steady work, and the newborn
pilots' one-time starter rewards cover the gap for now. Steady net
(`hive.py stats kpi`, 03:08 CET): -192,725 cr in the last hour, -117,684
an hour over 6 hours, -49,030 an hour over 24 hours. Paid once (rewards
minus goods bought for them): +1,375,723 cr in the last hour, +423,201 an
hour over 6 hours. Fuel alone: 219,870 cr in the last hour.

Each division's own net, last hour and 6 hours (`hive.py stats
contribution`, 02:30 CET): Command -4,210 and -6,534; Mining -44,698 and
-23,852; Logistics -34,186 and -32,618; Trade -16,437 and +31,281;
Military -37,446 and -36,891; Intel -35,488 and -35,289 cr an hour. Ships
idle by the store's alert: the fleet's idle share read 31.1% in the hour
from 01:00 CET against a median of 3.0% (`stats alerts`).

## Strategy

Suggi's goals stand as Trinity wrote them in ENT-068 (G1 to G5: dominate,
the grand fleet, a sovereign empire, enterprise income and extraction,
explore and master), with the subgoals O1 to O9; I copied them unchanged
into ENT-069. My plan P1 to P6 stands with one change in P6.

Decided this turn (mine to decide, rule F7 says the wallet figures are
the Fleet Admiral's):
- **The treasury helps a pilot no ship can help.** Until now a poor pilot
  got credits only from a richer ship of its own division. The sweep keeps
  every working ship at 30,000 cr, and a giver had to stay above 30,000,
  so after the birth wave no division had a giver. Now the faction
  treasury lifts such a pilot from under 5,000 to 6,000 cr, at most
  400,000 cr a day, a pilot at most once in 6 hours. Its first dry run
  named 33 pilots and 156,200 cr.
- **A route can name the empires it is for** (`requires.empire`), so a
  Solarian starter mission is never sent to a Voidborn pilot again.
- **The census cut waits for Suggi.** My orders asked the scouts to burn a
  third less on reading. Oracle showed that every way to do it leaves
  scouts docked without work, which his rule F8 forbids. That rule is his,
  so the question goes to him (Advice); until then no cut.

Not decided by me: Trinity took the dispatcher's 5,000 cr "only paying
work" line out at 02:17 CET (commit c9d78f7c, naming a Suggi directive; I
have not heard it from Suggi directly).

## Divisions

**Mining (Zero, two turns).** Found the newborns' home fields mined out
(Sol and Haven), put them on starter missions and one-ship skill gathers;
waiting miners fell from 63 to 0 by 01:49 CET, then 16 waited at 03:03
CET. A lift let the five-minute pass send two Voidborn miners toward Sol
(errors ENT-146). Suggestions: seats for ten Solarian miners -- accepted,
queued; `requires.empire` -- accepted, built; buying carbon at 4 cr for
the reserve -- open, it waits for the foundry's funding; a plan warning
for a row beyond a newborn's reach -- open, not built; the dispatcher's
5,000 line reading paid-once rewards -- overtaken, Trinity removed the
line. Thread: Zero's routes and my builds now agree; the 4-cr carbon is
the same offer as his last turn, still unread by Trade.

**Intel (Oracle).** Regional census lists for the newborns' homes, two
Altais missions paid on their first runs (3,500 and 800 cr). He capped
the census and took the caps back in ten minutes when they left scouts
idle. Suggestions: treasury top-ups -- accepted, built; plan rows of away
ships -- accepted, his copy installed; the docked watch -- put to Suggi;
the patch notes -- accepted, done.

**Logistics (Apollo).** 55 newborn haulers set on their home boards;
waiting haulers 55 to 16. The loop cap is not in: his haulers hold no
cargo worth carrying (a scan of storage against every book). Suggestions:
top-up to 5,000 -- accepted at 6,000; a give route of Mining or Trade
naming a hauler receiver -- open, it is Zero's and Mercury's to write.

**Trade (Mercury).** 42 newborn traders on shared once tours, seven docked
crafts, the jump loop from 35 to 20 traders; the only division with a
positive 6-hour net (+31,281). His order step could not install because
the test gate was red; Trinity fixed it (queue ENT-244). Suggestions: the
gate's time limit -- done by Trinity; `requires.empire` -- accepted.

**Military (Apophis).** The first tier-2 hull, the Recursion, commissioned
for 354,571 cr; 20 home routes for 60 newborns; no ship lost. Suggestions:
fund newborns at 6,000 -- accepted as the line for every division; the
gate's limit -- done by Trinity; a stop that reads a moving station's
system -- accepted, his to build. His tug script is installed and runs.

Thread audit: every division reported the same blocker (poor newborns);
the five-minute pass and the dispatcher held as built. The fill gate
still reads HALT: 129 waiting at 03:12 CET, almost all newborns whose
once missions are done and whose regions hold no repeating route yet.

## Plans

- **Next turns (CET):** Zero 04:00, Oracle 04:15, Mercury 04:30, Apollo
  04:45, Apophis 05:00, mine 06:30. Orders ENT-069 name work that repeats
  in the newborns' regions as every Admiral's first gap (P6).
- **The top-ups wait for the leader.** The game pays out of the treasury
  only while the faction's leader is docked at one of our Lockbox
  stations. At 03:04 CET the leader flew a mission circuit far from them,
  so the 33 top-ups wait for its return. Next turn I read whether they
  landed; if the leader's work keeps it away, I give it home routes.
- **The command group:** the four new flagships got missions and hunts
  where they were born; the Crimson one got a new test hunt near its home
  (three results decide, rule F37). At 03:11 CET no flagship waited.
- **Built this turn** (commit 319e5221, the whole test suite passed in the
  install): treasury top-ups; once-mission tries not burned by engine
  outages or a board's skill gate; `requires.empire`; plan rows of away
  ships; the tug; the patch-notes sync; two red tests left by others'
  commits fixed.
- **Open builds not done:** DECISIONS Q64 to Q73 stand as written there
  (the outpost unload and refuel steps, the survey visit step, the group
  hunts' dispatcher step, among others); none was built this turn.

## Advice and Suggestions

- **For Suggi, the docked watch (requests ENT-381, ENT-398).** The scouts'
  reading runs cost about 466,000 cr a day (2,416 runs in 24 hours). Reading less
  saves fuel, but a scout that does not read sits docked, and his rule
  "never idle" counts it as idle. Oracle asks whether a docked scout with
  nothing due to read may count as working. My view: yes, for scouts
  only, while every place the plans use stays read within its hour; it
  would save about 155,000 cr a day. Until he says so, the scouts read as
  now.
- **The fleet's hole is work, not money.** About 129 ships waited at the
  end, mostly newborns far from our home who finished their starter
  missions. Each Admiral now must find repeating work in those regions.
- **A stranger wrote to one of our drones** ("anything interesting?"). Our
  rule: no reply without Suggi's word; my default is no reply.
- **Pace (Morpheus, queue ENT-239).** Several changes of rules in one day
  make results hard to read. I keep my governance changes to one orders
  entry a turn; a daily release is Trinity's call.

## Learnings

- **Two money lines with the same value cancel each other.** The sweep's
  keep line and the top-up's giver floor were both 30,000 cr, so once most
  pilots were poor, no division had a giver, and five Admirals asked the
  same thing in one round. Record: requests ENT-380, 384, 385, 386, 389;
  answer ENT-393; commit 319e5221. Change: the treasury is the giver of
  last resort, capped a day. Takeaway: when one figure of the purse
  changes, read every line that leans on it. Kept in
  `knowledge/money-figures.md`.
- **A red test from another hand blocks everyone.** Two tests failed on
  the clean repository (a new table without its handbook subject, a test
  state the dispatcher change outgrew); every member's install stops on
  them. I ran each on a clean copy, then fixed both in my install.
- Skill: collective-docs changed -- a pitfall on a suite left red by
  another hand: prove it on a clean copy, fix it in the same install.

## Cross-links

- `reports/2026-11-22_zero_newborn-miners-home-missions-skill-gathers-seats-asked.md` -- Mining, first turn of the round.
- `reports/2026-11-23_zero_newborn-miners-empire-missions-voidborn-guard.md` -- Mining, second turn.
- `reports/2026-11-23_oracle_newborn-regions-read-by-newborns-census-cut-put-to-unity.md` -- Intel.
- `reports/2026-11-23_apollo_newborn-haulers-on-home-boards-loop-kept.md` -- Logistics.
- `reports/2026-11-23_mercury_newborn-traders-on-home-tours-docked-crafts-cut-loop.md` -- Trade.
- `reports/2026-11-23_apophis_recursion-commissioned-newborns-home-work-wallets-short.md` -- Military.
- `communications/orders.log` ENT-068, ENT-069; `communications/requests.log` ENT-378 to ENT-417; `communications/queue.log` ENT-246.
- `governance/strategy.md`; `governance/rulebook.md` (F7, F8, F10, F37).
